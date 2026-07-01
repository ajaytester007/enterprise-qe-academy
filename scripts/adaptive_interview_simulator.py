#!/usr/bin/env python3
"""Local adaptive interview simulator for generated v4 knowledge nodes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

NODES = Path("outputs/v4/knowledge_nodes.json")


def load_nodes():
    if not NODES.exists():
        raise SystemExit("Missing outputs/v4/knowledge_nodes.json. Run scripts/generate_v4_platform_core.py first.")
    return json.loads(NODES.read_text(encoding="utf-8"))


def score_answer(answer: str) -> tuple[int, list[str]]:
    text = answer.lower()
    signals = {
        "scope/assumptions": ["scope", "assumption", "constraint", "requirement"],
        "technical approach": ["design", "approach", "architecture", "implementation"],
        "testing": ["test", "validation", "automation", "regression"],
        "edge cases": ["edge", "negative", "boundary", "failure", "risk"],
        "evidence": ["evidence", "report", "metric", "log", "trace", "dashboard"],
        "readiness": ["production", "ready", "monitor", "rollback", "ci/cd", "pipeline"],
    }
    points = 0
    notes = []
    for label, words in signals.items():
        hit = any(w in text for w in words)
        points += 15 if hit else 0
        if not hit:
            notes.append(f"Add more detail on {label}.")
    length_bonus = min(10, max(0, len(answer.split()) // 20))
    points = min(100, points + length_bonus)
    return points, notes or ["Strong structure. Add specific tools, evidence, and tradeoffs to push toward principal-level depth."]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=int, default=0)
    args = p.parse_args()
    nodes = load_nodes()
    node = nodes[min(args.index, len(nodes)-1)]
    print(f"\nInterviewer: {node['title']}\n")
    print(node["problem"])
    print("\nAnswer below. Finish by pressing Enter twice.\n")
    chunks = []
    while True:
        line = input()
        if not line:
            break
        chunks.append(line)
    answer = "\n".join(chunks)
    score, notes = score_answer(answer)
    print(f"\nScore: {score}/100")
    print("\nFeedback:")
    for note in notes:
        print(f"- {note}")
    print("\nFollow-up:")
    print(node["followups"][0] if node.get("followups") else "How would you improve this design?")


if __name__ == "__main__":
    main()
