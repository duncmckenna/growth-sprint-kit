"""Check each store's public homepage for its stack. One polite GET per domain; robots.txt respected.

Absence is reported as 'unknown' when Google Tag Manager is present, because pixels loaded
through GTM don't appear in the raw HTML.
"""
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor
from urllib import robotparser

import requests

from .common import load_accounts, save_accounts

SIGNATURES = {
    "shopify": [r"cdn\.shopify\.com", r"Shopify\.theme", r"myshopify\.com"],
    "klaviyo": [r"static\.klaviyo\.com", r"klaviyo\.js", r"_learnq", r"a\.klaviyo\.com"],
    "hubspot": [r"js\.hs-scripts\.com", r"js\.hsforms\.net"],
    "customerio": [r"track\.customer\.io", r"assets\.customer\.io"],
    "meta_pixel": [r"connect\.facebook\.net/[^\"']*fbevents\.js", r"fbq\("],
    "tiktok_pixel": [r"analytics\.tiktok\.com", r"ttq\.load"],
    "google_ads": [r"googleadservices\.com", r"['\"]AW-\d{6,}"],
    "gtm": [r"googletagmanager\.com/gtm\.js", r"GTM-[A-Z0-9]{4,}"],
}
GBP = [r'Shopify\.currency\s*=\s*\{"active":"GBP"', r'"currency(Code)?"\s*:\s*"GBP"', r"priceCurrency\"?\s*[:=]\s*\"GBP"]
TAG_MANAGED = {"meta_pixel", "tiktok_pixel", "google_ads"}


def detect(html, domain):
    found = {k: any(re.search(p, html) for p in pats) for k, pats in SIGNATURES.items()}
    result = {}
    for k, v in found.items():
        if k == "gtm":
            continue
        result[k] = True if v else ("unknown" if k in TAG_MANAGED and found["gtm"] else False)
    result["gtm"] = found["gtm"]
    result["gbp"] = any(re.search(p, html) for p in GBP)
    result["uk_tld"] = domain.endswith(".uk")
    return result


class Fetcher:
    def __init__(self, cfg, session=None):
        t = cfg["techcheck"]
        contact = cfg.get("contact_for_user_agent") or "no-contact-set"
        # Standard "compatible" bot format: identifies us honestly but is accepted more widely.
        self.ua = f"Mozilla/5.0 (compatible; OutraProspectorResearch/0.1; +mailto:{contact})"
        self.timeout = t["timeout_seconds"]
        self.delay = t["delay_seconds"]
        self.retries = t.get("retries_on_429", 3)
        self.max_backoff = t.get("max_backoff_seconds", 60)
        self.http = session or requests.Session()
        self.http.headers.update({"User-Agent": self.ua, "Accept": "text/html,application/xhtml+xml",
                                  "Accept-Language": "en-GB,en;q=0.9"})

    def _get(self, url, retries=None):
        """GET with short, capped backoff on 429/503 (honours Retry-After up to max_backoff)."""
        retries = self.retries if retries is None else retries
        for attempt in range(retries + 1):
            r = self.http.get(url, timeout=self.timeout, allow_redirects=True)
            if r.status_code not in (429, 503) or attempt == retries:
                return r
            ra = r.headers.get("Retry-After", "") if hasattr(r, "headers") else ""
            wait = float(ra) if ra.replace(".", "", 1).isdigit() else self.delay * (2 ** (attempt + 1))
            time.sleep(min(wait, self.max_backoff) + random.uniform(0, 1))
        return r

    def allowed(self, domain):
        rp = robotparser.RobotFileParser()
        try:
            r = self._get(f"https://{domain}/robots.txt", retries=0)   # no backoff on robots.txt
            if r.status_code >= 400:          # RFC 9309: 4xx (incl. 429) -> treat as no restrictions
                return True
            rp.parse(r.text.splitlines())
            return rp.can_fetch(self.ua, f"https://{domain}/")
        except requests.RequestException:
            return True

    def homepage(self, domain):
        if not self.allowed(domain):
            return None, "blocked_by_robots"
        time.sleep(self.delay)
        try:
            r = self._get(f"https://{domain}/")
        except requests.RequestException as e:
            return None, f"error: {type(e).__name__}"
        if r.status_code != 200:
            return None, f"http_{r.status_code}"
        return r.text, "ok"


RETRYABLE = ("http_429", "http_503", "http_500", "http_502", "error:")


def run(cfg, fetcher=None, refresh=False, retry_failed=False, max_minutes=None, quiet=False):
    """Checks homepages with visible progress, saving every 10 sites so it can be stopped and resumed."""
    import sys
    fetcher = fetcher or Fetcher(cfg)
    accounts = load_accounts()
    max_minutes = max_minutes or cfg["techcheck"].get("max_minutes", 30)
    deadline = time.time() + max_minutes * 60
    if retry_failed:
        todo = [d for d, a in accounts.items() if str(a.get("tech_status", "")).startswith(RETRYABLE)]
    else:
        todo = [d for d, a in accounts.items() if refresh or "tech_status" not in a]

    def one(d):
        if time.time() > deadline:
            return d, None, None
        html, status = fetcher.homepage(d)
        return d, status, (detect(html, d) if html else None)

    done = skipped = 0
    with ThreadPoolExecutor(max_workers=cfg["techcheck"]["workers"]) as ex:
        for d, status, tech in ex.map(one, todo):
            if status is None:
                skipped += 1
                continue
            done += 1
            accounts[d]["tech_status"] = status
            if tech:
                accounts[d]["tech"] = tech
            if not quiet:
                flags = ",".join(k for k in ("shopify", "klaviyo", "hubspot", "gbp") if tech and tech.get(k) is True)
                print(f"[{done}/{len(todo)}] {d}: {status}{' (' + flags + ')' if flags else ''}", file=sys.stderr, flush=True)
            if done % 10 == 0:
                save_accounts(accounts)
    save_accounts(accounts)
    ok = sum(1 for d in todo if accounts[d].get("tech_status") == "ok")
    res = {"checked": done, "ok": ok}
    if skipped:
        res["not_reached_time_limit"] = skipped
        res["hint"] = "Run techcheck again to continue where it stopped."
    return res
