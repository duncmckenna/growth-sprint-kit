# growth_calc: deterministic SaaS acquisition maths. Paste into the code tool and call the functions.
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
