#!/usr/bin/env python3
"""One-command Enterprise QE practice pipeline.

Creates a tutor session, exports ChatGPT prompt modes, and optionally creates an
interview pack from the same filters.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    print("$ " + " ".join(cmd))
    completed = subprocess.run(cmd, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip(), file=sys.stderr)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed.stdout


def find_created_report(output: str) -> Path:
    for line in output.splitlines():
        if "Created tutor report:" in line:
            return Path(line.split("Created tutor report:", 1)[1].strip())
    raise SystemExit("Could not find created tutor report in start_practice_session output.")


def main() -> None:
    p = argparse.ArgumentParser(description="Run practice session + prompt export + optional interview pack in one command.")
    p.add_argument("--domain")
    p.add_argument("--role", default="Lead Quality Engineer")
    p.add_argument("--difficulty")
    p.add_argument("--category")
    p.add_argument("--keyword")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--mode", choices=["questions", "hints", "solutions", "tutor"], default="tutor")
    p.add_argument("--prompt-mode", choices=["tutor", "mock", "coding", "whiteboard", "panel", "all"], default="all")
    p.add_argument("--include-pack", action="store_true", help="Also generate outputs/interview_pack_pipeline.md")
    p.add_argument("--include-solutions", action="store_true", help="Include model answers in the generated interview pack.")
    args = p.parse_args()

    start_cmd = [sys.executable, "scripts/start_practice_session.py", "--count", str(args.count), "--seed", str(args.seed), "--mode", args.mode]
    for flag in ("domain", "role", "difficulty", "category", "keyword"):
        value = getattr(args, flag)
        if value:
            start_cmd += [f"--{flag}", value]

    start_output = run(start_cmd)
    report = find_created_report(start_output)

    export_cmd = [sys.executable, "scripts/export_chatgpt_prompt.py", "--report", str(report), "--mode", args.prompt_mode]
    run(export_cmd)

    if args.include_pack:
        pack_cmd = [sys.executable, "scripts/generate_interview_pack.py", "--role", args.role, "--count", str(args.count), "--seed", str(args.seed), "--out", "outputs/interview_pack_pipeline.md"]
        for flag in ("domain", "difficulty", "category"):
            value = getattr(args, flag)
            if value:
                pack_cmd += [f"--{flag}", value]
        if args.include_solutions:
            pack_cmd.append("--include-solutions")
        run(pack_cmd)

    print("\nDone. Review outputs/prompts/ and outputs/interview_pack_pipeline.md if generated.")


if __name__ == "__main__":
    main()
