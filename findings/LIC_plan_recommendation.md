# LIC Plan Recommendation — Children's College Education Goal

_Prepared: 10 Nov 2026 · Source: 69 official PDFs (Sales Brochure, Policy Document, CIS) for 23 LIC plans downloaded from licindia.in_

---

## 1. The goal

| Item | Value |
|---|---|
| Monthly contribution | ₹10,000 (for two children) |
| Contribution period | 10 years |
| Total paid in | ₹10,000 × 12 × 10 = **₹12,00,000** |
| Target payout | ~₹7 lakh, at the end of year 10, for college education |
| Assumption used | ₹7 lakh **per child** (₹14 lakh total). A total of ₹7 lakh would be less than the ₹12 lakh paid in, which no savings plan is designed to do. |

---

## 2. Executive summary

- **No plan matches the goal exactly.** None of the 23 plans in the Endowment, Pension and Money Back categories accepts monthly premiums for 10 years and pays a lump sum at the end of year 10.
- **Best fit: LIC's Nav Jeevan Shree (Plan 912, UIN 512N387V02).** It is the only regular-premium plan that can mature in **exactly 10 years** (pay for 6 years). The maturity amount is **fully guaranteed** and does not depend on bonuses.
  - **Option A (pay 6 years, matures at year 10):** two policies at ₹5L sum assured each cost about **₹17,500/month for 6 years** (about ₹12.6L in total, roughly the same as the ₹12L budget). They return about **₹8.9L per child (₹17.8L total)** at year 10.
  - **Option B (pay 10 years, matures at year 15):** about **₹10,800/month for 10 years** returns about **₹10.9L per child (₹21.9L total)**, but at year 15.
- **Alternative if both children are 13 or younger: LIC's Amritbaal (Plan 774).** It is a dedicated children's higher-education plan. You pay for 5–7 years, and it matures at a chosen child age between 18 and 25, with a guaranteed addition of 8% of the sum assured every year. It had the highest return of the plans analysed (about 5.6% a year).
- **Realistic return range:** guaranteed LIC savings plans in this set return about **5–6% a year**. Plans that depend on bonuses showed **about 1–5% a year** in LIC's own 4% and 8% illustrations.

---

## 3. Method

1. **Crawl.** The three category pages were parsed for their plan tables. Each plan page was opened and every PDF link was collected.
2. **Pick the latest version.** For each document type (Sales Brochure, Policy Document, CIS), versions labelled with an end date ("From … To dd/mm/yyyy") were treated as superseded. The "onwards" or undated version was kept.
3. **Extract text** from all 69 PDFs with `pypdf`.
4. **Screen each plan** against the goal using the brochure's Eligibility section: policy term, premium-paying term (PPT), entry age, minimum sum assured, and premium type (regular, limited or single).
5. **Quantify the shortlist** from each brochure's *Sample Illustrative Premium* table, guaranteed-addition rates and *Benefit Illustration* table. The effective annual return (IRR) was computed with premiums paid at the start of each year and benefits received at the end of the year.
6. **Size to the budget** using LIC's monthly premium conversion factor (0.0861–0.0862 × annual premium).

The scripts are in `../scripts/`:

| Script | Purpose |
|---|---|
| `01_download_pdfs.py` | Crawls the 3 category pages and downloads the latest Sales Brochure, Policy Document and CIS for every plan |
| `02_extract_text.py` | Converts every PDF to text (`pip install pypdf`) |
| `03_extract_key_sections.py` | Pulls the Eligibility, Guaranteed Additions, Maturity, Sample Premium and Benefit Illustration sections from each brochure |
| `04_compare_returns.py` | Computes IRR for every shortlisted scenario and sizes the goal |

---

## 4. Screening: all 23 plans

### 4.1 Endowment plans (12)

