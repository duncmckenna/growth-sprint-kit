# Outra prospector: setup and run

Finds UK D2C brands that are actively advertising on Meta, run Shopify + Klaviyo, and run paid media in-house with no agency involved. Claude Code runs the whole thing.

## One-off setup (do this days before the interview; Meta verification can take time)
1. **Meta Ad Library API access.** It's free and official, and UK commercial ads are covered.
   - Go to developers.facebook.com, create an app, and complete identity verification for the Ad Library API.
   - Generate a user access token. Extend it to the long-lived version, which lasts about 60 days.
   - Run `export META_AD_LIBRARY_TOKEN=...`, or put it in your shell profile.
   - Set `meta.graph_version` in `config.yaml` to the current Graph API version.
2. **Install the dependencies:** `pip install -r requirements.txt`, then run `python -m pytest -q` (it should show 7 passed).
3. **Config:** put a contact email in `contact_for_user_agent` in `config.yaml`, and check the keyword lists per category.
4. **Optional seed lists:** drop exports in `data/imports/` named `storeleads_*.csv`, `builtwith_*.csv` or `manual_*.csv`. Storeleads CSV export needs its Pro plan, and BuiltWith needs its Lists product. Neither is required: the Ad Library seed already selects brands that are actively spending.

## Run
Open Claude Code in this folder and type:
```
/prospect home_furniture garden_outdoor
```
Or run it with no arguments for all categories. Claude runs the Python stages, fans out research subagents for the agency check, merges the results and summarises them.

**Outputs:**
- `out/prospects.csv`: every account with its route, tier, score, evidence URLs and Ad Library link.
- `out/summary.md`: counts plus the top 15 self-serve targets.

**To run headless** (for example, overnight before the day):
```
claude -p "/prospect home_furniture"
```

## For the interview
- Run it in advance on 1–2 categories so you have a real sample, and say that you did.
- On the day, re-run one keyword live (`seed-ads --category pet`, then `techcheck`, then `/classify-agency` on one batch) to show it working.
- The in-house-only share among classified brands is your week-1 sizing test for the filter.
