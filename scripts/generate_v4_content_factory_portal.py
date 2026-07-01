from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "outputs/v4/content_factory/content_factory_report.json"
CONTENT = ROOT / "outputs/v4/content_factory/enriched_content.json"
DOC = ROOT / "docs/docs/v4/content-factory.md"


def main() -> None:
    if not REPORT.exists() or not CONTENT.exists():
        raise SystemExit("Missing content factory outputs. Run scripts/build_v4_content_factory.py first.")
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    rows = json.loads(CONTENT.read_text(encoding="utf-8"))
    DOC.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# v4 Content Factory",
        "",
        "The Content Factory enriches catalog questions with stronger model answers, validation strategy, evidence expectations, coding prompts, whiteboard prompts, and Mermaid diagrams.",
        "",
        "## Summary",
        "",
        f"- Enriched items: **{report['enriched_items']}**",
        f"- Average quality score: **{report['average_quality_score']}/100**",
        f"- Selected rows: **{report['selected_rows']}**",
        "",
        "## Category coverage",
        "",
    ]
    for category, count in sorted(report.get("category_counts", {}).items()):
        lines.append(f"- **{category}**: {count}")
    lines += ["", "## Sample enriched content", ""]
    for row in rows[:10]:
        lines += [
            f"### {row['id']} — {row['title']}",
            "",
            f"- Domain: {row['domain']}",
            f"- Role: {row['role']}",
            f"- Difficulty: {row['difficulty']}",
            f"- Quality score: {row['quality_score']}/100",
            "",
            row["learning_objective"],
            "",
            "#### Model answer excerpt",
            "",
            row["model_answer"][:900] + ("..." if len(row["model_answer"]) > 900 else ""),
            "",
            "#### Diagram",
            "",
            "```mermaid",
            row["mermaid_diagram"],
            "```",
            "",
        ]
    DOC.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {DOC}")


if __name__ == "__main__":
    main()
