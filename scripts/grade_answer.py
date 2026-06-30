#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Generate scorecard.")
    p.add_argument("--question-id", required=True)
    args = p.parse_args()

    rubric = json.loads(Path("practice/rubrics/default_qe_rubric.json").read_text(encoding="utf-8"))
    lines = [f"# Scorecard — {args.question_id}", "", "| Dimension | Max | Score | Notes |", "|---|---:|---:|---|"]
    for d in rubric["dimensions"]:
        lines.append(f"| {d['name']} | {d['points']} |  | {d['criteria']} |")
    lines += ["", "Total: ___ / 100"]
    out = Path("practice/scorecards") / f"{args.question_id}_scorecard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
