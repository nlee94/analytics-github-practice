"""Sanity checks on the sample data. Exit code 1 if any check fails.

This is the kind of script that belongs in CI (Session 9 adds it): cheap, fast,
and it turns "I think the data is fine" into something a machine verifies.

Usage:
    python python/data_quality_checks.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from paths import SAMPLE_DIR


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def _check(name: str, condition: bool, detail: str = "") -> CheckResult:
    return CheckResult(name=name, passed=bool(condition), detail=detail)


def run_checks(sample_dir: Path = SAMPLE_DIR) -> list[CheckResult]:
    flights = pd.read_csv(sample_dir / "flights_sample.csv", parse_dates=["flight_date"])
    findings = pd.read_csv(
        sample_dir / "audit_findings_sample.csv",
        parse_dates=["audit_date", "opened_date", "closed_date"],
    )

    cancelled = flights["cancelled"]
    return [
        _check(
            "flights: no missing keys",
            flights[["flight_date", "flight_number", "origin", "dest"]].notna().all().all(),
        ),
        _check(
            "flights: origin differs from dest",
            (flights["origin"] != flights["dest"]).all(),
        ),
        _check(
            "flights: cancelled flights have no delay, operated flights do",
            flights.loc[cancelled, "dep_delay_min"].isna().all()
            and flights.loc[~cancelled, "dep_delay_min"].notna().all(),
            f"{int(cancelled.sum())} cancelled of {len(flights)}",
        ),
        _check(
            "flights: departure delay within [-30, 600] minutes",
            flights["dep_delay_min"].dropna().between(-30, 600).all(),
            f"min {flights['dep_delay_min'].min():.0f}, max {flights['dep_delay_min'].max():.0f}",
        ),
        _check(
            "findings: finding_id is unique",
            findings["finding_id"].is_unique,
            f"{len(findings)} findings",
        ),
        _check(
            "findings: severity is Low/Medium/High",
            findings["severity"].isin(["Low", "Medium", "High"]).all(),
        ),
        _check(
            "findings: closed_date is on or after opened_date",
            (findings["closed_date"].dropna() >= findings.loc[findings["closed_date"].notna(),
                                                              "opened_date"]).all(),
        ),
        _check(
            "findings: status is Closed exactly when closed_date is present",
            ((findings["status"] == "Closed") == findings["closed_date"].notna()).all(),
            f"{int((findings['status'] != 'Closed').sum())} still open",
        ),
    ]


def main() -> int:
    results = run_checks()
    for r in results:
        flag = "PASS" if r.passed else "FAIL"
        suffix = f"  ({r.detail})" if r.detail else ""
        print(f"[{flag}] {r.name}{suffix}")
    failed = [r for r in results if not r.passed]
    print(f"\n{len(results) - len(failed)} passed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
