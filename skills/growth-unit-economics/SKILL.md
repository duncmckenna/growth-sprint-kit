---
name: growth-unit-economics
description: Compute SaaS acquisition maths with code, never in prose: customer break-even, CAC ceiling, funnel back-solve and decomposition, ramp, sensitivity, CAC by channel.
---

# Growth unit economics

Use this whenever a growth or acquisition answer depends on numbers: pricing pay-back, CAC limits, funnel data, targets or budgets.

**Rule: never do the arithmetic in prose.**
1. Load `scripts/growth_calc.py`, or paste the library below into the code tool, then call its functions. Every figure in the answer must come from that output.
2. If code execution isn't available, say so and show each calculation step by step.

## Workflow
1. **Definitions check first.** Is the target gross or net, incremental or total? Is the budget new money or existing? Are trials card-entered only? What exactly is "activation"? Ask whichever of these change the answer. Tag every input:
   - [F] given
   - [A] assumed
2. **Customer side:** `breakeven(price)` gives the spend at which the product pays for itself. That is the qualification floor. Qualify on the conservative case; sell on the vendor's reported range.
3. **Vendor side:** `cac_ceiling(arpa)` gives the maximum affordable CAC by churn and payback. Use 6-month payback when the plan window is 6 months or less. The ceiling decides the motion: self-serve, sales-assisted, or field sales.
4. **If funnel data is supplied:**
   - `decompose()` finds the biggest absolute leak, which is the first fix.
   - `channel_table()` gives CAC by channel against the ceiling.
   - Compare against benchmarks; card-required B2B trials typically convert 25–35% trial→paid. If the data contradicts a benchmark, flag it as a question.
5. **Run-rate vs target:** current volume × conversion × window. If the baseline already beats the target, say so early and frame it as upside, plus a question about the definition.
6. **Plan:**
   - `backsolve()` gives the volumes needed per stage.
   - `ramp()` gives month-by-month paid accounts, excluding conversions that land after the window.
   - `split_gain()` separates the volume effect from the conversion effect.
   - `sensitivity()` puts the two most uncertain rates on the axes, with the plan case marked.
7. **Capacity:** human touches per month (demos plus onboarding calls) against stated capacity. The assist threshold is set by capacity first, value second.
8. **Output:** short markdown tables, each with a one-line "so what". List every [A] in an assumptions block.