| Plan No. | Plan | UIN | Key eligibility (from brochure) | Verdict |
|---|---|---|---|---|
| 717 | Single Premium Endowment | 512N283V03 | Single premium only | ❌ No monthly premiums |
| 714 | New Endowment Plan | 512N277V03 | Term 12–35 yrs; premiums for full term; bonus-based | ❌ No 10-year term; returns not guaranteed |
| 715 | New Jeevan Anand | 512N279V03 | Entry 18+; term 15–35 yrs; whole-life cover after maturity | ❌ Term too long |
| 733 | Jeevan Lakshya | 512N297V03 | Entry 18–50; term 13–25; PPT = term − 3 | ❌ Term too long |
| 736 | Jeevan Labh | 512N304V03 | Term/PPT: 16/10, 21/15, 25/16; bonus-based | ⚠️ Pays for 10 yrs, but matures at year 16; payout not guaranteed |
| 774 | **Amritbaal** | 512N365V02 | Child entry 30 days–13 yrs; maturity at age 18–25; PPT 5/6/7; min term 10; GA ₹80 per ₹1,000 SA per year | ✅ **Shortlisted (child education plan)** |
| 912 | **Nav Jeevan Shree** | 512N387V02 | Entry 30 days–60 yrs; PPT 6/8/10/12/15; **term 10 possible with PPT 6**; min SA ₹5L; GA 8.5–9.5% of premiums paid | ✅ **Best fit for a 10-year maturity** |
| 881 | Bima Lakshmi | 512N389V01 | Women only; entry 18–50; term 25 | ❌ Women only; 25-year term |
| 888 | New Jeevan Sathi – Single Premium | 512N393V01 | Joint life (spouses), single premium | ❌ |
| 889 | New Jeevan Sathi – Limited Premium | 512N394V01 | Joint life for a married couple; 10-yr term only with 5-yr PPT | ❌ Couple plan, not for children |
| 890 | New Bima Jyoti | 512N395V01 | Term 15–20; PPT = term − 5; GA 6% of premiums paid | ⚠️ Guaranteed, but matures at year 15 and has a low return |
| 770 | Bima Platinum | 512N397V01 | PPT 10 needs a minimum 20-yr term | ❌ Term too long |

### 4.2 Pension plans (6)

| Plan No. | Plan | UIN | Type | Verdict |
|---|---|---|---|---|
| 867 | New Pension Plus | 512L347V01 | Unit-linked pension (market risk, 5-yr lock-in) | ❌ Retirement product |
| 857 | Jeevan Akshay-VII | 512N337V07 | Immediate annuity | ❌ Pays a pension, not a lump sum |
| 758 | New Jeevan Shanti | 512N338V08 | Deferred annuity | ❌ |
| 862 | Saral Pension | 512N342V05 | Standard immediate annuity | ❌ |
| 879 | Smart Pension | 512N386V01 | Immediate annuity | ❌ |
| 892 | New Jeevan Dhara II | 512N398V01 | Deferred annuity | ❌ |

### 4.3 Money Back plans (5)

| Plan No. | Plan | UIN | Key eligibility | Verdict |
|---|---|---|---|---|
| 748 | Bima Shree | 512N316V03 | Term 14–28; min SA ₹10L (aimed at high-net-worth buyers) | ❌ |
| 720 | New Money Back – 20 yrs | 512N280V03 | Term 20, PPT 15 | ❌ |
| 721 | New Money Back – 25 yrs | 512N278V03 | Term 25, PPT 20 | ❌ |
| 732 | New Children's Money Back | 512N296V03 | Child 0–12; premiums until the child is 25 | ❌ Long PPT, low return |
| 734 | Jeevan Tarun | 512N299V03 | Child 30 days–12 yrs; premiums until the child is 20; payouts at ages 20–24 | ❌ Long PPT, low return |

---

## 5. Return comparison (from LIC's own illustrations)

| Plan / scenario (brochure sample) | Premium paid | Amount received | Multiple | IRR p.a. | Guaranteed? |
|---|---:|---:|---:|---:|:---:|
| Nav Jeevan Shree — pay 8 / term 20 (age 30, SA 10L) | 9,56,000 | 25,17,459 | 2.63× | **5.99%** | ✅ |
| Amritbaal — pay 7 / term 20 (child age 5, SA 5L) | 5,15,375 | 13,00,000 | 2.52× | **5.56%** | ✅ |
| Nav Jeevan Shree — pay 10 / term 15 (age 35, SA 5L) | 6,28,250 | 10,93,696 | 1.74× | **5.31%** | ✅ |
| Nav Jeevan Shree — pay 6 / term 10 (age 35, SA 5L) | 6,08,100 | 8,87,664 | 1.46× | **5.12%** | ✅ |
| Jeevan Labh — pay 16 / term 25 @ 8% scenario | 1,60,400 | 3,70,000 | 2.31× | 4.76% | ❌ |
| Jeevan Tarun @ 8% scenario | 2,00,070 | 3,33,000 | 1.66× | 4.35% | ❌ |
| New Bima Jyoti — pay 10 / term 15 (age 30, SA 10L) | 12,28,500 | 17,73,955 | 1.44× | 3.51% | ✅ |
| New Children's Money Back @ 8% scenario | 2,33,640 | 3,17,000 | 1.36× | 3.43% | ❌ |
| Jeevan Labh — pay 16 / term 25 @ 4% scenario | 1,60,400 | 2,20,000 | 1.37× | 1.80% | ❌ |
| Jeevan Tarun @ 4% scenario | 2,00,070 | 2,20,000 | 1.10× | 0.87% | ❌ |

