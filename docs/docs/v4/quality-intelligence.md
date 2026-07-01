# v4 Quality Intelligence Layer

The Quality Intelligence Layer turns Enterprise QE Academy v4 from a content generator into a governed learning platform.

## What it adds

- Automated knowledge-node quality scoring
- Placeholder and shallow-answer detection
- Rubric validation
- Evidence/readiness validation
- Static GitHub Pages dashboard generation
- GitHub Actions artifact workflow
- One-command v4 release builder

## Local commands

```powershell
python .\scripts\build_v4_release.py --domain Banking --role "Lead Quality Engineer" --difficulty Hard --limit 250
```

Or run each step manually:

```powershell
python .\scripts\generate_v4_platform_core.py --domain Banking --role "Lead Quality Engineer" --difficulty Hard --limit 250
python .\scripts\generate_v4_portal_pages.py
python .\scripts\assess_v4_quality.py
python .\scripts\generate_v4_quality_dashboard.py
```

## Generated outputs

- `outputs/v4/quality_report.json`
- `outputs/v4/quality_report.md`
- `outputs/v4/quality_gate_status.json`
- `docs/docs/v4/quality-dashboard.md`

## Recommended gate policy

Use the gate as a warning initially. Once content quality improves, run:

```powershell
python .\scripts\assess_v4_quality.py --fail-on-gate
```

This can later become a required GitHub Actions quality gate before publishing curated packs.