## Library
```python
import math

def fmt(x): return f"£{x:,.0f}"

def breakeven(price, gains=(0.10, 0.15, 0.20, 0.25, 0.30), multiple=1.0):
    """Customer-side: monthly ad spend at which a fee pays for itself (fee / efficiency gain)."""
    rows = [(f"{g:.0%}", fmt(price * multiple / g)) for g in gains]
    print(f"| CPA gain | Spend to cover fee x{multiple:g} |\n|---|---|")
    for r in rows: print(f"| {r[0]} | {r[1]} |")
    return rows

def cac_ceiling(arpa_month, gm=0.80, churns=(0.03, 0.05, 0.08), ltv_cac=3.0, paybacks=(6, 12)):
    """Vendor-side: max affordable CAC by churn (LTV:CAC) and by payback months."""
    print(f"| Monthly churn | Lifetime (mo) | LTV (GM) | Max CAC at {ltv_cac:g}:1 |\n|---|---|---|---|")
    for c in churns:
        ltv = arpa_month * gm / c
        print(f"| {c:.0%} | {1/c:.1f} | {fmt(ltv)} | {fmt(ltv/ltv_cac)} |")
    for p in paybacks:
        print(f"- {p}-month payback caps CAC at {fmt(arpa_month * gm * p)}")

def backsolve(target_paid, months, stages):
    """stages: list of (name, conversion) from top to bottom, e.g. [('visit->trial',0.03),('trial->paid',0.25)].
    Returns monthly volume needed at each stage, working backwards."""
    per_month = target_paid / months
    need = per_month
    out = [("paid", need)]
    for name, conv in reversed(stages):
        need = need / conv
        out.append((name.split("->")[0], need))
    print(f"Target {target_paid} in {months} months = {per_month:.1f}/month")
    for name, n in reversed(out): print(f"- {name}: {n:,.0f}/month")
    return list(reversed(out))

def decompose(counts):
    """counts: ordered dict-like list of (stage, count). Prints step rates and absolute losses."""
    print("| Step | From | To | Rate | Lost |\n|---|---|---|---|---|")
    worst = None
    for (a, na), (b, nb) in zip(counts, counts[1:]):
        lost = na - nb
        print(f"| {a}→{b} | {na:,} | {nb:,} | {nb/na:.1%} | {lost:,} |")
        if worst is None or lost > worst[1]: worst = (f"{a}→{b}", lost)
    print(f"Overall {counts[0][0]}→{counts[-1][0]}: {counts[-1][1]/counts[0][1]:.1%}. Biggest absolute loss: {worst[0]} ({worst[1]:,}).")
    return worst

def channel_table(channels, cac_cap=None):
    """channels: list of dicts {name, spend, trials, paid}. Prints CAC and trial->paid per channel."""
    print("| Channel | Spend | Trials | Paid | Trial→paid | CAC |\n|---|---|---|---|---|---|")
    ts = tt = tp = 0
    for c in channels:
        cac = c["spend"] / c["paid"] if c["paid"] and c["spend"] else 0
        flag = " ⚠" if cac_cap and cac > cac_cap else ""
        print(f"| {c['name']} | {fmt(c['spend'])} | {c['trials']} | {c['paid']} | {c['paid']/c['trials']:.1%} | {fmt(cac) if cac else '–'}{flag} |")
        ts += c["spend"]; tt += c["trials"]; tp += c["paid"]
    print(f"| **Total** | {fmt(ts)} | {tt} | {tp} | {tp/tt:.1%} | {fmt(ts/tp) if tp else '–'} |")

def ramp(months, trials, conv, lag_months=1):
    """trials, conv: lists per month (or scalars). Trials convert lag_months later; conversions after the window are excluded."""
    T = trials if isinstance(trials, list) else [trials] * months
    C = conv if isinstance(conv, list) else [conv] * months
    paid = [0.0] * months
    for m in range(months):
        if m + lag_months < months: paid[m + lag_months] += T[m] * C[m]
    cum = 0
    print("| Month | Trials | Conv | Paid | Cumulative |\n|---|---|---|---|---|")
    for m in range(months):
        cum += paid[m]; print(f"| {m+1} | {T[m]:,.0f} | {C[m]:.1%} | {paid[m]:.1f} | {cum:.1f} |")
    return cum

def split_gain(base_trials, base_conv, new_trials, new_conv):
    """Split the uplift in paid accounts into volume and conversion effects."""
    base, new = base_trials * base_conv, new_trials * new_conv
    vol = (new_trials - base_trials) * base_conv
    conv = new_trials * (new_conv - base_conv)
    print(f"Paid {base:.1f} → {new:.1f} (+{new-base:.1f}): volume effect +{vol:.1f}, conversion effect +{conv:.1f}")

def sensitivity(f, xs, ys, xlabel, ylabel, mark=None):
    """Grid of f(x, y). mark=(x, y) highlights the plan case."""
    print(f"| {ylabel} \\ {xlabel} | " + " | ".join(f"{x:g}" for x in xs) + " |")
    print("|---|" + "---|" * len(xs))
    for y in ys:
        cells = []
        for x in xs:
            v = f(x, y); s = f"{v:,.1f}"
            cells.append(f"**{s}**" if mark == (x, y) else s)
        print(f"| {y:g} | " + " | ".join(cells) + " |")
```

## Example calls
```python
breakeven(699)
cac_ceiling(699)
backsolve(100, 12, [("visit->trial", 0.03), ("trial->paid", 0.25)])
decompose([("trial", 300), ("connected", 146), ("paid", 46)])
channel_table([{"name": "Meta", "spend": 9000, "trials": 120, "paid": 10}], cac_cap=3355)
ramp(6, [140, 150, 170, 190, 205, 205], [0.09, 0.10, 0.12, 0.14, 0.16, 0.17])
split_gain(140, 0.09, 205, 0.17)
sensitivity(lambda a, b: 140 * a * b, [0.4, 0.5, 0.6, 0.7], [0.2, 0.3, 0.4], "activation", "activated→paid", mark=(0.5, 0.3))
```

**Reference values for checking a run at £699/month:**
- Break-even spend: £6,990 at 10%, £3,495 at 20%, £2,330 at 30%.
- CAC ceiling: £3,355 at 6-month payback, £6,710 at 12-month.
- At 3:1 LTV:CAC: £3,728 with 5% churn.
