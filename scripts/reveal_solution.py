#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Reveal hint or solution for a question.")
    p.add_argument("--id", required=True)
    p.add_argument("--level", choices=["hint1", "hint2", "solution"], default="hint1")
    args = p.parse_args()

    q = None
    for line in Path("catalog/questions.jsonl").read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if item["id"] == args.id:
            q = item
            break
    if not q:
        raise SystemExit(f"Question not found: {args.id}")

    bank = json.loads(Path("solutions/solved/seed_solution_bank.json").read_text(encoding="utf-8"))
    pack = bank.get(q["category"]) or bank.get(q["domain"].upper().replace(" ", "_")) or {
        "hint1": "Clarify scope and risk.",
        "hint2": "Discuss approach, tests, evidence, and production readiness.",
        "solution": "Use the Enterprise QE answer framework."
    }

    print(f"{q['id']} — {q['title']}")
    print("")
    print(pack[args.level])

if __name__ == "__main__":
    main()
