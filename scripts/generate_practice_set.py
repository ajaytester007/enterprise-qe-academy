#!/usr/bin/env python3
import argparse, json, random
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Generate a markdown practice set.")
    p.add_argument("--catalog", default="catalog/questions.jsonl")
    p.add_argument("--out", default="outputs/practice_set.md")
    p.add_argument("--count", type=int, default=50)
    p.add_argument("--difficulty")
    p.add_argument("--category")
    p.add_argument("--domain")
    args = p.parse_args()

    qs = [json.loads(line) for line in Path(args.catalog).read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.difficulty: qs = [q for q in qs if q["difficulty"] == args.difficulty]
    if args.category: qs = [q for q in qs if q["category"] == args.category]
    if args.domain: qs = [q for q in qs if q["domain"].lower() == args.domain.lower()]
    random.seed(100)
    selected = random.sample(qs, min(args.count, len(qs)))

    lines = ["# Generated Enterprise QE Practice Set", ""]
    for i, q in enumerate(selected, 1):
        lines += [
            f"## {i}. {q['id']} — {q['title']}",
            f"- Difficulty: {q['difficulty']}",
            f"- Category: {q['category']}",
            f"- Domain: {q['domain']}",
            f"- Role: {q['role']}",
            "",
            f"**Problem:** {q['problem_statement']}",
            "",
            "### Answer Template",
            "1. Clarifying questions",
            "2. Naive approach",
            "3. Optimized approach",
            "4. Code / SQL / API strategy",
            "5. Tests and evidence",
            "6. Complexity",
            "7. Whiteboard explanation",
            "8. Follow-up questions",
            ""
        ]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out} with {len(selected)} questions.")

if __name__ == "__main__":
    main()
