# Enterprise QE Academy Enhancement Quickstart

This patch upgrades the practice workflow so the local VS Code repo and GitHub Pages site can support stronger interview preparation.

## 1. Generate a new tutor session

```powershell
python .\scripts\start_practice_session.py --count 5 --domain Banking --role "Lead Quality Engineer" --difficulty Hard --mode tutor
```

## 2. Export the newest session without copying timestamps

```powershell
python .\scripts\export_chatgpt_prompt.py --latest
```

## 3. Export all prompt modes

```powershell
python .\scripts\export_chatgpt_prompt.py --report latest --mode all
```

Generated files are written to:

```text
outputs/prompts/
```

Modes generated:

- Tutor prompt
- Mock interview prompt
- Coding challenge prompt
- Whiteboard prompt
- Panel interview prompt

## 4. Generate a full interview pack

```powershell
python .\scripts\generate_interview_pack.py --domain Banking --role "Lead Quality Engineer" --difficulty Hard --count 25 --include-solutions
```

Output:

```text
outputs/interview_pack.md
```

## 5. Validate quickly

```powershell
python .\scripts\export_chatgpt_prompt.py --latest --mode all
python .\scripts\generate_interview_pack.py --domain Banking --role "Lead Quality Engineer" --count 5 --include-solutions
```

## 6. Commit and push

```powershell
git status
git add scripts\export_chatgpt_prompt.py scripts\generate_interview_pack.py ENHANCEMENT_QUICKSTART.md outputs\prompts outputs\interview_pack.md
git commit -m "Enhance practice prompt exporter and interview pack generator"
git push origin main
```

## 7. Optional GitHub Pages refresh

If your site is built with MkDocs:

```powershell
cd docs
mkdocs gh-deploy
```
