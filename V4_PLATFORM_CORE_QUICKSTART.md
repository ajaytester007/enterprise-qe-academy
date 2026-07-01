# Enterprise QE Academy v4 Platform Core Quickstart

Apply this patch from the real repo root, not the parent folder:

```powershell
cd C:\GitHub\Enterprise_QE_Academy_Consumable_GitSolution\enterprise_qe_academy_consumable_solution
Copy-Item ..\enterprise_qe_academy_v4_platform_core_patch.zip . -Force
Expand-Archive .\enterprise_qe_academy_v4_platform_core_patch.zip -DestinationPath . -Force
Remove-Item .\enterprise_qe_academy_v4_platform_core_patch.zip -Force
```

Generate v4 assets:

```powershell
python .\scripts\generate_v4_platform_core.py --domain Banking --role "Lead Quality Engineer" --difficulty Hard --limit 250
python .\scripts\generate_v4_portal_pages.py
python .\scripts\adaptive_interview_simulator.py --index 0
```

Commit:

```powershell
git status
git add platform_core scripts docs outputs .github V4_PLATFORM_CORE_QUICKSTART.md
git commit -m "Add Enterprise QE Academy v4 platform core"
git push origin main
```

Recommended next command after this lands:

```powershell
python .\scripts\generate_v4_platform_core.py --limit 0
python .\scripts\generate_v4_portal_pages.py
```

Use `--limit 0` only when you are ready to generate from the full catalog.
