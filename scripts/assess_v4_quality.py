#!/usr/bin/env python3
"""Assess Enterprise QE Academy v4 content quality and readiness.

Produces:
- outputs/v4/quality_report.json
- outputs/v4/quality_report.md
- outputs/v4/quality_gate_status.json

The checks are intentionally standard-library only and deterministic so they run
both locally and in GitHub Actions.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from platform_core.repo_paths import ensure_repo_imports

ROOT = ensure_repo_imports(Path(__file__).resolve())
OUT = ROOT / "outputs" / "v4"
NODES = OUT / "knowledge_nodes.json"
QUALITY_JSON = OUT / "quality_report.json"
QUALITY_MD = OUT / "quality_report.md"
GATE_JSON = OUT / "quality_gate_status.json"

PLACEHOLDER_PATTERNS = [
    re.compile(r"placeholder", re.I),
    re.compile(r"todo", re.I),
    re.compile(r"tbd", re.I),
    re.compile(r"lorem", re.I),
    re.compile(r"use the enterprise qe answer framework", re.I),
]

@dataclass
class NodeAssessment:
    id: str
    title: str
    domain: str
    role: str
    difficulty: str
    score: int
    status: str
    issues: List[str]
    strengths: List[str]


def load_nodes() -> List[Dict[str, Any]]:
    if not NODES.exists():
        raise SystemExit(f"Missing {NODES}. Run scripts/generate_v4_platform_core.py first.")
    return json.loads(NODES.read_text(encoding="utf-8"))


def has_placeholder(text: str) -> bool:
    return any(p.search(text or "") for p in PLACEHOLDER_PATTERNS)


def score_node(node: Dict[str, Any]) -> NodeAssessment:
    issues: List[str] = []
    strengths: List[str] = []
    score = 100

    required = ["id", "title", "domain", "role", "difficulty", "category", "concept", "problem"]
    for field in required:
        if not str(node.get(field, "")).strip():
            score -= 8
            issues.append(f"Missing required field: {field}")

    problem = str(node.get("problem", ""))
    answer = str(node.get("model_answer", ""))
    hints = node.get("hints", []) or []
    followups = node.get("followups", []) or []
    rubric = node.get("rubric", []) or []
    evidence = node.get("evidence", []) or []
    exercise_types = node.get("exercise_types", []) or []
    skills = node.get("skills", []) or []

    if len(problem) < 120:
        score -= 8
        issues.append("Problem statement is too short for enterprise interview practice.")
    else:
        strengths.append("Enterprise-length problem statement")

    if len(answer) < 450:
        score -= 15
        issues.append("Model answer is too short; needs interview-quality depth.")
    else:
        strengths.append("Detailed model answer")

    if has_placeholder(answer):
        score -= 20
        issues.append("Model answer appears generic or placeholder-like.")

    if len(hints) < 2:
        score -= 6
        issues.append("Needs at least two progressive hints.")
    else:
        strengths.append("Progressive hints present")

    if len(followups) < 3:
        score -= 6
        issues.append("Needs at least three follow-up interview questions.")
    else:
        strengths.append("Follow-up questions present")

    total_rubric = 0
    for r in rubric:
        try:
            total_rubric += int(r.get("points", 0))
        except Exception:
            pass
    if total_rubric != 100:
        score -= 10
        issues.append(f"Rubric points total {total_rubric}, expected 100.")
    else:
        strengths.append("100-point rubric")

    if len(evidence) < 3:
        score -= 5
        issues.append("Needs stronger evidence/readiness artifacts.")
    else:
        strengths.append("Evidence expectations present")

    if not exercise_types:
        score -= 5
        issues.append("Missing exercise type classification.")
    if not skills:
        score -= 5
        issues.append("Missing skill mapping.")

    status = "pass" if score >= 85 and not any("placeholder" in x.lower() for x in issues) else "review"
    if score < 70:
        status = "fail"

    return NodeAssessment(
        id=str(node.get("id", "UNKNOWN")),
        title=str(node.get("title", "Untitled")),
        domain=str(node.get("domain", "Unknown")),
        role=str(node.get("role", "Unknown")),
        difficulty=str(node.get("difficulty", "Unknown")),
        score=max(0, min(100, score)),
        status=status,
        issues=issues,
        strengths=strengths,
    )


def counts(items: Iterable[str]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for item in items:
        out[item] = out.get(item, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))


def markdown_report(summary: Dict[str, Any], assessments: List[NodeAssessment]) -> str:
    top_issues = summary.get("top_issues", {})
    issue_lines = ["| Issue | Count |", "|---|---:|"]
    for issue, count in list(top_issues.items())[:20]:
        issue_lines.append(f"| {issue} | {count} |")

    weakest = sorted(assessments, key=lambda a: a.score)[:25]
    weak_lines = ["| Score | Status | ID | Title | Main issue |", "|---:|---|---|---|---|"]
    for a in weakest:
        main_issue = a.issues[0] if a.issues else "None"
        weak_lines.append(f"| {a.score} | {a.status} | {a.id} | {a.title} | {main_issue} |")

    return (
        "# v4 Quality Intelligence Report\n\n"
        f"- Total nodes: **{summary['total_nodes']}**\n"
        f"- Passed: **{summary['passed']}**\n"
        f"- Review: **{summary['review']}**\n"
        f"- Failed: **{summary['failed']}**\n"
        f"- Average score: **{summary['average_score']}**\n"
        f"- Quality gate: **{summary['quality_gate']}**\n\n"
        "## Top issues\n\n" + "\n".join(issue_lines) + "\n\n"
        "## Lowest-scoring nodes\n\n" + "\n".join(weak_lines) + "\n\n"
        "## Recommended next actions\n\n"
        "1. Expand model answers below 450 characters into structured, domain-specific solutions.\n"
        "2. Replace placeholder-like answers with concrete scenario evidence, edge cases, automation strategy, and production readiness.\n"
        "3. Keep the rubric total at exactly 100 for every scenario.\n"
        "4. Use this report as a GitHub Actions quality gate before publishing v4 packs.\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-average", type=int, default=75)
    parser.add_argument("--max-fail-rate", type=float, default=0.20)
    parser.add_argument("--fail-on-gate", action="store_true")
    args = parser.parse_args()

    nodes = load_nodes()
    assessments = [score_node(n) for n in nodes]
    issue_counts = counts(issue for a in assessments for issue in a.issues)
    total = len(assessments) or 1
    passed = sum(1 for a in assessments if a.status == "pass")
    review = sum(1 for a in assessments if a.status == "review")
    failed = sum(1 for a in assessments if a.status == "fail")
    average = round(sum(a.score for a in assessments) / total, 2)
    fail_rate = failed / total
    gate = "pass" if average >= args.min_average and fail_rate <= args.max_fail_rate else "fail"

    summary = {
        "total_nodes": len(assessments),
        "passed": passed,
        "review": review,
        "failed": failed,
        "average_score": average,
        "fail_rate": round(fail_rate, 4),
        "quality_gate": gate,
        "thresholds": {"min_average": args.min_average, "max_fail_rate": args.max_fail_rate},
        "top_issues": issue_counts,
    }
    payload = {"summary": summary, "assessments": [asdict(a) for a in assessments]}
    OUT.mkdir(parents=True, exist_ok=True)
    QUALITY_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    QUALITY_MD.write_text(markdown_report(summary, assessments), encoding="utf-8")
    GATE_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {QUALITY_JSON}")
    print(f"Wrote {QUALITY_MD}")
    print(f"Quality gate: {gate} | average={average} | failed={failed}/{len(assessments)}")
    if args.fail_on_gate and gate != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
