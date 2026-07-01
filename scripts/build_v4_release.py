#!/usr/bin/env python3
"""One-command v4 release builder.

Runs platform-core generation, portal generation, quality assessment, and quality dashboard generation.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args):
    print("$", " ".join(args))
    subprocess.check_call(args, cwd=ROOT)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--domain", default="Banking")
    p.add_argument("--role", default="Lead Quality Engineer")
    p.add_argument("--difficulty", default="Hard")
    p.add_argument("--limit", type=int, default=250)
    p.add_argument("--fail-on-gate", action="store_true")
    args = p.parse_args()

    py = sys.executable
    run([py, "scripts/generate_v4_platform_core.py", "--domain", args.domain, "--role", args.role, "--difficulty", args.difficulty, "--limit", str(args.limit)])
    run([py, "scripts/generate_v4_portal_pages.py"])
    assess = [py, "scripts/assess_v4_quality.py"]
    if args.fail_on_gate:
        assess.append("--fail-on-gate")
    run(assess)
    run([py, "scripts/generate_v4_quality_dashboard.py"])
    print("v4 release build complete.")


if __name__ == "__main__":
    main()
