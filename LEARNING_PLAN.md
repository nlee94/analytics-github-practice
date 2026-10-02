# GitHub for a Working Data Analyst

**A 3-week plan: 12 sessions of about 40 minutes, built around SQL and Python rather than a traditional codebase.**

## Who this is for

You write SQL and Python for a living and need to work the way engineering-minded analytics teams work on GitHub: branches, pull requests, reviews, automated checks, and repos that stay clean of data and secrets. You do not need to become a software engineer.

## How it works

Every session is hands-on inside the practice repo this file ships with (`analytics-github-practice/`). The repo is a tiny, fully synthetic "airline operations analytics" project: two small CSV samples, three SQL queries (one has a bug on purpose), a few Python scripts, a notebook in two formats, and the GitHub plumbing (`.github/`) a real team would have.

By the end you will have created a GitHub repo, made 20-odd commits, opened and merged about 8 pull requests, resolved a merge conflict, wired up CI, and locked down `main`.

**Pace.** 4 sessions a week, about 40 minutes each. Each session has a **Done when** line: stop there even if you didn't finish everything. If life happens, do 2 a week. Order matters more than the calendar.

**Assumptions.** Comfortable with SQL and Python. Git experience anywhere from "none" to "I've clicked Commit in an IDE." Windows or Mac. Python 3.10+. Do all of this in a **personal** GitHub account with the synthetic data provided; never put client code or data in a personal repo.

**Progress tracking.** This file lives in the repo. Tick each session below (`- [x]`) and commit the change. That is real practice.

## Progress

- [ ] Session 0 — Setup
- [ ] Session 1 — Commits
- [ ] Session 2 — Push to GitHub, README, .gitignore
- [ ] Session 3 — Branches and your first pull request
- [ ] Session 4 — Undo and recovery
- [ ] Session 5 — Anatomy of a good analytics PR
- [ ] Session 6 — Being the reviewer
- [ ] Session 7 — Merge conflicts, on purpose
- [ ] Session 8 — Notebooks and Databricks in Git
- [ ] Session 9 — CI: the PR that checks itself
- [ ] Session 10 — Protecting `main`
- [ ] Session 11 — The daily loop, history, and tags
- [ ] Session 12 — Capstone

## What you'll be able to do

1. Work on a branch and open a clear PR, daily, without thinking about it.
2. Review a teammate's SQL or Python PR and leave comments that help.
3. Keep data, credentials, and notebook output out of the repo, every time.
4. Read and modify a GitHub Actions workflow that lints SQL and Python and runs tests on every PR.
5. Connect a repo to Databricks Git folders and push a notebook change through a PR.
6. Recover from the common mistakes: wrong branch, bad commit, merge conflict, committed secret.

## The daily loop you're learning (memorize this)

```bash
git switch main && git pull            # start from the latest
git switch -c feat/short-description   # branch
# ...edit, run, check...
git add -p && git commit -m "..."      # small, deliberate commits
git push -u origin feat/short-description
gh pr create --fill                    # or open the PR on GitHub
# review -> merge -> delete branch
git switch main && git pull
```

`CHEATSHEET.md` (same folder) has every command used below, grouped by "I want to...".

---

## Session 0 — Setup (about 30 min, before Week 1)

