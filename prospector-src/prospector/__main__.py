"""CLI: python -m prospector <command>

  seed-ads [--category X ...]      Meta Ad Library keyword search -> accounts (UK, active ads)
  import <csv> --source NAME       Storeleads / BuiltWith / manual CSV -> accounts
  ad-activity                      Meta Ad Library lookup for imported accounts
  page-activity                    Re-pull full active ads per shortlisted brand (accurate 'established')
  techcheck [--refresh|--retry-failed]  Homepage stack check (Shopify, Klaviyo, pixels, GBP)
  dnscheck                         Detect Shopify stores via DNS (fast; not rate-limited)
  export-batches [--all]           Write research batches for /classify-agency
  merge                            Validate + merge subagent research results
  score                            Write out/prospects.csv and out/summary.md
  status                           Counts at each stage
"""
import argparse
import json

from . import classify, imports, meta_ads, score, techcheck
from .common import load_accounts, load_config


def main():
    ap = argparse.ArgumentParser(prog="prospector")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("seed-ads"); s.add_argument("--category", action="append")
    s = sub.add_parser("import"); s.add_argument("csv"); s.add_argument("--source", required=True)
    sub.add_parser("ad-activity")
    sub.add_parser("page-activity")
    s = sub.add_parser("techcheck"); s.add_argument("--refresh", action="store_true"); s.add_argument("--retry-failed", action="store_true"); s.add_argument("--max-minutes", type=float)
    s = sub.add_parser("export-batches"); s.add_argument("--all", action="store_true"); s.add_argument("--refresh", action="store_true"); s.add_argument("--limit", type=int)
    sub.add_parser("merge"); sub.add_parser("score"); sub.add_parser("status"); sub.add_parser("dnscheck")
    a = ap.parse_args()
    cfg = load_config()

    if a.cmd == "seed-ads":
        res = meta_ads.seed_from_ads(cfg, categories=a.category)
    elif a.cmd == "import":
        res = imports.import_csv(a.csv, a.source)
    elif a.cmd == "ad-activity":
        res = meta_ads.enrich_ad_activity(cfg)
    elif a.cmd == "page-activity":
        res = meta_ads.refresh_page_activity(cfg)
    elif a.cmd == "techcheck":
        res = techcheck.run(cfg, refresh=a.refresh, retry_failed=a.retry_failed, max_minutes=a.max_minutes)
    elif a.cmd == "export-batches":
        res = classify.export_batches(cfg, include_all=a.all, refresh=a.refresh, limit=a.limit)
    elif a.cmd == "dnscheck":
        res = techcheck.dnscheck()
    elif a.cmd == "merge":
        res = classify.merge_results()
    elif a.cmd == "score":
        res = score.run(cfg)
    else:
        accs = load_accounts().values()
        res = {"accounts": len(accs),
               "tech_checked": sum(1 for x in accs if "tech" in x),
               "prefiltered": sum(1 for x in accs if classify.prefilter(x)),
               "classified": sum(1 for x in accs if "agency" in x)}
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
