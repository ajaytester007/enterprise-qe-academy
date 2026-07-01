# Enterprise QE Academy v5 Interactive Platform Quickstart

This patch adds a lightweight v5 interactive platform foundation that can be deployed through GitHub Pages while keeping the current Python/Markdown workflow intact.

## What this adds

- Static interactive v5 web app scaffold
- Interview session state model
- Readiness and JD bridge data loader
- Browser-side practice launcher
- GitHub Pages documentation page
- One-command v5 static build script
- GitHub Actions workflow for v5 artifact generation

## Apply from repo root

```powershell
cd C:\GitHub\Enterprise_QE_Academy_Consumable_GitSolution\enterprise_qe_academy_consumable_solution

Copy-Item ..\enterprise_qe_academy_v5_interactive_platform_patch.zip . -Force
Expand-Archive .\enterprise_qe_academy_v5_interactive_platform_patch.zip -DestinationPath . -Force
Remove-Item .\enterprise_qe_academy_v5_interactive_platform_patch.zip -Force

python .\scripts\build_v5_static_platform.py

git status
git add webapp platform_core scripts docs outputs .github V5_INTERACTIVE_PLATFORM_QUICKSTART.md
git commit -m "Add v5 interactive platform foundation"
git push origin main
```

## Local preview

After building:

```powershell
python -m http.server 8000 -d outputs/v5/site
```

Open:

```text
http://localhost:8000
```

## Notes

This is intentionally backend-free for GitHub Pages compatibility. The next v5 step can add FastAPI/SQLite/Postgres for persistent accounts, saved sessions, and real-time AI coaching.
