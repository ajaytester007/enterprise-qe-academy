#!/usr/bin/env python3
"""Generate Enterprise QE Academy v4 platform-core assets.

Outputs:
- outputs/v4/knowledge_nodes.json
- outputs/v4/domain_packs/*.json
- outputs/v4/interview_simulator_config.json
- outputs/v4/coding_lab_manifest.json
- outputs/v4/whiteboard_studio_manifest.json
- outputs/v4/learning_analytics.json
- docs/docs/v4/generated/index.md
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

from platform_core.knowledge_model import build_node, group_counts, read_jsonl, write_json, write_markdown

ROOT = Path.cwd()
CATALOG = ROOT / "catalog" / "questions.jsonl"
OUT = ROOT / "outputs" / "v4"
DOCS = ROOT / "docs" / "docs" / "v4" / "generated"


def select_rows(rows: List[dict], domain: str | None, role: str | None, difficulty: str | None, limit: int) -> List[dict]:
    out = []
    for row in rows:
        if domain and str(row.get("domain", "")).lower() != domain.lower():
            continue
        if role and str(row.get("role", "")).lower() != role.lower():
            continue
        if difficulty and str(row.get("difficulty", "")).lower() != difficulty.lower():
            continue
        out.append(row)
        if limit and len(out) >= limit:
            break
    return out


def domain_pack(nodes):
    by_domain: Dict[str, list] = {}
    for n in nodes:
        by_domain.setdefault(n.domain, []).append(n)
    packs = {}
    for domain, items in sorted(by_domain.items()):
        packs[domain] = {
            "domain": domain,
            "scenario_count": len(items),
            "roles": group_counts(items, "role"),
            "difficulties": group_counts(items, "difficulty"),
            "categories": group_counts(items, "category"),
            "featured_scenarios": [n.to_dict() for n in items[:10]],
        }
    return packs


def simulator_config():
    return {
        "interviewer_profiles": [
            {"id": "friendly_lead", "name": "Friendly QE Lead", "style": "encouraging", "challenge_level": 2},
            {"id": "skeptical_architect", "name": "Skeptical QA Architect", "style": "deep technical follow-up", "challenge_level": 4},
            {"id": "hiring_manager", "name": "Hiring Manager", "style": "business outcome and delivery focus", "challenge_level": 3},
            {"id": "bar_raiser", "name": "Bar Raiser", "style": "behavioral, evidence, ambiguity", "challenge_level": 5},
        ],
        "turn_policy": [
            "Ask one question only.",
            "Wait for candidate answer.",
            "Score against rubric.",
            "Ask one clarifying follow-up.",
            "Give improvement note and next drill.",
        ],
        "adaptive_rules": {
            "score_lt_60": "downgrade difficulty and provide structured hint",
            "score_60_to_84": "keep difficulty and ask sharper follow-up",
            "score_ge_85": "upgrade difficulty or switch to architecture/coding variant",
        },
    }


def coding_lab_manifest(nodes):
    coding = [n for n in nodes if "coding" in n.exercise_types]
    return {
        "supported_languages": ["java", "python", "sql", "javascript", "typescript"],
        "execution_mode": "scaffold-first; browser/runtime integration can be added later",
        "exercise_count": len(coding),
        "starter_templates": {
            "java": "public class Solution { public static boolean validate(String input) { return input != null; } }",
            "python": "def validate(value):\n    return value is not None\n",
            "sql": "-- Write validation query here\nSELECT 1;",
            "typescript": "export function validate(value: unknown): boolean { return value !== null && value !== undefined; }",
        },
        "sample_exercises": [n.to_dict() for n in coding[:10]],
    }


def whiteboard_manifest(nodes):
    wb = [n for n in nodes if "whiteboard" in n.exercise_types]
    return {
        "diagram_types": ["system_context", "api_sequence", "data_pipeline", "database_schema", "ci_cd_flow"],
        "evaluation_dimensions": ["scalability", "reliability", "security", "testability", "observability", "data_quality"],
        "exercise_count": len(wb),
        "sample_exercises": [n.to_dict() for n in wb[:10]],
    }


def analytics(nodes):
    return {
        "total_nodes": len(nodes),
        "by_domain": group_counts(nodes, "domain"),
        "by_role": group_counts(nodes, "role"),
        "by_difficulty": group_counts(nodes, "difficulty"),
        "by_category": group_counts(nodes, "category"),
        "readiness_bands": {
            "foundation": "0-59",
            "interview_capable": "60-74",
            "strong_candidate": "75-89",
            "principal_ready": "90-100",
        },
    }


def docs_page(nodes, packs):
    lines = [
        "Enterprise QE Academy v4 generated platform core.",
        "",
        "## Generated assets",
        "",
        "- `outputs/v4/knowledge_nodes.json`",
        "- `outputs/v4/domain_packs/*.json`",
        "- `outputs/v4/interview_simulator_config.json`",
        "- `outputs/v4/coding_lab_manifest.json`",
        "- `outputs/v4/whiteboard_studio_manifest.json`",
        "- `outputs/v4/learning_analytics.json`",
        "",
        "## Coverage snapshot",
        "",
        f"- Knowledge nodes: **{len(nodes)}**",
        f"- Domain packs: **{len(packs)}**",
        "",
        "## Next build targets",
        "",
        "1. Replace scaffold model answers with curated domain-specific solutions.",
        "2. Wire the coding lab manifest to Monaco editor pages.",
        "3. Add persistent candidate progress tracking.",
        "4. Add diagram validation for whiteboard exercises.",
        "5. Connect resume/job-description gap analysis to recommended practice sessions.",
    ]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--domain")
    p.add_argument("--role")
    p.add_argument("--difficulty")
    p.add_argument("--limit", type=int, default=500, help="Limit nodes for fast local generation. Use 0 for all catalog rows.")
    args = p.parse_args()

    rows = select_rows(read_jsonl(CATALOG), args.domain, args.role, args.difficulty, args.limit)
    if not rows:
        raise SystemExit("No catalog rows matched the selected filters.")
    nodes = [build_node(row) for row in rows]
    packs = domain_pack(nodes)

    write_json(OUT / "knowledge_nodes.json", [n.to_dict() for n in nodes])
    for domain, pack in packs.items():
        safe = domain.lower().replace(" ", "_").replace("/", "_").replace("&", "and")
        write_json(OUT / "domain_packs" / f"{safe}.json", pack)
    write_json(OUT / "interview_simulator_config.json", simulator_config())
    write_json(OUT / "coding_lab_manifest.json", coding_lab_manifest(nodes))
    write_json(OUT / "whiteboard_studio_manifest.json", whiteboard_manifest(nodes))
    write_json(OUT / "learning_analytics.json", analytics(nodes))
    write_markdown(DOCS / "index.md", "Enterprise QE Academy v4 Platform Core", docs_page(nodes, packs))

    print(f"Generated {len(nodes)} v4 knowledge nodes")
    print(f"Generated {len(packs)} domain pack(s)")
    print(f"Wrote assets under: {OUT}")
    print(f"Wrote docs page: {DOCS / 'index.md'}")


if __name__ == "__main__":
    main()
