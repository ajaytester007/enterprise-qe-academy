from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = DOCS / "site"
RAW_V5 = ROOT / "docs" / "v5"
WORKTREE = ROOT / "_gh_pages_deploy"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


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
    parser = argparse.ArgumentParser(description="Deploy cleaned v5 app to gh-pages without v5/v5 nesting.")
    parser.add_argument("--message", default="Deploy v5 interview session engine", help="Commit message for gh-pages.")
    parser.add_argument("--skip-build", action="store_true", help="Skip mkdocs build if docs/site already exists.")
    args = parser.parse_args()

    if not args.skip_build:
        if SITE.exists():
            shutil.rmtree(SITE)
        run(["mkdocs", "build"], cwd=DOCS)

    target_v5 = SITE / "v5"
    if target_v5.exists():
        shutil.rmtree(target_v5)
    target_v5.mkdir(parents=True, exist_ok=True)
    copytree_contents(RAW_V5, target_v5)

    if WORKTREE.exists():
        shutil.rmtree(WORKTREE)
    run(["git", "fetch", "origin", "gh-pages"], cwd=ROOT)
    run(["git", "worktree", "add", "-B", "gh-pages", str(WORKTREE), "origin/gh-pages"], cwd=ROOT)

    for child in WORKTREE.iterdir():
        if child.name != ".git":
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    copytree_contents(SITE, WORKTREE)
    (WORKTREE / ".nojekyll").write_text("", encoding="utf-8")
    run(["git", "add", "-A"], cwd=WORKTREE)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=WORKTREE, text=True, capture_output=True, check=True).stdout.strip()
    if status:
        run(["git", "commit", "-m", args.message], cwd=WORKTREE)
        run(["git", "push", "origin", "gh-pages"], cwd=WORKTREE)
    else:
        print("No gh-pages changes to deploy.")
    run(["git", "worktree", "remove", str(WORKTREE)], cwd=ROOT)
    print("Deployment complete. Verify: git ls-tree -r origin/gh-pages --name-only | Select-String \"v5\"")


if __name__ == "__main__":
    main()
