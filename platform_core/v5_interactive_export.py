from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "questions.jsonl"
OUT = ROOT / "outputs" / "v5" / "site" / "data" / "questions.json"
DOCS_OUT = ROOT / "docs" / "v5" / "data" / "questions.json"


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _first(*values: Any, default: str = "") -> str:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return default


def normalize(row: dict[str, Any], index: int) -> dict[str, Any]:
    concept = _first(row.get("concept"), row.get("skill"), row.get("category"), default="Enterprise QE")
    domain = _first(row.get("domain"), row.get("industry"), default="General")
    role = _first(row.get("role"), default="Quality Engineer")
    difficulty = _first(row.get("difficulty"), default="Medium")
    qid = _first(row.get("id"), default=f"Q-{index+1:05d}")
    title = _first(row.get("title"), row.get("name"), default=f"{concept} for {domain} interview readiness")
    problem = _first(
        row.get("problem"),
        row.get("prompt"),
        row.get("question"),
        row.get("description"),
        default=f"Design, implement, test, or whiteboard a {difficulty.lower()} solution involving {concept} for {domain}. Explain assumptions, edge cases, validation strategy, quality risks, evidence expected, complexity, and production-readiness considerations.",
    )
    model_answer = _first(
        row.get("model_answer"),
        row.get("answer"),
        row.get("solution"),
        default=(
            f"A strong answer for {concept} in {domain} starts by clarifying business scope, data/application boundaries, risk, and success criteria. "
            "Then define the technical approach, automation strategy, edge cases, observability, CI/CD quality gates, and production-readiness evidence. "
            "Close with residual risks, rollback/monitoring plan, and stakeholder sign-off evidence."
        ),
    )
    return {
        "id": qid,
        "title": title,
        "domain": domain,
        "role": role,
        "difficulty": difficulty,
        "category": _first(row.get("category"), row.get("category_name"), default="GENERAL"),
        "concept": concept,
        "problem": problem,
        "hint1": _first(row.get("hint1"), default=f"Clarify scope, business grain, inputs, outputs, dependencies, and risk for {concept} in {domain}."),
        "hint2": _first(row.get("hint2"), default="Structure the answer using approach, edge cases, validation strategy, evidence, CI/CD readiness, and follow-up risks."),
        "model_answer": model_answer,
        "followups": row.get("followups") or row.get("follow_up_questions") or [
            "How would you automate this?",
            "How would you prove readiness?",
            "What risks remain?",
        ],
    }


def export_questions(limit: int = 5000) -> Path:
    rows = _load_jsonl(CATALOG)
    normalized = [normalize(row, i) for i, row in enumerate(rows[:limit])]
    if not normalized:
        normalized = [normalize({}, 0)]
    for path in [OUT, DOCS_OUT]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
    return OUT
