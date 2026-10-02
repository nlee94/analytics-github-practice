# analytics-github-practice

A small, fully synthetic "airline operations analytics" repo used by [`LEARNING_PLAN.md`](LEARNING_PLAN.md) to learn Git and GitHub the way a working data analyst uses them: SQL, Python, a notebook, tiny sample data, and the GitHub plumbing (`.github/`) a real team would have.

**Everything here is fake.** Airports, flight numbers, delays, and audit findings are generated with a fixed random seed by `python/make_sample_data.py`.

Maintainer: *Nathan Lee* — started *2026-10-02*

## Layout

```
.
├── LEARNING_PLAN.md          the 12-session plan (tick sessions off and commit)
├── CHEATSHEET.md             commands grouped by "I want to..."
├── README.md                 you are here
├── requirements.txt          pandas, duckdb, pytest, ruff, sqlfluff, nbstripout
├── pyproject.toml            ruff and pytest configuration
├── .sqlfluff                 SQL lint configuration
├── .gitignore                data-analytics flavoured; read the comments
├── .gitattributes            line-ending rules so Windows and Mac diffs stay clean
├── .github/
│   ├── workflows/ci.yml      lint + test on every PR (Session 9)
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/analysis_request.md
│   ├── CODEOWNERS            (Session 10)
│   └── dependabot.yml
├── data/
│   ├── README.md             what is committed here and what is not, plus a data dictionary
│   └── sample/               two tiny synthetic CSVs (the only data that is committed)
├── sql/                      one query per file; 03 has a planted bug (Session 3)
├── python/
│   ├── analytics_db.py       runs the SQL files against the CSVs with DuckDB
│   ├── run_sql.py            CLI: python python/run_sql.py sql/<file>.sql
│   ├── delay_report.py       the same daily summary in pandas (tests check SQL == Python)
│   ├── data_quality_checks.py  simple checks on the sample data (Session 9 adds it to CI)
│   └── make_sample_data.py   regenerates data/sample/
├── notebooks/
│   ├── explore_delays.py     Databricks source-format notebook (Session 8)
│   └── explore_delays.ipynb  Jupyter notebook with outputs baked in, on purpose (Session 8)
├── tests/test_queries.py     pytest suite; one test fails until Session 3, one is skipped until Session 5
├── docs/
│   ├── REVIEW_CHECKLIST.md   what to look for when reviewing analytics PRs (Session 6)
│   └── TEAM_GITHUB_NORMS_TEMPLATE.md   one-page norms doc to fill in (Session 12)
└── exercises/session06/      a deliberately sloppy script to review
```

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux
pip install -r requirements.txt

python python/run_sql.py sql/01_daily_delay_summary.sql   # run a query
python python/delay_report.py                              # same numbers, in pandas
python python/data_quality_checks.py                       # sample-data sanity checks
pytest                                                     # expect 1 failed, 1 skipped on a fresh copy
ruff check .                                               # Python lint
sqlfluff lint sql/                                         # SQL lint
```

DuckDB runs the SQL against the CSVs with zero setup, so the queries can be executed and tested locally. At work the same queries would run in your warehouse (e.g. Databricks SQL); a few date functions differ, and `.sqlfluff` notes where to change the dialect.

## Conventions used in this repo

- **Branches:** `feat/…`, `fix/…`, `chore/…`, `docs/…`, `refactor/…`, `ci/…`. Nobody commits directly to `main`.
- **Commits:** imperative subject line, ≤ 72 characters; the body explains why.
- **Pull requests:** fill the template (what / why / how verified). Squash-merge. Delete the branch.
- **SQL:** one query per file, header comment with purpose and grain, lowercase identifiers, UPPER keywords. See `sql/README.md`.
- **Python:** `ruff` clean; no hard-coded machine paths; secrets from environment variables.
- **Data:** never committed, except the tiny synthetic samples in `data/sample/`. See `data/README.md`.
- **Notebooks:** Databricks source format, or outputs stripped with `nbstripout`.

## Which session touches what

| Session | Files |
|---|---|
| 1 | `LEARNING_PLAN.md`, `sql/README.md` |
| 2 | `README.md`, `.gitignore`, `data/README.md` |
| 3 | `sql/03_top_delay_routes.sql`, `tests/test_queries.py` |
| 4 | any file; the drill is about Git, not the content |
| 5 | `sql/04_audit_findings_by_area.sql` (you create it), `sql/README.md`, `.github/ISSUE_TEMPLATE/` |
| 6 | `exercises/session06/sloppy_delay_report.py`, `python/delay_report.py`, `docs/REVIEW_CHECKLIST.md` |
| 7 | `sql/01_daily_delay_summary.sql`, `python/delay_report.py` |
| 8 | `notebooks/` |
| 9 | `.github/workflows/ci.yml`, `python/data_quality_checks.py`, `.github/dependabot.yml` |
| 10 | `.github/CODEOWNERS`, repo settings |
| 11 | history and tags; no file changes required |
| 12 | `docs/TEAM_GITHUB_NORMS_TEMPLATE.md` (copy into your new repo) |
