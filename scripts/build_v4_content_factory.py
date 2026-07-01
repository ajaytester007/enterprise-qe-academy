from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from platform_core.content_factory import build_content_factory


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Enterprise QE Academy v4 enriched content factory outputs.")
    parser.add_argument("--domain", default="Banking")
    parser.add_argument("--role", default="Lead Quality Engineer")
    parser.add_argument("--difficulty", default="Hard")
    parser.add_argument("--limit", type=int, default=250)
    parser.add_argument("--catalog", default="catalog/questions.jsonl")
    parser.add_argument("--out", default="outputs/v4/content_factory")
    args = parser.parse_args()

    report = build_content_factory(
        ROOT / args.catalog,
        ROOT / args.out,
        domain=args.domain,
        role=args.role,
        difficulty=args.difficulty,
        limit=args.limit,
    )
    print("Content Factory complete")
    print(f"Enriched items: {report['enriched_items']}")
    print(f"Average quality score: {report['average_quality_score']}/100")
    print(f"Output: {ROOT / args.out}")


if __name__ == "__main__":
    main()
