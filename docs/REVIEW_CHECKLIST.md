# Review checklist for analytics PRs

Before anything else, read the PR description. If you can't tell *what* changed, *why*,
and *how it was verified*, ask for that first; the code can wait.

## Correctness (blocking)

- **Grain.** One row per what? Does the `GROUP BY` / join actually produce that grain? Any
  fan-out from joins? (Ask for row counts before and after.)
- **Filters.** Are cancelled / test / deleted / duplicate rows handled the way the definition says?
- **NULLs.** `fillna(0)`, `COALESCE`, `WHERE x != 'y'` (which drops NULLs): deliberate or accidental?
- **Definitions in two places** (SQL and Python, or two queries): do they still agree? Is there a test?
- **Dates.** Time zones, inclusive vs exclusive ends, hard-coded "as of" dates.
- **Verification.** Were the numbers checked against something known (a dashboard, last week's run)?

## Safety (blocking)

- Tokens, passwords, connection strings, or usernames in code, config, or notebook output.
- Data files, exports, or notebook outputs committed.
- Hard-coded paths to someone's laptop (`C:/Users/...`, `/Users/...`, `Downloads`, `Desktop`).

## Reliability

- Bare `except:` or swallowed errors; silent fallbacks to a different data source.
- Scripts that write to fixed locations or overwrite outputs without saying so.
- `SELECT *` feeding anything downstream (a schema change breaks it silently).
- Does CI pass? If not, why is the PR open?

## Readability

- Would a new team member understand this in six months? Names, a header with purpose and grain,
  CTEs over nested subqueries, consistent case, one statement per line.
- Magic numbers named (thresholds, cutoffs) and defined once.
- The PR is small enough to actually read. If not, ask to split it.

## Housekeeping

- Lint and tests pass. New queries added to the catalog. Unused imports and dead code removed.
- Commit messages and PR title say what changed.

## How to write the comments

- **Blocking:** "This includes cancelled flights in the average; the header says they're excluded.
  Needs `WHERE NOT cancelled`."
- **Suggestion:** use the "Add a suggestion" button so the author can commit your fix in one click.
- **Question:** "Is the 15-minute threshold from the ops standard, or chosen here?"
- **Nit:** "nit: `f` → `flights`". Say it's a nit, so the author knows it's optional.
- Say what's good, too. A review is not only a list of defects.
- Approve when you'd be comfortable seeing this run in production with your name next to it.
