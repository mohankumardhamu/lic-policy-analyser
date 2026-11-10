#!/usr/bin/env python3
"""
Step 2 - Extract plain text from every downloaded PDF.

Walks <ROOT> (the folder produced by 01_download_pdfs.py) and writes one .txt per
PDF into <OUT>, named  <PlanFolder>__<DocType>.txt  e.g.
    774_LIC_s_Amritbaal_512N365V02___Sales_Brochure.txt

Requires: pypdf   (pip install pypdf)

Usage:
    python3 02_extract_text.py [--root ~/Downloads/LIC_Plans] [--out ./txt]
"""
import argparse
import logging
import os
import re

import pypdf

logging.getLogger("pypdf").setLevel(logging.ERROR)   # silence font-encoding warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.expanduser("~/Downloads/LIC_Plans"))
    ap.add_argument("--out", default="./txt")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    count = 0
    for folder, _, files in os.walk(args.root):
        for f in sorted(files):
            if not f.lower().endswith(".pdf"):
                continue
            plan = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(folder))
            name = f"{plan}__{f[:-4].replace(' ', '_')}.txt"
            try:
                reader = pypdf.PdfReader(os.path.join(folder, f))
                body = "\n".join((page.extract_text() or "") for page in reader.pages)
            except Exception as e:                       # keep going on a broken PDF
                body = f"ERROR extracting text: {e}"
            with open(os.path.join(args.out, name), "w", encoding="utf-8") as fh:
                fh.write(body)
            count += 1
            print(f"{len(body):>8} chars  {name}")
    print(f"\nExtracted {count} PDFs into {args.out}")


if __name__ == "__main__":
    main()
