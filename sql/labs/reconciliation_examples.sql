-- Enterprise QE Academy SQL Reconciliation Examples

SELECT business_key, COUNT(*) AS record_count
FROM target_table
GROUP BY business_key
HAVING COUNT(*) > 1;

SELECT 'source' AS layer, COUNT(*) FROM source_table
UNION ALL
SELECT 'target' AS layer, COUNT(*) FROM target_table;

SELECT business_key FROM source_table
EXCEPT
SELECT business_key FROM target_table;
