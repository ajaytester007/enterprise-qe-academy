"""Builds the static v5 interactive platform for GitHub Pages."""
from __future__ import annotations

from pathlib import Path
import json
import shutil
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "v5" / "site"
WEBAPP = ROOT / "webapp" / "v5"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def collect_platform_data() -> dict[str, Any]:
    v4 = ROOT / "outputs" / "v4"
    data = {
        "readinessDashboard": read_json(v4 / "readiness_dashboard.json", {}),
        "learningAnalytics": read_json(v4 / "learning_analytics.json", {}),
        "qualityReport": read_json(v4 / "quality_report.json", {}),
        "knowledgeNodes": read_json(v4 / "knowledge_nodes.json", []),
        "generatedAt": "static-build",
    }
    jd_dir = v4 / "jd_readiness"
    data["jdReadiness"] = []
    if jd_dir.exists():
        for path in sorted(jd_dir.glob("*_analysis.json")):
            data["jdReadiness"].append(read_json(path, {}))
    return data


def build_site() -> Path:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    for path in WEBAPP.rglob("*"):
        if path.is_file():
            target = OUT / path.relative_to(WEBAPP)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

    data = collect_platform_data()
    (OUT / "data").mkdir(exist_ok=True)
    (OUT / "data" / "platform-data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    return OUT
