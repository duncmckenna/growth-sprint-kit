---
description: Research who runs each brand's paid media (in-house only / hybrid / agency-run) with parallel subagents
---

Research batches are in `data/classify/batches/batch_*.json`. Each file holds 10 or fewer `{domain, brand}` objects.

1. List the batch files. For each batch that has no matching `data/classify/results/<same name>`, launch one subagent (Agent/Task tool, general-purpose type). **Launch them in parallel, at most 5 at a time.** Give each the prompt below with its batch contents pasted in.
2. When each subagent returns, extract the JSON array from its reply. Write it to `data/classify/results/<batch name>` exactly as returned; don't edit classifications. If the JSON is invalid, ask that subagent once to return valid JSON only.
3. When every batch has a result file, stop. Don't run the merge; the caller does that.

## Subagent prompt (paste the batch where it says)

```
You are a B2B research analyst. For each brand below, first judge FIT, then who runs its paid media.

FIT for Outra's £699/month self-serve product:
- fit "yes": a genuine UK-based D2C brand (own site, sells to UK consumers) of SME / mid-market size
- fit "enterprise": a large retailer or household name with its own data team (e.g. national chains), not self-serve
- fit "no": marketplace, dropshipper/throwaway store, app, publisher, non-UK brand, or not a consumer brand
- fit "unsure": not enough evidence
Also give uk_based (yes/no/unsure), a short category (e.g. "sofas", "beds & mattresses", "fashion") and a one-line fit_reason.

Then determine who runs its paid media (Meta/TikTok/Google ads) day to day. If fit is "no", skip this and return classification "unknown":
- in_house_only: an in-house paid social/PPC/performance person or team and no evidence of a paid-media agency
- hybrid: in-house paid role(s) AND an agency working on paid media
- agency_run: an agency runs paid media and there's no in-house paid specialist
- unknown: not enough evidence

Use WebSearch and WebFetch only. Check, in this order:
1. The brand's own careers/jobs page and recent job ads for paid social, PPC, performance or acquisition roles. Read the wording about agencies ("manage our agency partners" → hybrid; "own paid social in-house" / "bring paid in-house" → in-house signal).
2. Agency websites, case studies and awards entries that name the brand as a paid media / paid social / PPC client. Search queries like: "<brand>" paid social agency case study; "<brand>" PPC agency; "<brand>" performance marketing agency.
3. Public search-result snippets showing job titles at the brand (paid social, PPC, performance, acquisition, growth marketing). Do NOT open, log in to or browse linkedin.com, facebook.com or instagram.com pages; snippets in search results only.

Rules:
- Never guess. A classification other than "unknown" needs at least one evidence item with a working URL.
- Agency evidence older than 2 years is low confidence (agencies churn). A creative/branding-only agency does not count as paid-media agency involvement; note it.
- trigger: "open_paid_role" if an open paid role is advertised now; "new_hire" if a paid role holder started in the last ~90 days (from public evidence); "agency_exit" if evidence shows paid moved in-house recently; else "none".
- Spend at most ~6 searches per brand; move on.

Return ONLY a JSON array, one object per brand, no prose:
[{"domain": "...", "brand": "...", "fit": "yes|enterprise|no|unsure", "uk_based": "yes|no|unsure", "category": "...", "fit_reason": "<=15 words",
  "classification": "in_house_only|hybrid|agency_run|unknown",
  "confidence": "high|med|low",
  "evidence": [{"signal": "job_ad|agency_case_study|award|title_snippet|other", "summary": "<=20 words", "url": "https://...", "date": "YYYY-MM or unknown"}],
  "in_house_roles_public": ["Paid Social Manager", "..."],
  "trigger": "open_paid_role|new_hire|agency_exit|none",
  "notes": "<=25 words"}]

Brands:
<PASTE BATCH JSON>
```
