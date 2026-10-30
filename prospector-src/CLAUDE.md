# Outra prospector

This repo finds UK D2C brands for Outra's £699/month self-serve platform that:
1. are actively advertising on Meta in the UK,
2. run Shopify + Klaviyo (or HubSpot / Customer.io),
3. run paid media **in-house with no agency involved** (Duncan's filter: agency involvement, not spend, decides the route).

The output is `out/prospects.csv` and `out/summary.md`, company-level and routed:
- `self_serve_outbound`
- `agency_channel`
- `qualify_first_touch`

## Pipeline (run `/prospect` to do all of it)

| Step | Command | What it does |
|---|---|---|
| 1 | `python -m prospector seed-ads` | Meta Ad Library API: wedge keywords → advertisers with active UK ads → domains from ad captions |
| 1b | `python -m prospector import <csv> --source storeleads\|builtwith\|manual` | Optional extra seed lists |
| 1c | `python -m prospector ad-activity` | Ad Library lookup for imported accounts |
| 2 | `python -m prospector techcheck` | One polite homepage GET per domain: Shopify, Klaviyo, HubSpot, Customer.io, pixels, GBP |
| 2b | `python -m prospector page-activity` | Re-pull each shortlisted brand's own active ads by page_id: accurate ad count + `established` (an ad running 30+ days) |
| 3 | `python -m prospector export-batches` then `/classify-agency` then `python -m prospector merge` | Agency-involvement research by parallel subagents |
| 4 | `python -m prospector score` | Scores, tiers and routes |

`python -m prospector status` shows the counts at each stage. Every stage is resumable, and state lives in `data/accounts.json`.

## Hard rules
- **Company-level only.** Never collect named individuals' contact details in this repo. People-finding happens in Sales Navigator, Apollo or Cognism under their licences.
- **No LinkedIn automation.** Never log in to, browse, scrape or automate LinkedIn, Facebook or Instagram pages. Use the official Ad Library API only, never scrape the Ad Library website.
- **Polite fetching.** techcheck fetches one homepage per domain, respects robots.txt and sends an identifying User-Agent. Don't add crawling of other pages.
- **Never fabricate a classification.** No cited URL means `unknown`. The merge step enforces this; don't work around it.
- **Never change config weights to make a result look better.** If a result looks wrong, report it.
- **Facts vs inference.** Tag claims in summaries as [F] observed or [I] inferred.

## Known limits (say these out loud in the interview)
- Ad caption domains are noisy. Pages with no resolvable domain go to `data/meta_unresolved_pages.json` for a manual look.
- Pixels loaded through Google Tag Manager are invisible in raw HTML, so they show as `unknown`, not `false`.
- Keyword search finds advertisers whose ad text matches. It is a seed, not a census. Exact-phrase search (config) cuts noise.
- Keyword results come newest-first, which favours brand-new advertisers. `page-activity` corrects this; throwaway domains (e.g. `brand-com.store`) are penalised and kept out of research.
- Agency involvement is hard to see from outside. Expect many `unknown`s, which route to `qualify_first_touch` (ask "Who runs your paid media day to day?").
