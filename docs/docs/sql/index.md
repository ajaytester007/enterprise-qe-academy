# SQL and Data Validation Practice

SQL is essential for Enterprise QE, Data QA, ETL testing, healthcare payer validation, and banking reconciliation work.

## Core Topics

- Source-to-target validation
- Duplicate detection
- Join-based reconciliation
- Missing record checks
- Count, sum, and control-total validation
- Window functions
- Grouping and aggregation
- Null handling
- Data profiling

## Sample SQL Patterns

### Duplicate Business Keys

```sql
SELECT business_key, COUNT(*) AS record_count
FROM target_table
GROUP BY business_key
HAVING COUNT(*) > 1;
```

### Source-to-Target Count Check

```sql
SELECT 'source' AS layer, COUNT(*) AS row_count
FROM source_table
UNION ALL
SELECT 'target' AS layer, COUNT(*) AS row_count
FROM target_table;
```

### Missing Records

```sql
SELECT business_key FROM source_table
EXCEPT
SELECT business_key FROM target_table;
```

## Generated Examples

- [SQL Generated Example 1](../solutions/generated/SQL-00004/)
- [SQL Generated Example 2](../solutions/generated/SQL-00076/)
- [SQL Generated Example 3](../solutions/generated/SQL-00130/)
