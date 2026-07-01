#!/usr/bin/env python3
"""Generate lightweight GitHub Pages markdown entry points for v4 assets."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
try:
    from platform_core.repo_paths import ensure_repo_imports
    ROOT = ensure_repo_imports(Path(__file__).resolve())
except Exception:
    ROOT = Path.cwd()

OUT = ROOT / "outputs" / "v4"
DOCS = ROOT / "docs" / "docs" / "v4"


def load(name):
    path = OUT / name
    if not path.exists():
        raise SystemExit(f"Missing {path}. Run generate_v4_platform_core.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def table(counts):
    lines = ["| Item | Count |", "|---|---:|"]
    for k, v in list(counts.items())[:25]:
        lines.append(f"| {k} | {v} |")
    return "\n".join(lines)


def main():
    analytics = load("learning_analytics.json")
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "index.md").write_text(
        "# Enterprise QE Academy v4\n\n"
        "## Platform modules\n\n"
        "- Knowledge Engine\n"
        "- Adaptive Interview Simulator\n"
        "- Coding Lab Scaffold\n"
        "- Whiteboard Studio Scaffold\n"
        "- Learning Analytics\n"
        "- Enterprise Domain Packs\n\n"
        "## Coverage by domain\n\n"
        + table(analytics["by_domain"])
        + "\n\n## Coverage by difficulty\n\n"
        + table(analytics["by_difficulty"])
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {DOCS / 'index.md'}")


if __name__ == "__main__":
    main()
