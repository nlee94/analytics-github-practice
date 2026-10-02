"""Tests for the SQL queries and the pandas report.

Run with `pytest` from the repo root (pyproject.toml puts python/ on the path).

On a fresh copy of the repo one test FAILS on purpose (Session 3) and one is
SKIPPED until you write the query it checks (Session 5).
"""

from __future__ import annotations

import pandas as pd
import pytest

import analytics_db
import data_quality_checks
import delay_report
from paths import SAMPLE_DIR, SQL_DIR


@pytest.fixture(scope="module")
def con():
    return analytics_db.connect()


def _dates_as_text(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """DuckDB and pandas represent dates differently; compare them as YYYY-MM-DD text."""
    out = df.copy()
    out[column] = pd.to_datetime(out[column]).dt.strftime("%Y-%m-%d")
    return out


def test_sql_01_matches_python(con):
    """The SQL daily summary and the pandas daily summary must agree."""
    sql_out = analytics_db.run_sql_file(con, SQL_DIR / "01_daily_delay_summary.sql")
    py_out = delay_report.daily_delay_summary(delay_report.load_flights())

    sql_out = _dates_as_text(sql_out, "flight_date").sort_values("flight_date")
    py_out = _dates_as_text(py_out, "flight_date").sort_values("flight_date")

    # atol allows for SQL and pandas rounding .x5 values differently.
    pd.testing.assert_frame_equal(
        sql_out.reset_index(drop=True),
        py_out[sql_out.columns].reset_index(drop=True),
        check_dtype=False,
        check_exact=False,
        atol=0.1,
    )


def test_sql_03_excludes_cancelled_flights(con):
    """Deliberately fails on a fresh clone. See LEARNING_PLAN.md, Session 3."""
    out = analytics_db.run_sql_file(con, SQL_DIR / "03_top_delay_routes.sql")
    flights = delay_report.load_flights()
    operated = flights[~flights["cancelled"]]
    expected = (operated["origin"] + "-" + operated["dest"]).value_counts()

    for row in out.itertuples(index=False):
        assert row.flights == expected[row.route], (
            f"{row.route}: query counted {row.flights} flights, expected "
            f"{expected[row.route]} -- cancelled flights must be excluded"
        )


def test_sql_04_audit_findings_by_area(con):
    """Session 5 exercise: one row per area x severity, count of not-Closed findings."""
    path = SQL_DIR / "04_audit_findings_by_area.sql"
    if not path.exists():
        pytest.skip("Session 5 not done yet: create sql/04_audit_findings_by_area.sql")

    out = analytics_db.run_sql_file(con, path)
    findings = pd.read_csv(SAMPLE_DIR / "audit_findings_sample.csv")
    expected_open = int((findings["status"] != "Closed").sum())

    assert {"area", "severity", "open_findings"} <= set(out.columns)
    assert not out.duplicated(["area", "severity"]).any(), "grain must be area x severity"
    assert int(out["open_findings"].sum()) == expected_open


def test_data_quality_checks_pass():
    results = data_quality_checks.run_checks()
    failed = [r.name for r in results if not r.passed]
    assert not failed, f"failing checks: {failed}"
