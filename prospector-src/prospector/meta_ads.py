"""Meta Ad Library API (official, free). UK-delivered commercial ads are covered.

Requires a Meta developer app + identity verification, and a user access token in
the env var named in config (META_AD_LIBRARY_TOKEN). Do the verification days ahead.
"""
import json
import math
import os
import time
from datetime import datetime, timedelta, timezone

import requests

from .common import load_accounts, normalise_domain, save_accounts, upsert, write_json, DATA

FIELDS = ",".join([
    "id", "page_id", "page_name", "ad_creative_link_captions", "ad_creative_link_titles",
    "ad_delivery_start_time", "publisher_platforms", "ad_snapshot_url",
])


class MetaAdLibrary:
    def __init__(self, cfg, session=None):
        m = cfg["meta"]
        self.base = f"https://graph.facebook.com/{m['graph_version']}/ads_archive"
        self.token = os.environ.get(m["token_env"], "")
        self.country = cfg["country"]
        self.limit = m["limit"]
        self.max_pages = m["max_pages_per_keyword"]
        self.delay = m["request_delay_seconds"]
        self.search_type = m.get("search_type", "KEYWORD_UNORDERED")
        self.http = session or requests.Session()

    def _params(self, **extra):
        p = {
            "access_token": self.token,
            "ad_reached_countries": json.dumps([self.country]),
            "ad_active_status": "ACTIVE",
            "ad_type": "ALL",
            "fields": FIELDS,
            "limit": self.limit,
        }
        p.update(extra)
        return p

    def _paged(self, params):
        if not self.token:
            raise SystemExit("No Meta token: set the env var named in config.meta.token_env")
        url, pages = self.base, 0
        while url and pages < self.max_pages:
            r = self.http.get(url, params=params if pages == 0 else None, timeout=30)
            if r.status_code != 200:
                raise RuntimeError(f"Ad Library API {r.status_code}: {r.text[:300]}")
            body = r.json()
            yield from body.get("data", [])
            url = body.get("paging", {}).get("next")
            pages += 1
            time.sleep(self.delay)

    def search_terms(self, term):
        return list(self._paged(self._params(search_terms=term, search_type=self.search_type)))

    def by_page_ids(self, page_ids):
        return list(self._paged(self._params(search_page_ids=json.dumps(page_ids[:10]))))


