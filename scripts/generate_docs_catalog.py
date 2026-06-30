#!/usr/bin/env python3
"""
Generate browsable MkDocs pages from catalog/questions.jsonl.

Run from repo root:
  python scripts/generate_docs_catalog.py
"""
import json
from collections import defaultdict
from pathlib import Path

CATALOG = Path("catalog/questions.jsonl")
DOCS = Path("docs/docs")
QUESTION_DIR = DOCS / "questions" / "generated"
CATALOG_DIR = DOCS / "catalog"

def load_questions():
    return [json.loads(line) for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")

def question_page(q):
    outline = "\n".join([f"- {x}" for x in q.get("solution_outline", [])])
    tags = ", ".join(q.get("tags", []))
    return f"""# {q['id']} — {q['title']}

## Metadata

| Field | Value |
|---|---|
| Difficulty | {q['difficulty']} |
| Category | {q['category']} |
| Concept | {q['concept']} |
| Domain | {q['domain']} |
| Role | {q['role']} |
| Context | {q.get('context', '')} |
| Tags | {tags} |

## Problem Statement

{q['problem_statement']}

## Clarifying Questions

- What are the expected input and output formats?
- What data volume, performance, or reliability constraints matter?
- What should happen for null, empty, duplicate, malformed, or boundary inputs?
- What evidence is required for release readiness?

## Solution Strategy

{outline}

## Testing Strategy

- Positive path validation
- Negative and boundary testing
- Data-driven test coverage
- Regression test automation
- Evidence capture through terminal, reports, logs, or CI output

## Whiteboard Explanation

Explain the business flow, the technical validation point, the selected test or algorithm strategy, and the production risk being reduced.

## Interview Follow-ups

- How would you automate this?
- How would you scale it?
- How would you debug failures?
- How would you capture evidence?
- How would this change in a cloud or microservices environment?
"""

def grouped_index(title, groups, description):
    lines = [f"# {title}", "", description, ""]
    for group_name in sorted(groups):
        qs = groups[group_name]
        lines += [f"## {group_name}", "", f"Count: **{len(qs)}**", ""]
        for q in qs[:100]:
            lines.append(f"- [{q['id']} — {q['title']}](../questions/generated/{q['id']}/)")
        if len(qs) > 100:
            lines.append(f"- ... {len(qs)-100} more. Use site search or CLI catalog search.")
        lines.append("")
    return "\n".join(lines)

def main():
    questions = load_questions()
    by_category, by_domain, by_difficulty, by_role = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)

    for q in questions:
        write(QUESTION_DIR / f"{q['id']}.md", question_page(q))
        by_category[q["category"]].append(q)
        by_domain[q["domain"]].append(q)
        by_difficulty[q["difficulty"]].append(q)
        by_role[q["role"]].append(q)

    write(CATALOG_DIR / "index.md", f"""# Catalog Browser

The academy currently contains **{len(questions):,}** generated question pages.

Use these browser pages:

- [Browse by Category](by-category.md)
- [Browse by Domain](by-domain.md)
- [Browse by Difficulty](by-difficulty.md)
- [Browse by Role](by-role.md)

## CLI Search

```powershell
python scripts\\search_catalog.py --keyword masking --limit 10
python scripts\\search_catalog.py --category SQL_DATA_VALIDATION --difficulty Hard --limit 20
python scripts\\search_catalog.py --domain Banking --role "Lead Quality Engineer"
```
""")

    write(CATALOG_DIR / "by-category.md", grouped_index("Browse by Category", by_category, "Questions grouped by technical category."))
    write(CATALOG_DIR / "by-domain.md", grouped_index("Browse by Domain", by_domain, "Questions grouped by enterprise domain."))
    write(CATALOG_DIR / "by-difficulty.md", grouped_index("Browse by Difficulty", by_difficulty, "Questions grouped by difficulty level."))
    write(CATALOG_DIR / "by-role.md", grouped_index("Browse by Role", by_role, "Questions grouped by target role."))

    print(f"Generated {len(questions):,} question pages.")
    print(f"Wrote catalog browser under {CATALOG_DIR}")

if __name__ == "__main__":
    main()
