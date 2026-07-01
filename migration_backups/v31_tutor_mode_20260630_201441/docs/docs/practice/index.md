# Practice Engine

The Practice Engine turns the catalog into interactive interview preparation.

## Start Practice

```powershell
python scripts\start_practice_session.py --role "Lead Quality Engineer" --domain Banking --difficulty Hard --count 10 --mode hints
```

## Reveal Hints and Solutions

```powershell
python scripts\reveal_solution.py --id SQL-00076 --level hint1
python scripts\reveal_solution.py --id SQL-00076 --level hint2
python scripts\reveal_solution.py --id SQL-00076 --level solution
```

## Generate Interview Pack

```powershell
python scripts\generate_interview_pack.py --role "QE Architect" --domain "Healthcare Payer" --count 25
```

## Generate Skill Path

```powershell
python scripts\generate_skill_path.py --skill SQL --weeks 4
python scripts\generate_skill_path.py --skill Playwright --weeks 4
```
