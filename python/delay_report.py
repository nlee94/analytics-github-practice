"""Daily departure-delay report, in pandas.

sql/01_daily_delay_summary.sql produces the same numbers in SQL. The test suite
checks that the two agree, which is a cheap way to catch definition drift when a
metric lives in more than one place.

Usage:
    python python/delay_report.py
    python python/delay_report.py --out outputs/daily_delays.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from paths import SAMPLE_DIR

# A flight is "delayed" when it departs more than this many minutes late.
# The same threshold appears in sql/01_daily_delay_summary.sql.
DELAY_THRESHOLD_MIN = 15


def load_flights(sample_dir: Path = SAMPLE_DIR) -> pd.DataFrame:
    """Load the synthetic flights sample with proper dtypes."""
    return pd.read_csv(sample_dir / "flights_sample.csv", parse_dates=["flight_date"])


def daily_delay_summary(
    flights: pd.DataFrame, threshold_min: int = DELAY_THRESHOLD_MIN
) -> pd.DataFrame:
    """One row per flight_date: scheduled, cancelled, delayed counts and average delay.

    Cancelled flights count toward flights_scheduled and flights_cancelled but are
    excluded from flights_delayed and avg_dep_delay_min.
    """
    operated = flights[~flights["cancelled"]]

    summary = flights.groupby("flight_date").agg(
        flights_scheduled=("flight_number", "size"),
        flights_cancelled=("cancelled", "sum"),
    )
    delayed = (operated["dep_delay_min"] > threshold_min).groupby(operated["flight_date"]).sum()
    avg_delay = operated.groupby("flight_date")["dep_delay_min"].mean().round(1)

    summary["flights_delayed"] = delayed.reindex(summary.index, fill_value=0)
    summary["avg_dep_delay_min"] = avg_delay.reindex(summary.index)
    return summary.reset_index()


def main() -> None:
    parser = argparse.ArgumentParser(description="Print the daily delay summary.")
    parser.add_argument("--out", type=Path, help="optional CSV path for the report")
    args = parser.parse_args()

    report = daily_delay_summary(load_flights())
    print(report.to_string(index=False))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        report.to_csv(args.out, index=False)
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
