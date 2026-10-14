"""Service layer coordinating RAWG, data processing, and SQLite."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from math import ceil
from typing import Any, Callable
from threading import Lock

if __package__ and __package__.startswith("src."):
    from src.api.rawg_api import RAWG_MAX_PAGE_SIZE, RawgApiClient, RawgApiError
    from src.api.steam_api import SteamApiClient, SteamApiError, SteamConnectionError
    from src.database.database import GameDatabase
    from src.utils.data_processing import process_games
    from src.utils.time_utils import thailand_now
else:  # Supports imports when Streamlit runs src/app.py as a script.
    from api.rawg_api import RAWG_MAX_PAGE_SIZE, RawgApiClient, RawgApiError
    from api.steam_api import SteamApiClient, SteamApiError, SteamConnectionError
    from database.database import GameDatabase
    from utils.data_processing import process_games
    from utils.time_utils import thailand_now

PAGE_SIZE = 100
LIVE_TOP_GAMES_LIMIT = PAGE_SIZE

# Shared lock for all GameService instances in this Streamlit process.
# This prevents multiple Streamlit sessions/tabs from refreshing
# the same shared database snapshot at the same time.
_LIVE_TOP_REFRESH_LOCK = Lock()
_CATALOG_REFRESH_LOCK = Lock()
_PLAYERS_REFRESH_LOCK = Lock()
_RAWG_IMPORT_LOCK = Lock()

@dataclass(frozen=True)
class SyncResult:
    """A concise result for the dashboard after synchronizing RAWG data."""

    fetched: int
    saved: int


@dataclass(frozen=True)
class PlayerRefreshResult:
    """Outcome of one refresh pass over Steam-compatible games."""

    updated: int
    unavailable: int
    failed: int
    skipped: bool = False


@dataclass(frozen=True)
class LiveTopRefreshResult:
    """Outcome of refreshing the Steam-ranked games used on the Home page."""

    saved: int
    skipped: bool = False


@dataclass(frozen=True)
class CatalogRefreshResult:
    """Outcome of refreshing the locally stored RAWG discovery catalogue."""

    saved: int
    skipped: bool = False


class GameService:
    """Provide dashboard-ready game data without exposing API or SQL details."""

    def __init__(
        self,
        api_client: RawgApiClient,
        database: GameDatabase,
        steam_client: SteamApiClient | None = None,
    ) -> None:
        self.api_client = api_client
        self.database = database
        self.steam_client = steam_client or SteamApiClient()
        self.database.initialize()

    def sync_games(self, page_size: int = PAGE_SIZE) -> SyncResult:
        """Fetch RAWG data, normalize it, and save it to SQLite."""
        raw_games = self.api_client.fetch_games(page_size)
        games = self.save_rawg_games(raw_games)
        saved = len(games)
        return SyncResult(fetched=len(raw_games), saved=saved)

    def get_games(self) -> list[dict[str, Any]]:
        """Retrieve all games currently saved in SQLite."""
        return self.database.get_games()

    def get_game_details(self, game_id: int, *, fetch_developers: bool = True) -> dict[str, Any] | None:
        """Load missing developer data only for the selected RAWG game.

        Successful empty responses are cached as well. Failed requests leave
        the cache unset, so a later visit can try again.
        """
        with _RAWG_IMPORT_LOCK:
            games = self.database.get_games_by_ids([game_id])
            if not games:
                return None
            game = games[0]
            if (
                fetch_developers and game_id > 0
                and not game["developers"] and not game["developers_updated_at"]
            ):
                details = process_games([self.api_client.fetch_game_details(game_id)])
                if not details or details[0]["game_id"] != game_id:
                    raise RawgApiError("RAWG returned invalid game details")
                updated_at = thailand_now().isoformat()
                self.database.save_developers(game_id, details[0]["developers"], updated_at)
                game["developers"] = details[0]["developers"]
                game["developers_updated_at"] = updated_at
            return game

    def save_rawg_games(
        self, raw_games: list[dict[str, Any]], *,
        catalog_start_rank: int | None = None, replace_snapshot: bool = False,
    ) -> list[dict[str, Any]]:
        """Normalize and save list data without extra developer requests.

        Preserve cached developer data; get_game_details loads missing names
        only when someone opens the selected game.
        """
        with _RAWG_IMPORT_LOCK:
            games = list({game["game_id"]: game for game in process_games(raw_games)}.values())
            cached = {game["game_id"]: game for game in self.database.get_games_by_ids(game["game_id"] for game in games)}
            raw_by_id = {game["id"]: game for game in raw_games if isinstance(game, dict) and isinstance(game.get("id"), int)}
            updated_at = thailand_now().isoformat()
            for game in games:
                previous = cached.get(game["game_id"])
                if "developers" in raw_by_id.get(game["game_id"], {}):
                    game["developers_updated_at"] = updated_at
                elif previous and previous["developers_updated_at"]:
                    game["developers"] = previous["developers"]
                    game["developers_updated_at"] = previous["developers_updated_at"]
            if catalog_start_rank is None:
                self.database.insert_games(games, updated_at=updated_at)
            else:
                self.database.save_catalog_games(
                    games, updated_at=updated_at, start_rank=catalog_start_rank,
                    replace_snapshot=replace_snapshot,
                )
            return games

    def get_live_top_games(self) -> list[dict[str, Any]]:
        """Retrieve the current Home-page ranking from SQLite."""
        return self.database.get_live_top_games()

    def get_popular_games(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Retrieve locally stored popular RAWG games for the Home page."""
        return self.database.get_popular_games(limit=limit)

    def search_games(self, search_term: str) -> list[dict[str, Any]]:
        """Find games from SQLite; a blank search deliberately returns no results."""
        return self.database.search_games(search_term)

    def search_or_import_games(
        self, search_term: str, page_size: int = PAGE_SIZE
    ) -> list[dict[str, Any]]:
        """Search SQLite first, fetching and saving RAWG results only on a miss."""
        local_games = self.database.search_games(search_term)
        if local_games:
            return local_games
        return self.search_and_import_games(search_term, page_size)

    def search_and_import_games(self, search_term: str, page_size: int = PAGE_SIZE) -> list[dict[str, Any]]:
        """Find titles in RAWG and make their normalized data available locally."""
        raw_games = _fetch_rawg_window(
            lambda rawg_page: self.api_client.search_games(
                search_term, RAWG_MAX_PAGE_SIZE, page=rawg_page
            ),
            display_page=1,
            page_size=page_size,
        )
        self.save_rawg_games(raw_games)
        return self.database.search_games(search_term)

    def import_search_page(
        self, search_term: str, page: int, page_size: int = PAGE_SIZE
    ) -> list[dict[str, Any]]:
        """Fetch one later RAWG search page, save it, and retain RAWG's order."""
        if page < 1:
            raise ValueError("หน้าข้อมูลต้องเริ่มที่ 1")
        raw_games = _fetch_rawg_window(
            lambda rawg_page: self.api_client.search_games(
                search_term, RAWG_MAX_PAGE_SIZE, page=rawg_page
            ),
            display_page=page,
            page_size=page_size,
        )
        games = self.save_rawg_games(raw_games)
        return self.database.get_games_by_ids(game["game_id"] for game in games)

    def refresh_current_players(
        self,
        minimum_interval: timedelta = timedelta(minutes=15),
        force: bool = False,
        game_ids: set[int] | None = None,
    ) -> PlayerRefreshResult:
        """
        Refresh Steam player counts.

        A shared lock prevents multiple Streamlit sessions from
        refreshing the same database simultaneously.
        """
        with _PLAYERS_REFRESH_LOCK:
            now = thailand_now()
            last_refresh = self.database.get_metadata("players_last_refresh")

            if (
                game_ids is None
                and not force
                and _is_fresh(
                    last_refresh,
                    now,
                    minimum_interval,
                )
            ):
                return PlayerRefreshResult(
                    0,
                    0,
                    0,
                    skipped=True,
                )

            updated = 0
            unavailable = 0
            failed = 0
            readings: list[tuple[int, int | None]] = []

            games = (
                self.database.get_games_by_ids(sorted(game_ids))
                if game_ids is not None else self.database.get_games()
            )
            for game in games:

                steam_app_id = game["steam_app_id"]

                if game["steam_lookup_status"] == "unavailable":
                    unavailable += 1
                    continue

                try:
                    if steam_app_id is None:
                        steam_app_id = self.steam_client.find_app_id(
                            game["name"]
                        )
                        self.database.set_steam_mapping(
                            game["game_id"],
                            steam_app_id,
                        )

                    if steam_app_id is None:
                        unavailable += 1
                        continue

                    current_players = self.steam_client.get_current_players(
                        steam_app_id
                    )

                    readings.append(
                        (game["game_id"], current_players)
                    )
                    updated += 1

                except SteamConnectionError:
                    failed += 1
                    break

                except SteamApiError:
                    failed += 1

            self.database.update_current_players_bulk(
                readings,
                now.isoformat(),
            )

            if game_ids is None:
                self.database.set_metadata(
                    "players_last_refresh",
                    now.isoformat(),
                )

            return PlayerRefreshResult(
                updated,
                unavailable,
                failed,
            )

    def refresh_catalog(
        self,
        minimum_interval: timedelta = timedelta(hours=24),
        force: bool = False,
    ) -> CatalogRefreshResult:
        """
        Refresh RAWG discovery data once per shared interval.

        Only one Streamlit session can perform the refresh at a time.
        Other sessions wait and then re-check the database.
        """
        with _CATALOG_REFRESH_LOCK:
            now = thailand_now()
            last_refresh = self.database.get_metadata("catalog_last_refresh")

            if not force and _is_fresh(
                last_refresh,
                now,
                minimum_interval,
            ):
                return CatalogRefreshResult(0, skipped=True)

            raw_games = _fetch_rawg_window(
                lambda rawg_page: self.api_client.fetch_games(
                    RAWG_MAX_PAGE_SIZE,
                    ordering="-added",
                    page=rawg_page,
                ),
                display_page=1,
                page_size=PAGE_SIZE,
            )

            games = self.save_rawg_games(raw_games, catalog_start_rank=1, replace_snapshot=True)
            saved = len(games)

            self.database.set_metadata(
                "catalog_last_refresh",
                now.isoformat(),
            )

            return CatalogRefreshResult(saved)

    def import_catalog_page(self, page: int, page_size: int = PAGE_SIZE) -> list[dict[str, Any]]:
        """Fetch, persist, and return one later page of RAWG popular discoveries."""
        if page < 1:
            raise ValueError("หน้าข้อมูลต้องเริ่มที่ 1")
        raw_games = _fetch_rawg_window(
            lambda rawg_page: self.api_client.fetch_games(
                RAWG_MAX_PAGE_SIZE, ordering="-added", page=rawg_page
            ),
            display_page=page,
            page_size=page_size,
        )
        games = self.save_rawg_games(
            raw_games, catalog_start_rank=(page - 1) * page_size + 1,
            replace_snapshot=page == 1,
        )
        return self.database.get_games_by_ids(game["game_id"] for game in games)

    def refresh_live_top_games(
        self,
        minimum_interval: timedelta = timedelta(minutes=15),
        force: bool = False,
    ) -> LiveTopRefreshResult:
        """
        Refresh the latest available Steam Top snapshot once per shared interval.

        Multiple Streamlit sessions may call this method at the same time.
        The lock ensures that only one session performs the refresh.

        After waiting for the lock, the session checks the database again.
        If another session has already refreshed the data, this session
        simply uses that new snapshot instead of calling Steam again.
        """
        with _LIVE_TOP_REFRESH_LOCK:
            # IMPORTANT:
            # Re-read these values AFTER acquiring the lock.
            # Another tab may have refreshed the database while we were waiting.
            now = thailand_now()
            last_refresh = self.database.get_metadata("live_top_last_refresh")
            saved_games = self.database.get_live_top_games(
                limit=LIVE_TOP_GAMES_LIMIT
            )

            # Another tab may have already completed the refresh.
            if (
                not force
                and saved_games
                and _is_fresh(last_refresh, now, minimum_interval)
            ):
                return LiveTopRefreshResult(
                    len(saved_games),
                    skipped=True,
                )

            # Only the session that reaches this point will call Steam.
            games = self.steam_client.get_most_played_games(
                limit=PAGE_SIZE
            )

            refreshed_at = thailand_now()
            
            # Save one complete snapshot.
            saved = self.database.save_live_top_games(
                games,
                refreshed_at.isoformat(),
            )

            # Mark the shared database snapshot as refreshed.
            self.database.set_metadata(
                "live_top_last_refresh",
                now.isoformat(),
            )

            return LiveTopRefreshResult(saved)


