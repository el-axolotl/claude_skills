#!/usr/bin/env python3
"""Dump a filled-out questionnaire .xlsx (from generate_questionnaire.py) to JSON.

Reads the fixed column order (MITRE Category, Severity, Question, Answer,
Description/Abuse Context) and prints one JSON object per row to stdout so the
answers can be reasoned over when building a threat model. Does no analysis itself.

Usage:
    python read_questionnaire.py --input "Acme_Security_Questionnaire.xlsx"
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit(
        "openpyxl is required but not installed.\n"
        "Run: pip install openpyxl"
    )

EXPECTED_HEADERS = [
    "MITRE Category",
    "Severity",
    "Question",
    "Answer",
    "Description/Abuse Context",
]

KEY_MAP = {
    "MITRE Category": "mitre_category",
    "Severity": "severity",
    "Question": "question",
    "Answer": "answer",
    "Description/Abuse Context": "description",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to the filled-out questionnaire .xlsx")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"Input file not found: {input_path}")

    wb = load_workbook(input_path, read_only=True, data_only=True)
    ws = wb.active

    rows_iter = ws.iter_rows(values_only=True)
    headers = list(next(rows_iter))
    if headers != EXPECTED_HEADERS:
        sys.exit(
            "Unexpected header row.\n"
            f"Expected: {EXPECTED_HEADERS}\n"
            f"Found:    {headers}"
        )

    rows = []
    for raw_row in rows_iter:
        if all(v is None for v in raw_row):
            continue
        row = {KEY_MAP[h]: ("" if v is None else v) for h, v in zip(headers, raw_row)}
        rows.append(row)

    print(json.dumps({"sheet_title": ws.title, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
