# How we use GitHub — <team name>

*One page. If it doesn't fit on one page, it's a manual, not a set of norms.*

## Repos

- `<repo-1>` — <what lives here>. `<repo-2>` — <what lives here>. `adhoc/` folders take dated one-offs.
- Never in a repo: data extracts, credentials, notebook outputs, Excel deliverables.
  Those live in <warehouse / lakehouse / SharePoint / secret scope>.

## Branches

- `main` is protected: no direct pushes; PR with green CI required; <N> approval(s).
- Names: `feat/…`, `fix/…`, `chore/…`, `adhoc/YYYY-MM-DD-topic`. Include the ticket id when there is one.
- Branches live less than a week. Merge `main` into long-running branches daily.

## Pull requests

- Use the template: what / why / how verified (query output or row counts, before and after).
- Aim for under 400 changed lines; split otherwise.
- CODEOWNERS auto-assigns reviewers; anyone may review. First review within one business day.
- The author merges after approval, using squash merge. Branches are deleted on merge.

## Commits

- Imperative subject, 72 characters or fewer; body explains why. Squash on merge, so branch
  commits can be messy.

## SQL and Python

- SQL: one query per file, header comment (purpose, grain, notes), lowercase identifiers,
  UPPER keywords, `sqlfluff` clean.
- Python: `ruff` clean, no machine-specific paths, secrets from the environment or secret scopes.
- Notebooks: Databricks source format, or `nbstripout` installed. No outputs committed.

## Automation

- CI runs lint and tests on every PR. Dependabot PRs are reviewed weekly by <owner>.

## Snapshots

- Tag when numbers go to leadership: `vYYYY.MM-<audience>`, with a release note saying what changed.

## Owners

- Repo admins: <names>. Questions: <channel>.
