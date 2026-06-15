#!/usr/bin/env python3
"""
update_captions.py
Reads captions.csv and writes captions.json for the Vibhav Lal portfolio website.

Usage:
    python3 /Users/Shared/veebz/myweb/update_captions.py

The CSV file must have these columns (row 1 = headers):
    category, filename, title, description

Open captions.csv in Numbers, TextEdit, or any text editor to edit it.
After running, commit and push captions.json to GitHub to update the live site.
"""

import csv
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_FILE  = BASE_DIR / "captions.csv"
JSON_FILE = BASE_DIR / "captions.json"

VALID_CATEGORIES = {"lego", "sketches", "rubiks", "woodwork"}


def csv_to_json():
    if not CSV_FILE.exists():
        print(f"ERROR: {CSV_FILE} not found.")
        sys.exit(1)

    captions = {cat: {} for cat in VALID_CATEGORIES}
    skipped = 0

    with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        # Normalise header names (strip spaces, lowercase)
        reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]

        required = {"category", "filename", "title", "description"}
        missing = required - set(reader.fieldnames)
        if missing:
            print(f"ERROR: Missing columns in CSV: {missing}")
            print(f"Found columns: {reader.fieldnames}")
            sys.exit(1)

        for row_num, row in enumerate(reader, start=2):
            category    = row.get("category", "").strip().lower()
            filename    = row.get("filename", "").strip()
            title       = row.get("title", "").strip()
            description = row.get("description", "").strip()

            if not category and not filename:
                continue  # blank row

            if category not in VALID_CATEGORIES:
                print(f"  Row {row_num}: unknown category '{category}' — skipped")
                skipped += 1
                continue

            # Accept filenames with or without .jpg extension
            filename = filename.replace(".jpg", "").replace(".JPG", "").replace(".jpeg", "")
            captions[category][filename] = {"title": title, "description": description}

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(captions, f, indent=2, ensure_ascii=False)

    total = sum(len(v) for v in captions.values())
    print(f"Done. {total} captions written to captions.json ({skipped} rows skipped).")
    print("Next: git add captions.json && git commit -m 'update captions' && git push")


if __name__ == "__main__":
    csv_to_json()
