#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def iter_catalog(path):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            yield json.loads(line)

def main():
    p = argparse.ArgumentParser(description="Search Enterprise QE Academy question catalog.")
    p.add_argument("--catalog", default="catalog/questions.jsonl")
    p.add_argument("--keyword")
    p.add_argument("--category")
    p.add_argument("--difficulty")
    p.add_argument("--domain")
    p.add_argument("--role")
    p.add_argument("--limit", type=int, default=25)
    args = p.parse_args()

    hits = []
    for q in iter_catalog(args.catalog):
        blob = json.dumps(q).lower()
        if args.keyword and args.keyword.lower() not in blob: continue
        if args.category and q["category"] != args.category: continue
        if args.difficulty and q["difficulty"] != args.difficulty: continue
        if args.domain and q["domain"].lower() != args.domain.lower(): continue
        if args.role and q["role"].lower() != args.role.lower(): continue
        hits.append(q)
        if len(hits) >= args.limit: break

    for q in hits:
        print(f'{q["id"]} | {q["difficulty"]} | {q["category"]} | {q["domain"]} | {q["role"]}')
        print(f'  {q["title"]}')
        print(f'  {q["problem_statement"]}')
        print()
    print(f"Returned {len(hits)} result(s).")

if __name__ == "__main__":
    main()
