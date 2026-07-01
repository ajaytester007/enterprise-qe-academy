# Enterprise QE Academy v5 — Interview Session Engine 2.0

This patch upgrades the v5 GitHub Pages app into a real one-question-at-a-time mock interview tool.

## Build from repo root

```powershell
cd C:\GitHub\Enterprise_QE_Academy_Consumable_GitSolution\enterprise_qe_academy_consumable_solution

Copy-Item ..\enterprise_qe_academy_v5_interview_session_engine_2_patch.zip . -Force
Expand-Archive .\enterprise_qe_academy_v5_interview_session_engine_2_patch.zip -DestinationPath . -Force
Remove-Item .\enterprise_qe_academy_v5_interview_session_engine_2_patch.zip -Force

python .\scripts\build_v5_interview_engine.py --limit 5000
python -m http.server 8000 -d outputs\v5\site
```

Open local preview:

```text
http://localhost:8000
```

## Commit source changes to main

```powershell
git status
git add webapp platform_core scripts docs outputs .github V5_INTERVIEW_SESSION_ENGINE_2_QUICKSTART.md
git commit -m "Add v5 interview session engine 2.0"
git push origin main
```

## Deploy to GitHub Pages without v5/v5 nesting

```powershell
python .\scripts\deploy_v5_gh_pages.py --message "Deploy v5 interview session engine 2.0"
```

Verify the published branch:

```powershell
git fetch origin gh-pages
git ls-tree -r origin/gh-pages --name-only | Select-String "v5"
```

Expected:

```text
v5/app.js
v5/data/questions.json
v5/index.html
v5/styles.css
```

Live URL:

```text
https://ajaytester007.github.io/enterprise-qe-academy/v5/
```

## Features

- One-question-at-a-time interview mode
- Answer textbox with local autosave
- Hint 1, Hint 2, model answer, follow-ups, and self-critique checklist
- Enterprise QE 100-point scoring rubric
- Question navigation and mark-for-review
- Timer and progress analytics
- Readiness label
- Copy current question as a ChatGPT interviewer prompt
- Markdown export of the completed session