def aggregate_by_page(ads, now=None, established_days=30):
    """Collapse ads into one record per advertiser page."""
    now = now or datetime.now(timezone.utc)
    pages = {}
    for ad in ads:
        pid = ad.get("page_id")
        if not pid:
            continue
        p = pages.setdefault(pid, {"page_id": pid, "page_name": ad.get("page_name"), "ad_ids": set(),
                                   "domains": {}, "platforms": set(), "latest_start": None, "earliest_start": None, "snapshot": None})
        p["ad_ids"].add(ad.get("id"))
        for cap in ad.get("ad_creative_link_captions") or []:
            d = normalise_domain(cap)
            if d:
                p["domains"][d] = p["domains"].get(d, 0) + 1
        p["platforms"].update(ad.get("publisher_platforms") or [])
        st = ad.get("ad_delivery_start_time")
        if st:
            dt = datetime.fromisoformat(st.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if not p["latest_start"] or dt > p["latest_start"]:
                p["latest_start"] = dt
            if not p["earliest_start"] or dt < p["earliest_start"]:
                p["earliest_start"] = dt
        p["snapshot"] = p["snapshot"] or ad.get("ad_snapshot_url")
    out = []
    for p in pages.values():
        top = max(p["domains"], key=p["domains"].get) if p["domains"] else None
        out.append({
            "page_id": p["page_id"],
            "page_name": p["page_name"],
            "domain": top,
            "active_ads": len(p["ad_ids"]),
            "platforms": sorted(p["platforms"]),
            "latest_ad_start": p["latest_start"].date().isoformat() if p["latest_start"] else None,
            "recent_ads": bool(p["latest_start"] and p["latest_start"] >= now - timedelta(days=30)),
            "established": bool(p["earliest_start"] and p["earliest_start"] <= now - timedelta(days=established_days)),
            "earliest_ad_start": p["earliest_start"].date().isoformat() if p["earliest_start"] else None,
            "ad_library_url": f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=GB&view_all_page_id={p['page_id']}",
        })
    return out


def seed_from_ads(cfg, client=None, categories=None):
    """Search wedge keywords, group by advertiser, upsert accounts that resolve to a domain."""
    client = client or MetaAdLibrary(cfg)
    accounts = load_accounts()
    raw_log, unresolved = {}, []
    for cat, terms in cfg["categories"].items():
        if categories and cat not in categories:
            continue
        for term in terms:
            ads = client.search_terms(term)
            raw_log[term] = len(ads)
            for page in aggregate_by_page(ads, established_days=cfg["meta"].get("established_days", 30)):
                if not page["domain"]:
                    unresolved.append({**page, "category": cat, "keyword": term})
                    continue
                prev = accounts.get(page["domain"], {})
                upsert(accounts, page["domain"], source="meta_ad_library", page_id=page["page_id"],
                       brand=page["page_name"], categories=[cat], keywords=[term],
                       active_ads=max(page["active_ads"], prev.get("active_ads", 0)),
                       recent_ads=page["recent_ads"] or prev.get("recent_ads", False),
                       established=page["established"] or prev.get("established", False),
                       earliest_ad_start=min(filter(None, [page["earliest_ad_start"], prev.get("earliest_ad_start")]), default=None),
                       latest_ad_start=page["latest_ad_start"], platforms=page["platforms"],
                       ad_library_url=page["ad_library_url"])
    save_accounts(accounts)
    write_json(DATA / "meta_unresolved_pages.json", unresolved)
    return {"ads_per_keyword": raw_log, "accounts": len(accounts), "unresolved_pages": len(unresolved)}


def enrich_ad_activity(cfg, client=None):
    """For accounts from CSV imports (no page_id yet): search brand name, match on caption domain."""
    client = client or MetaAdLibrary(cfg)
    accounts = load_accounts()
    checked = 0
    for d, acc in accounts.items():
        if acc.get("page_id") or acc.get("ad_check_done"):
            continue
        term = acc.get("brand") or d.split(".")[0]
        pages = [p for p in aggregate_by_page(client.search_terms(term)) if p["domain"] == d]
        if pages:
            p = max(pages, key=lambda x: x["active_ads"])
            upsert(accounts, d, page_id=p["page_id"], active_ads=p["active_ads"], recent_ads=p["recent_ads"],
                   latest_ad_start=p["latest_ad_start"], platforms=p["platforms"], ad_library_url=p["ad_library_url"])
        else:
            acc["active_ads"] = acc.get("active_ads", 0)
        acc["ad_check_done"] = True
        checked += 1
    save_accounts(accounts)
    return {"checked": checked}


def refresh_page_activity(cfg, client=None, only_prefiltered=True):
    """Keyword results are newest-first and capped, so re-pull each shortlisted brand's own
    active ads by page_id (10 per call) for an accurate ad count and 'established' flag."""
    from .classify import prefilter
    client = client or MetaAdLibrary(cfg)
    accounts = load_accounts()
    by_page = {a["page_id"]: d for d, a in accounts.items()
               if a.get("page_id") and (not only_prefiltered or prefilter(a))}
    ids = list(by_page)
    est_days = cfg["meta"].get("established_days", 30)
    for i in range(0, len(ids), 10):
        ads = client.by_page_ids(ids[i:i + 10])
        for p in aggregate_by_page(ads, established_days=est_days):
            d = by_page.get(p["page_id"])
            if d:
                upsert(accounts, d, active_ads=p["active_ads"], established=p["established"],
                       earliest_ad_start=p["earliest_ad_start"], recent_ads=p["recent_ads"],
                       latest_ad_start=p["latest_ad_start"])
                accounts[d]["page_activity_refreshed"] = True
    save_accounts(accounts)
    return {"pages_refreshed": len(ids)}


def active_ads_score(n, cap=50):
    return min(math.log1p(n) / math.log1p(cap), 1.0) if n else 0.0
