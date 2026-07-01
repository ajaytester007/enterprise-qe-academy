#!/usr/bin/env python3
"""Validate catalog, solution-bank, report, and prompt-export readiness."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

CATALOG = Path("catalog/questions.jsonl")
REQUIRED_Q_KEYS = {"id", "title", "difficulty", "category", "concept", "domain", "role", "problem_statement"}
SOLUTION_BANKS = [Path("solutions/solved/seed_solution_bank.json"), Path("solutions/solved/enhanced_solution_bank.json")]
REPORT_DIR = Path("practice/reports")


def load_catalog() -> list[dict]:
    if not CATALOG.exists():
        raise AssertionError(f"Missing {CATALOG}")
    rows = []
    for line_no, line in enumerate(CATALOG.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"Invalid JSONL at {CATALOG}:{line_no}: {exc}") from exc
        missing = REQUIRED_Q_KEYS - set(row)
        if missing:
            raise AssertionError(f"Question {row.get('id', '<unknown>')} missing keys: {sorted(missing)}")
        rows.append(row)
    if not rows:
        raise AssertionError("Catalog has zero questions")
    return rows


def validate_solution_banks(categories: set[str], domains: set[str]) -> tuple[int, int]:
    entries: dict[str, dict] = {}
    for path in SOLUTION_BANKS:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise AssertionError(f"{path} must be a JSON object")
            entries.update(data)
    bad = [k for k, v in entries.items() if not isinstance(v, dict) or not (v.get("model") or v.get("solution"))]
    if bad:
        raise AssertionError(f"Solution bank entries missing model/solution: {bad[:10]}")
    category_hits = len(categories.intersection(entries))
    normalized_domain_keys = {d.upper().replace(" ", "_").replace("-", "_") for d in domains}
    domain_hits = len(normalized_domain_keys.intersection(entries))
    return category_hits, domain_hits


def validate_reports() -> int:
    reports = list(REPORT_DIR.glob("session_*.md"))
    if not reports:
        raise AssertionError("No practice reports found. Run scripts/start_practice_session.py first.")
    return len(reports)


def main() -> None:
    p = argparse.ArgumentParser(description="Validate Enterprise QE Academy practice assets.")
    p.add_argument("--strict", action="store_true", help="Fail if solution coverage is low.")
    args = p.parse_args()

    rows = load_catalog()
    ids = [r["id"] for r in rows]
    dupes = [qid for qid, count in Counter(ids).items() if count > 1]
    if dupes:
        raise AssertionError(f"Duplicate question IDs: {dupes[:20]}")

    categories = {r["category"] for r in rows}
    domains = {r["domain"] for r in rows}
    category_hits, domain_hits = validate_solution_banks(categories, domains)
    report_count = validate_reports()

    category_pct = (category_hits / max(len(categories), 1)) * 100
    domain_pct = (domain_hits / max(len(domains), 1)) * 100

    print("Practice asset validation passed")
    print(f"Questions: {len(rows)}")
    print(f"Categories: {len(categories)}; solution-bank coverage: {category_hits}/{len(categories)} ({category_pct:.1f}%)")
    print(f"Domains: {len(domains)}; solution-bank coverage: {domain_hits}/{len(domains)} ({domain_pct:.1f}%)")
    print(f"Reports: {report_count}")

    if args.strict and category_pct < 50:
        raise AssertionError("Strict mode failed: category solution coverage below 50%")


if __name__ == "__main__":
    main()
