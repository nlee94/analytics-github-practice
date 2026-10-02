# Git & GitHub cheat sheet for analysts

Organized by what you're trying to do. Commands assume Git 2.23+ (`switch`/`restore`) and the GitHub CLI (`gh`).

## One-time setup

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"     # same email as GitHub
git config --global init.defaultBranch main
git config --global pull.rebase false                # plain merges; simplest mental model
gh auth login                                        # GitHub.com, HTTPS, browser
git config --global core.editor "code --wait"        # optional: VS Code for commit messages
```

## Every day

```bash
git switch main && git pull                 # start from the latest main
git switch -c feat/short-description        # new branch
git status                                  # your dashboard; run it constantly
git add -p                                  # stage hunk by hunk (y/n/s to split)
git commit -m "Imperative subject line"
git push -u origin feat/short-description   # -u once; plain `git push` after that
gh pr create --fill                         # PR from the terminal (--web to use the browser form)
gh pr view --web                            # open the PR page
# ...review, merge on GitHub (squash), delete branch...
git switch main && git pull
git branch -d feat/short-description        # -D if it was never merged
```

## Starting from something that already exists

```bash
git clone https://github.com/<org>/<repo>.git        # copy a repo
gh repo clone <org>/<repo>                           # same, via gh
gh pr checkout 42                                    # get a colleague's PR branch locally
git fetch origin && git switch -c feat/x origin/feat/x   # manual version of the above
```

## Looking at what changed

```bash
git diff                          # unstaged changes
git diff --staged                 # what will go into the next commit
git diff main...feat/x            # everything the branch changed vs main
git log --oneline --graph --all   # history as a picture
git log -p -- sql/01_daily_delay_summary.sql   # every change to one file, with diffs
git log -S "NOT cancelled" -- sql/            # which commit added/removed that text
git blame sql/03_top_delay_routes.sql         # who changed each line, and when
git show <sha>                    # one commit in full
git show <sha>:sql/01_daily_delay_summary.sql  # the file as it was at that commit
```

## Undo (mild to serious)

| I want to... | Command | Safe? |
|---|---|---|
| Throw away my edits to a file | `git restore <file>` | Edits are gone for good |
| Unstage a file (keep the edits) | `git restore --staged <file>` | Yes |
| Fix the last commit's message | `git commit --amend -m "..."` | Only if not pushed yet |
| Add a forgotten file to the last commit | `git add <file> && git commit --amend --no-edit` | Only if not pushed yet |
| Undo the last commit but keep the changes | `git reset --soft HEAD~1` | Yes (local) |
| Undo a commit that's already pushed | `git revert <sha>` | Yes: makes a new commit |
| Park my edits and come back later | `git stash` / `git stash pop` | Yes |
| Find a commit I "lost" | `git reflog` | Yes, read-only |
| Wipe everything back to the last commit | `git reset --hard` | Destructive: last resort |

A `git revert` does not remove anything from history. A leaked secret must be **rotated**; reverting only stops the bleeding going forward.

## I'm on the wrong branch

```bash
git stash                      # park the edits
git switch correct-branch      # or: git switch -c new-branch
git stash pop                  # bring them back
```

If you already committed on `main` by accident (and haven't pushed):

```bash
git branch feat/oops           # a branch pointing at your commit
git reset --hard origin/main   # move main back to what GitHub has
git switch feat/oops           # carry on from the branch
```

## Merge conflicts

```bash
git fetch origin
git merge origin/main          # or: git pull origin main
# edit files: keep what you mean, delete <<<<<<< ======= >>>>>>> markers
python python/run_sql.py sql/<file>.sql   # prove it still runs
pytest
git add <file>
git commit                     # accept the default merge message
git push
```

`git merge --abort` backs out if you get lost. The **Resolve conflicts** button on the PR page does the same thing in a browser for simple cases.

## Keeping a long-lived branch current

```bash
git switch feat/x
git merge main                 # bring main's changes into your branch
# or, if the team prefers linear history:
git rebase main                # replays your commits on top of main; then `git push --force-with-lease`
```

Never rebase a branch someone else has checked out. When unsure, merge.

## Tags and releases

```bash
git tag -a v2026.09-ops-review -m "Numbers shown at the September ops review"
git push origin --tags
git switch --detach v2026.09-ops-review    # look around at that snapshot
git switch main                            # come back
gh release create v2026.09-ops-review --generate-notes
```

## GitHub CLI grab bag

```bash
gh repo create <name> --public --source=. --remote=origin --push
gh pr status                   # my PRs, PRs I'm reviewing
gh pr list / gh pr view 42 / gh pr checks 42 / gh pr merge 42 --squash
gh issue create / gh issue list
gh run list / gh run view --log   # Actions runs
gh browse                      # open the repo in a browser
```

## What never goes in a repo (and what to do instead)

| Never commit | Do this instead |
|---|---|
| Data extracts, exports, parquet, xlsx | Keep them in the warehouse/lakehouse; commit the query that produces them; commit tiny synthetic samples only |
| Tokens, passwords, connection strings | `.env` locally (git-ignored), read via `os.environ`; Databricks secret scopes / Key Vault at work |
| Notebook outputs | `nbstripout`, or Databricks source-format `.py` notebooks |
| Files > 50 MB | GitHub warns at 50 MB and blocks at 100 MB; use Git LFS or, better, don't version data |
| Hard-coded paths to your laptop | Paths relative to the repo root, or config/parameters |
| `report_final_v2_FINAL.xlsx` | The report is regenerated from code; version the code |

## Branch names and commit messages

- Branches: `feat/…`, `fix/…`, `chore/…`, `docs/…`, `refactor/…`, `adhoc/2026-09-24-topic`. Add the ticket number if there is one: `feat/AA-123-audit-aging`.
- Commit subject: imperative mood, ≤ 72 characters, no trailing period. "Exclude cancelled flights from on-time %" not "fixed stuff" or "Fixing the on-time query."
- Body (optional): *why*, not what. The diff already shows what.
- PR description: What / Why / How verified. For analytics, "how verified" means query output or row counts, before and after.

## .gitignore patterns worth knowing

```gitignore
data/*            # ignore everything under data/...
!data/README.md   # ...except these. (Would NOT work with `data/` — a fully ignored
!data/sample/     #    directory can't have exceptions inside it.)
*.parquet         # any parquet file, anywhere
outputs/          # the whole folder
.env              # exact file name
```

`git status --ignored` shows what is being ignored. `git check-ignore -v <path>` tells you which rule matched.

## Glossary

- **origin** — the default name for the remote copy of the repo (on GitHub).
- **HEAD** — the commit you're currently on; usually the tip of your branch.
- **upstream / tracking branch** — the remote branch your local branch pushes to and pulls from (`-u` sets it).
- **fast-forward** — a merge that just moves the label forward because nothing diverged.
- **squash merge** — combine all the branch's commits into one on `main`. Most analytics teams use this.
- **rebase** — replay your commits on top of another branch; rewrites history, so only on your own unshared branches.
- **detached HEAD** — you checked out a commit or tag rather than a branch. Fine for looking; make a branch before committing.
- **fork** — your own copy of someone else's repo on GitHub (open source workflow; rarely needed inside a company).
- **draft PR** — a PR marked "not ready"; useful for early feedback on an approach.
- **status check** — a CI result attached to a commit; rulesets can require it to pass before merge.
