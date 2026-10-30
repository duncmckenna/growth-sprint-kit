from collections import Counter

from .common import OUT, is_junk_domain, load_accounts, write_csv
from .meta_ads import active_ads_score

COLUMNS = ["tier", "route", "score", "brand", "domain", "fit", "fit_category", "uk_based", "categories", "agency_class", "agency_confidence",
           "trigger", "active_ads", "established", "earliest_ad_start", "junk_domain", "recent_ads", "latest_ad_start", "shopify", "klaviyo", "other_crm",
           "meta_pixel", "uk_signal", "evidence_urls", "ad_library_url", "sources"]


def _route(label):
    if label in ("hybrid", "agency_run"):
        return "agency_channel"
    if label == "in_house_only":
        return "self_serve_outbound"
    return "qualify_first_touch"


def score_account(acc, cfg):
    w = cfg["scoring"]["weights"]
    t = acc.get("tech") or {}
    label = (acc.get("agency") or {}).get("classification", "unknown")
    feats = {
        "shopify": t.get("shopify") is True or bool(acc.get("declared_shopify")),
        "klaviyo": t.get("klaviyo") is True or bool(acc.get("declared_klaviyo")),
        "other_crm": t.get("hubspot") is True or t.get("customerio") is True,
        "uk_signal": bool(t.get("gbp") or t.get("uk_tld")),
        "meta_pixel": t.get("meta_pixel") is True,
    }
    base = sum(w[k] for k, v in feats.items() if v)
    base += w["active_ads"] * active_ads_score(acc.get("active_ads", 0))
    base += w["recent_ads"] * bool(acc.get("recent_ads"))
    base += w.get("established", 0) * bool(acc.get("established"))
    junk = is_junk_domain(acc["domain"])
    base += w.get("junk_domain", 0) * junk
    base = max(base, 0)
    trig = (acc.get("agency") or {}).get("trigger", "none")
    if trig in ("open_paid_role", "new_hire", "agency_exit"):
        base += 1.0
    score = round(base * cfg["scoring"]["agency_multiplier"][label], 2)
    tiers = cfg["scoring"]["tiers"]
    tier = "A" if score >= tiers["A"] else "B" if score >= tiers["B"] else "C"
    route = _route(label)
    fit = (acc.get("fit") or {}).get("fit")
    uk = (acc.get("fit") or {}).get("uk_based")
    if fit == "no" or uk == "no":
        route, score, tier = "not_icp", 0, "-"
    elif fit == "enterprise":
        route, tier = "enterprise_sales", "-"
    if route == "agency_channel":
        tier = "-"
    ag = acc.get("agency") or {}
    return {
        **feats, "tier": tier, "route": route, "score": score, "brand": acc.get("brand") or acc["domain"],
        "domain": acc["domain"], "categories": acc.get("categories", []), "agency_class": label,
        "agency_confidence": ag.get("confidence", ""), "trigger": trig, "active_ads": acc.get("active_ads", 0),
        "recent_ads": bool(acc.get("recent_ads")), "latest_ad_start": acc.get("latest_ad_start", ""),
        "established": bool(acc.get("established")), "earliest_ad_start": acc.get("earliest_ad_start", ""),
        "junk_domain": junk, "fit": fit or "", "fit_category": (acc.get("fit") or {}).get("category", ""),
        "uk_based": uk or "",
        "evidence_urls": [e["url"] for e in ag.get("evidence") or []],
        "ad_library_url": acc.get("ad_library_url", ""), "sources": acc.get("sources", []),
    }


def run(cfg):
    rows = [score_account(a, cfg) for a in load_accounts().values()]
    rows.sort(key=lambda r: (r["route"] != "self_serve_outbound", -r["score"]))
    write_csv(OUT / "prospects.csv", rows, COLUMNS)
    tiers = Counter(r["tier"] for r in rows if r["route"] != "agency_channel")
    routes = Counter(r["route"] for r in rows)
    labels = Counter(r["agency_class"] for r in rows)
    lines = [
        "# Prospect run summary", "",
        f"- Accounts: {len(rows)}",
        f"- Routes: " + ", ".join(f"{k} {v}" for k, v in routes.most_common()),
        f"- Agency classification: " + ", ".join(f"{k} {v}" for k, v in labels.most_common()),
        f"- Self-serve tiers: " + ", ".join(f"{k} {v}" for k, v in sorted(tiers.items())),
        f"- With Klaviyo detected or declared: {sum(r['klaviyo'] for r in rows)}",
        f"- Actively advertising on Meta (UK): {sum(1 for r in rows if r['active_ads'])}",
        "", "## Top 15 self-serve targets", "",
        "| Tier | Brand | Score | Agency | Trigger | Active ads | Evidence |", "|---|---|---|---|---|---|---|",
    ]
    for r in [r for r in rows if r["route"] == "self_serve_outbound"][:15]:
        ev = r["evidence_urls"][0] if r["evidence_urls"] else ""
        lines.append(f"| {r['tier']} | {r['brand']} | {r['score']} | {r['agency_class']} ({r['agency_confidence']}) "
                     f"| {r['trigger']} | {r['active_ads']} | {ev} |")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return {"rows": len(rows), **{f"route_{k}": v for k, v in routes.items()}}
