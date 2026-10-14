"""Shared project paths and independent snapshot refresh settings."""

from __future__ import annotations

from datetime import timedelta
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "gaming_statistics.db"


def resolve_database_path(value: str | Path | None = None) -> Path:
    """Resolve configured relative paths against the project directory."""
    path = Path(value or os.getenv("GAMING_DASHBOARD_DB") or DEFAULT_DATABASE_PATH).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


def _nonnegative_integer(name: str, default: int) -> int:
    try:
        return max(0, int(os.getenv(name, str(default))))
    except ValueError:
        return default


def live_refresh_interval() -> timedelta:
    return timedelta(minutes=_nonnegative_integer("PLAYER_REFRESH_MINUTES", 15))


def catalog_refresh_interval() -> timedelta:
    return timedelta(hours=_nonnegative_integer("CATALOG_REFRESH_HOURS", 24))