def _is_fresh(value: str | None, now: datetime, interval: timedelta) -> bool:
    if not value:
        return False
    try:
        last_refresh = datetime.fromisoformat(value)
    except ValueError:
        return False
    if last_refresh.tzinfo is None:
        last_refresh = last_refresh.replace(tzinfo=UTC)
    return now - last_refresh < interval


def _fetch_rawg_window(
    fetch_rawg_page: Callable[[int], list[dict[str, Any]]],
    display_page: int,
    page_size: int,
) -> list[dict[str, Any]]:
    """Return one display-sized window from RAWG's fixed 40-record pages."""
    if display_page < 1:
        raise ValueError("หน้าข้อมูลต้องเริ่มที่ 1")
    if page_size < 1:
        raise ValueError("จำนวนเกมต่อหน้าต้องมากกว่า 0")

    start = (display_page - 1) * page_size
    first_rawg_page = start // RAWG_MAX_PAGE_SIZE + 1
    skip = start % RAWG_MAX_PAGE_SIZE
    rawg_pages_needed = ceil((skip + page_size) / RAWG_MAX_PAGE_SIZE)
    games: list[dict[str, Any]] = []

    for rawg_page in range(first_rawg_page, first_rawg_page + rawg_pages_needed):
        rawg_games = fetch_rawg_page(rawg_page)
        games.extend(rawg_games)
        if len(rawg_games) < RAWG_MAX_PAGE_SIZE:
            break
    return games[skip : skip + page_size]
