from src.database.database import GameDatabase


def test_database_closes_connections_and_rolls_back_failed_batch(tmp_path, monkeypatch):
    import sqlite3
    import pytest
    from src.database.database import DatabaseError

    database = GameDatabase(tmp_path / "lifecycle.db")
    connect = database.connect
    connections = []

    def track_connection():
        connection = connect()
        connections.append(connection)
        return connection

    monkeypatch.setattr(database, "connect", track_connection)
    database.insert_games([sample_game(1, "Saved game")])
    with pytest.raises(DatabaseError):
        database.insert_games([sample_game(2, "New game"), {**sample_game(3), "name": None}])
    assert [game["game_id"] for game in database.get_games()] == [1]
    for connection in connections:
        with pytest.raises(sqlite3.ProgrammingError, match="closed"):
            connection.execute("SELECT 1")


def test_popular_limit_preserves_order_and_only_decodes_requested_records(tmp_path, monkeypatch):
    from unittest.mock import Mock

    database = GameDatabase(tmp_path / "limited.db")
    database.save_catalog_games([sample_game(3), sample_game(1), sample_game(2)], "2026-10-13T20:00:00+07:00")
    decoder = Mock(wraps=database._game_from_row)
    monkeypatch.setattr(database, "_game_from_row", decoder)
    assert [game["game_id"] for game in database.get_popular_games(limit=2)] == [3, 1]
    assert decoder.call_count == 2


def test_existing_database_migrates_and_preserves_games_and_developer_cache(tmp_path):
    import sqlite3
    from src.database.database import CREATE_GAMES_TABLE

    path = tmp_path / "old.db"
    old_schema = CREATE_GAMES_TABLE.replace("    developers TEXT NOT NULL DEFAULT '[]',\n", "").replace("    developers_updated_at TEXT,\n", "")
    with sqlite3.connect(path) as connection:
        connection.execute(old_schema)
        connection.execute("INSERT INTO games (game_id, name, current_players) VALUES (1, 'Saved game', 123)")

    database = GameDatabase(path)
    assert database.get_games()[0]["developers"] == []
    database.save_developers(1, ["Studio A", "Studio B"], "2026-10-13T18:00:00+07:00")
    restored = GameDatabase(path).get_games()[0]
    assert restored["name"] == "Saved game"
    assert restored["current_players"] == 123
    assert restored["developers"] == ["Studio A", "Studio B"]
    assert restored["developers_updated_at"] == "2026-10-13T18:00:00+07:00"


def sample_game(game_id: int = 1, name: str = "Portal 2") -> dict:
    return {
        "game_id": game_id,
        "name": name,
        "rating": 4.6,
        "released": "2011-04-18",
        "genres": ["Puzzle"],
        "developers": [],
        "developers_updated_at": None,
        "platforms": ["PC"],
        "metacritic": 95,
        "ratings_count": 2500,
        "image": "https://example.test/portal.jpg",
        "steam_app_id": None,
        "steam_lookup_status": "pending",
        "current_players": None,
        "players_updated_at": None,
        "catalog_updated_at": None,
        "is_live_top": 0,
        "live_rank": None,
    }


def test_database_initializes_inserts_and_reads_games(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.initialize()

    assert database.insert_games([sample_game()]) == 1
    assert database.get_games() == [sample_game()]
    assert database.game_exists(1) is True


def test_database_upsert_prevents_duplicate_game_ids(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games([sample_game(name="Old name")])
    database.insert_games([sample_game(name="New name")])

    games = database.get_games()
    assert len(games) == 1
    assert games[0]["name"] == "New name"


def test_database_lists_game_library_by_latest_catalog_update(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games([sample_game(1, "Older")], updated_at="2026-09-23T09:00:00+07:00")
    database.insert_games([sample_game(2, "Newer")], updated_at="2026-09-23T10:00:00+07:00")

    assert [game["name"] for game in database.get_games()] == ["Newer", "Older"]


def test_database_keeps_rawg_catalogue_in_api_order(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.save_catalog_games(
        [sample_game(3, "Third"), sample_game(1, "First")],
        updated_at="2026-09-23T09:00:00+07:00",
        start_rank=101,
    )
    database.save_catalog_games(
        [sample_game(2, "Second")],
        updated_at="2026-09-23T10:00:00+07:00",
        start_rank=1,
        replace_snapshot=False,
    )

    assert [game["name"] for game in database.get_popular_games()] == [
        "Second",
        "Third",
        "First",
    ]


def test_database_reads_selected_games_in_requested_order(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games([sample_game(1, "First"), sample_game(2, "Second")])

    games = database.get_games_by_ids([2, 1, 999])

    assert [game["name"] for game in games] == ["Second", "First"]
    assert games[0]["current_players"] is None


def test_database_search_is_partial_case_insensitive_and_blank_is_safe(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games([sample_game(name="Portal 2"), sample_game(2, "Hades")])

    assert [game["name"] for game in database.search_games("PORT")] == ["Portal 2"]
    assert database.search_games("unknown") == []
    assert database.search_games("   ") == []


def test_database_search_treats_like_wildcards_as_plain_text(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games([sample_game(name="100%_ Orange Juice"), sample_game(2, "Hades")])

    assert [game["name"] for game in database.search_games("100%_")] == ["100%_ Orange Juice"]
    assert database.search_games("%") == [database.get_games()[0]]


def test_database_persists_steam_player_data(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games([sample_game()])

    database.set_steam_mapping(1, 620)
    database.update_current_players(1, 3456, "2026-09-22T10:00:00+00:00")

    game = database.get_games()[0]
    assert game["steam_app_id"] == 620
    assert game["steam_lookup_status"] == "found"
    assert game["current_players"] == 3456
    assert game["players_updated_at"] == "2026-09-22T10:00:00+00:00"


def test_database_persists_multiple_player_counts_in_one_batch(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games([sample_game(1, "Portal 2"), sample_game(2, "Hades")])

    saved = database.update_current_players_bulk(
        [(1, 3456), (2, 7890)], "2026-09-22T10:00:00+00:00"
    )

    assert saved == 2
    assert {game["name"]: game["current_players"] for game in database.get_games()} == {
        "Portal 2": 3456,
        "Hades": 7890,
    }


def test_database_replaces_and_reads_the_live_top_snapshot(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.save_live_top_games(
        [
            {
                **sample_game(game_id=-730, name="Counter-Strike 2"),
                "steam_app_id": 730,
                "steam_lookup_status": "found",
                "current_players": 999,
                "live_rank": 1,
            }
        ],
        "2026-09-22T10:00:00+00:00",
    )

    games = database.get_live_top_games()
    assert [game["name"] for game in games] == ["Counter-Strike 2"]
    assert games[0]["is_live_top"] == 1
    assert games[0]["players_updated_at"] == "2026-09-22T10:00:00+00:00"


def test_database_orders_live_games_by_current_player_count(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.save_live_top_games(
        [
            {
                **sample_game(game_id=-730, name="Fewer players"),
                "steam_app_id": 730,
                "steam_lookup_status": "found",
                "current_players": 100,
                "live_rank": 1,
            },
            {
                **sample_game(game_id=-570, name="More players"),
                "steam_app_id": 570,
                "steam_lookup_status": "found",
                "current_players": 200,
                "live_rank": 2,
            },
        ],
        "2026-09-22T10:00:00+00:00",
    )

    assert [game["name"] for game in database.get_live_top_games()] == [
        "More players",
        "Fewer players",
    ]
