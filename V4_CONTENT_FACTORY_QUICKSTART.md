# Enterprise QE Academy v4 Content Factory Quickstart

Apply from the real repository root:

```powershell
cd C:\GitHub\Enterprise_QE_Academy_Consumable_GitSolution\enterprise_qe_academy_consumable_solution

Copy-Item ..\enterprise_qe_academy_v4_content_factory_patch.zip . -Force
Expand-Archive .\enterprise_qe_academy_v4_content_factory_patch.zip -DestinationPath . -Force
Remove-Item .\enterprise_qe_academy_v4_content_factory_patch.zip -Force

python .\scripts\build_v4_content_release.py --domain Banking --role "Lead Quality Engineer" --difficulty Hard --limit 250

git status
git add platform_core scripts docs outputs .github V4_CONTENT_FACTORY_QUICKSTART.md
git commit -m "Add v4 content factory enrichment layer"
git push origin main
```

## What this adds

- `platform_core/content_factory.py`
- `scripts/build_v4_content_factory.py`
- `scripts/generate_v4_content_factory_portal.py`
- `scripts/build_v4_content_release.py`
- `docs/docs/v4/content-factory.md`
- `.github/workflows/v4-content-factory.yml`
- Generated enriched content under `outputs/v4/content_factory/`

## Purpose

This layer improves the actual learning value of the academy by converting catalog questions into richer interview-coaching assets:

- stronger model answers
- assumptions
- edge cases
- validation strategy
- release evidence
- follow-up questions
- common mistakes
- coding prompts
- whiteboard prompts
- Mermaid diagrams
- quality scoring
