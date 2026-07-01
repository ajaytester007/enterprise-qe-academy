#!/usr/bin/env python3
"""Structured v4 knowledge model for Enterprise QE Academy.

This module intentionally uses only the Python standard library so it works in
GitHub Actions and on a clean local checkout without extra installs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List
import json


@dataclass
class RubricDimension:
    name: str
    points: int
    description: str


@dataclass
class KnowledgeNode:
    id: str
    title: str
    domain: str
    role: str
    difficulty: str
    category: str
    concept: str
    problem: str
    skills: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    exercise_types: List[str] = field(default_factory=list)
    model_answer: str = ""
    hints: List[str] = field(default_factory=list)
    followups: List[str] = field(default_factory=list)
    rubric: List[RubricDimension] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["rubric"] = [asdict(r) for r in self.rubric]
        return data


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required catalog file: {path}")
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def default_rubric() -> List[RubricDimension]:
    return [
        RubricDimension("Problem understanding", 15, "Clarifies scope, business context, constraints, and assumptions."),
        RubricDimension("Technical approach", 20, "Presents a realistic design or implementation approach."),
        RubricDimension("Edge cases and risks", 15, "Covers failure modes, boundary cases, negative scenarios, and quality risks."),
        RubricDimension("Testing strategy", 20, "Defines unit, API, integration, data, performance, security, and regression validation."),
        RubricDimension("Evidence and observability", 10, "Explains logs, metrics, traces, reports, screenshots, test evidence, and readiness signals."),
        RubricDimension("Communication", 20, "Gives a structured answer suitable for a lead or architect interview."),
    ]


def infer_skills(row: Dict[str, Any]) -> List[str]:
    text = " ".join(str(row.get(k, "")) for k in ["title", "category", "concept", "problem_statement"]).lower()
    skills: List[str] = []
    candidates = {
        "API": ["api", "rest", "graphql"],
        "Security": ["security", "pii", "privacy", "auth", "token"],
        "Performance": ["performance", "sla", "latency", "throughput"],
        "Data Quality": ["data", "etl", "snowflake", "databricks", "validation"],
        "Automation": ["automation", "selenium", "playwright", "cypress"],
        "Java": ["java", "regex", "string", "normalization"],
        "CI/CD": ["ci/cd", "pipeline", "quality gate", "github actions", "jenkins"],
        "Architecture": ["architecture", "design", "whiteboard", "system"],
    }
    for skill, needles in candidates.items():
        if any(n in text for n in needles):
            skills.append(skill)
    return skills or [str(row.get("category", "General QE"))]


def build_model_answer(row: Dict[str, Any]) -> str:
    concept = row.get("concept", "quality engineering")
    domain = row.get("domain", "enterprise")
    role = row.get("role", "Quality Engineer")
    return (
        f"For {concept} in a {domain} context, I would first clarify the business workflow, data grain, "
        f"systems involved, regulatory or operational risk, and the exact acceptance criteria expected from a {role}. "
        "I would then design the validation approach across happy path, negative path, boundary conditions, integration points, "
        "data integrity, security/privacy, performance, and operational readiness. The automation strategy would separate fast checks "
        "for pull requests from deeper regression, data reconciliation, and non-functional suites that run on schedule or before release. "
        "Evidence would include executable test results, traceable requirements coverage, defect triage notes, logs, metrics, dashboards, "
        "API payload samples, database reconciliation results, and a go/no-go summary. Production readiness would require monitoring, "
        "rollback criteria, alert thresholds, test data controls, access controls, and support handoff."
    )


def build_node(row: Dict[str, Any]) -> KnowledgeNode:
    skills = infer_skills(row)
    concept = str(row.get("concept", "Enterprise QE"))
    domain = str(row.get("domain", "General"))
    return KnowledgeNode(
        id=str(row.get("id", "UNKNOWN")),
        title=str(row.get("title", "Untitled scenario")),
        domain=domain,
        role=str(row.get("role", "Quality Engineer")),
        difficulty=str(row.get("difficulty", "Medium")),
        category=str(row.get("category", "GENERAL")),
        concept=concept,
        problem=str(row.get("problem_statement", row.get("title", ""))),
        skills=skills,
        prerequisites=["Enterprise QA fundamentals", "Requirements analysis", "Test strategy", "Defect lifecycle"],
        tags=sorted(set([domain, concept, str(row.get("category", "GENERAL"))] + skills)),
        exercise_types=["interview", "whiteboard"] + (["coding"] if any(s in skills for s in ["Java", "Data Quality", "API"]) else []),
        model_answer=build_model_answer(row),
        hints=[
            f"Start by clarifying scope, systems, data, and risk for {concept} in {domain}.",
            "Use a structure: assumptions, approach, validation, edge cases, evidence, readiness, risks.",
        ],
        followups=[
            "How would you automate this in CI/CD?",
            "What evidence proves the release is ready?",
            "Which production risks remain after testing?",
            "How would you explain this to a business stakeholder?",
        ],
        rubric=default_rubric(),
        evidence=["Allure or HTML report", "CI run link", "Traceability matrix", "Defect summary", "Go/no-go notes"],
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")


def group_counts(nodes: Iterable[KnowledgeNode], attr: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for n in nodes:
        key = str(getattr(n, attr))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
