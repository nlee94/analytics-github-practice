"""Repo-relative paths, defined once so no script hard-codes a machine-specific path."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = REPO_ROOT / "data" / "sample"
SQL_DIR = REPO_ROOT / "sql"
