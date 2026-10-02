-- Purpose: Aging of open audit findings, for the weekly audit committee pack.
-- Grain: one row per open finding (status <> 'Closed'), with an age bucket.
-- Notes: as_of_date is a parameter CTE so results are reproducible. At work this would
--        come from a query parameter or dashboard widget.

WITH params AS (
    SELECT DATE '2026-09-30' AS as_of_date
),

open_findings AS (
    SELECT
        finding_id,
        area,
        severity,
        owner_team,
        status,
        opened_date
    FROM audit_findings
    WHERE status <> 'Closed'
),

aged AS (
    SELECT
        open_findings.finding_id,
        open_findings.area,
        open_findings.severity,
        open_findings.owner_team,
        open_findings.status,
        open_findings.opened_date,
        DATE_DIFF('day', open_findings.opened_date, params.as_of_date) AS days_open
    FROM open_findings
    CROSS JOIN params
)

SELECT
    finding_id,
    area,
    severity,
    owner_team,
    status,
    opened_date,
    days_open,
    CASE
        WHEN days_open <= 30 THEN '0-30'
        WHEN days_open <= 60 THEN '31-60'
        WHEN days_open <= 90 THEN '61-90'
        ELSE '90+'
    END AS age_bucket
FROM aged
ORDER BY days_open DESC, severity ASC, finding_id ASC;
