"""Run a .sql file from sql/ against the sample data and print the result.

Usage:
    python python/run_sql.py sql/01_daily_delay_summary.sql
    python python/run_sql.py sql/03_top_delay_routes.sql --csv outputs/routes.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

from analytics_db import connect, run_sql_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("sql_file", type=Path, help="path to a .sql file")
    parser.add_argument("--csv", type=Path, help="also write the result to this CSV path")
    args = parser.parse_args()

    result = run_sql_file(connect(), args.sql_file)
    print(result.to_string(index=False))
    print(f"\n{len(result)} rows")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(args.csv, index=False)
        print(f"wrote {args.csv}")


if __name__ == "__main__":
    main()
