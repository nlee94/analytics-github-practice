-- Purpose: Daily departure-delay summary for the ops dashboard.
-- Grain: one row per flight_date.
-- Notes: A flight is "delayed" when dep_delay_min > 15 (the DOT-style definition).
--        Cancelled flights count toward flights_scheduled and flights_cancelled but are
--        excluded from flights_delayed and avg_dep_delay_min.
--        The same definition lives in python/delay_report.py (DELAY_THRESHOLD_MIN);
--        tests/test_queries.py checks that the two agree.

SELECT
    flight_date,
    COUNT(*) AS flights_scheduled,
    SUM(CASE WHEN cancelled THEN 1 ELSE 0 END) AS flights_cancelled,
    SUM(CASE WHEN NOT cancelled AND dep_delay_min > 15 THEN 1 ELSE 0 END) AS flights_delayed,
    ROUND(AVG(CASE WHEN NOT cancelled THEN dep_delay_min END), 1) AS avg_dep_delay_min
FROM flights
GROUP BY flight_date
ORDER BY flight_date;
