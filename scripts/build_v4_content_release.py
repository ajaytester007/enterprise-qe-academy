from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(args: list[str]) -> None:
    print("$", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="One-command v4 content factory release builder.")
    parser.add_argument("--domain", default="Banking")
    parser.add_argument("--role", default="Lead Quality Engineer")
    parser.add_argument("--difficulty", default="Hard")
    parser.add_argument("--limit", type=int, default=250)
    args = parser.parse_args()

    run([PY, "scripts/build_v4_content_factory.py", "--domain", args.domain, "--role", args.role, "--difficulty", args.difficulty, "--limit", str(args.limit)])
    run([PY, "scripts/generate_v4_content_factory_portal.py"])
    print("v4 content factory release complete")


if __name__ == "__main__":
    main()
