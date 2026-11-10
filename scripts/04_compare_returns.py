#!/usr/bin/env python3
"""
Step 4 - Compare plans by effective annual return (IRR) and size them to the goal.

Inputs are the figures published in each plan's Sales Brochure (sample premium
tables, guaranteed-addition rates and benefit illustrations) - see
findings/LIC_plan_recommendation.md for the source of every number.

Cash-flow convention: yearly premiums paid at the start of each policy year
(t = 0 .. PPT-1), maturity / survival benefits received at the end of year t.

Usage:
    python3 04_compare_returns.py
"""

MONTHLY_FACTOR = 0.0862   # LIC monthly premium conversion factor (Nav Jeevan Shree; ~0.0861 for others)


def irr(cashflows):
    """Annual IRR of [(year, amount), ...] by bisection."""
    lo, hi = -0.5, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        npv = sum(c / (1 + mid) ** t for t, c in cashflows)
        lo, hi = (mid, hi) if npv > 0 else (lo, mid)
    return mid


def flows(premium, ppt, payouts):
    return [(t, -premium) for t in range(ppt)] + list(payouts)


def ga_on_premium(premium, ppt, term, rate):
    """Guaranteed Additions = rate x total annual premiums paid so far, every year of the term."""
    return sum(rate * premium * min(year, ppt) for year in range(1, term + 1))


def scenarios():
    s = []
    # Amritbaal (774): age 5, BSA 5L, PPT 7, term 20; GA = Rs 80 per 1000 BSA per year -> 8L
    s.append(("Amritbaal 774 - pay 7 / term 20 (guaranteed)", 73_625, 7, [(20, 500_000 + 0.08 * 500_000 * 20)]))
    # Nav Jeevan Shree (912): age 35, BSA 5L; GA 8.5% (term 10-13) / 9.0% (term 14-17) of premiums paid
    p = 101_350
    s.append(("Nav Jeevan Shree 912 - pay 6 / term 10 (guaranteed)", p, 6, [(10, 500_000 + ga_on_premium(p, 6, 10, 0.085))]))
    p = 62_825
    s.append(("Nav Jeevan Shree 912 - pay 10 / term 15 (guaranteed)", p, 10, [(15, 500_000 + ga_on_premium(p, 10, 15, 0.09))]))
    # Brochure illustration: age 30, BSA 10L, PPT 8, term 20 -> 25,17,459
    s.append(("Nav Jeevan Shree 912 - pay 8 / term 20 (guaranteed)", 119_500, 8, [(20, 2_517_459)]))
    # New Bima Jyoti (890): age 30, BSA 10L, PPT 10, term 15, GA 6% of premiums paid
    p = 122_850
    s.append(("New Bima Jyoti 890 - pay 10 / term 15 (guaranteed)", p, 10, [(15, 1_000_000 + ga_on_premium(p, 10, 15, 0.06))]))
    # Jeevan Labh (736): brochure illustration age 30, BSA 2L, 25/16
    s.append(("Jeevan Labh 736 - pay 16 / term 25 @4% scenario", 10_025, 16, [(25, 220_000)]))
    s.append(("Jeevan Labh 736 - pay 16 / term 25 @8% scenario", 10_025, 16, [(25, 370_000)]))
    # Jeevan Tarun (734): age 5, option 4, BSA 2L: 30k/yr survival in years 15-19 + maturity
    sb = [(t, 30_000) for t in range(15, 20)]
    s.append(("Jeevan Tarun 734 @4% scenario", 13_338, 15, sb + [(20, 70_000)]))
    s.append(("Jeevan Tarun 734 @8% scenario", 13_338, 15, sb + [(20, 183_000)]))
    # New Children's Money Back (732): age 5, BSA 2L, 20-year term
    s.append(("New Children's Money Back 732 @8% scenario", 11_682, 20,
              [(13, 40_000), (15, 40_000), (17, 40_000), (20, 197_000)]))
    return s


def main():
    print(f"{'Plan / scenario':55s} {'Paid':>11s} {'Received':>11s} {'Multiple':>9s} {'IRR':>7s}")
    for name, prem, ppt, payouts in scenarios():
        paid, got = prem * ppt, sum(a for _, a in payouts)
        print(f"{name:55s} {paid:>11,.0f} {got:>11,.0f} {got / paid:>8.2f}x {irr(flows(prem, ppt, payouts)) * 100:>6.2f}%")

    print("\nGoal sizing: two children, one policy each at minimum Basic Sum Assured Rs 5,00,000")
    for label, p, ppt, term, rate in [("Nav Jeevan Shree 6-pay / 10-year", 101_350, 6, 10, 0.085),
                                      ("Nav Jeevan Shree 10-pay / 15-year", 62_825, 10, 15, 0.09)]:
        monthly = p * MONTHLY_FACTOR
        maturity = 500_000 + ga_on_premium(p, ppt, term, rate)
        print(f"  {label}: ~Rs {monthly:,.0f}/month per child (Rs {2 * monthly:,.0f} total) for {ppt} yrs "
              f"= Rs {2 * monthly * 12 * ppt:,.0f} paid -> Rs {maturity:,.0f} per child "
              f"(Rs {2 * maturity:,.0f} total) at year {term}")


if __name__ == "__main__":
    main()
