from __future__ import annotations

import argparse
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from platform_core.jd_intelligence import analyze_jd, analysis_to_markdown, build_dashboard, write_json, write_markdown

SAMPLE_JD = """# Lead Quality Engineer - Banking API and Data Platforms

We need a Lead Quality Engineer with 10+ years of experience in banking, API testing, SQL, Java or Python automation, CI/CD, security and PII controls, performance/SLA validation, and enterprise data quality. Experience with Snowflake, Databricks, Postman, RestAssured, Playwright or Selenium, GitHub Actions/Jenkins, and Agile delivery is preferred. The role requires stakeholder leadership, release readiness reporting, risk-based testing, and production-quality evidence.
"""

def ensure_sample_jd() -> Path:
    sample = ROOT / "jobs" / "sample_banking_lead_qe_jd.md"
    sample.parent.mkdir(parents=True, exist_ok=True)
    if not sample.exists():
        sample.write_text(SAMPLE_JD, encoding="utf-8")
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description="Build v4 JD Intelligence Bridge and Readiness Dashboard artifacts.")
    parser.add_argument("--jd", nargs="*", help="One or more JD text/markdown files. If omitted, a sample Banking Lead QE JD is used.")
    parser.add_argument("--out-dir", default="outputs/v4/jd_readiness")
    args = parser.parse_args()

    jd_paths = [Path(p) for p in args.jd] if args.jd else [ensure_sample_jd()]
    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    analyses = []
    for jd in jd_paths:
        if not jd.is_absolute():
            jd = ROOT / jd
        if not jd.exists():
            raise FileNotFoundError(f"JD file not found: {jd}")
        analysis = analyze_jd(ROOT, jd)
        analyses.append(analysis)
        slug = jd.stem.lower().replace(" ", "_")
        write_json(out_dir / f"{slug}_analysis.json", asdict(analysis))
        write_markdown(out_dir / f"{slug}_analysis.md", analysis_to_markdown(analysis))

    write_json(ROOT / "outputs" / "v4" / "readiness_dashboard.json", [asdict(a) for a in analyses])
    write_markdown(ROOT / "docs" / "docs" / "v4" / "readiness-dashboard.md", build_dashboard(ROOT, analyses))
    print(f"Generated {len(analyses)} JD readiness analysis file(s).")
    print(f"Dashboard: docs/docs/v4/readiness-dashboard.md")
    print(f"Output dir: {out_dir}")

if __name__ == "__main__":
    main()
