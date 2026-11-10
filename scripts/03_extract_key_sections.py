#!/usr/bin/env python3
"""
Step 3 - Pull the sections that matter for plan comparison out of each Sales Brochure.

For every *Sales_Brochure.txt produced by step 2 it prints / saves:
  * the opening description (plan type: endowment, annuity, single premium, ...)
  * the "Eligibility Conditions" block (entry age, policy term, premium paying term, min SA)
  * Guaranteed Addition / Maturity Benefit wording
  * the "Sample Illustrative Premium" table
  * the start of the "Benefit Illustration" table (year-wise premiums and benefits)

Usage:
    python3 03_extract_key_sections.py [--txt ./txt] [--out key_sections.md] [plan numbers ...]
    e.g. python3 03_extract_key_sections.py 774 912 890
"""
import argparse
import glob
import os
import re

SECTIONS = [
    ("Eligibility", r"eligibility", 1600),
    ("Guaranteed Additions", r"rate of guaranteed additions?|guaranteed additions? shall accrue at the rate", 1000),
    ("Maturity Benefit", r"maturity benefit\s*:", 800),
    ("Sample Illustrative Premium", r"sample illustrative (annual )?premium", 1200),
    ("Benefit Illustration", r"benefit illustration", 4000),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plans", nargs="*", help="plan numbers to include (default: all)")
    ap.add_argument("--txt", default="./txt")
    ap.add_argument("--out", default="key_sections.md")
    args = ap.parse_args()

    out = []
    for path in sorted(glob.glob(os.path.join(args.txt, "*Sales_Brochure.txt"))):
        fname = os.path.basename(path)
        if args.plans and not any(fname.startswith(p + "_") for p in args.plans):
            continue
        t = re.sub(r"\s+", " ", open(path, encoding="utf-8").read())
        out.append(f"\n## {fname}\n\n**Intro:** {t[:450]}\n")
        for title, pattern, length in SECTIONS:
            m = re.search(pattern, t, re.I)
            out.append(f"\n**{title}:** " + (t[m.start():m.start() + length] if m else "_not found_") + "\n")

    report = "".join(out)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("# Key sections from LIC sales brochures\n" + report)
    print(report)
    print(f"\nSaved to {args.out}")


if __name__ == "__main__":
    main()
