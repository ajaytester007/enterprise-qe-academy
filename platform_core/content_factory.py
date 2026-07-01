from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

PLACEHOLDER_PATTERNS = [
    "Use the Enterprise QE answer framework",
    "Design, implement, test, or whiteboard",
    "generic placeholder",
    "TBD",
    "TODO",
]

CATEGORY_PATTERNS = {
    "SECURITY_PRIVACY": {
        "focus": "data protection, least privilege, auditability, masking, encryption, retention, consent, and regulatory evidence",
        "risks": ["PII leakage", "over-permissive access", "weak audit trail", "inconsistent masking", "retention violations"],
        "evidence": ["masked data screenshots", "access-control matrix", "audit log samples", "negative authorization tests", "encryption validation evidence"],
    },
    "PERFORMANCE_RELIABILITY": {
        "focus": "SLO/SLA definition, p95/p99 latency, throughput, error budget, saturation, resiliency, failover, and recovery",
        "risks": ["latency regression", "downstream saturation", "retry storms", "capacity gaps", "unverified failover"],
        "evidence": ["load-test report", "latency percentiles", "throughput graph", "APM traces", "capacity recommendation"],
    },
    "JAVA_STRINGS": {
        "focus": "input normalization, null safety, encoding, validation rules, boundary tests, internationalization, and maintainable utilities",
        "risks": ["catastrophic regex backtracking", "locale-sensitive bugs", "null handling gaps", "incorrect trimming", "invalid unicode assumptions"],
        "evidence": ["unit-test matrix", "boundary cases", "code coverage", "static analysis", "complexity notes"],
    },
    "API_TESTING": {
        "focus": "contract validation, schema compatibility, idempotency, auth, throttling, negative tests, and observability",
        "risks": ["contract drift", "auth bypass", "poor error handling", "unsafe retries", "missing backward compatibility"],
        "evidence": ["OpenAPI contract tests", "Postman/Newman report", "negative test results", "trace IDs", "defect triage summary"],
    },
    "DATA_ENGINEERING": {
        "focus": "source-to-target validation, reconciliation, schema drift, data quality rules, lineage, and recoverability",
        "risks": ["silent data loss", "duplicate records", "late-arriving data", "schema drift", "broken lineage"],
        "evidence": ["reconciliation report", "DQ rule results", "lineage proof", "exception queue", "rerun validation"],
    },
}

DOMAIN_EXAMPLES = {
    "Banking": ["account onboarding", "payments", "customer profile", "KYC", "statement generation", "fraud-monitoring"],
    "Healthcare": ["claims", "eligibility", "FHIR APIs", "HL7 feeds", "provider directory", "clinical integration"],
    "Retail": ["order fulfillment", "inventory", "pricing", "returns", "loyalty", "store operations"],
    "Insurance": ["policy administration", "claims intake", "billing", "underwriting", "commissions"],
    "Energy": ["meter reads", "outage management", "work orders", "asset maintenance", "billing"],
}

ROLE_EXPECTATIONS = {
    "Lead Quality Engineer": "lead-level ownership, cross-team coordination, automation strategy, risk-based prioritization, and release evidence",
    "Senior QA Engineer": "hands-on test design, automation implementation, defect analysis, and CI/CD integration",
    "QA Architect": "enterprise standards, reusable frameworks, governance, observability, and multi-team enablement",
    "Test Manager": "planning, governance, stakeholder reporting, release risk, resourcing, and readiness sign-off",
}

