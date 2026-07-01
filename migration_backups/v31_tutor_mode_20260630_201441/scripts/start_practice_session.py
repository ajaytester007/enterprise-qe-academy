#!/usr/bin/env python3
import argparse, json, random, datetime
from pathlib import Path

CATALOG = Path("catalog/questions.jsonl")
SESSION_DIR = Path("practice/sessions")
REPORT_DIR = Path("practice/reports")
SOLVED_BANK = Path("solutions/solved/seed_solution_bank.json")

def load_catalog():
    return [json.loads(line) for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]

def load_bank():
    return json.loads(SOLVED_BANK.read_text(encoding="utf-8")) if SOLVED_BANK.exists() else {}

def filter_questions(qs, args):
    if args.category:
        qs = [q for q in qs if q["category"] == args.category]
    if args.domain:
        qs = [q for q in qs if q["domain"].lower() == args.domain.lower()]
    if args.role:
        qs = [q for q in qs if q["role"].lower() == args.role.lower()]
    if args.difficulty:
        qs = [q for q in qs if q["difficulty"] == args.difficulty]
    if args.keyword:
        qs = [q for q in qs if args.keyword.lower() in json.dumps(q).lower()]
    return qs

def answer_pack(q, bank):
    return bank.get(q["category"]) or bank.get(q["domain"].upper().replace(" ", "_")) or {
        "hint1": "Clarify scope, inputs, outputs, and business risk.",
        "hint2": "Structure the answer around approach, tests, edge cases, evidence, and production readiness.",
        "solution": "Use the Enterprise QE answer framework: clarify context, propose approach, cover tests, discuss automation, capture evidence, and explain tradeoffs."
    }

def main():
    p = argparse.ArgumentParser(description="Start an Enterprise QE practice session.")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--category")
    p.add_argument("--domain")
    p.add_argument("--role")
    p.add_argument("--difficulty")
    p.add_argument("--keyword")
    p.add_argument("--mode", choices=["questions", "hints", "solutions"], default="hints")
    p.add_argument("--seed", type=int, default=2026)
    args = p.parse_args()

    qs = filter_questions(load_catalog(), args)
    if not qs:
        raise SystemExit("No questions matched filters.")

    random.seed(args.seed)
    selected = random.sample(qs, min(args.count, len(qs)))
    bank = load_bank()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = f"session_{ts}"
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    (SESSION_DIR / f"{session_id}.json").write_text(json.dumps({
        "session_id": session_id,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "filters": vars(args),
        "questions": selected
    }, indent=2), encoding="utf-8")

    lines = [f"# Practice Session: {session_id}", "", "## Questions", ""]
    for i, q in enumerate(selected, 1):
        pack = answer_pack(q, bank)
        lines += [
            f"### {i}. {q['id']} — {q['title']}",
            "",
            f"- Difficulty: {q['difficulty']}",
            f"- Category: {q['category']}",
            f"- Domain: {q['domain']}",
            f"- Role: {q['role']}",
            "",
            f"**Problem:** {q['problem_statement']}",
            "",
            "**Your Answer Notes:**",
            "",
            "- ",
            ""
        ]
        if args.mode in ("hints", "solutions"):
            lines += [f"<details><summary>Hint 1</summary>\n\n{pack['hint1']}\n\n</details>", ""]
            lines += [f"<details><summary>Hint 2</summary>\n\n{pack['hint2']}\n\n</details>", ""]
        if args.mode == "solutions":
            lines += [f"<details><summary>Full Solution</summary>\n\n{pack['solution']}\n\n</details>", ""]
        lines += ["**Self Score:** ___ / 100", "", "**Improvement Notes:**", "", "- ", ""]

    report = REPORT_DIR / f"{session_id}.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created session JSON: {SESSION_DIR / (session_id + '.json')}")
    print(f"Created practice report: {report}")

if __name__ == "__main__":
    main()
