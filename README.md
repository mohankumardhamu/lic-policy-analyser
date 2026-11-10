# LIC Policy Analyser

A small set of Python scripts for comparing **LIC (Life Insurance Corporation of India)** savings plans using LIC's own published documents. They:

1. download the latest Sales Brochure, Policy Document and Customer Information Sheet (CIS) for every plan in the **Endowment**, **Money Back** and **Pension** categories on [licindia.in](https://licindia.in),
2. extract the text from those PDFs,
3. pull out the sections that matter for comparison (eligibility, guaranteed additions, maturity benefit, sample premiums, benefit illustrations), and
4. calculate the effective annual return (IRR) of each shortlisted plan and size it to a savings goal.

The worked result is in [`findings/LIC_plan_recommendation.md`](findings/LIC_plan_recommendation.md): a screening of all 23 plans against a children's college-education goal.

> **Disclaimer:** This project uses only LIC's public product literature. It is not personalised financial advice, and premiums in the findings are estimates from LIC's sample tables. Get an exact quote from LIC before buying any policy.

---

## Repository layout

```
.
├── README.md
├── scripts/
│   ├── 01_download_pdfs.py          # crawl licindia.in and download the latest PDFs per plan
│   ├── 02_extract_text.py           # PDF -> plain text (pypdf)
│   ├── 03_extract_key_sections.py   # pull comparison-relevant sections from each brochure
│   └── 04_compare_returns.py        # IRR comparison + goal sizing
└── findings/
    └── LIC_plan_recommendation.md   # full analysis and recommendation
```

The downloaded PDFs and generated files (`cache/`, `txt/`, `key_sections.md`) are **not** committed. Run the scripts to recreate them.

---

## Key findings (summary)

Full details, tables and sources are in the [findings report](findings/LIC_plan_recommendation.md).

| Plan | Scenario (from brochure) | IRR p.a. | Guaranteed? |
|---|---|---:|:---:|
| Nav Jeevan Shree (912) | pay 8 / term 20 | **5.99%** | ✅ |
| Amritbaal (774) | pay 7 / term 20, child aged 5 | **5.56%** | ✅ |
| Nav Jeevan Shree (912) | pay 10 / term 15 | 5.31% | ✅ |
| Nav Jeevan Shree (912) | pay 6 / term 10 | 5.12% | ✅ |
| Jeevan Labh (736) | pay 16 / term 25, 8% scenario | 4.76% | ❌ |
| Jeevan Tarun (734) | 8% scenario | 4.35% | ❌ |
| New Bima Jyoti (890) | pay 10 / term 15 | 3.51% | ✅ |
| New Children's Money Back (732) | 8% scenario | 3.43% | ❌ |
| Jeevan Labh (736) | 4% scenario | 1.80% | ❌ |
| Jeevan Tarun (734) | 4% scenario | 0.87% | ❌ |

- **Best fit for a 10-year goal:** **LIC's Nav Jeevan Shree (912)**. It is the only regular-premium plan that can mature in exactly 10 years (6-year premium-paying term), and its maturity value is fully guaranteed.
- **Best for children aged 13 or younger:** **LIC's Amritbaal (774)**, a dedicated child-education plan with a guaranteed addition of 8% of the sum assured each year.
- **Realistic returns:** guaranteed LIC savings plans in this set return about **5–6% a year**. Bonus-based plans showed about **1–5% a year** in LIC's own 4% and 8% illustrations.
- None of the 6 pension plans fits a lump-sum goal; they are annuity or retirement products.

---

## Requirements

- Python 3.9 or later
- `curl` (used by the downloader; preinstalled on macOS and most Linux distributions)
- [`pypdf`](https://pypi.org/project/pypdf/), needed only by step 2

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pypdf
```

Steps 1, 3 and 4 use only the Python standard library.

---

## Usage

Run the scripts from the repository root, in order. Each step's output feeds the next.

### Step 1: download the PDFs

```bash
python3 scripts/01_download_pdfs.py --out . --cache ./cache
```

| Option | Default | Meaning |
|---|---|---|
| `--out` | `~/Downloads/LIC_Plans` | Where the plan folders are created |
| `--cache` | `./cache` | Where raw HTML pages are stored |

For each category page (`endowment-plans`, `pension-plan`, `money-back-plans`) the script:

1. reads the plan table (Sl. No. | Plan Name | Plan No. | UIN),
2. opens every plan page and collects all PDF links,
3. keeps only the **current** version of each document type. A label with an end date ("… To dd/mm/yyyy") is treated as superseded; among the rest, the newest upload timestamp (`?t=`) wins,
4. saves it as `<out>/<Category>/<PlanNo - Plan Name (UIN)>/<Doc type>.pdf`, and
5. checks that every file really starts with `%PDF-`, then prints a status report.

Resulting layout (69 PDFs for 23 plans at the time of the analysis):

```
Endowment Plans/
  912 - LIC's Nav Jeevan Shree (512N387V02)/
    CIS.pdf
    Policy Document.pdf
    Sales Brochure.pdf
  ...
Money Back Plans/
  ...
Pension Plans/
  ...
```

### Step 2: extract text

```bash
python3 scripts/02_extract_text.py --root . --out ./txt
```

Walks `--root` and writes one `.txt` per PDF into `--out`, named `<PlanFolder>__<DocType>.txt`, for example `774_LIC_s_Amritbaal_512N365V02___Sales_Brochure.txt`. A PDF that fails to parse is logged in its output file and the run continues.

### Step 3: extract the key sections

```bash
# all plans
python3 scripts/03_extract_key_sections.py --txt ./txt --out key_sections.md

# only selected plan numbers
python3 scripts/03_extract_key_sections.py 774 912 890
```

For every `*Sales_Brochure.txt` it captures:

- the opening description (plan type),
- **Eligibility Conditions**: entry age, policy term, premium-paying term, minimum sum assured,
- **Guaranteed Additions** wording,
- **Maturity Benefit** wording,
- the **Sample Illustrative Premium** table, and
- the start of the **Benefit Illustration** table.

The result is printed and saved as Markdown in `key_sections.md`. This is the raw material for screening plans by hand.

### Step 4: compare returns and size the goal

```bash
python3 scripts/04_compare_returns.py
```

Sample output:

```
Plan / scenario                                                Paid    Received  Multiple     IRR
Amritbaal 774 - pay 7 / term 20 (guaranteed)                515,375   1,300,000     2.52x   5.56%
Nav Jeevan Shree 912 - pay 6 / term 10 (guaranteed)         608,100     887,664     1.46x   5.12%
Nav Jeevan Shree 912 - pay 10 / term 15 (guaranteed)        628,250   1,093,696     1.74x   5.31%
...

Goal sizing: two children, one policy each at minimum Basic Sum Assured Rs 5,00,000
  Nav Jeevan Shree 6-pay / 10-year: ~Rs 8,736/month per child (Rs 17,473 total) for 6 yrs = Rs 1,258,037 paid -> Rs 887,664 per child (Rs 1,775,328 total) at year 10
  ...
```

---

## How the returns are calculated

- **Inputs** are taken from each plan's Sales Brochure: sample premium tables, guaranteed-addition (GA) rates and benefit illustrations. The source of every number is listed in Appendix A of the findings report.
- **Cash-flow convention:** annual premiums are paid at the start of each policy year (t = 0 … PPT−1), and maturity or survival benefits are received at the end of year t.
- **IRR** is found by bisection on the net present value over the range −50% to +50%.
- **Guaranteed Additions on premiums** (Nav Jeevan Shree, New Bima Jyoti): each year, GA = rate × total annual premiums paid so far. These are added up over the whole term.
- **Guaranteed Additions on sum assured** (Amritbaal): ₹80 per ₹1,000 Basic Sum Assured each year, simple.
- **Monthly premium** = 0.0862 × annual premium (LIC's monthly-mode factor).
- **Bonus-based plans** (Jeevan Labh, Jeevan Tarun, New Children's Money Back) use LIC's IRDAI-mandated 4% and 8% illustration scenarios. These are **not guaranteed** and are not upper or lower limits on the actual payout.

### Adapting it to your own goal

Edit `scenarios()` in `scripts/04_compare_returns.py` to add plans or change premiums. Each scenario is a tuple:

```python
(name, annual_premium, premium_paying_term_years, [(year, payout), ...])
```

To change the goal sizing, edit the list at the end of `main()` (label, annual premium, PPT, term, GA rate). Use premiums from LIC's premium calculator for the actual age of the life assured.

---

## Notes and limitations

- **Scraping depends on licindia.in's HTML.** If LIC changes the page structure, the regexes in `plan_rows()` and `pdf_links()` in step 1 may need updating.
- **Sample premiums are for a specific age** (for example, 35 years for Nav Jeevan Shree). Actual premiums depend on age, health, payment mode and rebates.
- **Text extraction is best effort.** Some brochure tables come out of `pypdf` with merged columns, so check figures against the PDF.
- Plan list, versions and GA rates reflect the documents downloaded on **10 Nov 2026**.