1. **Install Git** from git-scm.com. Windows: the installer defaults are fine.
2. **Tell Git who you are** (use the same email as your GitHub account, or GitHub's no-reply address, so commits link to your profile):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   git config --global init.defaultBranch main
   git config --global pull.rebase false
   ```
3. **GitHub account.** Create one if needed and turn on two-factor authentication; GitHub requires it for anyone who contributes code.
4. **GitHub CLI.** Install from cli.github.com, then `gh auth login` (GitHub.com, HTTPS, log in via browser). This also stores your Git credentials, so `git push` just works. SSH keys are the other common route; not needed here.
5. **Editor.** VS Code with the GitLens extension is the usual professional setup. Any editor works.
6. **Set up the practice repo.** Unzip it, open a terminal in the folder, and run:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate         # Windows
   pip install -r requirements.txt
   python python/run_sql.py sql/01_daily_delay_summary.sql
   pytest
   ruff check .
   sqlfluff lint sql/
   ```
   Expected: the query prints a small table, and `pytest` reports **1 failed, 1 skipped**, rest passed. The failure is intentional; it's the bug you fix in Session 3. If `ruff` or `sqlfluff` flag style issues in files you didn't write (tool versions drift), run `ruff check --fix .` and `sqlfluff fix sql/` now, before your first commit.

**Read (10 min).** GitHub Docs → Get started → "Hello World".

**Done when.** `git --version`, `gh auth status`, and the `run_sql.py` command all work.

---

## Week 1 — Git fundamentals on real analytics files

### Session 1 — Commits: turning the folder into a repo

**Concepts.** Working tree → staging area → commit. A commit is a snapshot of everything, with a message. `git status` is your dashboard; `git diff` shows what you changed; `git log` is history.

**Do.**
1. In the repo folder: `git init`, then `git status`. Everything is "untracked."
2. `git add .` then `git status` again. Now it's staged. Notice what is *not* listed (`.venv/`, `__pycache__/`): the `.gitignore` is already working.
3. `git commit -m "Initial commit: synthetic airline ops analytics practice repo"`
4. Tick Sessions 0 and 1 in the Progress list above. `git diff` to see the change, then `git add LEARNING_PLAN.md` and `git commit -m "Mark sessions 0-1 complete"`.
5. `git log --oneline`, then `git show HEAD`. Read what a commit actually contains.
6. Open `sql/README.md` and add your name under **Maintainers**. Stage it with `git add -p` (answer `y` to the hunk). This is how you commit *part* of your changes. Commit.

**Read (15 min).** Pro Git, sections 2.1–2.2 "Recording Changes to the Repository" (git-scm.com/book).

**Done when.** `git log --oneline` shows 3 commits and you can explain `add` vs `commit` in one sentence.

### Session 2 — Push to GitHub, README, and .gitignore

**Concepts.** A remote (`origin`) is just another copy of the repo. `push` sends commits; `pull` fetches and merges. `.gitignore` decides what Git never sees, which makes it the single most important file for data work.

**Do.**
1. Create the GitHub repo straight from the terminal:
   ```bash
   gh repo create analytics-github-practice --public --source=. --remote=origin --push
   ```
   Public means every feature in this plan works on a free account, and the data is synthetic. Use `--private` if you prefer; Session 10's enforcement features then need GitHub Pro.
2. `gh repo view --web`. Look at the file list, the rendered README, the commit count, the **Actions** tab (a workflow already ran; it's red because of the Session 3 bug, ignore it for now).
3. **Data hygiene drill.**
   - Create `data/raw/big_extract.csv` (copy `data/sample/flights_sample.csv` there). `git status` → nothing to commit. Open `.gitignore`, find the lines responsible, and read the comment about why `data/*` is used instead of `data/`.
   - Create a file `.env` containing `DATABRICKS_TOKEN=not-a-real-token`. `git status` → still nothing. This is where real credentials live; code reads them with `os.environ`.
   - Create `outputs/report.xlsx` (any content). Ignored. Outputs are regenerated from code, not stored.
4. Edit `README.md`: replace the maintainer placeholder with your name and today's date. `git commit -am "docs: add maintainer info to README"`, then `git push`. Refresh GitHub.
5. `git remote -v`, then `git log --oneline origin/main`: local and remote now match.

**Read (5 min).** GitHub Docs → "Ignoring files", then `data/README.md` in the repo.

**Done when.** The repo is on GitHub and `.env`, `data/raw/`, `outputs/` never appear in `git status`.

### Session 3 — Branches and your first pull request (fixing the planted bug)

**Concepts.** A branch is a movable label on a commit; creating one is free. Professional rule #1: **nobody commits directly to `main`**. Every change goes through a PR, even your own, even a one-liner. A PR is a request to merge, plus a conversation, plus a permanent record.

**Do.**
1. `git switch -c fix/on-time-pct-excludes-cancelled`
2. `python python/run_sql.py sql/03_top_delay_routes.sql`. The header says cancelled flights are excluded; the numbers say otherwise. `pytest -k cancelled` shows the failing test with the expected counts.
3. Fix the query (one `WHERE` clause in the CTE). `pytest` → all green. `sqlfluff lint sql/`.
4. `git add -p`, then `git commit -m "Exclude cancelled flights from route on-time %"`. Note the message shape: imperative, under 72 characters, says what changed.
5. `git push -u origin fix/on-time-pct-excludes-cancelled`, then `gh pr create --web` (or click the "Compare & pull request" banner on GitHub). The PR template appears. Fill What / Why / How verified; paste `on_time_pct` before and after for one route.
6. On the PR page: read the **Files changed** tab, leave a comment on one line of your own diff, then **Squash and merge** and delete the branch when offered.
7. Back home: `git switch main && git pull && git branch -d fix/on-time-pct-excludes-cancelled`. `git log --oneline` shows one squashed commit. The Actions tab is green now.

**Read (10 min).** GitHub Docs → "About pull requests".

**Done when.** The PR is merged, `pytest` passes on `main`, and local `main` matches GitHub.

### Session 4 — Undo, recover, and the secret you will commit by accident one day

**Concepts.** Undo tools, mild to serious: `git restore <file>` throws away unstaged edits; `git restore --staged <file>` unstages; `git commit --amend` fixes the last *unpushed* commit; `git revert <sha>` adds a new commit that undoes a pushed one (the safe way); `git stash` parks edits when you're on the wrong branch. Leave `git reset --hard` and `git push --force` alone until you understand `git reflog`.

**Do.** All on a branch: `git switch -c chore/undo-drill`.
1. Edit `sql/01_daily_delay_summary.sql` (anything). `git restore sql/01_daily_delay_summary.sql`. Gone.
2. Edit it again, `git add` it, then `git restore --staged sql/01_daily_delay_summary.sql`. Still edited, no longer staged. Commit it with a typo in the message, then `git commit --amend -m "Tweak daily summary comment"`.
3. Wrong-branch drill: `git switch main`, edit `README.md`, "realize" you're on `main`. `git stash`, `git switch chore/undo-drill`, `git stash pop`. Commit.
4. Secret drill: create `settings.py` containing `DATABRICKS_TOKEN = "dapi-not-a-real-token-123"`. Commit and push. Now `git revert HEAD` and push. Open the branch's commit list on GitHub: the token is still readable in the earlier commit. Reverting doesn't unpublish. A real leaked token gets **rotated** immediately, then the branch and PR get deleted, then `.gitignore` gets fixed so it can't recur. (GitHub's push protection blocks many real token formats; don't rely on it.)
5. `git log --oneline --graph --all` and `git reflog`. Git kept everything, including the amended commit.
6. Close the loop: push, open a PR for the drill branch, and **close it without merging**. Delete the branch on GitHub and locally (`git branch -D chore/undo-drill`; capital D because it was never merged).

**Read (10 min).** Pro Git 2.4 "Undoing Things". Skim GitHub Docs → "Removing sensitive data from a repository" so you know it exists.

**Done when.** You can do drills 1–4 with the cheat sheet open and without hesitating.

---

## Week 2 — Working like a team

### Session 5 — Anatomy of a good analytics PR (issue → branch → commits → PR)

**Concepts.** Small PRs get reviewed; big ones get rubber-stamped. A PR description answers What / Why / How I verified it; for analytics that means query output or row counts, before and after. Commit messages: imperative subject line, body explains *why*. `Closes #12` in the description links the issue and closes it on merge.

**Do.**
1. On GitHub, open an Issue using the **Analysis request** template: "Open audit findings by area and severity." Definition: one row per `area` × `severity`, count of findings whose status is not `Closed`, sorted by area then severity. Note the issue number.
2. `git switch main && git pull && git switch -c feat/audit-findings-by-area`
3. Write `sql/04_audit_findings_by_area.sql` following the header convention in `sql/README.md`. Run it with `run_sql.py`. `pytest`: the previously skipped test now runs and checks your column names (`area`, `severity`, `open_findings`) and the total.
4. Two logical commits: the query, then the catalog row in `sql/README.md`. Push. `gh pr create --web`. In the description, paste the output table and write `Closes #<number>`.
5. Squash and merge. Watch the issue close itself. `git switch main && git pull`.

**Read (10 min).** "How to Write a Git Commit Message" (cbea.ms/git-commit), the seven rules. GitHub Docs → "Linking a pull request to an issue".

**Done when.** The issue shows as closed by your PR and `pytest` reports 0 skipped.

### Session 6 — Being the reviewer

**Concepts.** Review is where teams catch wrong grain, silent NULL handling, hard-coded paths, and leaked secrets before they reach a dashboard. Comment types: **blocking** (must fix), **suggestion** (GitHub's "Add a suggestion" lets the author accept with one click), **question**, **nit**. Outcomes: Comment, Approve, Request changes. Reviewing well is the fastest way to be trusted with more.

**Do.**
1. Play the careless teammate: `git switch -c feat/refactor-delay-report`, copy `exercises/session06/sloppy_delay_report.py` over `python/delay_report.py`, commit "Refactor delay report", push, open a PR. Notice CI goes red; a reviewer would see that first.
2. Switch hats. With `docs/REVIEW_CHECKLIST.md` open, review the PR on GitHub. Find at least five problems (there are more). Leave inline comments, make at least two of them **suggestions**, and finish with **Request changes**.
3. Switch back. Accept one suggestion with **Commit suggestion** (a commit made from the browser), then `git pull` the branch locally and decide what to do with the rest.
4. Decide the outcome: fix everything and merge, or close without merging and keep the original. Closing is a legitimate result of review. Either way, `main` must end with a correct `delay_report.py` and `pytest` green.

**Read (15 min).** Google's engineering practices: "The Standard of Code Review" and "What to look for in a code review" (google.github.io/eng-practices/review).

**Done when.** You left a review with inline comments, at least one suggestion was applied via the button, and you used Request changes.

### Session 7 — Merge conflicts, on purpose

**Concepts.** A conflict happens when two branches change the same lines and Git won't guess. It's normal, it's local, and it's undoable. Prevention: pull `main` often, keep branches short-lived, keep PRs small.

**Do.**
1. `git switch main && git pull`. Branch A: `git switch -c feat/delay-threshold-10`. The delay definition lives in two places: the `flights_delayed` line of `sql/01_daily_delay_summary.sql` and `DELAY_THRESHOLD_MIN` in `python/delay_report.py`. Change both from 15 to 10 (and the note in the SQL header). `pytest` proves they still agree. Commit, push, PR, merge.
2. Do **not** pull. `git switch main`, then Branch B: `git switch -c refactor/count-instead-of-sum`. On that same `flights_delayed` line, change `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` to `COUNT(CASE WHEN ... THEN 1 END)`. Commit, push, open the PR. GitHub: "This branch has conflicts that must be resolved."
3. Resolve locally: `git fetch origin`, then `git merge origin/main`. Open the file, find `<<<<<<<`, `=======`, `>>>>>>>`. Keep both intentions (`> 10` and `COUNT`), delete the markers. `python python/run_sql.py sql/01_daily_delay_summary.sql` and `pytest` to prove it works. `git add`, `git commit` (accept the default message), push. The PR is mergeable now; merge it.
4. Repeat 1–2 with two different edits to the `-- Purpose:` comment line, and this time use GitHub's **Resolve conflicts** button in the browser.

**Read (10 min).** GitHub Docs → "Resolving a merge conflict on GitHub" and "...using the command line".

**Done when.** Both PRs merged, `pytest` green on `main`, and `<<<<<<<` no longer scares you.

### Session 8 — Notebooks and Databricks in Git

**Concepts.** An `.ipynb` is JSON that includes cell *outputs*, so diffs are unreadable and query results (possibly sensitive) get committed. Two fixes: strip outputs before commit (`nbstripout`), or use Databricks' source format (a `.py` with `# COMMAND ----------` separators), which is what `notebooks/explore_delays.py` is. Databricks **Git folders** clone a GitHub repo into your workspace; you branch, commit, and push from the Databricks UI and review PRs on GitHub. Secrets go in Databricks secret scopes or Key Vault, never in notebooks.

**Do.**
1. Local: `git switch -c chore/strip-notebook-outputs`. Open `notebooks/explore_delays.ipynb` in a text editor and find the outputs baked in. Run `nbstripout notebooks/explore_delays.ipynb`, then `git diff --stat` and `git diff`. Then `nbstripout --install` so it happens automatically in this repo (`nbstripout --status` to confirm). Commit, PR, merge.
2. Databricks, if you have a workspace (Free Edition or your learning workspace): Settings → Linked accounts → add a GitHub credential. Workspace → Create → Git folder → paste the repo URL. From the Git dialog, create branch `feat/notebook-by-aircraft-type`, open `notebooks/explore_delays.py`, do the exercise in its last cell, **Commit & push**, open the PR on GitHub, merge, then **Pull** in Databricks and confirm `main` has the change. Notice how readable the `.py` diff is on GitHub.
3. No workspace? Do step 2's exercise locally on the `.py` file. The point is that a notebook change goes through a branch and a PR like everything else.

**Read (10 min).** Databricks docs → "Git integration for Databricks Git folders" (skim) and the best-practices page's advice on what to commit.

**Done when.** One notebook change went through a PR, and outputs are stripped on commit.

---

## Week 3 — Professional polish

### Session 9 — CI: the PR that checks itself

**Concepts.** GitHub Actions runs a workflow (YAML in `.github/workflows/`) on events such as `pull_request`. Ours: install dependencies → `ruff` (Python lint) → `sqlfluff` (SQL lint) → `pytest`. Results show as **checks** on the PR. Keep CI under two minutes or people start ignoring it. Dependabot keeps the actions and packages current through automatic PRs.

**Do.**
1. It has been running since Session 2. Open the **Actions** tab and read the log of the latest run. Then read `.github/workflows/ci.yml`; every line is commented.
2. `git switch -c ci/add-data-quality-step`. Add a step after the tests that runs `python python/data_quality_checks.py`. Push, open the PR, click **Details** on the check and watch it run. Merge.
3. Break it on purpose: `git switch -c chore/lint-fail-demo`, add `import os` (unused) to `python/run_sql.py`, push, open the PR. Red ✗, with ruff's message in the log. Fix it (`ruff check --fix .`), push, watch it go green. Close the PR without merging.
4. Read `.github/dependabot.yml`. Within a month you'll get automatic PRs bumping versions; reviewing and merging those is a normal chore.

**Read (15 min).** GitHub Docs → "Understanding GitHub Actions".

**Done when.** You have seen a check fail and pass, and CI runs a step you added.

### Session 10 — Protecting `main`: rulesets, CODEOWNERS, permissions

**Concepts.** Branch rulesets enforce the norms: require a PR, require passing checks, require review, block force-pushes. `CODEOWNERS` auto-requests reviewers by path (the `sql/` folder → the analytics leads). Repository roles: Read, Triage, Write, Maintain, Admin. Admins go through PRs too; the rules are for everyone. (Rulesets and CODEOWNERS work on public repos with a free account; private repos need GitHub Pro.)

**Do.**
1. Settings → Rules → Rulesets → New branch ruleset. Name `protect-main`, target the default branch, enable **Require a pull request before merging** (leave required approvals at 0: GitHub won't let you approve your own PR, so a solo repo can't satisfy 1), **Require status checks to pass** (add `checks`), and **Block force pushes**. Enforcement: Active.
2. Test it: on `main`, edit README, commit, `git push` → rejected. `git reset --soft HEAD~1` (undo the commit, keep the edit), branch, PR, merge.
3. Edit `.github/CODEOWNERS` to use your GitHub username. Open a PR that touches `sql/` and note the automatic reviewer request.
4. Settings → General → enable **Automatically delete head branches**. Settings → Collaborators → read the role descriptions.

**Read (10 min).** GitHub Docs → "About rulesets" and "About code owners".

**Done when.** A direct push to `main` is rejected and PRs need green checks.

### Session 11 — The daily loop, history as a tool, and tags

**Concepts.** Git history answers analyst questions: *when did this metric definition change, and why?* (`git log -p`, `git log -S`, `git blame`). Tags mark "the version we sent to leadership." Issues track requests; a Projects board is optional.

**Do.**
1. Run the daily loop (top of this file) twice with tiny changes, timed. Target: under 5 minutes each, PR included.
2. `git log --oneline --graph`. `git log -S "NOT cancelled" -- sql/03_top_delay_routes.sql` finds the commit that added the fix. `git blame sql/01_daily_delay_summary.sql`. `git log -p --follow python/delay_report.py`.
3. `git tag -a v2026.09-ops-review -m "Numbers shown at the September ops review"`, then `git push origin --tags`. On GitHub → Releases → draft a release from the tag; release notes are "what changed." Later, `git switch --detach v2026.09-ops-review` reruns exactly those queries; `git switch main` comes back.
4. `gh` speed-ups: `gh pr status`, `gh pr checkout <number>`, `gh pr view --web`, `gh issue list`.

**Read (5 min).** GitHub CLI manual → `gh pr`.

**Done when.** The loop feels boring (that's the goal) and you can find when a line changed without asking anyone.

### Session 12 — Capstone: set up a real repo the right way

**Do.** Create a brand-new repo for something real: a personal analysis, or the structure you'd propose for a team. Include everything this plan taught: a README with a "how to run" section, a data-aware `.gitignore`, `sql/` + `python/` + `tests/` + `notebooks/` layout, PR template, CODEOWNERS, CI, a ruleset on `main`, and a first merged PR. Then write `docs/TEAM_GITHUB_NORMS.md` from the template in the practice repo: one page a team could adopt. That document is a real consulting deliverable; most analytics teams don't have one.

**Done when.** Someone else could clone your repo and open a correct PR using only the README.

---

## After Week 3: keep it alive (5 min a day)

- Every change on a branch, even solo. Use a `wip/` prefix for scratch branches you may throw away.
- End of week: `git log --since="1 week ago" --oneline` is your status-report draft.
- Watch how others do it: pick a well-run public analytics repo (dbt Labs' `jaffle-shop`, or any Databricks solution accelerator on GitHub) and read five merged PRs.
- Stretch topics, only when a real need appears: interactive rebase (`git rebase -i`) for cleaning up a branch, `git worktree`, GitHub Codespaces, pre-commit hooks, dbt projects on GitHub, Databricks bundles (`databricks bundle`) for deploying jobs from a repo, signed commits.

## Questions to ask in your first week on any engagement

1. Which host: GitHub, GitHub Enterprise, Azure DevOps, GitLab? Same Git underneath, different UI and PR vocabulary.
2. Branch naming, PR template, who reviews analytics code, and which branches are protected?
3. Where do notebooks live: Databricks Git folders, or loose in the workspace? Source format or `.ipynb`?
4. How are secrets handled (secret scopes, Key Vault), and is push protection on?
5. Is there CI for SQL and Python? A dbt or data-engineering repo worth reading?
6. Where do one-off queries go? A dated `adhoc/` folder in the repo beats "nowhere."

## Resources (all free)

- **Pro Git** — git-scm.com/book — chapters 2, 3, and 6.
- **GitHub Docs** — docs.github.com/en/get-started, plus the pages named in each session.
- **GitHub Skills** — skills.github.com — "Introduction to GitHub" and "Review pull requests" are interactive and about 30 minutes each; fine substitutes for a session when you want a change of pace.
- **Oh Shit, Git!?!** — ohshitgit.com — plain-language recovery recipes.
- **Learn Git Branching** — learngitbranching.js.org — visual sandbox; do the introduction sequence before Session 3 if branches feel abstract.
- **Databricks docs** — "Git integration for Databricks Git folders".