@dataclass
class EnrichedContent:
    id: str
    title: str
    domain: str
    role: str
    difficulty: str
    category: str
    concept: str
    original_problem: str
    learning_objective: str
    assumptions: List[str]
    model_answer: str
    edge_cases: List[str]
    validation_strategy: List[str]
    evidence_expected: List[str]
    follow_up_questions: List[str]
    common_mistakes: List[str]
    coding_prompt: str
    whiteboard_prompt: str
    mermaid_diagram: str
    quality_score: int
    quality_notes: List[str]


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required catalog: {path}")
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def slug(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "item"


def get_value(row: Dict[str, Any], *names: str, default: str = "") -> str:
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip():
            return str(value).strip()
    return default


def normalize_category(category: str, concept: str) -> str:
    raw = f"{category} {concept}".upper()
    if "PII" in raw or "SEC" in raw or "PRIVACY" in raw:
        return "SECURITY_PRIVACY"
    if "PERF" in raw or "SLA" in raw or "RELIABILITY" in raw:
        return "PERFORMANCE_RELIABILITY"
    if "JAVA" in raw or "STRING" in raw or "NORMAL" in raw or "REGEX" in raw:
        return "JAVA_STRINGS"
    if "API" in raw or "REST" in raw or "CONTRACT" in raw:
        return "API_TESTING"
    if "DATA" in raw or "ETL" in raw or "SNOWFLAKE" in raw or "SQL" in raw:
        return "DATA_ENGINEERING"
    return category or "GENERAL_QE"


def category_profile(category: str) -> Dict[str, Any]:
    return CATEGORY_PATTERNS.get(category, {
        "focus": "requirements clarity, risk-based testing, automation design, observability, evidence, and production readiness",
        "risks": ["unclear scope", "missing negative tests", "weak traceability", "manual-only validation", "poor readiness evidence"],
        "evidence": ["test plan", "automation results", "defect summary", "traceability matrix", "release sign-off"],
    })


def build_model_answer(domain: str, role: str, difficulty: str, category: str, concept: str, problem: str) -> str:
    profile = category_profile(category)
    examples = DOMAIN_EXAMPLES.get(domain, ["critical enterprise workflow", "customer-facing transaction", "integration flow"])
    role_text = ROLE_EXPECTATIONS.get(role, "clear ownership of test strategy, automation, evidence, and production readiness")
    scenario = examples[0]
    return (
        f"I would start by clarifying the business workflow, data grain, upstream/downstream systems, and release risk for {concept} in a {domain} {scenario} scenario. "
        f"Because this is a {difficulty.lower()} {role} interview problem, I would show {role_text}.\n\n"
        f"My solution would focus on {profile['focus']}. I would define the acceptance criteria first, map them to testable controls, and separate validation into unit/component, API or integration, data, security, performance, and UAT evidence. "
        f"For automation, I would create reusable checks that run in CI/CD, tag tests by risk and domain, and publish results with traceable evidence.\n\n"
        f"For production readiness, I would require clear pass/fail gates, defect triage rules, rollback criteria, monitoring dashboards, log/trace correlation, and sign-off from engineering, product, security, and business stakeholders where applicable. "
        f"The key is not only proving that the happy path works, but proving that edge cases, failure behavior, auditability, and operational recovery are controlled."
    )


def build_mermaid(domain: str, category: str, concept: str) -> str:
    if category == "DATA_ENGINEERING":
        return """flowchart LR
  A[Source systems] --> B[Ingestion]
  B --> C[Validation rules]
  C --> D[Curated data]
  C --> E[Exception queue]
  D --> F[Analytics / downstream APIs]
  C --> G[Quality evidence]"""
    if category == "API_TESTING" or category == "PERFORMANCE_RELIABILITY":
        return """sequenceDiagram
  participant C as Client
  participant A as API Gateway
  participant S as Service
  participant D as Downstream
  C->>A: Request
  A->>S: Authenticated call
  S->>D: Dependency call
  D-->>S: Response / failure
  S-->>A: Contracted response
  A-->>C: Status, payload, trace id"""
    return f"""flowchart TD
  A[Requirement: {concept}] --> B[Risk analysis]
  B --> C[Test design]
  C --> D[Automation]
  D --> E[CI/CD quality gate]
  E --> F[{domain} release evidence]
  F --> G[Production readiness]"""


def enrich(row: Dict[str, Any], defaults: Dict[str, str]) -> EnrichedContent:
    qid = get_value(row, "id", "question_id", default="Q-UNKNOWN")
    domain = get_value(row, "domain", default=defaults.get("domain", "Enterprise"))
    role = get_value(row, "role", default=defaults.get("role", "Lead Quality Engineer"))
    difficulty = get_value(row, "difficulty", default=defaults.get("difficulty", "Hard"))
    concept = get_value(row, "concept", "skill", default="Enterprise QE")
    raw_category = get_value(row, "category", default="GENERAL_QE")
    category = normalize_category(raw_category, concept)
    title = get_value(row, "title", "name", default=f"{qid} — {concept} for {domain}")
    problem = get_value(row, "problem", "prompt", "question", default=f"Design a {concept} solution for {domain}.")
    profile = category_profile(category)
    risks = list(profile["risks"])
    evidence = list(profile["evidence"])
    model = build_model_answer(domain, role, difficulty, category, concept, problem)
    notes = []
    score = 100
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.lower() in model.lower() or pattern.lower() in problem.lower():
            score -= 10
            notes.append(f"Potential placeholder language detected: {pattern}")
    if len(model.split()) < 120:
        score -= 15
        notes.append("Model answer may be too short for interview coaching.")
    if not notes:
        notes.append("Generated content includes assumptions, strategy, risks, evidence, and readiness coverage.")
    return EnrichedContent(
        id=qid,
        title=title,
        domain=domain,
        role=role,
        difficulty=difficulty,
        category=category,
        concept=concept,
        original_problem=problem,
        learning_objective=f"Explain and defend a production-ready {concept} strategy for {domain} as a {role}.",
        assumptions=[
            f"The workflow is business-critical in {domain}.",
            "Requirements, expected outputs, and non-functional thresholds can be clarified with stakeholders.",
            "CI/CD, observability, and evidence retention are expected for release readiness.",
        ],
        model_answer=model,
        edge_cases=risks,
        validation_strategy=[
            "Clarify acceptance criteria and map each requirement to executable tests.",
            "Cover happy path, negative path, boundary conditions, failure modes, and regression impact.",
            "Automate repeatable checks and publish results as CI/CD quality-gate evidence.",
            "Validate observability with logs, metrics, traces, dashboards, and alert thresholds.",
            "Confirm release readiness with traceability, defect disposition, rollback criteria, and stakeholder sign-off.",
        ],
        evidence_expected=evidence,
        follow_up_questions=[
            "How would you automate this without making the suite brittle?",
            "What would you include in release-readiness evidence?",
            "How would you test failure behavior and recovery?",
            "Which risks would you escalate before go-live?",
            "How would you explain the result to a non-technical stakeholder?",
        ],
        common_mistakes=[
            "Jumping into tools before clarifying scope and risk.",
            "Only testing happy paths.",
            "Missing evidence that can survive audit or release review.",
            "Treating non-functional requirements as optional.",
            "Failing to connect automation results to business readiness.",
        ],
        coding_prompt=f"Create a small validation utility or test harness that checks {concept} rules for a {domain} workflow. Include positive, negative, null/empty, boundary, and malformed-input tests.",
        whiteboard_prompt=f"Whiteboard the {domain} flow for {concept}, including inputs, validation points, failure handling, observability, evidence, and release gates.",
        mermaid_diagram=build_mermaid(domain, category, concept),
        quality_score=max(0, min(100, score)),
        quality_notes=notes,
    )


def build_markdown(items: List[EnrichedContent], title: str) -> str:
    lines = [f"# {title}", "", f"Generated enriched content items: **{len(items)}**", ""]
    for item in items:
        lines += [
            f"## {item.id} — {item.title}", "",
            f"- Domain: {item.domain}",
            f"- Role: {item.role}",
            f"- Difficulty: {item.difficulty}",
            f"- Category: {item.category}",
            f"- Concept: {item.concept}",
            f"- Quality score: {item.quality_score}/100", "",
            "### Learning objective", "", item.learning_objective, "",
            "### Model answer", "", item.model_answer, "",
            "### Validation strategy", "",
        ]
        lines += [f"- {x}" for x in item.validation_strategy]
        lines += ["", "### Evidence expected", ""] + [f"- {x}" for x in item.evidence_expected]
        lines += ["", "### Follow-up questions", ""] + [f"- {x}" for x in item.follow_up_questions]
        lines += ["", "### Whiteboard diagram", "", "```mermaid", item.mermaid_diagram, "```", ""]
    return "\n".join(lines)


def build_content_factory(catalog_path: Path, out_dir: Path, *, domain: str, role: str, difficulty: str, limit: int) -> Dict[str, Any]:
    rows = read_jsonl(catalog_path)
    filtered = []
    for row in rows:
        row_domain = get_value(row, "domain", default=domain)
        row_role = get_value(row, "role", default=role)
        row_diff = get_value(row, "difficulty", default=difficulty)
        if domain and row_domain.lower() != domain.lower():
            continue
        if role and row_role.lower() != role.lower():
            continue
        if difficulty and row_diff.lower() != difficulty.lower():
            continue
        filtered.append(row)
    if not filtered:
        filtered = rows
    selected = filtered[:limit]
    defaults = {"domain": domain, "role": role, "difficulty": difficulty}
    enriched = [enrich(row, defaults) for row in selected]
    out_dir.mkdir(parents=True, exist_ok=True)
    dicts = [asdict(item) for item in enriched]
    write_jsonl(out_dir / "enriched_content.jsonl", dicts)
    write_json(out_dir / "enriched_content.json", dicts)
    (out_dir / "enriched_content.md").write_text(build_markdown(enriched, "Enterprise QE Academy v4 Content Factory"), encoding="utf-8")
    category_counts = Counter(item.category for item in enriched)
    domain_counts = Counter(item.domain for item in enriched)
    avg_quality = round(sum(item.quality_score for item in enriched) / max(len(enriched), 1), 2)
    report = {
        "total_catalog_rows": len(rows),
        "selected_rows": len(selected),
        "enriched_items": len(enriched),
        "average_quality_score": avg_quality,
        "category_counts": dict(category_counts),
        "domain_counts": dict(domain_counts),
        "generated_files": [
            str(out_dir / "enriched_content.jsonl"),
            str(out_dir / "enriched_content.json"),
            str(out_dir / "enriched_content.md"),
            str(out_dir / "content_factory_report.json"),
            str(out_dir / "content_factory_report.md"),
        ],
    }
    write_json(out_dir / "content_factory_report.json", report)
    report_md = ["# v4 Content Factory Report", "", f"Total catalog rows: **{len(rows)}**", f"Selected rows: **{len(selected)}**", f"Enriched items: **{len(enriched)}**", f"Average quality score: **{avg_quality}/100**", "", "## Category coverage", ""]
    report_md += [f"- {k}: {v}" for k, v in category_counts.most_common()]
    (out_dir / "content_factory_report.md").write_text("\n".join(report_md) + "\n", encoding="utf-8")
    return report
