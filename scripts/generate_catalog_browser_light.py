#!/usr/bin/env python3
"""
Generate lightweight MkDocs catalog browser pages from catalog/questions.jsonl.

This intentionally does NOT generate one markdown page per question.
It keeps the 10,000+ catalog as data while giving MkDocs lightweight browse pages.

Run from repo root:
  python scripts/generate_catalog_browser_light.py
"""
import json
from collections import defaultdict
from pathlib import Path

CATALOG = Path("catalog/questions.jsonl")
OUT = Path("docs/docs/catalog")
MAX_PER_GROUP = 150

def load_questions():
    return [json.loads(line) for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")

def row(q):
    return f"| `{q['id']}` | {q['difficulty']} | {q['category']} | {q['domain']} | {q['role']} | {q['title']} |"

def grouped_page(title, groups, description):
    lines = [f"# {title}", "", description, ""]
    for name in sorted(groups):
        qs = groups[name]
        lines += [
            f"## {name}",
            "",
            f"Total catalog records: **{len(qs)}**",
            "",
            "| ID | Difficulty | Category | Domain | Role | Title |",
            "|---|---|---|---|---|---|"
        ]
        for q in qs[:MAX_PER_GROUP]:
            lines.append(row(q))
        if len(qs) > MAX_PER_GROUP:
            lines += [
                "",
                f"Showing first {MAX_PER_GROUP}. Use CLI search for the full set:",
                "",
                "```powershell",
                f"python scripts\\search_catalog.py --keyword \"{name}\" --limit 50",
                "```",
            ]
        lines.append("")
    return "\n".join(lines)

def main():
    questions = load_questions()
    OUT.mkdir(parents=True, exist_ok=True)

    by_category = defaultdict(list)
    by_domain = defaultdict(list)
    by_difficulty = defaultdict(list)
    by_role = defaultdict(list)

    for q in questions:
        by_category[q["category"]].append(q)
        by_domain[q["domain"]].append(q)
        by_difficulty[q["difficulty"]].append(q)
        by_role[q["role"]].append(q)

    write(OUT / "index.md", f"""# Catalog Browser

The academy currently contains **{len(questions):,}** catalog records.

The full question database lives in:

```text
catalog/questions.jsonl
catalog/questions.csv
```

This MkDocs site intentionally uses lightweight catalog browse pages instead of generating one HTML page per question. That keeps the site fast and prevents local disk/build overload.

## Browse

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

## Generate Practice Set

```powershell
python scripts\\generate_practice_set.py --count 25 --difficulty Hard --domain Banking
```
""")

    write(OUT / "by-category.md", grouped_page("Browse by Category", by_category, "Lightweight browse view grouped by technical category."))
    write(OUT / "by-domain.md", grouped_page("Browse by Domain", by_domain, "Lightweight browse view grouped by enterprise domain."))
    write(OUT / "by-difficulty.md", grouped_page("Browse by Difficulty", by_difficulty, "Lightweight browse view grouped by difficulty."))
    write(OUT / "by-role.md", grouped_page("Browse by Role", by_role, "Lightweight browse view grouped by target role."))

    print(f"Generated lightweight catalog browser for {len(questions):,} records.")
    print(f"Wrote files under {OUT}")

if __name__ == "__main__":
    main()
