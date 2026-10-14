from pathlib import Path
import subprocess
import sys
from unittest.mock import Mock
from threading import Barrier, Event, get_ident

import pytest

from src.api.rawg_api import RawgApiClient, RawgApiError
from src.database.database import GameDatabase
from src.script import import_games as script
from src.utils.data_processing import process_game


def test_ranges_fetch_concurrently_with_independent_clients_and_one_sqlite_writer(tmp_path):
    barrier = Barrier(2)
    clients = []
    calls = []
    writer_thread = get_ident()

    class WriterDatabase(GameDatabase):
        def insert_games(self, games, updated_at=None):
            assert get_ident() == writer_thread
            return super().insert_games(games, updated_at)

    class WorkerClient:
        def __init__(self):
            self.session = Mock()
            self.first = True

        def fetch_games(self, page_size, ordering, page):
            if self.first:
                self.first = False
                barrier.wait(timeout=5)
            calls.append((page, get_ident()))
            return [{"id": page * 40 + index, "name": f"Game {page}-{index}", "developers": [{"name": "Studio"}]} for index in range(40)]

    def factory():
        client = WorkerClient()
        clients.append(client)
        return client

    database = WriterDatabase(tmp_path / "parallel.db")
    client = Mock()
    assert script.import_ranges(client, database, [[1, 2], [3, 4]], client_factory=factory) == (160, 0)
    assert sorted(page for page, _ in calls) == [1, 2, 3, 4]
    assert len({thread for _, thread in calls}) == 2
    assert len(clients) == 2
    assert len(database.get_games()) == 160
    assert all(game["developers"] == ["Studio"] for game in database.get_games())
    for worker in clients:
        worker.session.close.assert_called_once()
    client.fetch_game_details.assert_not_called()


def test_parallel_failure_stops_producers_without_losing_saved_pages(tmp_path):
    saved = Event()

    class WriterDatabase(GameDatabase):
        def insert_games(self, games, updated_at=None):
            result = super().insert_games(games, updated_at)
            saved.set()
            return result

    class WorkerClient:
        session = Mock()

        def fetch_games(self, page_size, ordering, page):
            if page >= 300:
                assert saved.wait(timeout=5)
                raise RawgApiError("offline")
            return [{"id": page * 40 + index, "name": "Game", "developers": []} for index in range(40)]

    database = WriterDatabase(tmp_path / "parallel-failure.db")
    with pytest.raises(RawgApiError, match="offline"):
        script.import_ranges(Mock(), database, [[1, 200], [300, 500]], client_factory=WorkerClient)
    assert len(database.get_games()) >= 40


@pytest.mark.parametrize("ranges", [[], [[0, 1]], [[2, 1]], [[1, 3], [3, 5]], [[1]], [[1, "2"]]])
def test_invalid_ranges_are_rejected_before_any_api_request(tmp_path, ranges):
    factory = Mock()
    with pytest.raises(ValueError):
        script.import_ranges(Mock(), GameDatabase(tmp_path / "invalid.db"), ranges, client_factory=factory)
    factory.assert_not_called()


