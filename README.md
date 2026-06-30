# Enterprise QE Academy v2

A generic Enterprise Quality Engineering academy with a searchable assessment catalog, solution templates, domain packs, executable Java samples, SQL/API/automation labs, and MkDocs documentation.

## v2 Content

- 10,080+ searchable catalog entries
- Java, SQL, API, automation, data quality, domain, cloud, AI QE, and whiteboarding structure
- 180 generated sample solution pages
- CLI search and practice-set generator
- Static search index for future custom UI
- Java 17 Maven/JUnit sample tests
- MkDocs site with expanded left navigation

## Upgrade Existing Repo

Copy the contents of this package into the root of your existing `enterprise-qe-academy` repo, then:

```powershell
git add .
git commit -m "Expand academy v2 catalog, docs, domains, and labs"
git push
cd docs
mkdocs gh-deploy
```

## Search Examples

```powershell
python scripts/search_catalog.py --keyword masking --limit 10
python scripts/search_catalog.py --category SQL_DATA_VALIDATION --difficulty Hard --limit 20
python scripts/search_catalog.py --domain Banking --role "Lead Quality Engineer"
```

## Practice Set

```powershell
python scripts/generate_practice_set.py --count 50 --difficulty Medium --domain Banking
```

## Java Samples

```powershell
cd java/core
mvn clean test
```
