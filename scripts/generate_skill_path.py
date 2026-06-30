#!/usr/bin/env python3
import argparse, json, random
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Generate skill path.")
    p.add_argument("--skill", required=True)
    p.add_argument("--weeks", type=int, default=4)
    args = p.parse_args()

    qs = [json.loads(line) for line in Path("catalog/questions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    matches = [q for q in qs if args.skill.lower() in json.dumps(q).lower()]
    random.seed(2026)
    random.shuffle(matches)
    per_week = max(5, min(25, len(matches)//max(args.weeks, 1))) if matches else 0

    lines = [f"# Skill Path — {args.skill}", "", f"Duration: **{args.weeks} weeks**", ""]
    idx = 0
    for w in range(1, args.weeks + 1):
        lines += [f"## Week {w}", ""]
        for q in matches[idx:idx+per_week]:
            lines.append(f"- `{q['id']}` {q['difficulty']} — {q['title']}")
        lines.append("")
        idx += per_week

    out = Path("practice/skill_paths") / f"{args.skill.lower().replace(' ', '_')}_{args.weeks}_weeks.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
