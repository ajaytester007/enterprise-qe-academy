from __future__ import annotations
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEBAPP = ROOT / "webapp" / "v5"
SITE = ROOT / "outputs" / "v5" / "site"
DOCS_APP = ROOT / "docs" / "v5"
MKDOCS_PAGE = ROOT / "docs" / "docs" / "v5" / "interview-engine.md"


def copytree_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Enterprise QE Academy v5 Interview Session Engine 2.0.")
    parser.add_argument("--limit", type=int, default=5000, help="Maximum catalog questions to export.")
    args = parser.parse_args()

    if SITE.exists():
        shutil.rmtree(SITE)
    shutil.copytree(WEBAPP, SITE)

    from platform_core.v5_interactive_export import export_questions
    data_path = export_questions(limit=args.limit)

    if DOCS_APP.exists():
        shutil.rmtree(DOCS_APP)
    shutil.copytree(SITE, DOCS_APP)

    MKDOCS_PAGE.parent.mkdir(parents=True, exist_ok=True)
    MKDOCS_PAGE.write_text("""# v5 Interview Session Engine 2.0

The v5 interview engine runs as a static GitHub Pages browser app.

## Features

- One-question-at-a-time mock interview flow.
- Domain, role, difficulty, keyword, session-size, and shuffle controls.
- Answer capture with local autosave.
- Hint 1, Hint 2, model answer, follow-up questions, and self-critique checklist.
- 100-point Enterprise QE scoring rubric.
- Question navigation and mark-for-review.
- Timer, progress metrics, readiness label, and completion summary.
- Copy-to-ChatGPT interviewer prompt.
- Exportable Markdown session summary.

## Live path

`/enterprise-qe-academy/v5/`

## Build command

```powershell
python .\\scripts\\build_v5_interview_engine.py --limit 5000
```
""", encoding="utf-8")

    print(f"Built v5 interview app: {SITE}")
    print(f"Copied deploy-ready app to: {DOCS_APP}")
    print(f"Exported catalog data: {data_path}")
    print(f"MkDocs page: {MKDOCS_PAGE}")


if __name__ == "__main__":
    main()
