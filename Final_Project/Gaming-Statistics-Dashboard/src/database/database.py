"""SQLite database access for normalized game records."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Any, Iterable


CREATE_GAMES_TABLE = """
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rating REAL,
    released TEXT,
    genres TEXT NOT NULL DEFAULT '[]',
    developers TEXT NOT NULL DEFAULT '[]',
    developers_updated_at TEXT,
    platforms TEXT NOT NULL DEFAULT '[]',
    metacritic INTEGER,
    ratings_count INTEGER,
    image TEXT,
    steam_app_id INTEGER,
    steam_lookup_status TEXT NOT NULL DEFAULT 'pending',
    current_players INTEGER,
    players_updated_at TEXT,
    catalog_updated_at TEXT,
    catalog_rank INTEGER,
    is_live_top INTEGER NOT NULL DEFAULT 0,
    live_rank INTEGER
)
"""

CREATE_METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS dashboard_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
"""

GAME_COLUMN_MIGRATIONS = {
    "developers": "TEXT NOT NULL DEFAULT '[]'",
    "developers_updated_at": "TEXT",
    "steam_app_id": "INTEGER",
    "steam_lookup_status": "TEXT NOT NULL DEFAULT 'pending'",
    "current_players": "INTEGER",
    "players_updated_at": "TEXT",
    "catalog_updated_at": "TEXT",
    "catalog_rank": "INTEGER",
    "is_live_top": "INTEGER NOT NULL DEFAULT 0",
    "live_rank": "INTEGER",
}


class DatabaseError(RuntimeError):
    """A readable application error for SQLite setup or query failures."""


