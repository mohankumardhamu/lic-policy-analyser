#!/usr/bin/env python3
"""
Step 1 - Crawl LIC plan category pages and download the latest PDFs for every plan.

For each category page (endowment / pension / money-back) the script:
  1. reads the plan table (Sl. No. | Plan Name | Plan No. | UIN No.),
  2. opens every plan page,
  3. collects all PDF links (Sales Brochure / Policy Document / CIS),
  4. for each document type keeps only the *current* version
     (labels with a "... To dd/mm/yyyy" end date are superseded; among the rest
     the newest upload timestamp `?t=` wins),
  5. saves it as  <OUT>/<Category>/<PlanNo - Plan Name (UIN)>/<Doc type>.pdf
     and checks the file really starts with %PDF-.

Usage:
    python3 01_download_pdfs.py [--out ~/Downloads/LIC_Plans] [--cache ./cache]

Only the Python standard library + `curl` are required.
"""
import argparse
import html
import os
import re
import subprocess
import time

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
BASE = "https://licindia.in"
CATEGORIES = {
    "endowment-plans": "Endowment Plans",
    "pension-plan": "Pension Plans",
    "money-back-plans": "Money Back Plans",
}


def fetch(url, path, tries=3):
    """Download url -> path with curl, retrying when the response is empty."""
    for _ in range(tries):
        subprocess.run(["curl", "-sL", "--max-time", "120", "-A", UA, "-o", path, url])
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            return True
        time.sleep(2)
    return False


def text(fragment):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment))).strip()


def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "", name.replace("’", "'")).strip()


def doc_type(label):
    l = label.lower()
    if "brochure" in l:
        return "Sales Brochure"
    if l.startswith("cis"):
        return "CIS"
    if "policy" in l:
        return "Policy Document"
    return label or "Document"


def plan_rows(category_html):
    """Yield (plan_name, plan_no, uin, plan_url) from a category page's table."""
    for row in re.findall(r"<tr.*?</tr>", category_html, re.S):
        if not re.search(r"512[A-Z]\d", row):          # UINs look like 512N277V03 / 512L347V01
            continue
        cells = [text(c) for c in re.findall(r"<td.*?</td>", row, re.S)]
        links = re.findall(r'href="([^"]+)"', row)
        if len(cells) < 4 or not links:
            continue
        url = links[0] if links[0].startswith("http") else BASE + links[0]
        yield cells[1], cells[2], cells[3], url


def pdf_links(plan_html):
    """Return {doc_type: [(is_current, upload_ts, label, href), ...]}."""
    docs = {}
    pattern = r'<a[^>]*href="([^"]*/documents/20121/[^"]*\.pdf[^"]*)"[^>]*>(.*?)</a>'
    for m in re.finditer(pattern, plan_html, re.S | re.I):
        href, label = m.group(1), text(m.group(2))
        ts = re.search(r"[?&]t=(\d+)", href)
        current = not re.search(r"\bto\s+\d{2}/\d{2}/\d{4}", label.lower())
        docs.setdefault(doc_type(label), []).append((current, int(ts.group(1)) if ts else 0, label, href))
    return docs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.expanduser("~/Downloads/LIC_Plans"))
    ap.add_argument("--cache", default="./cache", help="where raw HTML pages are stored")
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)

    report = []
    for slug, cat_name in CATEGORIES.items():
        cat_path = os.path.join(args.cache, f"{slug}.html")
        if not fetch(f"{BASE}/en/web/guest/{slug}", cat_path):
            print(f"!! could not fetch category {slug}")
            continue
        cat_html = open(cat_path, encoding="utf-8", errors="ignore").read()

        for name, plan_no, uin, url in plan_rows(cat_html):
            page = os.path.join(args.cache, re.sub(r"[^a-z0-9]+", "-", url.split("/")[-1].lower()).strip("-") + ".html")
            fetch(url, page)
            docs = pdf_links(open(page, encoding="utf-8", errors="ignore").read())
            folder = os.path.join(args.out, cat_name, safe(f"{plan_no} - {name} ({uin})"))
            os.makedirs(folder, exist_ok=True)
            if not docs:
                report.append((cat_name, name, "-", "NO PDFs FOUND", url))
                continue
            for dtype, versions in docs.items():
                _, _, label, href = max(versions)     # current first, then newest upload
                dest = os.path.join(folder, f"{dtype}.pdf")
                ok = fetch(href if href.startswith("http") else BASE + href, dest)
                magic = open(dest, "rb").read(5) if ok else b""
                status = f"OK {os.path.getsize(dest) / 1024:.0f} KB" if magic == b"%PDF-" else f"FAILED {magic!r}"
                report.append((cat_name, name, dtype, status, label))

    for r in report:
        print(" | ".join(r))
    print(f"\n{sum(1 for r in report if r[3].startswith('OK'))} PDFs downloaded to {args.out}")


if __name__ == "__main__":
    main()
