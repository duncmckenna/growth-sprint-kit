"""Agency-involvement research is done by Claude Code subagents (see .claude/commands/classify-agency.md).

This module only prepares batches and validates/merges what the agents return, so a
classification without cited evidence can never reach the scored list.
"""
import json
from pathlib import Path

from .common import DATA, is_junk_domain, is_nonretail, load_accounts, read_json, save_accounts, write_json

LABELS = {"in_house_only", "hybrid", "agency_run", "unknown"}
CONF = {"high", "med", "low"}
TRIGGERS = {"open_paid_role", "new_hire", "agency_exit", "none"}
FITS = {"yes", "no", "enterprise", "unsure"}
BATCH_DIR = DATA / "classify" / "batches"
RESULT_DIR = DATA / "classify" / "results"


def prefilter(acc):
    """Worth researching: a D2C stack signal (Shopify via DNS/HTML, Klaviyo, HubSpot, Customer.io)
    and no evidence it's non-UK. Fit and UK base are then confirmed by the research agents."""
    t = acc.get("tech") or {}
    d = acc.get("domain", "")
    stack = any(t.get(k) is True for k in ("shopify", "klaviyo", "hubspot", "customerio")) \
        or acc.get("declared_klaviyo") or acc.get("shopify_dns")
    uk_known = t.get("gbp") or d.endswith(".uk") or acc.get("source_country") == "GB"
    uk_unknown = acc.get("tech_status") != "ok"          # couldn't read the page: let research decide
    return bool(stack and (uk_known or uk_unknown) and not is_junk_domain(d) and not is_nonretail(d))


def research_rank(acc):
    """Order research by likely fit: UK signal, established advertiser, Klaviyo, ad volume."""
    t = acc.get("tech") or {}
    return (bool(t.get("gbp") or acc.get("domain", "").endswith(".uk")), bool(acc.get("established")),
            t.get("klaviyo") is True, acc.get("active_ads", 0))


def export_batches(cfg, include_all=False, refresh=False, limit=None):
    accounts = load_accounts()
    rows = [a for a in accounts.values()
            if (include_all or prefilter(a)) and (refresh or "agency" not in a)]
    rows.sort(key=research_rank, reverse=True)
    limit = limit or cfg["classify"].get("max_brands")
    if limit:
        rows = rows[:limit]
    size = cfg["classify"]["batch_size"]
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    for old in BATCH_DIR.glob("batch_*.json"):
        old.unlink()
    for i in range(0, len(rows), size):
        chunk = [{"domain": a["domain"], "brand": a.get("brand") or a["domain"]} for a in rows[i:i + size]]
        write_json(BATCH_DIR / f"batch_{i // size + 1:03d}.json", chunk)
    return {"brands": len(rows), "batches": -(-len(rows) // size) if rows else 0}


def _validate(r):
    errs = []
    label = r.get("classification")
    if label not in LABELS:
        errs.append(f"bad classification {label!r}")
    if r.get("confidence") not in CONF:
        r["confidence"] = "low"
    if r.get("trigger") not in TRIGGERS:
        r["trigger"] = "none"
    ev = [e for e in r.get("evidence") or [] if isinstance(e, dict) and str(e.get("url", "")).startswith("http")]
    r["evidence"] = ev
    if label in LABELS - {"unknown"} and not ev:
        errs.append("no cited evidence; downgraded to unknown")
        r["classification"], r["confidence"] = "unknown", "low"
    return r, errs


def merge_results():
    accounts = load_accounts()
    merged, problems = 0, []
    for f in sorted(RESULT_DIR.glob("*.json")):
        try:
            results = json.loads(Path(f).read_text())
        except json.JSONDecodeError as e:
            problems.append(f"{f.name}: invalid JSON ({e})")
            continue
        for r in results:
            d = r.get("domain")
            if d not in accounts:
                problems.append(f"{f.name}: unknown domain {d!r}")
                continue
            r, errs = _validate(r)
            problems += [f"{d}: {e}" for e in errs]
            accounts[d]["agency"] = {k: r.get(k) for k in
                                     ("classification", "confidence", "evidence", "in_house_roles_public", "trigger", "notes")}
            fit = r.get("fit") if r.get("fit") in FITS else "unsure"
            accounts[d]["fit"] = {"fit": fit, "uk_based": r.get("uk_based", "unsure"),
                                  "category": r.get("category", ""), "fit_reason": r.get("fit_reason", "")}
            merged += 1
    save_accounts(accounts)
    write_json(DATA / "classify" / "merge_problems.json", problems)
    return {"merged": merged, "problems": len(problems)}
