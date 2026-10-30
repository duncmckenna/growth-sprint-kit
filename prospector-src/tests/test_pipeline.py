import json
from datetime import datetime, timedelta, timezone

from prospector import classify, imports, meta_ads, score, techcheck
from prospector.common import DATA, OUT, ROOT, load_accounts, load_config, normalise_domain

CFG = load_config(ROOT / "config.yaml")
NOW = datetime.now(timezone.utc)


def iso(days_ago):
    return (NOW - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%S+0000")


class FakeMeta:
    """Stands in for the Ad Library API."""
    def __init__(self, by_term):
        self.by_term = by_term
    def search_terms(self, term):
        return self.by_term.get(term, [])


ADS = {
    "sofa": [
        {"id": "1", "page_id": "p1", "page_name": "Loaf Sofas", "ad_creative_link_captions": ["WWW.LOAFSOFAS.CO.UK"],
         "ad_delivery_start_time": iso(5), "publisher_platforms": ["facebook", "instagram"]},
        {"id": "2", "page_id": "p1", "page_name": "Loaf Sofas", "ad_creative_link_captions": ["loafsofas.co.uk"],
         "ad_delivery_start_time": iso(60), "publisher_platforms": ["instagram"]},
        {"id": "3", "page_id": "p2", "page_name": "Big Retailer", "ad_creative_link_captions": ["amazon.co.uk"],
         "ad_delivery_start_time": iso(10)},
        {"id": "4", "page_id": "p3", "page_name": "AgencyRun Beds", "ad_creative_link_captions": ["agencyrunbeds.com"],
         "ad_delivery_start_time": iso(90)},
    ]
}

HTML_SHOPIFY_KLAVIYO = """<html><script src="https://cdn.shopify.com/s/x.js"></script>
<script>Shopify.currency = {"active":"GBP","rate":"1.0"};</script>
<script src="https://static.klaviyo.com/onsite/js/klaviyo.js?company_id=X"></script>
<script src="https://www.googletagmanager.com/gtm.js?id=GTM-ABC123"></script></html>"""
HTML_PLAIN = "<html><body>hello</body></html>"


class FakeFetcher:
    pages = {"loafsofas.co.uk": HTML_SHOPIFY_KLAVIYO, "agencyrunbeds.com": HTML_SHOPIFY_KLAVIYO,
             "plainshop.co.uk": HTML_PLAIN}
    def homepage(self, d):
        return (self.pages[d], "ok") if d in self.pages else (None, "http_404")


def test_normalise_domain():
    assert normalise_domain("WWW.BRAND.CO.UK") == "brand.co.uk"
    assert normalise_domain("https://shop.brand.com/p?x=1") == "brand.com"
    assert normalise_domain("amazon.co.uk") is None
    assert normalise_domain("Shop now") is None


def test_aggregate_by_page():
    pages = {p["page_id"]: p for p in meta_ads.aggregate_by_page(ADS["sofa"], now=NOW)}
    assert pages["p1"]["domain"] == "loafsofas.co.uk"
    assert pages["p1"]["active_ads"] == 2 and pages["p1"]["recent_ads"] is True
    assert pages["p2"]["domain"] is None            # marketplace caption filtered as noise
    assert pages["p3"]["recent_ads"] is False


def run_seed_and_tech():
    res = meta_ads.seed_from_ads(CFG, client=FakeMeta(ADS), categories=["home_furniture"])
    assert res["unresolved_pages"] == 1
    techcheck.run(CFG, fetcher=FakeFetcher())


def test_techcheck_detection():
    run_seed_and_tech()
    t = load_accounts()["loafsofas.co.uk"]["tech"]
    assert t["shopify"] and t["klaviyo"] and t["gbp"] and t["uk_tld"]
    assert t["meta_pixel"] == "unknown"             # GTM present -> absence is unknown, not False
    assert techcheck.detect(HTML_PLAIN, "x.com")["meta_pixel"] is False


def test_csv_import_and_prefilter(tmp_path):
    csv_path = tmp_path / "storeleads_test.csv"
    csv_path.write_text("Domain,Store Name,Installed Apps\nhttps://www.plainshop.co.uk,Plain Shop,\"Klaviyo, Judge.me\"\n,Empty,\n")
    res = imports.import_csv(csv_path, "storeleads")
    assert res == {"rows_imported": 1, "rows_skipped": 1, "accounts": 1}
    acc = load_accounts()["plainshop.co.uk"]
    assert acc["declared_klaviyo"] and acc["declared_shopify"] and acc["brand"] == "Plain Shop"
    techcheck.run(CFG, fetcher=FakeFetcher())
    assert classify.prefilter(load_accounts()["plainshop.co.uk"])   # declared Klaviyo + .uk


def test_classify_merge_enforces_evidence_and_scoring_routes():
    run_seed_and_tech()
    res = classify.export_batches(CFG)
    assert res["brands"] == 2 and res["batches"] == 1
    batch = json.loads((classify.BATCH_DIR / "batch_001.json").read_text())
    assert {b["domain"] for b in batch} == {"loafsofas.co.uk", "agencyrunbeds.com"}
    classify.RESULT_DIR.mkdir(parents=True, exist_ok=True)
    (classify.RESULT_DIR / "batch_001.json").write_text(json.dumps([
        {"domain": "loafsofas.co.uk", "classification": "in_house_only", "confidence": "high",
         "evidence": [{"signal": "job_ad", "summary": "Paid Social Manager, owns paid in-house",
                       "url": "https://example.com/jobs/1", "date": "2026-10"}],
         "trigger": "open_paid_role"},
        {"domain": "agencyrunbeds.com", "classification": "agency_run", "confidence": "med", "evidence": []},
    ]))
    m = classify.merge_results()
    assert m == {"merged": 2, "problems": 1}
    accs = load_accounts()
    assert accs["agencyrunbeds.com"]["agency"]["classification"] == "unknown"   # no evidence -> downgraded

    score.run(CFG)
    rows = (OUT / "prospects.csv").read_text().splitlines()
    assert rows[1].startswith("A,self_serve_outbound") and "loafsofas.co.uk" in rows[1]
    assert "qualify_first_touch" in rows[2]
    assert "Top 15 self-serve targets" in (OUT / "summary.md").read_text()


def test_hybrid_routes_to_agency_channel():
    acc = {"domain": "h.co.uk", "tech": {"shopify": True, "klaviyo": True, "gbp": True, "uk_tld": True},
           "active_ads": 30, "recent_ads": True,
           "agency": {"classification": "hybrid", "confidence": "high", "evidence": [{"url": "https://x"}]}}
    r = score.score_account(acc, CFG)
    assert r["route"] == "agency_channel" and r["tier"] == "-" and r["score"] == 0


class FakeResp:
    def __init__(self, body, code=200): self.body, self.status_code, self.text = body, code, json.dumps(body)
    def json(self): return self.body


class FakeSession:
    def __init__(self): self.calls = []
    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params))
        if len(self.calls) == 1:
            return FakeResp({"data": [ADS["sofa"][0]], "paging": {"next": "https://graph.facebook.com/next?page=2"}})
        return FakeResp({"data": [ADS["sofa"][1]]})


