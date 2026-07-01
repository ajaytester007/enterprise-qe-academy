#!/usr/bin/env python3
import argparse
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Export a practice report as a ChatGPT prompt template.")
    p.add_argument("--report", required=True)
    p.add_argument("--out", default="outputs/chatgpt_practice_prompt.md")
    args = p.parse_args()

    report = Path(args.report)
    content = report.read_text(encoding="utf-8")
    prompt = f"""# ChatGPT Tutor Prompt

Act as my Enterprise Quality Engineering interview coach.

Use the practice session below. For each question:
1. Ask me to answer first.
2. Do not reveal the answer immediately.
3. Provide Hint 1 if I ask for a clue.
4. Provide Hint 2 if I am still stuck.
5. Reveal the model answer only when I ask.
6. Score my answer out of 100 using the embedded rubric.
7. Ask follow-up interview questions.
8. Give improvement notes.

Start with Question 1 only.

---

{content}
"""
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prompt, encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
