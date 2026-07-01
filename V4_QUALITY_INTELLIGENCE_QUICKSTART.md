# Enterprise QE Academy v4 Quality Intelligence Quickstart

Apply this patch from the real repo root:

```powershell
cd C:\GitHub\Enterprise_QE_Academy_Consumable_GitSolution\enterprise_qe_academy_consumable_solution

Copy-Item ..\enterprise_qe_academy_v4_quality_intelligence_patch.zip . -Force
Expand-Archive .\enterprise_qe_academy_v4_quality_intelligence_patch.zip -DestinationPath . -Force
Remove-Item .\enterprise_qe_academy_v4_quality_intelligence_patch.zip -Force
```

Build and validate:

```powershell
python .\scripts\build_v4_release.py --domain Banking --role "Lead Quality Engineer" --difficulty Hard --limit 250
```

Inspect outputs:

```powershell
Get-ChildItem .\outputs\v4\
Get-Content .\outputs\v4\quality_report.md -TotalCount 80
Get-Content .\docs\docs\v4\quality-dashboard.md -TotalCount 80
```

Commit and deploy:

```powershell
git status
git add platform_core scripts docs outputs .github V4_QUALITY_INTELLIGENCE_QUICKSTART.md
git commit -m "Add v4 quality intelligence layer"
git push origin main
```

Important: always run these commands from `enterprise_qe_academy_consumable_solution`, not the parent folder.
