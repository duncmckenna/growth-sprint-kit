# KNOWLEDGE (public edition): growth acquisition sprint

Public, role-based version of the method. Paste private context (brief documents, people notes) separately on the day.


---

# 02 Intake: fill on the day and paste in at P0

Copy this block, fill what you know (leave a field blank if unknown) and paste it.

```
=== SPRINT INTAKE ===
Candidate/brief documents supplied (paste or attach each):
Exact brief text (paste verbatim, if different from 01):
Time available (mins) and hard stop time:
Output format they want (deck / doc / anything; slide count?):
Panel members for the review:
Materials supplied (data, dashboards, docs) — paste or summarise:
Outra login available? (Y/N; whose account; any data I may use):
Tools available (Claude / ChatGPT / Lovable — my accounts or theirs?):
Targets given (new customers, MRR, period):
Budget / headcount given:
Answers to my clarifying questions (from the panel):
  - Current trial volume & trial→paid (card-entered trials only?):
  - Demo funnel (booked / attended / next step taken; what counts as "next action"?):
  - Integration connect rate / activation data:
  - Is the target gross or net, incremental or total? Budget new or existing?
  - Current best-fit customers / segments:
  - Sales capacity for demos / onboarding:
  - Anything else said in the room:
Constraints or no-go areas mentioned:
My instinct right now (one line, optional):
=== END ===
```

## Defaults when a field is blank (always tagged [A] and shown on the assumptions slide)
| Variable | Default | Why |
|---|---|---|
| Period | 90-day plan with a 12-month target | Shows sequencing plus ambition |
| Target | 100 net new paying self-serve accounts in 12 months (about £70k MRR, about £840k ARR) | Round, testable, and big enough to matter; easy to rescale |
| Gross margin | 80% | Typical data-SaaS ballpark; flagged as an assumption |
| Monthly churn | 5% base (3% good, 8% bad) | Self-serve SMB range; there is no Outra data |
| CAC payback | 12 months or less | Common SaaS guardrail |
| Budget | Ask; otherwise size it from the CAC ceiling × target | Budget follows economics |
| Team | The existing team plus AI | Don't propose new hires first |


---

# 03 Strategy engine

Pre-built analysis to adapt on the day, not to recite. Every number is a scenario until the panel gives real inputs. Re-run with code whenever an input changes.

## §0 Read the supplied data first (run before §1 whenever the panel gives numbers)
1. **Definitions check.**
   - Is the target gross or net of churn? Incremental or total?
   - Self-serve only, or including sales-sourced?
   - Is the budget new money or the existing total?
   - Does "trial" mean card-entered sign-ups only?
   - What does "next action" mean after a demo?
   Ask the panel any of these that change the answer.
2. **Run-rate vs target.** Current volume × current conversion × window gives the baseline. If the baseline is at or above the target, say so early and frame it as a clarifying question plus an upside: "So I've read the 60 as incremental, which means the prize from fixing activation is large." Never present it as underperformance.
3. **Decompose the rate.** Overall rate = step A × step B (for example, connect rate × connected→paid). Count the trials lost at each step: the biggest absolute loss is the first fix.
4. **Benchmark check.** Compare against §07 benchmarks. If the data contradicts a "fact" in the pack (for example, a 9% trial→paid rate against card-required benchmarks of 25–35%), the data wins. Flag the contradiction as a question ("is the card step live for all sign-ups?").
5. **Ramp model (by month, in code):**
   - paid_m = trials_m × conversion_m
   - Split the gain into a conversion effect and a volume effect.
   - Trials started in the last ~3 weeks convert after the window closes. Exclude them, or show them separately.
   - Net of churn, apply an assumed monthly churn [A] to each new cohort when asked for net adds.
6. **Capacity model.** Human touches per month (demos plus activation sessions) = accounts routed to assist × sessions per account. Compare against the stated capacity (for example, the current demo volume). **The assist threshold is set by capacity first and by the value of a call second.**
7. **Budget → CAC per channel.** Build a table:

   | Channel | £/month | Expected trials | Trial→paid | Paid accounts | CAC |
   |---|---|---|---|---|---|

   Sum it and check the blended CAC against the §1 cap. This is the pipeline maths per channel that a CRO will look for.
8. **Sensitivity table.** Put the 2 most uncertain rates on the axes (for example, activation × activated→paid) and paid accounts in the cells. Mark the plan case and the break-even-to-target contour.

**Payback horizon:** default 12 months. When the plan window is 6 months or less, also show 6-month payback, since a short window suggests cash discipline.

## §1 Economics guardrails (computed; rerun with real inputs)

**Customer-side break-even.** Does Outra pay for itself? A customer needs monthly ad spend of at least fee ÷ efficiency gain.

| Efficiency gain | Break-even monthly spend | Spend for a 3× return on the fee |
|---|---|---|
| 10% | £6,990 | £20,970 |
| 15% | £4,660 | £13,980 |
| 20% | £3,495 | £10,485 |

So the ICP floor is roughly £5–7k/month of addressable paid media [I]. **Default floor: £7,000**, the break-even point in the conservative 10% case. Between about £4.7k and £7k, the product pays back only if the gain reaches about 15% or more, so treat that range as "borderline: trial with expectations set". Below that, the product cannot pay back even if it works. That is a qualification rule, not just a slide.

**Outra-side CAC ceiling.** ARPA is £699/month (£8,388/year), and gross margin is assumed at 80% [A].

| Monthly churn | Lifetime | LTV (gross margin) | Max CAC at 3:1 |
|---|---|---|---|
| 3% | 33 months | £18,640 | £6,213 |
| 5% | 20 months | £11,184 | £3,728 |
| 8% | 12.5 months | £6,990 | £2,330 |

A 12-month payback (gross margin) caps CAC at £6,710; a 6-month payback caps it at £3,355.

**What follows** [I]: at a CAC of roughly £2–4k, Outra can afford light sales assistance (a demo or onboarding call), but not a field-sales motion. The design is product-led acquisition with sales assist above a spend threshold, and the economics decide which accounts get a human.

**Usage-based pricing note:** the pricing calculator tiers by ad spend (Starter under £50k, Growth under £100k, then Scale) and floors the total at £699 [F] (§07). Expansion revenue from spend growth is therefore possible, but its size is unknown [I]. Ask the panel whether expansion is real before relying on NRR to offset churn.

**Funnel back-solve** (rerun with real rates). Target: 100 paid accounts in 12 months, about 8.3 a month.

**Benchmark** [F]: card-required B2B trials typically convert 25–35% trial→paid ("good"); no-card trials convert 4–6% (ChartMogul, Growth Unhinged and ProductLed, Jan 2026; §07 C). Outra's trial requires a card [F].