def test_import_adds_games_updates_duplicates_and_preserves_live_snapshot(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    old = process_game({"id": 1, "name": "Old name"})
    database.save_catalog_games([old], "2026-10-13T10:00:00+07:00")
    database.save_live_top_games([
        {**old, "steam_app_id": 620, "steam_lookup_status": "found", "current_players": 123, "live_rank": 1}
    ], "2026-10-13T10:00:00+07:00")
    database.save_developers(1, ["Cached studio"], "2026-10-13T10:00:00+07:00")
    database.set_metadata("catalog_last_refresh", "original refresh time")
    client = Mock()
    client.fetch_game_details.side_effect = lambda game_id: {"id": game_id, "developers": []}
    client.fetch_games.return_value = [{"id": 1, "name": "New name"}, {"id": 2, "name": "New game"}]

    assert script.import_games(client, database, start_page=26, pages=10) == (1, 1)
    client.fetch_games.assert_called_once_with(40, ordering="-added", page=26)
    game = database.get_live_top_games()[0]
    assert game["name"] == "New name"
    assert game["current_players"] == 123
    assert game["developers"] == ["Cached studio"]
    assert database.get_metadata("catalog_last_refresh") == "original refresh time"
    assert script.import_games(client, database, start_page=26, pages=1) == (0, 2)
    assert len(database.get_games()) == 2


def test_failed_later_page_keeps_previous_pages_and_returns_error(tmp_path, monkeypatch, capsys):
    path = tmp_path / "partial.db"
    client = Mock()
    client.fetch_game_details.side_effect = lambda game_id: {"id": game_id, "developers": []}
    client.fetch_games.side_effect = [
        [{"id": number, "name": f"Game {number}"} for number in range(1, 41)],
        RawgApiError("offline"),
    ]
    monkeypatch.setattr(script, "RawgApiClient", lambda: client)

    assert script.main(["--pages", "2", "--database", str(path)]) == 1
    assert len(GameDatabase(path).get_games()) == 40
    assert "offline" in capsys.readouterr().err


def test_script_skips_developer_requests_without_marking_empty_data_as_cached(tmp_path):
    database = GameDatabase(tmp_path / "developers.db")
    client = Mock()
    client.fetch_games.return_value = [{"id": 42, "name": "Hades"}]
    client.fetch_game_details.return_value = {"id": 42, "developers": [{"name": "Supergiant Games"}]}

    for _ in range(2):
        script.import_games(client, database, start_page=1, pages=1)
    assert database.get_games()[0]["developers"] == []
    assert database.get_games()[0]["developers_updated_at"] is None
    client.fetch_game_details.assert_not_called()
    # A later Details visit can still retrieve the missing data.
    from src.services.game_service import GameService
    GameService(client, database).get_game_details(42)
    assert database.get_games()[0]["developers"] == ["Supergiant Games"]
    client.fetch_game_details.assert_called_once_with(42)


@pytest.mark.parametrize("parallel", [False, True])
def test_one_import_page_uses_exactly_one_http_request_and_no_detail_requests(tmp_path, parallel):
    session = Mock()
    response = Mock()
    response.json.return_value = {"results": [{"id": index, "name": f"Game {index}"} for index in range(1, 41)]}
    session.get.return_value = response
    client = RawgApiClient(api_key="test-key", session=session)
    database = GameDatabase(tmp_path / "request-count.db")
    if parallel:
        assert script.import_ranges(client, database, [[26, 26]], client_factory=lambda: client) == (40, 0)
    else:
        assert script.import_games(client, database, start_page=26, pages=1) == (40, 0)
    session.get.assert_called_once_with(
        "https://api.rawg.io/api/games",
        params={"key": "test-key", "page_size": 40, "ordering": "-added", "page": 26},
        timeout=15,
    )
    assert all(game["developers_updated_at"] is None for game in database.get_games())


def test_script_paths_and_direct_launch_work_from_another_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GAMING_DASHBOARD_DB", raising=False)
    assert script.resolve_database_path(None) == script.PROJECT_ROOT / "data/gaming_statistics.db"
    assert script.resolve_database_path("data/custom.db") == script.PROJECT_ROOT / "data/custom.db"
    assert script.resolve_database_path(str(tmp_path / "custom.db")) == tmp_path / "custom.db"
    monkeypatch.setenv("GAMING_DASHBOARD_DB", "data/environment.db")
    assert script.resolve_database_path(None) == script.PROJECT_ROOT / "data/environment.db"
    result = subprocess.run(
        [sys.executable, str(Path(script.__file__)), "--help"],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "--start-page" in result.stdout
    assert "--with-developers" not in result.stdout


@pytest.mark.parametrize("option", ["--pages", "--start-page"])
@pytest.mark.parametrize("value", ["0", "-1", "abc", "", "1.5"])
def test_cli_rejects_invalid_page_arguments(option, value):
    with pytest.raises(SystemExit) as error:
        script.main([option, value])
    assert error.value.code == 2
