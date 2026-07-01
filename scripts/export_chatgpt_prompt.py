#!/usr/bin/env python3
"""Export Enterprise QE practice reports into reusable ChatGPT prompt packs.

Examples:
  python scripts/export_chatgpt_prompt.py --latest
  python scripts/export_chatgpt_prompt.py --report latest --mode all
  python scripts/export_chatgpt_prompt.py --report practice/reports/session_20260630_201441_tutor.md --mode mock
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPORT_DIR = Path("practice/reports")
DEFAULT_OUT_DIR = Path("outputs/prompts")


@dataclass(frozen=True)
class PromptMode:
    suffix: str
    title: str
    body: str


PROMPT_MODES: dict[str, PromptMode] = {
    "tutor": PromptMode(
        suffix="tutor_prompt",
        title="ChatGPT Tutor Prompt",
        body="""Act as my Enterprise Quality Engineering interview coach.

Use the practice session below. For each question:
1. Ask me to answer first.
2. Do not reveal the answer immediately.
3. Provide Hint 1 only if I ask for a clue.
4. Provide Hint 2 if I am still stuck.
5. Reveal the model answer only when I ask.
6. Score my answer out of 100 using the embedded rubric.
7. Ask follow-up interview questions.
8. Give improvement notes.

Start with Question 1 only.""",
    ),
    "mock": PromptMode(
        suffix="mock_interview_prompt",
        title="ChatGPT Mock Interview Prompt",
        body="""Act as a tough but fair Enterprise QE hiring panel interviewer.

Rules:
1. Ask one question at a time from the practice session below.
2. Do not show hints or model answers unless I explicitly ask.
3. Challenge vague answers with realistic follow-ups.
4. Evaluate scope, architecture, test strategy, automation depth, evidence, and communication.
5. Score each answer out of 100 using the embedded rubric.
6. Give a hiring recommendation after the final question: Strong Hire, Hire, Lean Hire, Lean No Hire, or No Hire.

Start with Question 1 only and wait for my answer.""",
    ),
    "coding": PromptMode(
        suffix="coding_challenge_prompt",
        title="ChatGPT Coding Challenge Prompt",
        body="""Act as my Enterprise QE coding-practice coach.

Use the practice session below to create hands-on exercises. For each question:
1. Convert the scenario into one practical coding, SQL, API, or automation challenge.
2. Ask me to solve it first.
3. Provide input/output examples and constraints.
4. Provide Hint 1 and Hint 2 only when requested.
5. Review my solution for correctness, edge cases, complexity, maintainability, and production readiness.
6. Reveal a model solution only when I ask.

Start with the first challenge only.""",
    ),
    "whiteboard": PromptMode(
        suffix="whiteboard_prompt",
        title="ChatGPT Whiteboard Interview Prompt",
        body="""Act as an Enterprise QE architecture whiteboard interviewer.

For each practice question below:
1. Ask me to draw or describe the architecture first.
2. Probe data flow, trust boundaries, test layers, CI/CD gates, observability, and failure modes.
3. Ask me to explain trade-offs and production readiness.
4. Do not reveal the model architecture until I ask.
5. Score my whiteboard answer and provide improvement notes.

Start with Question 1 only.""",
    ),
    "panel": PromptMode(
        suffix="panel_interview_prompt",
        title="ChatGPT Panel Interview Prompt",
        body="""Act as a three-person Enterprise QE interview panel: hiring manager, automation architect, and domain SME.

For each question below:
1. The hiring manager asks the main question.
2. The automation architect asks implementation and CI/CD follow-ups.
3. The domain SME asks risk, compliance, and evidence follow-ups.
4. Wait for my answer before scoring.
5. Score against the embedded rubric and summarize strengths and gaps.

Start with Question 1 only.""",
    ),
}


def newest_report(report_dir: Path = REPORT_DIR) -> Path:
    candidates = list(report_dir.glob("session_*.md"))
    if not candidates:
        raise FileNotFoundError(f"No session reports found under {report_dir}")

    def sort_key(path: Path) -> tuple[str, float]:
        match = re.search(r"session_(\d{8}_\d{6})", path.stem)
        return (match.group(1) if match else "", path.stat().st_mtime)

    return sorted(candidates, key=sort_key, reverse=True)[0]


def resolve_report(value: str | None, latest: bool) -> Path:
    if latest or value in (None, "latest", "LATEST"):
        return newest_report()
    report = Path(value)
    if report.exists():
        return report

    # Friendly fallback: allow users to pass only a timestamp or session id.
    raw = value.replace("\\", "/")
    token = Path(raw).stem
    patterns = []
    if re.fullmatch(r"\d{8}_\d{6}", token):
        patterns = [f"session_{token}*.md"]
    elif token.startswith("session_"):
        patterns = [f"{token}*.md"]
    for pattern in patterns:
        matches = sorted(REPORT_DIR.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        if matches:
            return matches[0]

    available = "\n".join(f"  - {p}" for p in sorted(REPORT_DIR.glob("session_*.md"))[-10:])
    raise FileNotFoundError(
        f"Report not found: {value}\n\nAvailable recent reports:\n{available or '  <none>'}\n\n"
        "Tip: use --latest or --report latest to export the newest report automatically."
    )


def session_slug(report: Path) -> str:
    stem = report.stem
    return stem[:-6] if stem.endswith("_tutor") else stem


def build_prompt(mode: PromptMode, report_text: str) -> str:
    return f"""# {mode.title}

{mode.body}

---

{report_text.rstrip()}
"""


def selected_modes(mode: str) -> Iterable[str]:
    return PROMPT_MODES.keys() if mode == "all" else [mode]


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a practice report as ChatGPT-ready prompt templates.")
    parser.add_argument("--report", help="Path, timestamp, session id, or 'latest'.")
    parser.add_argument("--latest", action="store_true", help="Export the newest report under practice/reports.")
    parser.add_argument("--mode", choices=[*PROMPT_MODES.keys(), "all"], default="tutor")
    parser.add_argument("--out", help="Output file path. Valid only when exporting one mode.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Output directory for generated prompts.")
    args = parser.parse_args()

    report = resolve_report(args.report, args.latest)
    report_text = report.read_text(encoding="utf-8")
    slug = session_slug(report)
    modes = list(selected_modes(args.mode))

    if args.out and len(modes) > 1:
        raise SystemExit("--out can only be used with a single --mode. Use --out-dir with --mode all.")

    written: list[Path] = []
    for mode_name in modes:
        mode = PROMPT_MODES[mode_name]
        out = Path(args.out) if args.out else Path(args.out_dir) / f"{slug}_{mode.suffix}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_prompt(mode, report_text), encoding="utf-8")
        written.append(out)

    print(f"Source report: {report}")
    for out in written:
        print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
