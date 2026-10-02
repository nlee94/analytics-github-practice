-- Purpose: Routes with the worst on-time performance, for the monthly ops review.
-- Grain: one row per route (origin-dest) with at least 3 operated flights.
-- Definition: on-time = departed no more than 15 minutes after schedule.
--             Cancelled flights are reported separately and must be EXCLUDED here.

WITH operated AS (
    SELECT
        origin,
        dest,
        dep_delay_min,
        CASE WHEN dep_delay_min <= 15 THEN 1 ELSE 0 END AS is_on_time
    FROM flights
)

SELECT
    origin || '-' || dest AS route,
    COUNT(*) AS flights,
    SUM(is_on_time) AS on_time_flights,
    ROUND(100.0 * SUM(is_on_time) / COUNT(*), 1) AS on_time_pct,
    ROUND(AVG(dep_delay_min), 1) AS avg_dep_delay_min
FROM operated
GROUP BY origin, dest
HAVING COUNT(*) >= 3
ORDER BY on_time_pct ASC, flights DESC;
