#!/usr/bin/env python3
"""Repository path helpers for Enterprise QE Academy scripts.

Keeps direct script execution working on Windows, GitHub Actions, and local shells.
"""
from __future__ import annotations

from pathlib import Path
import sys


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "catalog" / "questions.jsonl").exists() or (candidate / ".git").exists():
            return candidate
    return Path.cwd().resolve()


def ensure_repo_imports(start: Path | None = None) -> Path:
    root = find_repo_root(start)
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    return root
