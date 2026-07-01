#!/usr/bin/env python3
import argparse, json, random, datetime
from pathlib import Path

CATALOG = Path("catalog/questions.jsonl")
SESSION_DIR = Path("practice/sessions")
REPORT_DIR = Path("practice/reports")
COMPAT = Path("practice/prompts/domain_category_compatibility.json")
BANKS = [Path("solutions/solved/enhanced_solution_bank.json"), Path("solutions/solved/seed_solution_bank.json")]

def read_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

def load_catalog():
    return [json.loads(line) for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]

def load_bank():
    merged = {}
    for b in reversed(BANKS):
        if b.exists():
            merged.update(json.loads(b.read_text(encoding="utf-8")))
    return merged

def coherent(q, args, compat):
    if not args.coherent:
        return True
    if not q.get("domain") or not q.get("category"):
        return True
    allowed = compat.get(q["domain"])
    return not allowed or q["category"] in allowed

def filter_questions(qs, args):
    compat = read_json(COMPAT, {})
    out = []
    for q in qs:
        if args.category and q["category"] != args.category: continue
        if args.domain and q["domain"].lower() != args.domain.lower(): continue
        if args.role and q["role"].lower() != args.role.lower(): continue
        if args.difficulty and q["difficulty"] != args.difficulty: continue
        if args.keyword and args.keyword.lower() not in json.dumps(q).lower(): continue
        if not coherent(q, args, compat): continue
        out.append(q)
    return out

def pack_for(q, bank):
    return bank.get(q["category"]) or bank.get(q["domain"].upper().replace(" ", "_")) or {
        "model": "Use the Enterprise QE answer framework: clarify scope, propose approach, define test strategy, cover edge cases, describe evidence, and explain production readiness.",
        "followups": ["How would you automate this?", "How would you prove readiness?", "What risks remain?"]
    }

def hint1(q):
    return f"Clarify the scope, business grain, inputs, outputs, and risk for {q['concept']} in {q['domain']}."

def hint2(q):
    return f"Structure the answer using approach, edge cases, validation strategy, evidence, CI/CD readiness, and follow-up risks."

def main():
    p = argparse.ArgumentParser(description="Start a coherent Enterprise QE tutor/practice session.")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--category")
    p.add_argument("--domain")
    p.add_argument("--role")
    p.add_argument("--difficulty")
    p.add_argument("--keyword")
    p.add_argument("--mode", choices=["questions", "hints", "solutions", "tutor"], default="tutor")
    p.add_argument("--coherent", action="store_true", default=True)
    p.add_argument("--allow-mixed-domain", dest="coherent", action="store_false")
    p.add_argument("--seed", type=int, default=2026)
    args = p.parse_args()

    qs = filter_questions(load_catalog(), args)
    if not qs:
        raise SystemExit("No questions matched filters. Try --allow-mixed-domain or broader filters.")

    random.seed(args.seed)
    selected = random.sample(qs, min(args.count, len(qs)))
    bank = load_bank()

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = f"session_{ts}"
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    session = {"session_id": session_id, "created_at": datetime.datetime.now().isoformat(timespec="seconds"), "filters": vars(args), "questions": selected}
    (SESSION_DIR / f"{session_id}.json").write_text(json.dumps(session, indent=2), encoding="utf-8")

    lines = [f"# Tutor Practice Session: {session_id}", "", "## How to Practice", "", "1. Answer first without opening hints.", "2. Open Hint 1 only if stuck.", "3. Open Hint 2 if still stuck.", "4. Reveal the model answer.", "5. Score yourself and write improvement notes.", ""]
    for i, q in enumerate(selected, 1):
        pack = pack_for(q, bank)
        lines += [
            f"## {i}. {q['id']} — {q['title']}", "",
            f"- Difficulty: {q['difficulty']}",
            f"- Category: {q['category']}",
            f"- Concept: {q['concept']}",
            f"- Domain: {q['domain']}",
            f"- Role: {q['role']}", "",
            f"**Problem:** {q['problem_statement']}", "",
            "### Your Answer Notes", "", "- ", ""
        ]
        if args.mode in ("hints", "solutions", "tutor"):
            lines += [f"<details><summary>Hint 1</summary>\n\n{hint1(q)}\n\n</details>", ""]
            lines += [f"<details><summary>Hint 2</summary>\n\n{hint2(q)}\n\n</details>", ""]
        if args.mode in ("solutions", "tutor"):
            lines += [f"<details><summary>Model Answer</summary>\n\n{pack['model']}\n\n</details>", ""]
            lines += ["### Follow-up Questions", ""]
            for f in pack.get("followups", []):
                lines.append(f"- {f}")
            lines += ["", "### Scorecard", "", "| Dimension | Score | Notes |", "|---|---:|---|", "| Problem understanding | ___ / 15 | |", "| Technical approach | ___ / 20 | |", "| Edge cases and risks | ___ / 15 | |", "| Testing strategy | ___ / 20 | |", "| Evidence and observability | ___ / 10 | |", "| Communication | ___ / 20 | |", "", "**Total:** ___ / 100", "", "### Improvement Notes", "", "- ", ""]

    report = REPORT_DIR / f"{session_id}_tutor.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created tutor session JSON: {SESSION_DIR / (session_id + '.json')}")
    print(f"Created tutor report: {report}")

if __name__ == "__main__":
    main()
