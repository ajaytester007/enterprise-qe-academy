#!/usr/bin/env python3
"""Generate a static v4 quality dashboard for GitHub Pages."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from platform_core.repo_paths import ensure_repo_imports

ROOT = ensure_repo_imports(Path(__file__).resolve())
OUT = ROOT / "outputs" / "v4"
DOCS = ROOT / "docs" / "docs" / "v4"
QUALITY = OUT / "quality_report.json"
ANALYTICS = OUT / "learning_analytics.json"


def load(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing {path}. Run generate_v4_platform_core.py and assess_v4_quality.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def table_from_counts(counts, limit=20):
    rows = ["| Item | Count |", "|---|---:|"]
    for key, value in list(counts.items())[:limit]:
        rows.append(f"| {key} | {value} |")
    return "\n".join(rows)


def bar(value, total, width=20):
    if total <= 0:
        return "░" * width
    filled = round(width * value / total)
    return "█" * filled + "░" * (width - filled)


def main():
    quality = load(QUALITY)
    analytics = load(ANALYTICS)
    summary = quality["summary"]
    total = summary["total_nodes"] or 1
    assessments = quality["assessments"]
    weakest = sorted(assessments, key=lambda x: x["score"])[:15]

    weak_lines = ["| Score | Status | ID | Scenario |", "|---:|---|---|---|"]
    for item in weakest:
        weak_lines.append(f"| {item['score']} | {item['status']} | {item['id']} | {item['title']} |")

    body = f"""# v4 Quality Dashboard

## Executive readiness

| Metric | Value |
|---|---:|
| Total knowledge nodes | {summary['total_nodes']} |
| Passed | {summary['passed']} |
| Review | {summary['review']} |
| Failed | {summary['failed']} |
| Average quality score | {summary['average_score']} |
| Quality gate | {summary['quality_gate']} |

## Status mix

| Status | Count | Visual |
|---|---:|---|
| Pass | {summary['passed']} | `{bar(summary['passed'], total)}` |
| Review | {summary['review']} | `{bar(summary['review'], total)}` |
| Fail | {summary['failed']} | `{bar(summary['failed'], total)}` |

## Coverage by domain

{table_from_counts(analytics.get('by_domain', {}))}

## Coverage by difficulty

{table_from_counts(analytics.get('by_difficulty', {}))}

## Top quality issues

{table_from_counts(summary.get('top_issues', {}), limit=25)}

## Lowest scoring scenarios

{"\n".join(weak_lines)}

## How to use this dashboard

- Use this page before publishing new enterprise packs.
- Treat `fail` scenarios as blockers for premium/interview-ready content.
- Treat `review` scenarios as acceptable for internal practice but not final curated packs.
- Expand short or placeholder answers before scaling the catalog.
"""
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "quality-dashboard.md").write_text(body, encoding="utf-8")
    print(f"Wrote {DOCS / 'quality-dashboard.md'}")


if __name__ == "__main__":
    main()
