"""Timezone helpers used by the dashboard and refresh services."""

from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo


THAILAND_TIMEZONE = ZoneInfo("Asia/Bangkok")


def thailand_now() -> datetime:
    """Return the current timezone-aware time in Thailand."""
    return datetime.now(THAILAND_TIMEZONE)


def parse_timestamp(value: str) -> datetime | None:
    """Parse an ISO timestamp, treating legacy timezone-less values as UTC."""
    try:
        timestamp = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return timestamp.replace(tzinfo=UTC) if timestamp.tzinfo is None else timestamp


def format_thailand_timestamp(value: str) -> str:
    """Format an ISO timestamp in Thailand time, to second precision."""
    timestamp = parse_timestamp(value)
    if timestamp is None:
        return value
    return f"{timestamp.astimezone(THAILAND_TIMEZONE):%Y-%m-%d %H:%M:%S} UTC+7"
