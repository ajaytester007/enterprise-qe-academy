# Enterprise QE Academy / Assessment Factory

Generic 2026 assessment practice, whiteboarding, and evidence-generation platform for modernization-heavy IT departments.

## Includes

- 1620 searchable starter questions
- CSV and JSONL catalog
- Python search and practice-set scripts
- Java 17 Maven/JUnit executable sample module
- MkDocs documentation site
- GitHub Actions CI workflow
- Templates for question, solution, and evidence documentation

## Quick Start

```powershell
cd enterprise_qe_academy_consumable_solution
python scripts/search_catalog.py --keyword masking --limit 10
python scripts/generate_practice_set.py --count 50 --difficulty Medium --domain Banking
cd java/enterprise-qe-core
mvn clean test
```

## Local Docs Site

```powershell
cd docs
pip install mkdocs-material
mkdocs serve
```

## Publish to GitHub

```powershell
git init
git add .
git commit -m "Initial Enterprise QE Academy"
git branch -M main
git remote add origin https://github.com/ajaytester007/enterprise-qe-academy.git
git push -u origin main
```
