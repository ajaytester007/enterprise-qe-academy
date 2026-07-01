# Enterprise QE Academy v4 — JD Intelligence Bridge + Readiness Dashboard

This patch adds job-description driven readiness intelligence.

## What it does

- Reads one or more job descriptions from `jobs/` or any local markdown/text file.
- Extracts required skills, domain, seniority, and keyword signals.
- Maps the JD to generated v4 knowledge nodes and catalog coverage.
- Produces a readiness score, gap list, interview focus plan, portfolio recommendations, and resume talking points.
- Generates a GitHub Pages dashboard page under `docs/docs/v4/readiness-dashboard.md`.

## Run from the real repo root

```powershell
cd C:\GitHub\Enterprise_QE_Academy_Consumable_GitSolution\enterprise_qe_academy_consumable_solution

python .\scripts\build_v4_jd_readiness_release.py --jd .\jobs\sample_banking_lead_qe_jd.md
```

For a real JD:

```powershell
New-Item -ItemType Directory -Force .\jobs
notepad .\jobs\target_jd.md
python .\scripts\build_v4_jd_readiness_release.py --jd .\jobs\target_jd.md
```

## Commit and deploy

```powershell
git status
git add platform_core scripts docs outputs jobs .github V4_JD_READINESS_QUICKSTART.md
git commit -m "Add v4 JD readiness intelligence bridge"
git push origin main
```
