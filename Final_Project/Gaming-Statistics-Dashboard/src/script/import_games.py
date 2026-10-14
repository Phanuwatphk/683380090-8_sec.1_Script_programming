"""Import additional RAWG pages into the dashboard's SQLite database."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import Full, Queue
import sys
from threading import Event
from typing import Callable

if not __package__:  # Support direct execution from any working directory.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.config import PROJECT_ROOT, resolve_database_path
from src.api.rawg_api import RAWG_MAX_PAGE_SIZE, RawgApiClient, RawgApiError
from src.database.database import DatabaseError, GameDatabase
from src.services.game_service import GameService
from src.utils.data_processing import process_games

# Inclusive [first_page, last_page]; one page-fetch worker per range.
PAGE_RANGES = [
    [101, 250],
    [251, 500],
    [501, 750],
    [751, 1000],
]


def validate_ranges(page_ranges: list[list[int]]) -> None:
    if not page_ranges:
        raise ValueError("PAGE_RANGES must contain at least one range")
    for item in page_ranges:
        if len(item) != 2 or any(type(value) is not int for value in item):
            raise ValueError("Each page range must contain two integers")
        if item[0] < 1 or item[1] < item[0]:
            raise ValueError("Page ranges must be positive and ascending")
    ordered = sorted(page_ranges)
    if any(current[0] <= previous[1] for previous, current in zip(ordered, ordered[1:])):
        raise ValueError("Page ranges must not overlap")


def import_ranges(
    client: RawgApiClient, database: GameDatabase, page_ranges: list[list[int]], *,
    client_factory: Callable[[], RawgApiClient] | None = None,
) -> tuple[int, int]:
    """Fetch ranges concurrently and save completed pages through one writer.

    A bounded queue prevents buffering the entire catalog while the writer
    saves each page. Each fetch worker owns its HTTP session. Developer
    detail requests are skipped for bulk imports.
    """
    validate_ranges(page_ranges)
    workers = len(page_ranges)
    factory = client_factory or (lambda: RawgApiClient(api_key=client.api_key))
    service = GameService(client, database)
    queue = Queue(maxsize=workers * 2)
    stop = Event()

    def publish(message) -> None:
        while not stop.is_set():
            try:
                queue.put(message, timeout=0.1)
                return
            except Full:
                continue

    def fetch_range(first: int, last: int) -> None:
        worker_client = None
        try:
            worker_client = factory()
            for page in range(first, last + 1):
                if stop.is_set():
                    break
                raw_games = worker_client.fetch_games(RAWG_MAX_PAGE_SIZE, ordering="-added", page=page)
                publish((page, raw_games, None))
                if len(raw_games) < RAWG_MAX_PAGE_SIZE:
                    break
        except Exception as error:
            publish((None, None, error))
        finally:
            try:
                if worker_client is not None:
                    worker_client.session.close()
            finally:
                publish(None)

    added = updated = finished = 0
    print(f"Fetching {page_ranges} with {workers} page workers", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for first, last in page_ranges:
            executor.submit(fetch_range, first, last)
        try:
            while finished < workers:
                message = queue.get()
                if message is None:
                    finished += 1
                    continue
                page, raw_games, error = message
                if error is not None:
                    raise error
                existing = database.get_games_by_ids(game["game_id"] for game in process_games(raw_games))
                games = service.save_rawg_games(raw_games)
                page_added = len(games) - len(existing)
                added += page_added
                updated += len(existing)
                print(f"Page {page}: {page_added} added, {len(existing)} updated", flush=True)
        finally:
            stop.set()
    return added, updated


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def import_games(
    client: RawgApiClient,
    database: GameDatabase,
    *,
    start_page: int,
    pages: int,
) -> tuple[int, int]:
    """Save each page immediately; repeated runs update existing RAWG IDs."""
    database.initialize()
    service = GameService(client, database)
    added = updated = 0
    for page in range(start_page, start_page + pages):
        raw_games = client.fetch_games(RAWG_MAX_PAGE_SIZE, ordering="-added", page=page)
        existing = database.get_games_by_ids(game["game_id"] for game in process_games(raw_games))
        games = service.save_rawg_games(raw_games)
        page_added = len(games) - len(existing)
        added += page_added
        updated += len(existing)
        print(f"Page {page}: {page_added} added, {len(existing)} updated", flush=True)
        if len(raw_games) < RAWG_MAX_PAGE_SIZE:
            break
    return added, updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-page", type=positive_int, help="Override PAGE_RANGES with one sequential range (default start: 1)")
    parser.add_argument("--pages", type=positive_int, help="Sequential override page count (default count: 5)")
    parser.add_argument("--database", help="SQLite path; relative paths use the project root")
    args = parser.parse_args(argv)
    # Construct the client first so .env configuration is available for the DB path.
    client = RawgApiClient()
    path = resolve_database_path(args.database)
    print(f"Database: {path}", flush=True)
    try:
        if args.start_page is not None or args.pages is not None:
            added, updated = import_games(
                client, GameDatabase(path), start_page=args.start_page or 1,
                pages=args.pages or 5,
            )
        else:
            added, updated = import_ranges(client, GameDatabase(path), PAGE_RANGES)
    except (RawgApiError, DatabaseError, ValueError) as error:
        print(f"Import stopped: {error}. Pages already saved remain in the database.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Import interrupted. Pages already saved remain in the database.", file=sys.stderr)
        return 130
    print(f"Done: {added} added, {updated} updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
