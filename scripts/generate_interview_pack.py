#!/usr/bin/env python3
import argparse, json, random
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Generate interview pack.")
    p.add_argument("--role", default="Lead Quality Engineer")
    p.add_argument("--domain")
    p.add_argument("--count", type=int, default=25)
    args = p.parse_args()

    qs = [json.loads(line) for line in Path("catalog/questions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    qs = [q for q in qs if q["role"].lower() == args.role.lower()]
    if args.domain:
        qs = [q for q in qs if q["domain"].lower() == args.domain.lower()]

    random.seed(2026)
    selected = random.sample(qs, min(args.count, len(qs)))
    lines = [f"# Interview Pack — {args.role}", ""]
    if args.domain:
        lines += [f"Domain: **{args.domain}**", ""]
    for i, q in enumerate(selected, 1):
        lines += [f"## {i}. {q['id']} — {q['title']}", "", q["problem_statement"], "", "### Expected Coverage", "", "- Scope and assumptions", "- Technical approach", "- Edge cases", "- Testing strategy", "- Evidence", "- Follow-up questions", ""]

    out = Path("outputs/interview_pack.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