_The 4% and 8% scenarios are IRDAI-mandated illustrations of assumed investment returns. They are not guaranteed, and they are not the upper or lower limits of the actual payout._

---

## 6. Recommended plan: LIC's Nav Jeevan Shree (912)

### 6.1 Why it fits

- **Matures in exactly 10 years:** this is possible with the 6-year premium-paying term (the minimum term for PPT 6 is 10 years).
- **Fully guaranteed:** it is a non-par plan, so the maturity amount is fixed at purchase. Maturity = Basic Sum Assured + accrued Guaranteed Additions.
- **Guaranteed Addition rates** (% of total tabular annual premium paid, added every year of the term):

  | Policy term | GA rate |
  |---|---|
  | 10–13 yrs | 8.50% |
  | 14–17 yrs | 9.00% |
  | 18–20 yrs | 9.50% |

  Extra GA incentives apply for a high sum assured (+0.07% to +0.40%) and for buying online without an agent (+0.75% for PPT 6/8, +1.25% for PPT 10/12, +1.35% for PPT 15).
- **Entry age:** from 30 days. The policy can be on a child's life or on a parent's life.
- **Monthly mode** is allowed (monthly premium = 0.0862 × annual premium).
- **Minimum Basic Sum Assured:** ₹5,00,000, in multiples of ₹10,000.

### 6.2 Sized to the goal (two policies, one per child, SA ₹5L each)

Based on the brochure's sample premium for a 35-year-old life (₹1,01,350/yr for PPT 6 / term 10; ₹62,825/yr for PPT 10 / term 15):

| | **Option A: pay 6 / term 10** | **Option B: pay 10 / term 15** |
|---|---|---|
| Monthly premium per child | ~₹8,736 | ~₹5,416 |
| Monthly premium, both children | **~₹17,473** | **~₹10,831** |
| Paying period | 6 years | 10 years |
| Total paid | ~₹12.58 lakh | ~₹13.00 lakh |
| Guaranteed maturity per child | **~₹8.88 lakh** | **~₹10.94 lakh** |
| Total at maturity | **~₹17.75 lakh at year 10** | **~₹21.87 lakh at year 15** |
| Effective return | ~5.1% p.a. | ~5.3% p.a. |
| Meets "₹7L per child at year 10"? | ✅ Yes, with margin | ⚠️ Higher amount, but arrives 5 years later |

**Example of the maturity arithmetic (Option A, one child):**
GA per year = 8.5% × ₹1,01,350 × (number of annual premiums paid so far)
→ over years 1–10 the multipliers are 1, 2, 3, 4, 5, 6, 6, 6, 6, 6 = 45
→ GA = 0.085 × 1,01,350 × 45 = **₹3,87,664**
→ Maturity = ₹5,00,000 + ₹3,87,664 = **₹8,87,664**

---

## 7. Alternative: LIC's Amritbaal (774), if the children are 13 or younger

- Built for children's higher education. Maturity can be set at any child age from 18 to 25.
- **Guaranteed Addition of ₹80 per ₹1,000 Basic Sum Assured every policy year** (8% of SA, simple), for the whole term.
- **PPT:** 5, 6 or 7 years (limited premium), or single premium. **Minimum term 10 years** for limited premium.
- **Brochure example:** child aged 5, SA ₹5L, PPT 7, term 20. The parent pays ₹73,625 a year for 7 years (₹5.15L in total) and the child receives **₹13,00,000** at age 25 (IRR about 5.56%).
- **Premium Waiver Benefit rider:** if the parent (proposer) dies, future premiums are waived.
- The online purchase rebate is 10% of the tabular premium.
- **Best when** college is 10 or more years away. The longer the term, the more guaranteed additions accrue.

