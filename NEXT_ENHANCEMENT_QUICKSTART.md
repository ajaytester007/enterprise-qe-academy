# Enterprise QE Academy — Next Enhancement Quickstart

This patch adds a one-command practice pipeline, asset validation, and standalone HTML practice-page generation.

## 1. Apply the patch

From the repo root:

```powershell
Expand-Archive .\enterprise_qe_academy_next_enhancement_patch.zip -DestinationPath . -Force
```

## 2. Run full local validation

```powershell
python .\scripts\validate_catalog.py
python .\scripts\validate_practice_assets.py
```

## 3. Generate a complete practice bundle in one command

```powershell
python .\scripts\practice_pipeline.py --domain Banking --role "Lead Quality Engineer" --difficulty Hard --count 5 --prompt-mode all --include-pack --include-solutions
```

This creates:

- a new JSON practice session under `practice/sessions/`
- a Markdown tutor report under `practice/reports/`
- ChatGPT prompt modes under `outputs/prompts/`
- an optional interview pack under `outputs/interview_pack_pipeline.md`

## 4. Generate a standalone HTML practice page

```powershell
python .\scripts\generate_practice_html.py --report latest
```

Output goes to:

```text
outputs/html/<session>.html
```

Open this file locally in a browser. It preserves expandable hints/model answers.

## 5. Suggested Git workflow

```powershell
git status
git add .
git commit -m "Add one-command practice pipeline and HTML practice export"
git push origin main
```

## 6. Suggested next layer after this patch

The next enhancement should add a richer solution generator that expands placeholder model answers into full STAR-style/interview-ready responses with domain-specific evidence, sample SQL/API/automation snippets, diagrams, and readiness scorecards.
