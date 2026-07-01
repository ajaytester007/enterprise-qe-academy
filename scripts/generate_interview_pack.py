#!/usr/bin/env python3
"""Generate role/domain interview packs with coverage, hints, rubrics, and model-answer references."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

CATALOG = Path("catalog/questions.jsonl")
BANKS = [Path("solutions/solved/seed_solution_bank.json"), Path("solutions/solved/enhanced_solution_bank.json")]


def load_catalog() -> list[dict]:
    return [json.loads(line) for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_bank() -> dict:
    merged = {}
    for path in BANKS:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            for key, value in data.items():
                if "solution" in value and "model" not in value:
                    value = {"model": value["solution"], "followups": value.get("followups", [])}
                merged[key] = value
    return merged


def model_for(q: dict, bank: dict) -> str:
    pack = bank.get(q.get("category")) or bank.get(q.get("domain", "").upper().replace(" ", "_"))
    if pack:
        return pack.get("model") or pack.get("solution") or ""
    return "Clarify scope, propose a risk-based solution, define automated validation, cover edge cases, and prove readiness with evidence."


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a complete Enterprise QE interview pack.")
    parser.add_argument("--role", default="Lead Quality Engineer")
    parser.add_argument("--domain")
    parser.add_argument("--difficulty")
    parser.add_argument("--category")
    parser.add_argument("--count", type=int, default=25)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--include-solutions", action="store_true")
    parser.add_argument("--out", default="outputs/interview_pack.md")
    args = parser.parse_args()

    qs = load_catalog()
    if args.role:
        qs = [q for q in qs if q["role"].lower() == args.role.lower()]
    if args.domain:
        qs = [q for q in qs if q["domain"].lower() == args.domain.lower()]
    if args.difficulty:
        qs = [q for q in qs if q["difficulty"].lower() == args.difficulty.lower()]
    if args.category:
        qs = [q for q in qs if q["category"].lower() == args.category.lower()]
    if not qs:
        raise SystemExit("No questions matched. Broaden filters and retry.")

    random.seed(args.seed)
    selected = random.sample(qs, min(args.count, len(qs)))
    bank = load_bank()

    lines = [f"# Interview Pack — {args.role}", ""]
    meta = []
    if args.domain: meta.append(f"Domain: **{args.domain}**")
    if args.difficulty: meta.append(f"Difficulty: **{args.difficulty}**")
    if args.category: meta.append(f"Category: **{args.category}**")
    if meta:
        lines += meta + [""]
    lines += [
        "## How to Use This Pack", "",
        "1. Answer each question out loud before reading hints or solutions.",
        "2. Capture evidence you would show in an interview: test reports, logs, dashboards, SQL, CI/CD runs, and defect examples.",
        "3. Score yourself using the rubric and improve the answer before moving on.", "",
        "## Standard Rubric", "",
        "| Dimension | Points |",
        "|---|---:|",
        "| Problem understanding | 15 |",
        "| Technical approach | 20 |",
        "| Edge cases and risks | 15 |",
        "| Testing strategy | 20 |",
        "| Evidence and observability | 10 |",
        "| Communication | 20 |", "",
    ]

    for i, q in enumerate(selected, 1):
        lines += [
            f"## {i}. {q['id']} — {q['title']}", "",
            f"- Difficulty: {q['difficulty']}",
            f"- Category: {q['category']}",
            f"- Domain: {q['domain']}",
            f"- Role: {q['role']}", "",
            f"**Question:** {q['problem_statement']}", "",
            "### Expected Coverage", "",
            "- Scope, assumptions, and business grain",
            "- Architecture or implementation approach",
            "- Positive, negative, boundary, failure, and data-quality cases",
            "- Automation strategy and CI/CD quality gates",
            "- Evidence: reports, logs, traces, screenshots, dashboards, and sign-off artifacts",
            "- Residual risks and production-readiness decision", "",
            "### Follow-up Prompts", "",
            "- How would you automate this?",
            "- How would you prove readiness?",
            "- What can still fail in production?", "",
        ]
        if args.include_solutions:
            lines += ["### Model Answer", "", model_for(q, bank), ""]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
