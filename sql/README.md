# sql/

One query per file, named `NN_snake_case_purpose.sql`. Every file starts with a header:

```sql
-- Purpose: what question this answers and who uses it.
-- Grain: one row per ...
-- Notes: definitions, exclusions, anything a reader would otherwise have to guess.
```

Git already records who changed a file and when, so headers don't repeat author/date.

Style: lowercase identifiers, UPPER keywords, CTEs instead of nested subqueries, every
expression aliased, no `SELECT *` in anything another query or dashboard depends on.
`sqlfluff lint sql/` enforces the mechanical parts (`sqlfluff fix sql/` repairs most of it).

Run any file locally: `python python/run_sql.py sql/<file>.sql`. The CSVs in `data/sample/`
are exposed as tables `flights` and `audit_findings` (DuckDB). At work, the same file would
run against the warehouse; `.sqlfluff` says where to switch the dialect.

## Query catalog

| File | Purpose | Grain |
|---|---|---|
| `01_daily_delay_summary.sql` | Daily delay summary for the ops dashboard | one row per flight_date |
| `02_audit_findings_aging.sql` | Aging of open audit findings for the audit committee pack | one row per open finding |
| `03_top_delay_routes.sql` | Worst on-time routes for the monthly ops review | one row per route |

## Maintainers

- Nathan Lee