def test_meta_client_params_and_paging(monkeypatch):
    monkeypatch.setenv("META_AD_LIBRARY_TOKEN", "t")
    cfg = {**CFG, "meta": {**CFG["meta"], "request_delay_seconds": 0}}
    s = FakeSession()
    ads = meta_ads.MetaAdLibrary(cfg, session=s).search_terms("sofa")
    assert len(ads) == 2 and len(s.calls) == 2
    url, p = s.calls[0]
    assert url.endswith("/ads_archive") and p["ad_reached_countries"] == '["GB"]'
    assert p["ad_active_status"] == "ACTIVE" and p["search_terms"] == "sofa"
    assert s.calls[1][1] is None                    # next-page URL already carries params


def test_noise_filters():
    from prospector.common import is_junk_domain
    assert is_junk_domain("velora-com.store") and is_junk_domain("cheapsofas.shop")
    assert not is_junk_domain("loafsofas.co.uk") and not is_junk_domain("dfs.co.uk")
    pages = {p["page_id"]: p for p in meta_ads.aggregate_by_page(ADS["sofa"], now=NOW)}
    assert pages["p1"]["established"] is True       # one ad running for 60 days
    assert pages["p2"]["established"] is False
    junk = {"domain": "velora-com.store", "tech": {"shopify": True, "klaviyo": True, "gbp": True},
            "active_ads": 3, "recent_ads": True, "agency": {"classification": "in_house_only",
            "evidence": [{"url": "https://x"}]}}
    assert score.score_account(junk, CFG)["tier"] == "C"
    assert not classify.prefilter(junk)


def test_page_activity_refresh():
    run_seed_and_tech()
    class PageClient:
        def by_page_ids(self, ids):
            assert "p1" in ids
            return [dict(ADS["sofa"][0], id=str(n), ad_delivery_start_time=iso(120 if n == 0 else 2)) for n in range(12)]
    res = meta_ads.refresh_page_activity(CFG, client=PageClient())
    acc = load_accounts()["loafsofas.co.uk"]
    assert res["pages_refreshed"] >= 1 and acc["active_ads"] == 12 and acc["established"] is True


def test_domain_cleanup():
    assert normalise_domain("uk.koala.com") == "koala.com"
    assert normalise_domain("read.womanandwellness.co.uk") == "womanandwellness.co.uk"
    for junk in ["binge.reelshort.com", "c.menovels.com", "a.mobobooks.com", "api.whatsapp.com",
                 "calendly.com", "fb.com", "a.popstorys.com", "23272.advisorssearch.com", "m.bookcraze.net"]:
        assert normalise_domain(junk) is None, junk
    for keep in ["britishbedco.co.uk", "castlery.com", "barronbeds.co.uk", "alteregobeds.com"]:
        assert normalise_domain(keep) == keep, keep


def test_backoff_on_429(monkeypatch):
    monkeypatch.setattr(techcheck.time, "sleep", lambda s: None)
    class R:
        def __init__(self, code): self.status_code, self.text, self.headers = code, "<html>cdn.shopify.com</html>", {"Retry-After": "1"}
    class S:
        def __init__(self): self.n, self.headers = 0, {}
        def get(self, url, timeout=None, allow_redirects=True):
            self.n += 1
            if url.endswith("robots.txt"): return R(404)
            return R(429) if self.n < 4 else R(200)
    f = techcheck.Fetcher(CFG, session=S())
    html, status = f.homepage("brand.co.uk")
    assert status == "ok" and "shopify" in html