---

## 8. Plans considered but not recommended

| Plan | Why not |
|---|---|
| Jeevan Labh 16/10 | You pay for 10 years, but the money comes at year 16. Bonus-based, so the payout is not guaranteed. The illustrated IRR is only 1.8–4.8%. |
| New Bima Jyoti 15/10 | Guaranteed, but only about 3.5% IRR, and it matures at year 15. |
| Jeevan Tarun / New Children's Money Back | Premiums continue until the child is 20 or 25. Illustrated IRR is about 0.9–4.4%. |
| New Endowment / Jeevan Anand / Jeevan Lakshya / Bima Platinum | Minimum term is 12–20 years, so they can't deliver money at year 10. |

---

## 9. Caveats and next steps

1. **Premiums are estimates.** They come from LIC's sample tables (Nav Jeevan Shree uses a 35-year-old life). Actual premiums depend on the life assured's age, health, mode and rebates. Get an exact quote from the LIC premium calculator at licindia.in or an LIC agent before buying.
2. **Risk start for young children:** for a child under 8, life cover begins 2 years after the policy starts or on the policy anniversary after the child turns 8, whichever is earlier. Death before that refunds the premiums paid.
3. **Protect the premiums:** if the parent's income pays the premiums, add the **Premium Waiver Benefit rider** when the policy is on the child's life.
4. **GST:** currently exempt on these premiums, as stated in the brochures.
5. **Compare with non-insurance options.** A guaranteed 5–6% is safe but modest. PPF, Sukanya Samriddhi Yojana (for a daughter) or a disciplined mutual-fund SIP plus a separate term-insurance policy have historically returned more over 10 years. Check current rates before deciding.
6. **Needed to finalise:** the **current ages of both children**. With them it can be decided whether Amritbaal (maturity tied to the child's age) beats Nav Jeevan Shree (fixed 10-year term), and each child's policy can be sized precisely.

---

## Appendix A: Source files

All documents are saved under `~/Downloads/LIC_Plans/<Category>/<PlanNo - Plan Name (UIN)>/`:

- `Sales Brochure.pdf`: eligibility, benefits, sample premiums, benefit illustration
- `Policy Document.pdf`: legal contract terms
- `CIS.pdf`: Customer Information Sheet (a one-page "know your policy" summary)

The key figures above come from these brochures:

| Figure | Source |
|---|---|
| Nav Jeevan Shree sample premiums, GA rates, incentives | `Endowment Plans/912 - LIC's Nav Jeevan Shree (512N387V02)/Sales Brochure.pdf`, sections 3.C, 7, 9 |
| Amritbaal GA ₹80/1000, eligibility, illustration | `Endowment Plans/774 - LIC's Amritbaal (512N365V02)/Sales Brochure.pdf`, sections 1–3, 7, Benefit Illustration |
| New Bima Jyoti GA 6%, sample premiums | `Endowment Plans/890 - LIC's New Bima Jyoti (512N395V01)/Sales Brochure.pdf` |
| Jeevan Labh 25/16 illustration | `Endowment Plans/736 - LIC's Jeevan Labh Plan (512N304V03)/Sales Brochure.pdf` |
| Jeevan Tarun illustration | `Money Back Plans/734 - LIC's Jeevan Tarun (512N299V03)/Sales Brochure.pdf` |
| New Children's Money Back illustration | `Money Back Plans/732 - LIC's New Children's Money Back Plan (512N296V03)/Sales Brochure.pdf` |

## Appendix B: Re-running the analysis

```bash
cd ~/Downloads/LIC_Plans/scripts
python3 01_download_pdfs.py --out ~/Downloads/LIC_Plans --cache ./cache   # re-download latest PDFs
pip install pypdf
python3 02_extract_text.py --root ~/Downloads/LIC_Plans --out ./txt        # PDF -> text
python3 03_extract_key_sections.py --txt ./txt --out key_sections.md       # eligibility / premiums / illustrations
python3 04_compare_returns.py                                              # IRR comparison + goal sizing
```

_This analysis is based only on LIC's published product literature and is not personalised financial advice._
