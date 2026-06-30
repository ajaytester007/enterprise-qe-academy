# Enterprise QE Academy v2 Upgrade Steps

## 1. Back up current repo

```powershell
cd C:\GitHub\Enterprise_QE_Academy_Consumable_GitSolution\enterprise_qe_academy_consumable_solution
git status
git pull
```

## 2. Copy v2 files

Extract this ZIP and copy all contents over your existing repo root.

## 3. Validate locally

```powershell
python scripts/validate_catalog.py
python scripts/search_catalog.py --keyword masking --limit 10
python scripts/generate_practice_set.py --count 25 --difficulty Hard --domain Banking
cd java\core
mvn clean test
cd ..\..
```

## 4. Build docs locally

```powershell
cd docs
mkdocs serve
```

Open http://127.0.0.1:8000

## 5. Commit and push

```powershell
cd ..
git add .
git commit -m "Expand academy v2 catalog, docs, domains, and labs"
git push
```

## 6. Deploy GitHub Pages

```powershell
cd docs
mkdocs gh-deploy
```
