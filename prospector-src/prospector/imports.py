"""Import account lists exported from Storeleads, BuiltWith or a hand-made CSV.

Column names are matched loosely so exports work without editing. Storeleads CSV export
needs its Pro plan; BuiltWith exports come from its Lists product. Neither is required:
the Meta Ad Library seed works on its own.
"""
import csv

from .common import load_accounts, normalise_domain, save_accounts, upsert

DOMAIN_COLS = ["domain", "website", "url", "store url", "root domain", "site"]
NAME_COLS = ["name", "store name", "company", "brand", "title", "merchant name"]
APPS_COLS = ["apps", "installed apps", "technologies", "technology", "tech"]
CAT_COLS = ["categories", "category", "vertical"]
SALES_COLS = ["estimated monthly sales", "estimated sales", "monthly revenue", "est. monthly sales"]


def _pick(row, cols):
    low = {k.lower().strip(): v for k, v in row.items() if k}
    for c in cols:
        if low.get(c):
            return low[c]
    return None


def import_csv(path, source):
    accounts = load_accounts()
    added = skipped = 0
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            d = normalise_domain(_pick(row, DOMAIN_COLS))
            if not d:
                skipped += 1
                continue
            apps = (_pick(row, APPS_COLS) or "").lower()
            tech = {}
            if apps:
                tech = {"shopify": "shopify" in apps or source == "storeleads" or None,
                        "klaviyo": "klaviyo" in apps or None}
            upsert(accounts, d, source=source, brand=_pick(row, NAME_COLS),
                   import_category=_pick(row, CAT_COLS), est_sales=_pick(row, SALES_COLS),
                   **{f"declared_{k}": v for k, v in tech.items() if v})
            added += 1
    save_accounts(accounts)
    return {"rows_imported": added, "rows_skipped": skipped, "accounts": len(accounts)}