class GameDatabase:
    """Keep SQLite operations in one small, reusable persistence layer."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self._schema_initialized = False

    def connect(self) -> sqlite3.Connection:
        """Open a configured SQLite connection with dictionary-like rows."""
        try:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(self.database_path)
            connection.row_factory = sqlite3.Row
            return connection
        except (OSError, sqlite3.Error) as error:
            raise DatabaseError("ไม่สามารถเชื่อมต่อฐานข้อมูล SQLite ได้") from error

    def initialize(self) -> None:
        """Create the games table if it does not already exist."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถสร้างตาราง games ใน SQLite ได้") from error

    @contextmanager
    def _connection(self):
        """Commit or roll back the operation, then always close the connection."""
        with closing(self.connect()) as connection:
            with connection:
                yield connection

    def insert_games(self, games: Iterable[dict[str, Any]], updated_at: str | None = None) -> int:
        """Insert or update game records, using game_id to prevent duplicates."""
        records = list(games)
        if not records:
            return 0

        statement = """
        INSERT INTO games (
            game_id, name, rating, released, genres, platforms,
            metacritic, ratings_count, image, catalog_updated_at, developers, developers_updated_at
        ) VALUES (
            :game_id, :name, :rating, :released, :genres, :platforms,
            :metacritic, :ratings_count, :image, :catalog_updated_at, :developers, :developers_updated_at
        )
        ON CONFLICT(game_id) DO UPDATE SET
            name = excluded.name,
            rating = excluded.rating,
            released = excluded.released,
            genres = excluded.genres,
            developers = CASE WHEN excluded.developers_updated_at IS NOT NULL OR excluded.developers != '[]' THEN excluded.developers ELSE games.developers END,
            developers_updated_at = COALESCE(excluded.developers_updated_at, games.developers_updated_at),
            platforms = excluded.platforms,
            metacritic = excluded.metacritic,
            ratings_count = excluded.ratings_count,
            image = excluded.image,
            catalog_updated_at = excluded.catalog_updated_at
        """
        rows = [self._database_row({**game, "catalog_updated_at": updated_at}) for game in records]
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                connection.executemany(statement, rows)
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถบันทึกข้อมูลเกมลง SQLite ได้") from error
        return len(rows)

    def save_catalog_games(
        self,
        games: Iterable[dict[str, Any]],
        updated_at: str,
        start_rank: int = 1,
        replace_snapshot: bool = False,
    ) -> int:
        """Save a RAWG discovery page while preserving its API position.

        ``catalog_rank`` lets Home display consecutive API pages (1–100,
        then 101–200) even though the same database also stores searches and
        library entries with unrelated sort orders.
        """
        records = list(games)
        saved = self.insert_games(records, updated_at=updated_at)
        if not records:
            return saved
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                if replace_snapshot:
                    connection.execute("UPDATE games SET catalog_rank = NULL")
                connection.executemany(
                    "UPDATE games SET catalog_rank = ? WHERE game_id = ?",
                    [(start_rank + index, game["game_id"]) for index, game in enumerate(records)],
                )
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถบันทึกลำดับเกมยอดนิยมลง SQLite ได้") from error
        return saved

    def get_games(self) -> list[dict[str, Any]]:
        """Read all locally stored games in a stable, readable order."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                rows = connection.execute(
                    """
                    SELECT * FROM games
                    ORDER BY catalog_updated_at IS NULL, catalog_updated_at DESC, name COLLATE NOCASE
                    """
                ).fetchall()
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถอ่านข้อมูลเกมจาก SQLite ได้") from error
        return [self._game_from_row(row) for row in rows]

    def get_games_by_ids(self, game_ids: Iterable[int]) -> list[dict[str, Any]]:
        """Read stored games in the caller's requested order."""
        ids = list(dict.fromkeys(game_ids))
        if not ids:
            return []
        placeholders = ", ".join("?" for _ in ids)
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                rows = connection.execute(
                    f"SELECT * FROM games WHERE game_id IN ({placeholders})", ids
                ).fetchall()
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถอ่านข้อมูลเกมจาก SQLite ได้") from error
        games_by_id = {row["game_id"]: self._game_from_row(row) for row in rows}
        return [games_by_id[game_id] for game_id in ids if game_id in games_by_id]

    def search_games(self, search_term: str) -> list[dict[str, Any]]:
        """Find games by a case-insensitive literal partial name match."""
        term = search_term.strip()
        if not term:
            return []
        # ``%`` and ``_`` have a special meaning in SQL LIKE.  Escape them so
        # a search box always searches the text the visitor typed, rather than
        # unexpectedly returning every game for a query such as "%".
        escaped_term = (
            term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        )
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                rows = connection.execute(
                    """
                    SELECT * FROM games
                    WHERE name LIKE ? ESCAPE '\\' COLLATE NOCASE
                    ORDER BY name COLLATE NOCASE
                    """,
                    (f"%{escaped_term}%",),
                ).fetchall()
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถค้นหาข้อมูลเกมใน SQLite ได้") from error
        return [self._game_from_row(row) for row in rows]

    def game_exists(self, game_id: int) -> bool:
        """Return whether a RAWG game ID already exists in the database."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                row = connection.execute(
                    "SELECT 1 FROM games WHERE game_id = ?", (game_id,)
                ).fetchone()
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถตรวจสอบข้อมูลเกมใน SQLite ได้") from error
        return row is not None

    def set_steam_mapping(self, game_id: int, steam_app_id: int | None) -> None:
        """Persist a resolved Steam app ID, or remember that no exact match exists."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                connection.execute(
                    """
                    UPDATE games
                    SET steam_app_id = ?, steam_lookup_status = ?
                    WHERE game_id = ?
                    """,
                    (steam_app_id, "found" if steam_app_id is not None else "unavailable", game_id),
                )
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถบันทึกการจับคู่ Steam ได้") from error

    def update_current_players(
        self, game_id: int, current_players: int | None, updated_at: str
    ) -> None:
        """Store the latest Steam player reading for one mapped game."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                connection.execute(
                    """
                    UPDATE games
                    SET current_players = ?, players_updated_at = ?
                    WHERE game_id = ?
                    """,
                    (current_players, updated_at, game_id),
                )
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถบันทึกจำนวนผู้เล่น Steam ได้") from error

    def update_current_players_bulk(
        self, readings: Iterable[tuple[int, int | None]], updated_at: str
    ) -> int:
        """Persist multiple Steam readings in one SQLite transaction."""
        rows = [(current_players, updated_at, game_id) for game_id, current_players in readings]
        if not rows:
            return 0
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                connection.executemany(
                    """
                    UPDATE games
                    SET current_players = ?, players_updated_at = ?
                    WHERE game_id = ?
                    """,
                    rows,
                )
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถบันทึกจำนวนผู้เล่น Steam ได้") from error
        return len(rows)

    def save_live_top_games(self, games: Iterable[dict[str, Any]], updated_at: str) -> int:
        """Replace the displayed Steam Top list with one consistent live snapshot."""
        records = list(games)
        if not records:
            return 0
        statement = """
        INSERT INTO games (
            game_id, name, rating, released, genres, platforms, metacritic,
            ratings_count, image, steam_app_id, steam_lookup_status,
            current_players, players_updated_at, catalog_updated_at, is_live_top, live_rank
        ) VALUES (
            :game_id, :name, :rating, :released, :genres, :platforms, :metacritic,
            :ratings_count, :image, :steam_app_id, :steam_lookup_status,
            :current_players, :players_updated_at, :catalog_updated_at, 1, :live_rank
        )
        ON CONFLICT(game_id) DO UPDATE SET
            name = excluded.name,
            platforms = excluded.platforms,
            image = excluded.image,
            steam_app_id = excluded.steam_app_id,
            steam_lookup_status = excluded.steam_lookup_status,
            current_players = excluded.current_players,
            players_updated_at = excluded.players_updated_at,
            genres = CASE WHEN excluded.genres != '[]' THEN excluded.genres ELSE games.genres END,
            catalog_updated_at = excluded.catalog_updated_at,
            is_live_top = 1,
            live_rank = excluded.live_rank
        """
        rows = [
            self._database_row(
                {**game, "players_updated_at": updated_at, "catalog_updated_at": updated_at}
            )
            for game in records
        ]
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                connection.execute("UPDATE games SET is_live_top = 0, live_rank = NULL")
                connection.executemany(statement, rows)
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถบันทึกอันดับผู้เล่น Steam ได้") from error
        return len(rows)

    def get_live_top_games(self, limit: int = 100) -> list[dict[str, Any]]:
        """Read the latest Steam games ordered by current player count."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                rows = connection.execute(
                    """
                    SELECT * FROM games
                    WHERE is_live_top = 1
                    ORDER BY current_players DESC, live_rank ASC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถอ่านอันดับผู้เล่น Steam ได้") from error
        return [self._game_from_row(row) for row in rows]

    def get_popular_games(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Read RAWG discoveries stored locally, favouring broadly popular titles."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                query = """
                    SELECT * FROM games
                    WHERE game_id > 0
                    ORDER BY catalog_rank IS NULL, catalog_rank ASC,
                             ratings_count IS NULL, ratings_count DESC,
                             released IS NULL, released DESC, catalog_updated_at DESC
                    """
                parameters = ()
                if limit is not None:
                    if limit < 1:
                        raise ValueError("Game limit must be at least 1")
                    query += " LIMIT ?"
                    parameters = (limit,)
                rows = connection.execute(query, parameters).fetchall()
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถอ่านเกมยอดนิยมจาก SQLite ได้") from error
        return [self._game_from_row(row) for row in rows]

    def save_developers(self, game_id: int, developers: list[str], updated_at: str) -> None:
        """Cache detail metadata separately from catalog and player snapshots."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                connection.execute(
                    "UPDATE games SET developers = ?, developers_updated_at = ? WHERE game_id = ?",
                    (json.dumps(developers, ensure_ascii=False), updated_at, game_id),
                )
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถบันทึกข้อมูลผู้พัฒนาเกมได้") from error

    def get_metadata(self, key: str) -> str | None:
        """Read a small dashboard-wide value such as the last refresh timestamp."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                row = connection.execute(
                    "SELECT value FROM dashboard_metadata WHERE key = ?", (key,)
                ).fetchone()
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถอ่านข้อมูลสถานะ Dashboard ได้") from error
        return str(row["value"]) if row is not None else None

    def set_metadata(self, key: str, value: str) -> None:
        """Store a small dashboard-wide value."""
        try:
            with self._connection() as connection:
                self._prepare_schema(connection)
                connection.execute(
                    """
                    INSERT INTO dashboard_metadata (key, value) VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value
                    """,
                    (key, value),
                )
        except sqlite3.Error as error:
            raise DatabaseError("ไม่สามารถบันทึกข้อมูลสถานะ Dashboard ได้") from error

    def _prepare_schema(self, connection: sqlite3.Connection) -> None:
        """Create or migrate the schema once for this repository instance."""
        if self._schema_initialized:
            return
        connection.execute(CREATE_GAMES_TABLE)
        connection.execute(CREATE_METADATA_TABLE)
        existing_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(games)").fetchall()
        }
        for column, definition in GAME_COLUMN_MIGRATIONS.items():
            if column not in existing_columns:
                connection.execute(f"ALTER TABLE games ADD COLUMN {column} {definition}")
        self._schema_initialized = True

    @staticmethod
    def _database_row(game: dict[str, Any]) -> dict[str, Any]:
        return {
            **game,
            "developers_updated_at": game.get("developers_updated_at"),
            "genres": json.dumps(game.get("genres", []), ensure_ascii=False),
            "developers": json.dumps(game.get("developers", []), ensure_ascii=False),
            "platforms": json.dumps(game.get("platforms", []), ensure_ascii=False),
        }

    @staticmethod
    def _game_from_row(row: sqlite3.Row) -> dict[str, Any]:
        game = dict(row)
        # Older snapshots store RAWG's unrated sentinel as 0.0.
        if game["rating"] == 0:
            game["rating"] = None
        # This is ordering metadata for the Home feed, not a game attribute
        # consumed by the rest of the dashboard.
        game.pop("catalog_rank", None)
        game["genres"] = _decode_list(game["genres"])
        game["developers"] = _decode_list(game["developers"])
        game["platforms"] = _decode_list(game["platforms"])
        return game


def _decode_list(value: str | None) -> list[str]:
    """Read JSON list columns safely, including data from older local files."""
    try:
        decoded = json.loads(value or "[]")
    except (TypeError, json.JSONDecodeError):
        return []
    return [str(item) for item in decoded] if isinstance(decoded, list) else []
