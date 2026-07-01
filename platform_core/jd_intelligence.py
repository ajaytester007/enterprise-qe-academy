from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

SKILL_ALIASES: dict[str, list[str]] = {
    "Java": ["java", "junit", "testng", "maven", "gradle"],
    "Python": ["python", "pytest", "pandas", "fastapi", "flask"],
    "SQL": ["sql", "oracle", "sql server", "postgres", "postgresql", "mysql", "db2"],
    "API Testing": ["api", "rest", "rest assured", "postman", "newman", "soapui", "readyapi", "graphql"],
    "Playwright": ["playwright"],
    "Selenium": ["selenium", "webdriver"],
    "Cypress": ["cypress"],
    "CI/CD": ["ci/cd", "jenkins", "github actions", "gitlab", "azure devops", "pipeline"],
    "Cloud": ["aws", "azure", "gcp", "cloud", "lambda", "s3", "ec2", "cloudwatch"],
    "Snowflake": ["snowflake"],
    "Databricks": ["databricks", "spark", "pyspark"],
    "Data Quality": ["data quality", "dq", "validation", "reconciliation", "etl", "elt", "data pipeline"],
    "Performance": ["performance", "load", "jmeter", "k6", "gatling", "sla", "slo", "latency", "throughput"],
    "Security": ["security", "pii", "hipaa", "oauth", "jwt", "encryption", "masking", "privacy"],
    "Healthcare": ["healthcare", "payer", "provider", "claims", "facets", "fhir", "hl7", "edi", "hipaa"],
    "Banking": ["banking", "payments", "credit", "risk", "aml", "kyc", "iso 20022", "swift", "ach"],
    "Retail": ["retail", "ecommerce", "order management", "oms", "fulfillment", "supply chain"],
    "Leadership": ["lead", "manager", "strategy", "stakeholder", "governance", "roadmap", "mentoring", "offshore"],
    "Agile": ["agile", "scrum", "kanban", "jira", "xray", "zephyr"],
    "Architecture": ["architecture", "microservices", "event-driven", "kafka", "system design", "distributed"],
}

ROLE_LEVEL_TERMS = {
    "junior": 1,
    "qa engineer": 2,
    "senior": 3,
    "lead": 4,
    "manager": 4,
    "architect": 5,
    "principal": 5,
    "staff": 5,
}

@dataclass
class JDAnalysis:
    source: str
    role_title: str
    detected_domain: str
    seniority_level: int
    required_skills: list[str]
    preferred_skills: list[str]
    keyword_hits: dict[str, int]
    missing_from_academy: list[str]
    readiness_score: int
    readiness_band: str
    recommended_modules: list[dict[str, Any]]
    interview_focus: list[str]
    portfolio_recommendations: list[str]
    resume_talking_points: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_role_title(text: str) -> str:
    lines = [line.strip(" #-\t") for line in text.splitlines() if line.strip()]
    title_markers = ["title", "role", "position", "job"]
    for line in lines[:25]:
        low = line.lower()
        if any(marker in low for marker in title_markers) and len(line) <= 120:
            return re.sub(r"^(job|position|role|title)\s*[:\-]\s*", "", line, flags=re.I).strip()
    return lines[0][:100] if lines else "Target Role"


def detect_skills(text: str) -> tuple[list[str], dict[str, int]]:
    low = normalize(text)
    hits: dict[str, int] = {}
    for skill, aliases in SKILL_ALIASES.items():
        count = 0
        for alias in aliases:
            count += len(re.findall(r"(?<![a-z0-9])" + re.escape(alias.lower()) + r"(?![a-z0-9])", low))
        if count:
            hits[skill] = count
    ordered = sorted(hits, key=lambda s: (-hits[s], s))
    return ordered, hits


def detect_domain(skills: Iterable[str], text: str) -> str:
    domain_candidates = ["Healthcare", "Banking", "Retail"]
    scored = {d: 0 for d in domain_candidates}
    for skill in skills:
        if skill in scored:
            scored[skill] += 5
    low = normalize(text)
    for d in domain_candidates:
        for alias in SKILL_ALIASES[d]:
            scored[d] += low.count(alias.lower())
    best = max(scored, key=scored.get)
    return best if scored[best] > 0 else "Enterprise QE"


def detect_seniority(text: str) -> int:
    low = normalize(text)
    level = 2
    for term, value in ROLE_LEVEL_TERMS.items():
        if term in low:
            level = max(level, value)
    years = [int(y) for y in re.findall(r"(\d{1,2})\+?\s*(?:years|yrs)", low)]
    if years:
        max_years = max(years)
        if max_years >= 12:
            level = max(level, 5)
        elif max_years >= 8:
            level = max(level, 4)
        elif max_years >= 5:
            level = max(level, 3)
    return level


def academy_coverage(repo_root: Path) -> tuple[set[str], list[dict[str, Any]]]:
    nodes_path = repo_root / "outputs" / "v4" / "knowledge_nodes.json"
    nodes = read_json(nodes_path, default=[])
    covered: set[str] = set()
    module_rows: list[dict[str, Any]] = []
    for n in nodes or []:
        hay = " ".join(str(n.get(k, "")) for k in ["title", "domain", "role", "category", "concept", "difficulty"])
        skills, _ = detect_skills(hay)
        covered.update(skills)
        module_rows.append({
            "id": n.get("id"),
            "title": n.get("title"),
            "domain": n.get("domain"),
            "role": n.get("role"),
            "difficulty": n.get("difficulty"),
            "skills": skills,
        })
    # Also scan catalog if v4 nodes are not generated yet.
    catalog = repo_root / "catalog" / "questions.jsonl"
    if catalog.exists():
        for line in catalog.read_text(encoding="utf-8", errors="ignore").splitlines()[:20000]:
            if line.strip():
                skills, _ = detect_skills(line)
                covered.update(skills)
    return covered, module_rows


