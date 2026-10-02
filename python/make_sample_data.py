"""Generate the synthetic sample data in data/sample/.

Everything is invented: airports, flight numbers, delays, audit findings. A fixed
random seed makes the files reproducible, so the generator is the source of truth
and the CSVs are committed only because they are tiny and fake.

Usage:
    python python/make_sample_data.py
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from paths import REPO_ROOT, SAMPLE_DIR

SEED = 2026

ROUTES = [
    ("SEA", "SFO"), ("SFO", "SEA"), ("SEA", "LAX"), ("LAX", "SEA"), ("PDX", "SAN"),
    ("SAN", "PDX"), ("SEA", "ANC"), ("ANC", "SEA"), ("BOI", "SEA"), ("SEA", "SJC"),
]
AIRCRAFT = ["B737-800", "B737-9", "E175"]
CANCEL_REASONS = ["Weather", "Maintenance", "Crew", "Air Traffic Control"]
AREAS = ["Ground Ops", "Maintenance", "Flight Ops", "Cabin Safety", "Training", "Security"]
TEAMS = ["Station Ops", "Tech Ops", "Flight Standards", "Inflight", "Safety Programs"]
SEVERITIES = ["Low", "Medium", "High"]


def _dep_delay(rng: random.Random) -> int:
    """Skewed delay distribution: most flights close to on time, a long tail late."""
    r = rng.random()
    if r < 0.60:
        return rng.randint(-8, 10)
    if r < 0.85:
        return rng.randint(11, 45)
    if r < 0.95:
        return rng.randint(46, 120)
    return rng.randint(121, 300)


def make_flights(rng: random.Random) -> list[dict]:
    rows = []
    start = date(2026, 9, 1)
    for day in range(14):
        flight_date = start + timedelta(days=day)
        for i in range(6):
            origin, dest = ROUTES[(day * 6 + i) % len(ROUTES)]
            cancelled = rng.random() < 0.08
            dep_delay = None if cancelled else _dep_delay(rng)
            arr_delay = None if cancelled else dep_delay + rng.randint(-10, 8)
            aircraft = rng.choice(AIRCRAFT)
            sched_hour = rng.randint(6, 21)
            sched_minute = rng.choice(["00", "15", "30", "45"])
            rows.append(
                {
                    "flight_date": flight_date.isoformat(),
                    "flight_number": f"XA{100 + (day * 6 + i) % 40}",
                    "origin": origin,
                    "dest": dest,
                    "aircraft_type": aircraft,
                    "sched_dep_time": f"{sched_hour:02d}:{sched_minute}",
                    "dep_delay_min": dep_delay,
                    "arr_delay_min": arr_delay,
                    "cancelled": "true" if cancelled else "false",
                    "cancel_reason": rng.choice(CANCEL_REASONS) if cancelled else None,
                }
            )
    return rows


def make_audit_findings(rng: random.Random) -> list[dict]:
    rows = []
    latest_close = date(2026, 9, 20)
    for n in range(1, 31):
        audit_date = date(2026, 4, 1) + timedelta(days=rng.randint(0, 165))
        opened = audit_date + timedelta(days=rng.randint(1, 5))
        closed = None
        if rng.random() < 0.45:
            candidate = opened + timedelta(days=rng.randint(5, 90))
            closed = candidate if candidate <= latest_close else None
        status = "Closed" if closed else rng.choice(["Open", "In Progress"])
        rows.append(
            {
                "finding_id": f"F-2026-{n:03d}",
                "audit_id": f"AUD-2026-{(n - 1) // 6 + 1:02d}",
                "audit_date": audit_date.isoformat(),
                "area": rng.choice(AREAS),
                "severity": rng.choices(SEVERITIES, weights=[5, 3, 2])[0],
                "status": status,
                "opened_date": opened.isoformat(),
                "closed_date": closed.isoformat() if closed else None,
                "owner_team": rng.choice(TEAMS),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows):>3} rows -> {path.relative_to(REPO_ROOT)}")


def main() -> None:
    rng = random.Random(SEED)
    write_csv(SAMPLE_DIR / "flights_sample.csv", make_flights(rng))
    write_csv(SAMPLE_DIR / "audit_findings_sample.csv", make_audit_findings(rng))


if __name__ == "__main__":
    main()
