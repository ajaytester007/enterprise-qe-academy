# Practice Engine

The Practice Engine supports coherent tutor-style interview preparation.

## Recommended Tutor Session

```powershell
python scripts\start_practice_session.py --role "Lead Quality Engineer" --domain Banking --difficulty Hard --count 5 --mode tutor
```

This creates a Markdown report under:

```text
practice/reports/
```

Each question includes:

- question prompt
- Hint 1
- Hint 2
- model answer
- follow-up questions
- scorecard
- improvement notes

## Export to ChatGPT Tutor Prompt

```powershell
python scripts\export_chatgpt_prompt.py --report practice\reports\session_YYYYMMDD_HHMMSS_tutor.md
```

Then start a new ChatGPT thread and paste the generated prompt.

## Reveal One Solution

```powershell
python scripts\reveal_solution.py --id SQL-08230 --level solution
```

## Online IDE Direction

GitHub Pages is static, so it cannot run code by itself. For coding practice, use one of these:

1. GitHub Codespaces for full online IDE.
2. Local VS Code with this repo.
3. Future enhancement: React + FastAPI + Monaco editor.
