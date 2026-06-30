# Build and Deployment Steps

## 1. Extract

Extract the ZIP into:

```powershell
C:\GitHub\enterprise_qe_academy_consumable_solution
```

## 2. Review structure

```powershell
dir
tree /F
```

## 3. Search catalog

```powershell
python scripts/search_catalog.py --keyword masking --limit 10
python scripts/search_catalog.py --category SQL_DATA_VALIDATION --difficulty Hard --limit 20
python scripts/search_catalog.py --domain Banking --role "Lead Quality Engineer"
```

## 4. Generate a practice set

```powershell
python scripts/generate_practice_set.py --count 50 --difficulty Medium --domain Banking
```

Generated file:

```text
outputs/practice_set.md
```

## 5. Run Java sample tests

```powershell
cd java\enterprise-qe-core
mvn clean test
cd ..\..
```

## 6. Run catalog validation

```powershell
python scripts/validate_catalog.py
```

## 7. Run documentation site locally

```powershell
cd docs
pip install mkdocs-material
mkdocs serve
```

Open:

```text
http://127.0.0.1:8000
```

## 8. Publish GitHub repository

Create a new GitHub repo named:

```text
enterprise-qe-academy
```

Then:

```powershell
git init
git add .
git commit -m "Initial Enterprise QE Academy"
git branch -M main
git remote add origin https://github.com/ajaytester007/enterprise-qe-academy.git
git push -u origin main
```

## 9. Enable GitHub Pages

Recommended source:

```text
GitHub Actions or gh-pages branch after MkDocs deployment
```

## 10. Deploy docs with MkDocs

```powershell
cd docs
mkdocs gh-deploy
```