**Funnel assumptions** [A]:

| Trial → paid | Trials needed per month | Visits needed at 2% visit→trial | Visits needed at 5% |
|---|---|---|---|
| 25% | 33 | 1,667 | 667 |
| 35% | 24 | 1,190 | 476 |

**Why activation is the main lever** [A]: trial→paid = activation rate × activated→paid. With 50% of activated trials converting, raising activation (first audience live with a test running) from 50% to 70% moves trial→paid from 25% to 35%. That cuts the trials needed by about 30%, which is worth more than most acquisition channels.

**Market headroom** [I]: about 45,500 UK stores use Klaviyo [F] (Storeleads, Oct 2026). If 10–20% clear the spend floor [A], that leaves about 4,500–9,100 qualified accounts. 100 customers would be roughly 1–2% penetration, so the constraint is conversion and proof, not market size.

**Motion benchmark** [F]: from roughly $100 ASP upward, most B2B product-led companies layer sales over self-serve (ChartMogul GTM report). At £699 (about $900), a hybrid motion is the norm.

## §2 ICP and the wedge
Score candidate segments from 1 to 5 on each criterion:
1. Paid social/CTV spend at or above the floor
2. Household attributes predict purchase (affluence, life stage, property, moving)
3. Already on Klaviyo, HubSpot or Customer.io, plus Meta or TikTok (the integrations exist, so time to value is low)
4. UK-only customer base
5. Considered purchase or high AOV, so each efficiency gain is worth more
6. Reachable as a cluster (shared agencies, communities, app ecosystems)
7. Outra has a unique edge (move stage, property data)
8. **Paid media run in-house with no agency involved** (Duncan's filter: the test is agency involvement, not spend)

### The in-house-only filter (Duncan's call; default ON)
**Target:** brands whose paid media is run **in-house with no agency involved**, meaning there is a paid social, PPC or performance marketer on staff and no agency on paid. **The test is agency involvement, not spend.** A brand with an in-house hire that *also* uses an agency still carries the agency problem.

**Why agency involvement is the problem** [I]:
- **The agency is the real user and gatekeeper.** It controls the ad accounts and Business Manager, and decides which tools and data go in.
- **It may block a tool it didn't choose.** It may bring its own data and tooling, or see Outra as a threat to its value-add.
- **The win gets misattributed.** If performance improves, the agency takes the credit, and the brand doesn't see what Outra contributed.
- **Agencies need a different motion.** Agencies are typically served by the agency motion, not £699 self-serve, and putting their clients on self-serve risks channel conflict and cannibalisation (brief #3). **Frame the filter as routing each buyer to the right motion, never as "avoiding agencies".**

**Why in-house-only works** [I]:
- **One decision-maker who is also the hands-on user.** The person who builds the audience, runs the inclusion/exclusion test and connects Klaviyo is the same person who decides. That directly attacks the activation leak, because trials with no hands-on owner are the ones that never connect.
- **Credit for the result lands with Outra.** The lift is visible to the brand, which feeds proof, retention and case studies.
- **A spend floor comes as a bonus.** A dedicated hire usually implies meaningful spend. This is secondary, not the reason for the filter. Salary data for paid roles specifically isn't public (Digital Waffle's 2026 guide gives only a £46k average across all social roles), so treat the link as an inference.

**How to detect agency involvement:** no single external signal is reliable [I], so stack the evidence.
1. **In-house signal:**
   - **Licensed sources:** paid social, PPC or performance titles from Sales Navigator, Apollo or Cognism, kept at company level and PECR-safe.
   - **Hiring triggers:** open roles in these titles, or a new hire in role under 90 days.
2. **Agency signals to exclude:**
   - **Job-ad wording:** "manage our agency partners" or "work alongside our agency" signals agency involvement; "own our paid social in-house" signals none.
   - **Agency client lists:** the brand named on an agency's client page, in its case studies or in awards entries.
   - **LinkedIn mentions:** the brand appearing in agency staff's posts.
3. **Ask directly.** "Who runs your paid media day to day?" goes in the Lovable tool and the sign-up flow. It is the only fully reliable signal, so it is load-bearing.

**Routing:**
- **In-house only →** self-serve trial. This is the core target.
- **Hybrid (in-house plus agency), or agency-run →** the agency channel. Before the Agency plan launches, offer a joint session with the agency. These brands are routed, not lost, and become agency-plan pipeline.
- **Founder or generalist, with no specialist →** an activation session, because there is no hands-on owner.

**Limits to state honestly** [I]:
- **Hybrids are common, so the filter shrinks the list a lot.** That's deliberate, but size it in week 1: sample about 200 wedge brands and measure the in-house-only share. If it's too small, relax it to "in-house plus a non-paid agency" (for example, a creative-only agency).
- **Agency status changes.** Brands bring paid in-house as they grow, which is a trigger in its own right (a new paid hire after an agency exit). Re-check quarterly.
- **Job titles vary.** "Growth Marketer" and "Digital Marketing Manager" may own paid, so use title clusters, not one title.

**Persona consequence:** two users per account.
1. The paid media manager, who builds audiences and runs exclusion and lift tests. Message: practitioner, test-led.
2. The CRM or retention owner, who uses Klaviyo enrichment.

The economic buyer is the head of growth or the founder, and the message to them is the ROI and break-even verdict.

Starting hypotheses [I]:

| Segment | Why | Risk |
|---|---|---|
| **Home & living D2C** (furniture, beds, home décor, kitchenware) | Movers are their peak buyers; Home Move Triggers is unique; high AOV | Seasonal, discount-led |
| **Home services & energy D2C** (solar, heat pumps, EV chargers, smart home, broadband challengers) | Property type and tenure decide eligibility, so the data is the targeting | Lead-gen economics vary |
| **Premium subscription D2C** (food boxes, pet, baby, wellness) | Life stage and affluence predict LTV; strong CRM users | May lean on Meta broad targeting already |
| **Considered-purchase financial or insurance challengers** | Historic Outra strength | Compliance and vulnerability scrutiny; more enterprise-like |

**Recommended wedge (default)** [I]: home and living, plus home services, led by **movers**. It is the most defensible edge (Hometrack heritage, move-stage data), the easiest story to tell ("reach households 4–12 weeks before they move" [I]; check the product's actual timing claim), and every mover-adjacent category can be clustered. Duncan decides at P3.

## §3 Funnel map and likely leaks
Awareness → visit → trial start → connect integrations → first audience or enrichment live → first campaign spend → lift visible → paid → expand.

| Leak | Hypothesis | Fix to propose |
|---|---|---|
| Demo → next action (known, raised by the CEO) | Common causes in this category: the prospect never sees their own data in the demo; momentum fades without a booked next step; no shared definition of success. Ask which apply; don't assert. **On a slide, phrase it as an upgrade, not a diagnosis.** | Demo on the prospect's own CRM sample or segment; finish by booking an activation session in the calendar; a mutual action plan that defines a "win"; same-day follow-up drafted by AI from the call summary (summaries already exist) |
| Trial → activated | Integration friction; no clear first use case | Use-case templates by segment ("Movers in your catchment", "lookalike of your top 20% LTV"); a checklist; human assist above the spend threshold |
| Activated → paid | The 14-day trial ends before Outra's own stated 2–3 week learning window does [F] (§07), so many trials end before any lift is visible [I] | Start the trial clock at first audience live, or extend for qualified accounts; build in a holdout test so lift is measurable; send a "results so far" email on day 10 |
| Paid → retained (feeds acquisition via referrals and case studies) | Fuzzy attribution | A standard lift-test design; a monthly value report; case-study pipeline |

## §4 Channel scoring
Score each channel 1–5 on: ICP reach, intent, CAC fit within the ceiling, speed to signal (90 days), scalability, and Outra's right to win.

**Weighting:** CAC fit ×2 and speed ×2 when the plan window is 6 months or less, otherwise reach ×2 and scalability ×2.

**Dependency rule:** if a channel depends on something not yet launched, cap its speed score at 2 and say what it depends on. Check whether the agency offer is live before capping agencies.

| Channel | Role [I] | Notes |
|---|---|---|
| **Ecosystem distribution** (Klaviyo, HubSpot and Shopify app directories; integration co-marketing) | Capture intent at the point of setup | No Outra listings were found [F]. The bar is low [F]: Klaviyo needs 5 production installs, OAuth and a security review; HubSpot needs 3 unaffiliated installs; Shopify takes 0% revenue share on the first $1M. Klaviyo's partner programme also offers co-marketing |
| **Agency partners** | Leverage: one agency reaches many brands | A Head of Agency Sales exists and "Agency" is coming soon; offer a partner tier or revenue share; agencies run the lift tests |
| **Signal-based outbound to in-house-only paid teams**, using licensed firmographics, technographics (Klaviyo/Shopify), role or hiring signals, and agency-exclusion signals | Precise, testable, fast to signal | List = wedge category × Klaviyo/Shopify × in-house paid hire (or an open role for one) − agency signals; company-level lists; AI-personalised opener showing their own household insight; respect PECR (B2B corporate subscribers allow outreach with an opt-out, but sole traders count as individuals) |
| **Free value-first tool** (the Lovable build: break-even, fit and routing) | Converts curiosity to qualified trial; routes by spend | The P4 artefact. It extends the existing Playground and price calculator (§07) by adding email capture, a break-even verdict and routing, so it builds on what exists rather than replacing it |
| **Content and data PR** ("UK Movers Index" from aggregated Outra data) | Authority plus earned reach; the data is unique | Aggregated, non-personal; also useful for partners' content |
| **Paid search and LinkedIn** | Harvest intent; test messaging | Keep small until conversion rates are known |
| **Community and events** (UK D2C events, founder communities) | Trust and proof | Use for case-study amplification |

**Default top 3** [I], updated for the in-house filter:
1. Signal-based outbound to in-house-only paid teams in the wedge
2. The ecosystem plus the free value-first tool
3. Agency partners, sequenced after the Agency plan launches and focused on agency-run and hybrid brands, which the filter routes away from self-serve

Content and data PR run underneath as fuel. If the panel says agencies already drive most sign-ups, revisit the order.

## §5 Binding constraint (choose one and defend it)
Candidates:
- **Proof:** there are not enough self-serve case studies with measured lift.
- **Activation:** the trial is too short to show value.
- **Qualification:** too many sub-floor accounts burn demo time.
- **Ad-platform substitution:** "Meta's AI targeting means I don't need data."

The default argument [I] is that **proof and activation together** are the constraint. Acquisition spend before fixing them leaks money, so the first 30 days fix the funnel and generate proof, days 31–90 scale the channels, and the plan says so explicitly.

## §6 The objection to pre-empt (be honest: it's the strongest one)
**The objection:** "Meta's Advantage+ / broad targeting already finds my buyers. Why pay £699 for targeting it will override?"

**The evidence mostly supports the sceptic on Meta prospecting** [F] (§07 C):
- Meta's own tests show Advantage+ Audience beats manual targeting.
- Meta has removed detailed targeting exclusions.
- There is no published head-to-head showing that lookalike or custom seeds beat broad targeting.

**Don't argue against that. Reposition around where audience selection still decides the outcome** [I]:
1. **Enrich-first (Klaviyo, Customer.io, HubSpot):** personalise email and SMS by life stage, tenure and moving status, with no Meta involvement. This is the lowest-friction land and is measurable through flow revenue.
2. **Suppression and exclusion:** stop paying to reach households unlikely to buy. Outra already offers an exclusion audience, and Meta launched exclusion-only custom audiences in 2026 (agency-reported).
3. **Selection-led channels:** addressable TV (Sky AdSmart; Sky, ITV and Channel 4 plan a self-serve SME marketplace), DV360/programmatic, and Google.
4. **Creative insight:** "who your best customers actually are" briefs the creative, which is how Meta's AI now targets.
5. **Thin or new pixels:** seeds matter more when Meta has little conversion data (practitioner view, not tested).

**Then prove it account by account with Outra's own inclusion/exclusion-vs-control test.** Don't ask the market to take it on faith.

**Strategic implication** [I]: lead acquisition messaging with "Enrich your Klaviyo + cut wasted spend + measured test", not "better Meta targeting". Duncan decides at P3.

**Don't say** [F]: "Cookies are dying." Google kept third-party cookies in Chrome (Apr 2025) and retired most Privacy Sandbox APIs (Oct 2025). The real signal-loss story is iOS ATT (about 35% opt-in) and walled-garden measurement.

## §7 90-day plan skeleton
| Days | Focus | Experiments (with success and kill criteria) | Owner |
|---|---|---|---|
| 0–30 | Fix and measure | Instrument the funnel (with GTM tech, in the CRM); spend-threshold routing; demo redesign plus AI follow-up; trial clock change for 5–10 wedge accounts; 3 lift tests | Growth + GTM Tech + Client Success |
| 31–60 | Prove and package | 3 case studies; agency pilot with 3–5 agencies; free tool live; first outbound cohort (200 companies) | Agency Sales + Performance Marketing |
| 61–90 | Scale what works | Double the best channel; app directory listings; Movers Index launch; weekly growth review cadence | Growth |

## §8 KPI tree
- **North star:** paid accounts with a measured lift.
- **Leading indicators:** qualified trials (above the spend floor), activation rate within 7 days, time to first audience, trial→paid, CAC by channel, payback.
- **Guardrails:** churn and NRR, demo-to-close time, and the share of sub-floor sign-ups.


---

# 04 Lovable build: the "Is Outra worth it for you?" tool

**Why this artefact.** It is the acquisition strategy made tangible. It does three jobs at once:
1. A **lead magnet**: a free, useful answer for the prospect.
2. **Qualification**: it applies the spend floor from the economics.
3. **Routing**: below the floor goes to nurture, mid-range to self-serve trial, high spend or agency to a booked activation call.

So it demonstrates ICP, economics and funnel design in one working thing, built live with AI.

**How to position it.** Outra already has an Audience Playground and a price calculator (§07). This tool extends them with a pay-back verdict and a recommended next step. Say "the next iteration of the Playground"; never describe what the current tools lack.

At P4, Claude fills the `{{…}}` fields from the decisions made at P3 and gives Duncan the complete prompt, ready to paste.

## Prompt template (paste into Lovable)
```
Build a single-page web app called "Is Outra worth it for you?" — a free break-even and fit calculator for UK D2C growth teams considering Outra's self-serve household-data platform (£699/month, 14-day free trial, no annual contract).

Audience: {{WEDGE_SEGMENT_DESCRIPTION}} marketers. Tone: confident, plain English, UK spelling, no hype.

INPUTS (step 1, one card, sliders + selects with sensible defaults):
- Monthly paid media spend (£0–£200,000, default £15,000)
- Main channels (multi-select: Meta, TikTok, Google Ads, DV360/programmatic, Other)
- CRM / ESP (select: Klaviyo, HubSpot, Customer.io, Other, None)
- Category (select: {{CATEGORY_OPTIONS}})
- Average order value (£)
- % of customers who are UK households (default 90%)
- Who runs your paid media day to day? (select: In-house team member / Founder or generalist / Agency / Mix of in-house and agency)
- Are you an agency? (toggle)

CALCULATION (show the workings in an expandable "How we calculate this" panel):
- Addressable spend = monthly spend × share on Meta/TikTok/Google Ads/DV360 (assume 100% of the entered spend if any of those channels is selected; let the user adjust with a "% of spend on these channels" slider)
- Scenario efficiency gains: conservative {{EFF_LOW}}%, expected {{EFF_MID}}%, strong {{EFF_HIGH}}%
- Monthly value = addressable spend × efficiency gain
- Net monthly value = value − £699
- Break-even spend = £699 ÷ efficiency gain
- Show a small bar chart of net value across the three scenarios, and a line marking break-even.
- Label all efficiency figures clearly as "illustrative scenarios, not guarantees — your trial measures your real result".

ROUTING (step 2, result card). Put thresholds as named constants at the top of the code. Evaluate rules IN THIS ORDER and stop at the first match:
1. Agency = true → "Book a 30-minute agency session — see which of your clients clear break-even" (regardless of spend).
2. Addressable spend < {{BORDERLINE}} → "Outra probably isn't worth it yet" — offer the free guide "{{NURTURE_ASSET}}" (email capture) and say why honestly.
3. {{BORDERLINE}} ≤ spend < {{FLOOR}} → "Borderline: worth a trial only if household targeting fits your category" — trial CTA, with expectations stated plainly.
4. Paid media = Agency OR Mix of in-house and agency → "Bring your agency in — book a 30-minute session for you and your agency" (keeps the account; feeds the agency channel; tag the lead 'agency-involved' in /admin).
5. Spend ≥ {{ASSIST_THRESHOLD}} OR CRM = None/Other OR paid media = Founder or generalist → "Book a 30-minute activation session — we'll build your first audience with you" primary CTA, trial secondary.
6. Otherwise (spend ≥ {{FLOOR}}, CRM is Klaviyo/HubSpot/Customer.io, paid media = In-house team member, no agency) → "Start your 14-day trial" primary CTA + a suggested first use case for their category: {{USE_CASE_BY_CATEGORY}}.

LEAD CAPTURE: name, work email, company, website. Persist submissions in the browser's localStorage (wrap reads/writes in try/catch) so they survive refresh and route changes, and show them on a hidden /admin route as a table with "spend", "category" and "routed to" columns plus a "Clear" button. Do not send data anywhere. Add a visible note: "Prototype — no data leaves this page."

DESIGN: clean, modern, generous white space, one accent colour, mobile-first, accessible contrast. Header text "Is Outra worth it for you?" with subheading "{{VALUE_PROP_ONE_LINER}}". Footer: "Illustrative prototype built for discussion."

Do not use Outra's logo or claim real customer results. Use clearly fictional example numbers only.
```

## Default fill values (if Duncan doesn't change them)
- `EFF_LOW`, `EFF_MID`, `EFF_HIGH`: 10, 15, 25. Label 25% as "customer-reported range: 20–30% lower CPA in month one (Outra)"; 10% and 15% are conservative planning cases.
- `BORDERLINE`: £4,700 (break-even at the expected 15% case, rounded)
- `FLOOR`: £7,000 (break-even at the conservative 10% case, rounded)
- `ASSIST_THRESHOLD`: £25,000 (the point where the value of a human call justifies its cost; tagged [A])
- `NURTURE_ASSET`: "The UK Movers Playbook: reaching households before they move"
- `CATEGORY_OPTIONS`: Home & furniture; Home services & energy; Subscription (food, pet, baby); Fashion & beauty; Financial services; Other
- `USE_CASE_BY_CATEGORY`:
  - Home & furniture: "Prospect households likely to move in the next 3 months"
  - Home services & energy: "Target owner-occupied houses matching your install criteria"
  - Subscription: "Build a lookalike of your top 20% LTV customers by life stage and affluence"
  - Other: "Enrich your Klaviyo list and find your best-converting household profile"
- `VALUE_PROP_ONE_LINER`: "Find out in 60 seconds whether household data will pay for itself in your ad account."

## Iteration prompts (use if there is time)
1. "Add a 'Share result' button that copies a short summary of the inputs and result to the clipboard."
2. "Add an 'Agency mode': enter up to 10 client spend levels and show which clients clear break-even, with a total portfolio value."
3. "Make the routing thresholds editable on the /admin page so the growth team can tune them."

## Fallback if Lovable is slow or unavailable
Ask Claude to build the same specification as a single self-contained HTML file (or as a Claude artifact), and say so on the AI-process slide. Switching tools under pressure is itself a good story.

## Talking points for the panel
- "It's a qualification engine disguised as a free tool. The thresholds come straight from the unit economics."
- "Agencies get a portfolio view, which makes them a distribution channel."
- "In production the leads would write to agreed the CRM fields (agreed with the GTM tech owner), with UTM source and route captured for CAC by channel."


---

# 05 Live product protocol (only if an Outra login is provided)

Goal: 15 minutes or less of hands-on use that produces real screenshots and first-hand friction notes for the deck. Using the product you are asked to sell is a signal in itself.

## Rules
- **Duncan logs in himself.** Never paste credentials into any AI tool.
- **Ask before putting any Outra data, or customer data, into a personal AI account.** Say: "Is it OK to paste outputs into my Claude, or should I use yours?"
- **Only describe what you saw.** Don't extrapolate product capabilities. Tag observations as `[F] observed`.

## Script (time-box each step)
1. **Sign-up / first screen (2 min).** Note the steps, fields and time to the first useful screen. Is a use case suggested?
2. **Build one audience for the wedge (6 min).** For example, likely movers in the next 3 months, owner-occupiers, upper affluence bands, in one region. Note:
   - the available signals and filters
   - the audience size readout
   - the destinations offered
   - anything confusing
3. **Enrich view (3 min).** What appears once a CRM is connected? Is there a sample or demo dataset?
4. **Measurement (2 min).** Is there any built-in lift or results view? If not, that supports the activation and proof argument.
5. **Capture (2 min).** Take 3 screenshots for the deck: the audience builder, the audience size, and the destinations.

## Paste back to Claude in this format
```
LIVE PRODUCT NOTES
Time to first useful screen:
Audience built (filters, size):
Destinations offered:
Measurement/lift features seen:
Friction points (max 5):
Delights (max 3):
```
Claude then folds these into:
- the activation fixes (§3 of the strategy engine)
- one deck slide: "What I saw using it today"


---

# 06 Templates

## A. Strategy one-pager (P3)
```
THE ANSWER (2 sentences): Win [wedge] first, through [top 3 channels], with a [motion] funnel that [activation fix] — targeting [N] paid accounts in [period] at CAC ≤ £[x] (payback ≤ [y] months).

1. Who: wedge ICP + qualification floor (spend ≥ £[floor]/mo, stack, UK)
2. Why us / why now: [unique edge] + [market shift]
3. How they buy: self-serve below £[assist] / sales-assist above / agencies as multiplier
4. Channels (role · first experiment · success/kill metric):
   - Channel 1:
   - Channel 2:
   - Channel 3:
5. Activation & proof: [trial clock change, lift test, demo redesign]
6. 90-day plan: 0–30 / 31–60 / 61–90
7. KPIs: north star + leading + guardrails
8. What we won't do (and why):
9. Risks & how we'd know early:
10. Asks: [decisions needed from the CEO / resources]
```

## B. Deck (8–10 slides, 30-minute review: about 12 minutes presenting, the rest discussion)
1. **The answer.** The recommendation in one sentence, plus 3 numbers: target, CAC ceiling, 90-day milestone.
2. **What has to be true.** Economics guardrails: customer break-even and Outra's CAC ceiling. the CEO will care most about this slide.
3. **Who we win first.** ICP scoring and the wedge, with why it's ours to win.
4. **Where it leaks today.** Funnel map, the demo-to-next-action fix and activation (built on existing work, never a criticism of it).
5. **How we reach them.** Top 3 channels with their roles, plus what we deliberately won't do.
6. **Built in the last 2 hours.** The Lovable tool: live demo or screenshots, and the routing logic tied to the economics.
7. **The first 90 days.** Experiments, owners, success and kill criteria.
8. **How we'll know.** KPI tree and the weekly growth review cadence.
9. **How I used AI.** From the log: tools, parallel streams, critique loops, where I overrode the AI, time saved.
10. **Assumptions and the questions I'd answer in week 1.** Every `[A]` listed, plus what data would settle each.

**Appendix:** sensitivity tables; the evidence pack with sources; the counter-strategy steelman.

## C. AI process log (append one line per step; it becomes slide 9)
```
| Time | Tool | What I asked it to do | What I kept / changed (my judgement) | Value |
|------|------|-----------------------|--------------------------------------|-------|
```
Example rows:
- `0:12 | Claude | Built the issue tree + economics from the brief | Rejected "enterprise first" — wrong brief | 10 min saved`
- `0:25 | ChatGPT | Steelman: "Outra should go agency-only" | Adopted agency as channel #1, kept self-serve | Changed channel order`
- `1:05 | Lovable | Built break-even + routing calculator from my spec | Tuned threshold to £5k | Working artefact in 20 min`

**Story for slide 9.** I used AI in three ways:
1. As an **analyst**, for speed: structure, maths and research.
2. As a **sparring partner**, for quality: a steelman from a second model, plus a panel red-team.
3. As a **builder**, for tangibility: a working tool, not a mock-up.

The judgement calls stayed mine: the wedge, the thresholds, and what to cut.

## D. 60-second opener
```
"My recommendation: [answer]. Three reasons: [economics], [edge], [channel leverage].
I'll show you the numbers that drive it, a tool I built in the last hour that puts it into practice, and the first 90 days.
I'll also show how I used AI to get here — including where I disagreed with it."
```

## E. Steelman prompt (paste into ChatGPT or a second Claude chat at P2)
```
You are a sceptical, very experienced B2B SaaS growth advisor. A UK company, Outra, sells a £699/month self-serve platform giving D2C marketers household-level data (affluence, life stage, property, likely-to-move signals across 30M+ UK households): it enriches Klaviyo/HubSpot/Customer.io profiles and pushes prospecting and exclusion audiences to Meta, TikTok, Google Ads and DV360. 14-day free trial (card required), no annual contract. Known issue: big drop-off between demo and next action.

My draft acquisition strategy is: [PASTE 5-LINE SUMMARY].

1) Make the strongest possible case for a materially DIFFERENT strategy (different wedge, motion or channel mix). 
2) List the 5 weakest assumptions in my draft and what evidence would break each.
3) What would a CRO from Shopify challenge first?
Be blunt, concise, UK English. No preamble.
```


## F. Agency-involvement research prompt (live demo of the prospector, in any browser with web search on)
Paste this into Claude or ChatGPT with web search enabled. Replace the brands at the bottom with 3–5 from `prospects.csv`, or any wedge brands.
```
You are a B2B research analyst. For each UK brand below, determine who runs its paid media (Meta/TikTok/Google ads) day to day:
- in_house_only: an in-house paid social/PPC/performance person or team and no evidence of a paid-media agency
- hybrid: in-house paid role(s) AND an agency working on paid media
- agency_run: an agency runs paid media and there's no in-house paid specialist
- unknown: not enough evidence

Use web search only. Check, in this order:
1. The brand's own careers/jobs page and recent job ads for paid social, PPC, performance or acquisition roles. Read the wording about agencies ("manage our agency partners" → hybrid; "own paid social in-house" / "bring paid in-house" → in-house signal).
2. Agency websites, case studies and awards entries that name the brand as a paid media / paid social / PPC client. Search queries like: "<brand>" paid social agency case study; "<brand>" PPC agency; "<brand>" performance marketing agency.
3. Public search-result snippets showing job titles at the brand (paid social, PPC, performance, acquisition, growth marketing). Do NOT open, log in to or browse linkedin.com, facebook.com or instagram.com pages; snippets in search results only.

Rules:
- Never guess. A classification other than "unknown" needs at least one evidence item with a working URL.
- Agency evidence older than 2 years is low confidence (agencies churn). A creative/branding-only agency does not count as paid-media agency involvement; note it.
- trigger: "open_paid_role" if an open paid role is advertised now; "new_hire" if a paid role holder started in the last ~90 days (from public evidence); "agency_exit" if evidence shows paid moved in-house recently; else "none".
- Spend at most ~6 searches per brand; move on.

Return ONLY a JSON array, one object per brand, no prose:
[{"domain": "...", "brand": "...", "classification": "in_house_only|hybrid|agency_run|unknown",
  "confidence": "high|med|low",
  "evidence": [{"signal": "job_ad|agency_case_study|award|title_snippet|other", "summary": "<=20 words", "url": "https://...", "date": "YYYY-MM or unknown"}],
  "in_house_roles_public": ["Paid Social Manager", "..."],
  "trigger": "open_paid_role|new_hire|agency_exit|none",
  "notes": "<=25 words"}]

Brands:
[{{"domain": "example.co.uk", "brand": "Example"}}]
```


---

# 07 Evidence pack (researched 29 Oct 2026)



Cite as [F] with the URL. Recheck anything price- or feature-related on the day: the site changes often.

## A. Outra's self-serve offer as published

**Pricing and plans**
- Two plans, both £699/month [F] (https://outra.co.uk/pricing):
  - **Founder Membership**: unlimited profiles and audiences, locked-in price, priority onboarding, labelled as a this-month offer.
  - **Usage-Based**: up to 25k profiles and 3 audiences, with pro-rata overages.
- The SME page positions it as £699 all-in with unlimited use and no per-record fees [F] (/company/sme).
- The pricing calculator scales by ad-spend tier:
  - Starter (under £50k/month ad spend): 3 audiences
  - Growth (under £100k): 10 audiences
  - Scale: 25 audiences
  - Enrichment costs about £0.0012 per profile, and the total is floored at £699 [F] (pricing page code).
- **One "audience" means one segment on one channel** [F] (pricing FAQ).
- Enterprise and agency contracts are priced separately [F] (/lp/audiences-v2 FAQ).

**Trial**
- 14 days free, card required, cancel any time, no minimum ad spend [F] (/lp/audiences-v2).

**Time to value: the key tension** [F]
- The claims: first audience live in about 15 minutes, and Klaviyo set-up in about 10.
- But Outra's own guidance says to allow 2–3 weeks for learning before judging results, and that SME customers typically see CPA gains within the first month (/company/sme FAQ, /solutions/audiences FAQ).
- **So the trial (14 days) ends before Outra's own learning window (14–21 days) does.** This is the strongest fact-based argument for the activation and trial-design fix.

**Existing test design to build on** [F]
- The Audiences page sets out a 3-step flow: describe the business → get an audience recommendation → test an inclusion audience and an exclusion audience against your current best (/solutions/audiences).
- Pitch the lift test as productising this flow, not inventing it.

**Data** [F]
- Signals include:
  - life stage: family stage, age band, employment stage, move stage
  - household: tenure, property type and bedrooms, value band, garden/garage/driveway, area type
  - purchasing power: income band, credit score band, ultra-high-wealth flag
- Mover segments include predicted move, move intent, moving, just moved and recently moved, plus move anniversaries.
- Lifestyle segments include pet owners and multi-car households.
- The Playground shows about 400k households "just moved" (/blog/add-household-intelligence-to-klaviyo, /playground).
- Refresh rates: audiences weekly; life-event and intent signals weekly; demographics monthly.

**Destinations and integrations** [F]
- **Ad destinations named on the SME page:** Meta, TikTok, DV360/programmatic.
- **CRM/ESP named on the SME page:** Klaviyo, Customer.io, HubSpot.
- **Recent additions:**
  - Google Ads, including Performance Max (Sep 2026)
  - hashed email and mobile identifiers (Sep 2026)
  - email-only enrichment, with no postal address needed (Sep 2026)
- **Unconfirmed:** which CRM integrations are live in the product. Klaviyo is the one with full set-up documentation (Klaviyo guide: match rates are typically 70–90% for UK D2C lists).

**Marketplace listings**
- None found on the Shopify App Store, Klaviyo or HubSpot. Treat this as "not found", not "confirmed absent".

**ICP language Outra uses** [F]
- Founders and lean growth teams with no data team, for UK brands running paid ads.
- The blog focuses on Shopify + Klaviyo stacks and on the furniture, sleep, garden and kitchen categories.
- It says the product is weaker for pure-impulse, low-AOV categories (/blog/d2c-vertical-targeting-playbook, /blog/uk-household-data-d2c-guide).
- **So the "home & living + movers" wedge matches Outra's own content direction.** Present it as doubling down, not as a new idea.

**D2C proof that exists** [F] (/case-studies)
- **HIRO (D2C):** ROAS +146%, CPA −60%; DMA award shortlist.
- **Happy Dog:** CPA −70%, by targeting homes with gardens. A neat illustration of "household attributes predict purchase".
- **Index-only results:** GP Nutrition, The Lab Co. (ROAS +223%), Danetti (furniture, AOV up).
- Dayinsure: see Outra's case study page for current figures.
- **SME testimonial:** one, from Holloways of Ludlow (fewer price-shocked enquiries).

**Acquisition surfaces today** [F]
- **Calls to action:**
  - The trial call to action appears on /company/sme and the /lp pages.
  - The homepage, solution pages and pricing cards lead with Book a demo.
  - The demo booking is light: work email, then a 30-minute slot.
- **Free tools:** the Audience Playground/Builder (directional sizes, then "talk to us" for a real count) and the price calculator.
- **Content:** 34 blog posts, including pillar guides. The site is set up for AI search (llms.txt, "Ask AI about Outra" links).
- **Agency:** agency and enterprise pages marked "Soon" on the site at time of research.
- **Partnerships:** LightboxTV (Nov 2025) and AUDIENCES (Jun 2025).

**Positioning** [F]
- Deterministic, address-level and cookieless, explicitly set against lookalikes and Advantage+ guesswork (/company/about, /playground).
- **Data sources:**
  - public registers: VOA council tax bands, Land Registry, Companies House, electoral roll, ONS
  - licensed third-party data
- **Legal basis:** legitimate interest (/blog/uk-household-data-d2c-guide, /privacy).


## C. Market, competitors and constraints (researched 29 Oct 2026)

### Competitors
- **No UK self-serve household-data tool at a published price was found.** Experian Mosaic, CACI Acorn, TransUnion (property data, CAMEO), Sagacity and Royal Mail mover data are all sales-led with unpublished prices [F]:
  - experian.co.uk/business-products/mosaic
  - caci.co.uk/datasets/household-acorn
  - transunion.co.uk/product/property-data
  - sagacitysolutions.co.uk
  - royalmail.com/business/marketing/data/buy-marketing-data
- **Positioning implication** [I]: Outra is the only "self-serve, published price, live in minutes" option. The real competition is the substitutes below, not other data vendors.

### Substitutes
- **Klaviyo predictive analytics** [F]: CLV, churn risk and next order date, from first-party data only, with no household attributes. CLV needs 500+ customers and 180+ days of history (help.klaviyo.com/hc/en-us/articles/360020919731).
- **Shopify Audiences** [F]: US and Canada only, so not available to UK stores (agency source: charleagency.com).
- **Meta Advantage+ Audience** [F]:
  - Meta reported 33% lower cost per result than original audience options (test from 2023, cited by jonloomer.com).
  - Detailed targeting exclusions were removed in 2025 (developers.facebook.com, 21 Jan 2025).
  - Meta reportedly aims to fully automate targeting by the end of 2026 (WSJ via verdict.co.uk).
  - **No published head-to-head shows lookalike or custom seeds beating broad** (alexneiman.com, Mar 2026).
- **Exclusion-only custom audiences** [F]: launched Aug 2026, per an agency report (commonthreadco.com). Suppression remains a role for external data.
- **Independent caution** [F]: an academic field study found broker age and gender segments were often inaccurate (Neumann, Tucker & Whitfield, Marketing Science 2019; US and Australian data, dated). Expect a sharp panellist to know it, and answer with deterministic, address-level matching plus measured tests.

### Signal-loss facts
- Google kept third-party cookies in Chrome with no user-choice prompt (privacysandbox.google.com, 22 Apr 2025) [F].
- Google retired most Privacy Sandbox APIs, and the CMA released its commitments (adexchanger.com, Oct 2025) [F].
- iOS ATT opt-in is about 35% (Adjust, Q2 2025) [F].

### Market size
- **UK Shopify stores:** about 245–251k; about 6.2k on Plus (eightx.co, citing Storeleads/BuiltWith, 2026) [F, medium confidence].
- **UK stores using Klaviyo:** about 45.5k (storeleads.app, 23 Oct 2026) or about 42.6k (BuiltWith, Oct 2026) [F, medium; a proxy].
- **Klaviyo globally:** over 205k customers (Business Wire, Aug 2026) [F].
- **UK ad spend:** £46.7bn in 2025; social up 21% to a 24.7% share (AA/WARC via advanced-television.com, Apr 2026) [F].
- **Typical UK SMB Meta spend:** about £6.5k a year (Spendesk, data to 2022, weak) [F, weak]. On that figure, most SMBs spend less a month on Meta than the £699 fee, which supports a high spend floor. **There is no credible source for SME paid-social spend bands. Label any band [A].**

### Distribution
- **Shopify App Store:** 0% revenue share on the first $1M lifetime, then 15% (shopify.dev) [F].
- **Klaviyo marketplace:** needs OAuth, 5+ production installs, a security review and a demo recording (developers.klaviyo.com). The partner programme says it reaches 183k+ brands and offers co-marketing [F].
- **HubSpot marketplace:** needs 3+ unaffiliated installs and OAuth (developers.hubspot.com) [F].
- **Klaviyo → Meta segment sync:** minimum 100 profiles [F]. This is the path an enriched segment takes into ads.
- **Events:** K:LDN (Klaviyo London, Jun 2026, 1,000+ attendees); Pulse eCommerce Summit (Apr 2027); Retail Technology Show (Apr 2027); eCommerce Expo (Sep 2027) [F]. Confirm dates.
- **Addressable TV:** Sky, ITV and Channel 4 plan a joint self-serve SME video marketplace (thekeyword.co) [F]. An opening for Outra's Sky AdSmart audiences.

### Conversion benchmarks (ChartMogul, Growth Unhinged and ProductLed, Jan 2026) [F]
- Trial→paid median 8%.
- No-card trials: 4–6% good.
- **Card-required trials: 25–35% good, 50–60% great.**
- Hybrid self-serve + sales motion is the norm above about $100 ASP.
- There is no channel benchmark specific to martech at £500–1,000/month.

### Movers (for the wedge)
- **Residential transactions:** about 1.2M UK sales in 2025 (industry figures citing HMRC). HMRC monthly data: about 95k seasonally adjusted in Aug 2026 (gov.uk HMRC transactions commentary) [F].
- **All movers, renters included:** about 1.8M English households moved in the last 12 months, including about 822k private renters (English Housing Survey 2024-25) [F].
- **Spend figures (vendor-sourced or dated):** Royal Mail claims movers spend about £9bn a year on move-related goods and services, and that 65% switch suppliers. Furniture spend averages about £1.25k in year one (Norton Finance, 2019) [F, weak].

### Compliance
- **ICO v Experian:** the Upper Tribunal (Apr 2024) largely upheld Experian's position that legitimate interests can support modelled marketing data. Transparency through privacy notices still matters, and consent-based data can't be switched to legitimate interests (stephensonharwood.com; ICO statement May 2024) [F].
- **Data (Use and Access) Act 2025:** most provisions in force from 5 Feb 2026. It names direct marketing as an example of a legitimate interest, with the balancing test still applying. PECR fines now reach £17.5M or 4% of turnover (ico.org.uk) [F].
- **PECR for outbound:** email or SMS to bought-in lists needs consent that names the sender. B2B outreach to corporate subscribers is lighter, but sole traders count as individuals. Use company-level targeting plus LinkedIn and owned channels [I]. Check the current ICO guidance.


---

# 08 Quality gate (P5)

## Red-team lenses (run each; 3 bullets max per lens; then fix)
- **CEO:** Is it top-down and MECE? Do the unit economics drive the choices? Is there a marketplace-style flywheel (agencies, data and case studies compounding)? Is it optimistic but credible?
- **CRO:** Is there pipeline maths per channel? Is the sales-capacity load realistic? Is the handoff clear? Is the Shopify, Klaviyo and agency ecosystem used properly?
- **GTM technology lead:** Can it be instrumented in the CRM? Are the fields, UTMs, routing and attribution realistic? Has it been agreed rather than imposed? Is the AI automation concrete (call summary → follow-up → task)?
- **Sceptical D2C buyer:** "Why not just Meta broad?" "How do I know it worked?" "Is this GDPR-safe?" "What do I do on day 1?"
- **ICO / compliance:** Is any profiling transparent? Is PECR respected for outreach? Is there no use of vulnerability data for targeting? Is the data aggregated for PR?
- **Existing growth team:** Does anything read as criticism of existing work? Reframe it as building on that work.

## Rubric (score 1–5; fix anything below 4)
1. **Answer-first clarity:** could someone repeat the recommendation after one slide?
2. **Commercial rigour:** economics → ICP floor → motion → channels, all with shown workings.
3. **Specificity:** named segments, experiments, thresholds, owners and dates.
4. **Feasibility:** it fits the existing team, tools and budget logic.
5. **Evidence honesty:** facts, inferences and assumptions tagged; nothing invented.
6. **AI use:** visible, varied and judgement-led; a working artefact.
7. **Prioritisation:** a clear "won't do" list and a sequence (fix the funnel before scaling).

## Hard panel questions to prepare (generate fresh ones too)
1. "Why this wedge and not [X]?" Answer with the scoring and the unique edge, and the data that would change the call.
2. "Your conversion rates are made up." Agree: they are labelled assumptions. Show the sensitivity table and the week-1 data pull.
3. "What if Meta's AI makes targeting irrelevant?" Concede the point for Meta prospecting; the evidence supports it. Then pivot: enrich-first landing in Klaviyo, suppression, channels where selection still decides the outcome (addressable TV, programmatic), creative insight, and a measured inclusion/exclusion-vs-control test on every account (§03 §6).
4. "What would you do in week 1?" Funnel data pull, 5 demo-call reviews (AI-summarised), an agreed definition of activation, and instrumentation with the GTM tech owner.
5. "How does this work with our existing team?" Map the channels to the existing heads (Agency Sales, Partnerships, Performance Marketing, Client Success).
6. "What budget do you need?" Derive it from the CAC ceiling × target, phased, with experiments released by stage gate.
7. "How do you handle three motions at once?" Self-serve is the core; agency is the multiplier; enterprise stays separate and opportunistic, outside this brief.
8. "Where did AI get it wrong today?" Have one real example ready from the log.
9. "Why target in-house-only teams?" Because agency involvement, not spend, decides whether a self-serve trial succeeds. With no agency, the person who decides is the person who activates, the lift is credited to Outra, and there's no conflict with the coming Agency plan. Hybrid and agency-run brands are routed to the agency channel, not lost. Size it in week 1 with a sample of 200; if it's too narrow, relax it to allow creative-only agencies.
10. "How would you even know if they use an agency?" Stack the signals: job-ad wording, agency client lists and case studies, and LinkedIn. Then ask directly in the tool and the sign-up flow, which is the only fully reliable signal.

## Final checks before presenting
- [ ] Every number traces to a calculation.
- [ ] Every claim is tagged; there are no [I] items presented as fact.
- [ ] Duncan's proof points are used only from the context file, and no more than 2 in the deck.
- [ ] No criticism of existing work: the panel's own data is framed as upside.
- [ ] Run-rate vs target checked (§03 §0) if data was supplied.
- [ ] Budget → CAC-per-channel table and sensitivity table exist.
- [ ] The Lovable link works, and screenshots exist as a backup.
- [ ] The AI log has at least 6 rows, including at least one override.


---

## §9 Prospector pre-work: findings (run 30 Oct 2026, home_furniture seed)
The pipeline: Meta Ad Library API keyword seed → DNS and homepage stack check → ranked top 50 → parallel AI research agents judging fit and paid-media ownership → scored routes. [F] figures come from the run's own output.

| Step | Result |
|---|---|
| Seed: 5 keywords × 500 active UK ads | 270 advertiser domains, plus 277 pages with no resolvable domain |
| Shopify via DNS (homepages blocked, about half returned 429s) | 132 of 270 on Shopify |
| Prefiltered (stack signal, UK not ruled out, not junk) | 122 |
| Researched (top 50 by rank) | **Fit: 15 yes (30%), 15 no (30%), 20 unsure or enterprise (40%)** |
| Paid-media ownership | **49 of 50 unknown** (low confidence), 1 hybrid, 0 in-house-only. Own-site fetches were rate-limited for 46 of 50 |

**What I concluded:**
1. **Agency involvement is effectively unobservable from outside for SME D2C** [I, from 49/50 unknown]. So the in-house-only filter belongs **at first touch and in product**, not in list-building: ask "Who runs your paid media day to day?" in the free tool, at sign-up and in the outbound opener. Route on the answer. Collecting the answers also builds the dataset to size the segment, which is better than guessing from outside.
2. **Ad Library keyword search is a poor seed but a good activity check** [F, 30% fit; ad volume didn't predict fit]. Better: seed from category and stack sources (Storeleads UK + Klaviyo/Shopify + home categories, or a curated list), then use the Ad Library to confirm a brand is actively advertising and DNS to confirm Shopify.
3. **DNS beats scraping for stack detection on Shopify** [F, 132 detected despite 429s].

**Slide text (appendix, "What I tested before today"):**
> I built a pipeline that pulled 2,500 live UK furniture ads from Meta's Ad Library, checked 270 advertisers' stacks, and had AI research agents judge fit and who runs their paid media. Two lessons changed my plan: only 30% of advertisers were genuine UK D2C fits, so I seed from category and stack data and use ad activity as a filter. And agency involvement was invisible from outside in 49 of 50 cases, so I qualify it at first touch and in product, not in list-building.

**Say it this way:** it was a fast test of my own hypothesis, with a clear result and a design change. Present it as evidence of method, not as a polished prospect list.
