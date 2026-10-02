"""Run the repo's SQL files against the sample CSVs with DuckDB.

Why DuckDB? It runs standard SQL directly on CSV and Parquet files with zero setup,
so the queries in sql/ can be executed and tested locally. At work the same queries
would run in the warehouse (e.g. Databricks SQL), where a few functions differ.
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

from paths import SAMPLE_DIR


def connect(sample_dir: Path = SAMPLE_DIR) -> duckdb.DuckDBPyConnection:
    """Return an in-memory DuckDB connection with one view per sample CSV.

    data/sample/flights_sample.csv         -> view "flights"
    data/sample/audit_findings_sample.csv  -> view "audit_findings"
    """
    con = duckdb.connect(database=":memory:")
    for csv_path in sorted(sample_dir.glob("*.csv")):
        view_name = csv_path.stem.removesuffix("_sample")
        # The path comes from our own directory listing, not user input, so an
        # f-string is acceptable here. Never build SQL this way from external input.
        con.execute(
            f"CREATE VIEW {view_name} AS "
            f"SELECT * FROM read_csv_auto('{csv_path.as_posix()}', header = true)"
        )
    return con


def run_sql_file(con: duckdb.DuckDBPyConnection, sql_path: Path | str) -> pd.DataFrame:
    """Execute a .sql file and return the result as a DataFrame."""
    sql = Path(sql_path).read_text(encoding="utf-8")
    return con.execute(sql).df()
