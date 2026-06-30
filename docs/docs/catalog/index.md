# Catalog Browser

The academy currently contains **10,080** catalog records.

The full question database lives in:

```text
catalog/questions.jsonl
catalog/questions.csv
```

This MkDocs site intentionally uses lightweight catalog browse pages instead of generating one HTML page per question. That keeps the site fast and prevents local disk/build overload.

## Browse

- [Browse by Category](by-category.md)
- [Browse by Domain](by-domain.md)
- [Browse by Difficulty](by-difficulty.md)
- [Browse by Role](by-role.md)

## CLI Search

```powershell
python scripts\search_catalog.py --keyword masking --limit 10
python scripts\search_catalog.py --category SQL_DATA_VALIDATION --difficulty Hard --limit 20
python scripts\search_catalog.py --domain Banking --role "Lead Quality Engineer"
```

## Generate Practice Set

```powershell
python scripts\generate_practice_set.py --count 25 --difficulty Hard --domain Banking
```
