#!/usr/bin/env python3
import json
from pathlib import Path
required = {"id","title","difficulty","category","concept","domain","role","problem_statement","tags"}
ids = set()
count = 0
for line in Path("catalog/questions.jsonl").read_text(encoding="utf-8").splitlines():
    if not line.strip(): continue
    q = json.loads(line)
    count += 1
    missing = required - set(q)
    if missing: raise SystemExit(f"Missing {missing} in {q.get('id')}")
    if q["id"] in ids: raise SystemExit(f"Duplicate id: {q['id']}")
    ids.add(q["id"])
print(f"PASS: {count} catalog questions validated.")