def build_recommendations(required: list[str], modules: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    scored: list[tuple[int, dict[str, Any]]] = []
    req = set(required)
    for m in modules:
        overlap = req.intersection(set(m.get("skills") or []))
        if overlap:
            scored.append((len(overlap), {**m, "matched_skills": sorted(overlap)}))
    scored.sort(key=lambda x: (-x[0], str(x[1].get("title", ""))))
    return [row for _, row in scored[:limit]]


def readiness_band(score: int) -> str:
    if score >= 85:
        return "Interview-ready"
    if score >= 70:
        return "Strong with targeted practice"
    if score >= 55:
        return "Moderate readiness"
    return "Needs focused preparation"


def analyze_jd(repo_root: Path, jd_path: Path) -> JDAnalysis:
    text = read_text(jd_path)
    role_title = extract_role_title(text)
    required, hits = detect_skills(text)
    seniority = detect_seniority(text)
    domain = detect_domain(required, text)
    academy_skills, modules = academy_coverage(repo_root)
    missing = [s for s in required if s not in academy_skills]
    covered_required = [s for s in required if s in academy_skills]
    coverage_score = int(round((len(covered_required) / max(1, len(required))) * 70))
    seniority_score = min(20, seniority * 4)
    domain_score = 10 if domain in required or domain != "Enterprise QE" else 6
    score = min(100, coverage_score + seniority_score + domain_score)

    top_required = required[:10]
    recommended = build_recommendations(top_required, modules)
    focus = [
        f"Prepare a STAR-style story demonstrating {skill} in an enterprise delivery context."
        for skill in top_required[:6]
    ]
    portfolio = [
        f"Create or refresh a GitHub demo showing {skill} test strategy, automation evidence, and CI results."
        for skill in top_required[:5]
    ]
    resume_points = [
        f"Add a quantified bullet linking {skill} to business risk reduction, quality gates, or release readiness."
        for skill in top_required[:6]
    ]

    preferred = [s for s in required if hits.get(s, 0) == 1][6:12]
    return JDAnalysis(
        source=str(jd_path),
        role_title=role_title,
        detected_domain=domain,
        seniority_level=seniority,
        required_skills=top_required,
        preferred_skills=preferred,
        keyword_hits=hits,
        missing_from_academy=missing,
        readiness_score=score,
        readiness_band=readiness_band(score),
        recommended_modules=recommended,
        interview_focus=focus,
        portfolio_recommendations=portfolio,
        resume_talking_points=resume_points,
    )


def analysis_to_markdown(analysis: JDAnalysis) -> str:
    rows = []
    for mod in analysis.recommended_modules:
        rows.append(f"| {mod.get('id','')} | {mod.get('title','')} | {', '.join(mod.get('matched_skills', []))} | {mod.get('difficulty','')} |")
    modules = "\n".join(rows) if rows else "| — | No generated v4 modules matched yet. Run the v4 platform/content builds first. | — | — |"
    return f"""# JD Readiness Analysis

## Target role

- **Role:** {analysis.role_title}
- **Detected domain:** {analysis.detected_domain}
- **Seniority level:** {analysis.seniority_level}/5
- **Readiness score:** {analysis.readiness_score}/100 — **{analysis.readiness_band}**

## Required skills detected

{chr(10).join(f'- {s} ({analysis.keyword_hits.get(s, 0)} hits)' for s in analysis.required_skills) or '- None detected'}

## Skills not yet strongly covered by academy assets

{chr(10).join(f'- {s}' for s in analysis.missing_from_academy) or '- None. Current academy coverage maps well to this JD.'}

## Recommended academy modules

| Module ID | Title | Matched skills | Difficulty |
|---|---|---|---|
{modules}

## Interview focus plan

{chr(10).join(f'- {x}' for x in analysis.interview_focus)}

## Portfolio recommendations

{chr(10).join(f'- {x}' for x in analysis.portfolio_recommendations)}

## Resume talking-point suggestions

{chr(10).join(f'- {x}' for x in analysis.resume_talking_points)}
"""


def build_dashboard(repo_root: Path, analyses: list[JDAnalysis]) -> str:
    cards = []
    for a in analyses:
        cards.append(f"""
<div class=\"card\">
  <h3>{a.role_title}</h3>
  <p><strong>{a.readiness_score}/100</strong> — {a.readiness_band}</p>
  <p>Domain: {a.detected_domain} | Seniority: {a.seniority_level}/5</p>
  <p>Top skills: {', '.join(a.required_skills[:6])}</p>
</div>
""")
    return """# v4 Readiness Dashboard

This dashboard is generated from JD Intelligence Bridge outputs.

<div class=\"grid cards\">
""" + "\n".join(cards or ["<p>No JD analyses generated yet.</p>"]) + "\n</div>\n"
