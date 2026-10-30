---
description: Run the full prospecting pipeline end to end (optionally for named categories)
argument-hint: "[category ...] e.g. home_furniture garden_outdoor"
---

Run the Outra prospecting pipeline. Categories: $ARGUMENTS (if empty, use every category in config.yaml).

1. **Pre-flight**
   - Check that `META_AD_LIBRARY_TOKEN` is set: `test -n "$META_AD_LIBRARY_TOKEN"`. If it isn't, stop and tell me.
   - Check that `contact_for_user_agent` in config.yaml is filled. If it isn't, ask me for it.
2. **Seed.** Run `python -m prospector seed-ads`, adding `--category <c>` for each category given. Report the ads found per keyword and how many pages were unresolved.
3. If any CSVs exist in `data/imports/`, import each one (use the source named in the filename prefix: `storeleads_`, `builtwith_` or `manual_`), then run `python -m prospector ad-activity`.
4. **Tech check.** Run `python -m prospector techcheck`, then `python -m prospector page-activity` (re-pulls each shortlisted brand's full active ads, so 'established' is accurate).
5. **Agency research.**
   - Run `python -m prospector export-batches`.
   - Then follow `.claude/commands/classify-agency.md` exactly.
   - Then run `python -m prospector merge`. If `data/classify/merge_problems.json` is non-empty, summarise the problems.
6. **Score.** Run `python -m prospector score`.
7. **Report.** Show `out/summary.md`, then give me 3 bullets:
   - what's surprising
   - the share of brands that are in-house-only, among those classified with high or medium confidence. This is the week-1 sizing test for the filter.
   - what to check by hand

   Keep it short.
