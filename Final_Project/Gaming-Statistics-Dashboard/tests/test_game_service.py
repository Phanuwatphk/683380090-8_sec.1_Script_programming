from src.database.database import GameDatabase
from src.services.game_service import GameService


def test_home_uses_three_requests_and_only_opened_detail_fetches_developer(tmp_path):
    from unittest.mock import Mock
    from src.api.rawg_api import RawgApiClient

    session = Mock()

    def respond(url, params, timeout):
        response = Mock()
        if url.endswith("/games"):
            page = params.get("page", 1)
            first = (page - 1) * 40 + 1
            response.json.return_value = {"results": [{"id": number, "name": f"Game {number}"} for number in range(first, first + 40)]}
        else:
            assert url.endswith("/games/1")
            response.json.return_value = {"id": 1, "developers": [{"name": "Studio"}]}
        return response

    session.get.side_effect = respond
    service = GameService(RawgApiClient(api_key="test-key", session=session), GameDatabase(tmp_path / "home-requests.db"))
    assert service.refresh_catalog().saved == 100
    assert session.get.call_count == 3
    assert len(service.get_games()) == len(service.get_popular_games()) == 100
    assert service.search_games("Game 1")
    assert session.get.call_count == 3
    assert service.get_game_details(1)["developers"] == ["Studio"]
    assert session.get.call_count == 4
    assert service.get_game_details(1)["developers"] == ["Studio"]
    assert service.refresh_catalog().skipped
    assert session.get.call_count == 4


def test_developer_details_are_cached_even_when_rawg_has_no_developers(tmp_path):
    from unittest.mock import Mock
    from src.utils.data_processing import process_game

    for game_id, developers in [(42, [{"name": "Supergiant Games"}]), (43, [])]:
        client = Mock()
        client.fetch_game_details.return_value = {"id": game_id, "developers": developers}
        database = GameDatabase(tmp_path / f"{game_id}.db")
        game = process_game({"id": game_id, "name": "Saved name", "rating": 4.8})
        service = GameService(client, database)
        service.save_rawg_games([{"id": game_id, "name": "Saved name", "rating": 4.8}])
        client.fetch_game_details.assert_not_called()
        first = service.get_game_details(game_id)
        # A regular list refresh omits developers and must preserve cached details.
        service.save_rawg_games([{"id": game_id, "name": "Saved name", "rating": 4.8}])
        second = service.get_game_details(game_id)

        assert first["developers"] == second["developers"] == [item["name"] for item in developers]
        assert second["developers_updated_at"]
        assert second["name"] == "Saved name"
        assert second["rating"] == 4.8
        client.fetch_game_details.assert_called_once_with(game_id)


def test_steam_only_or_missing_games_do_not_call_rawg_details(tmp_path):
    from unittest.mock import Mock
    from src.utils.data_processing import process_game

    client = Mock()
    database = GameDatabase(tmp_path / "steam-details.db")
    database.insert_games([process_game({"id": -730, "name": "Counter-Strike 2"})])
    service = GameService(client, database)

    assert service.get_game_details(-730)["developers"] == []
    assert service.get_game_details(999) is None
    client.fetch_game_details.assert_not_called()


def test_failed_developer_request_can_be_retried_without_losing_saved_game(tmp_path):
    from unittest.mock import Mock
    from src.api.rawg_api import RawgApiError
    from src.utils.data_processing import process_game
    import pytest

    client = Mock()
    client.fetch_game_details.side_effect = [RawgApiError("offline"), {"id": 42, "developers": [{"name": "Studio"}]}]
    database = GameDatabase(tmp_path / "retry-details.db")
    database.insert_games([process_game({"id": 42, "name": "Saved game"})])
    service = GameService(client, database)

    with pytest.raises(RawgApiError, match="offline"):
        service.get_game_details(42)
    assert database.get_games()[0]["developers_updated_at"] is None
    assert service.get_game_details(42)["developers"] == ["Studio"]
    assert database.get_games()[0]["name"] == "Saved game"
    assert client.fetch_game_details.call_count == 2


class FakeRawgClient:
    def fetch_game_details(self, game_id):
        raise AssertionError("Game lists must not request developer details")

    def fetch_games(self, page_size: int):
        assert page_size == 2
        return [
            {
                "id": 1,
                "name": "Portal 2",
                "rating": 4.6,
                "genres": [{"name": "Puzzle"}],
                "platforms": [{"platform": {"name": "PC"}}],
            },
            {
                "id": 2,
                "name": "Hades",
                "rating": 4.8,
                "genres": [{"name": "Action"}],
                "platforms": [{"platform": {"name": "Nintendo Switch"}}],
            },
        ]


def test_service_fetches_processes_stores_and_searches(tmp_path):
    service = GameService(FakeRawgClient(), GameDatabase(tmp_path / "games.db"))

    result = service.sync_games(page_size=2)

    assert result.fetched == 2
    assert result.saved == 2
    assert [game["name"] for game in service.get_games()] == ["Hades", "Portal 2"]
    assert [game["name"] for game in service.search_games("portal")] == ["Portal 2"]
    assert service.search_games("missing") == []
    assert all(game["developers"] == [] for game in service.get_games())


class FakeSteamClient:
    def find_app_id(self, game_name: str):
        return {"Portal 2": 620}.get(game_name)

    def get_current_players(self, app_id: int):
        assert app_id == 620
        return 1234


def test_service_refreshes_and_persists_available_steam_player_counts(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games(
        [
            {
                "game_id": 1,
                "name": "Portal 2",
                "rating": None,
                "released": None,
                "genres": [],
                "platforms": [],
                "metacritic": None,
                "ratings_count": None,
                "image": None,
            },
            {
                "game_id": 2,
                "name": "Not on Steam",
                "rating": None,
                "released": None,
                "genres": [],
                "platforms": [],
                "metacritic": None,
                "ratings_count": None,
                "image": None,
            },
        ]
    )
    service = GameService(FakeRawgClient(), database, steam_client=FakeSteamClient())

    result = service.refresh_current_players(force=True)
    games = {game["name"]: game for game in service.get_games()}

    assert result.updated == 1
    assert result.unavailable == 1
    assert games["Portal 2"]["current_players"] == 1234
    assert games["Portal 2"]["players_updated_at"].endswith("+07:00")
    assert games["Not on Steam"]["steam_lookup_status"] == "unavailable"


def test_refreshing_selected_players_does_not_load_entire_library(tmp_path, monkeypatch):
    from unittest.mock import Mock
    from src.utils.data_processing import process_game

    database = GameDatabase(tmp_path / "selected-players.db")
    database.insert_games([
        process_game({"id": 1, "name": "Portal 2"}),
        process_game({"id": 2, "name": "Unselected game"}),
    ])
    database.set_steam_mapping(1, 620)
    all_games = Mock(side_effect=AssertionError("Selected refresh must not read the full library"))
    monkeypatch.setattr(database, "get_games", all_games)
    service = GameService(FakeRawgClient(), database, steam_client=FakeSteamClient())
    assert service.refresh_current_players(game_ids={1}).updated == 1
    selected, unselected = database.get_games_by_ids([1, 2])
    assert selected["current_players"] == 1234
    assert unselected["current_players"] is None
    all_games.assert_not_called()


class FakeRawgSearchClient(FakeRawgClient):
    def search_games(self, search_term: str, page_size: int, page: int = 1):
        assert search_term == "Minecraft"
        assert page_size == 40
        assert page == 1
        return [{"id": 70, "name": "Minecraft", "genres": [], "platforms": []}]


def test_service_imports_rawg_search_results_into_the_local_database(tmp_path):
    service = GameService(FakeRawgSearchClient(), GameDatabase(tmp_path / "games.db"))

    games = service.search_and_import_games("Minecraft")

    assert [game["name"] for game in games] == ["Minecraft"]
    assert games[0]["developers"] == []


def test_service_searches_sqlite_before_requesting_rawg(tmp_path):
    database = GameDatabase(tmp_path / "games.db")
    database.insert_games(
        [
            {
                "game_id": 1,
                "name": "Portal 2",
                "rating": None,
                "released": None,
                "genres": [],
                "platforms": [],
                "metacritic": None,
                "ratings_count": None,
                "image": None,
            }
        ]
    )

    class NoRequestRawgClient:
        def search_games(self, search_term: str, page_size: int):
            raise AssertionError("RAWG must not be called when SQLite has a match")

    service = GameService(NoRequestRawgClient(), database)

    assert [game["name"] for game in service.search_or_import_games("portal")] == ["Portal 2"]


def test_service_imports_from_rawg_when_sqlite_has_no_match(tmp_path):
    service = GameService(FakeRawgSearchClient(), GameDatabase(tmp_path / "games.db"))

    assert [game["name"] for game in service.search_or_import_games("Minecraft")] == ["Minecraft"]


def test_service_imports_and_returns_a_later_catalog_page_in_api_order(tmp_path):
    class FakePagedDiscoveryClient(FakeRawgClient):
        def __init__(self):
            self.calls = []

        def fetch_games(self, page_size: int, ordering: str | None = None, page: int = 1):
            self.calls.append((page_size, ordering, page))
            first_id = (page - 1) * 40 + 1
            return [
                {"id": game_id, "name": f"Game {game_id}", "genres": [], "platforms": []}
                for game_id in range(first_id, first_id + 40)
            ]

    client = FakePagedDiscoveryClient()
    service = GameService(client, GameDatabase(tmp_path / "games.db"))

    games = service.import_catalog_page(2, page_size=50)

    assert [game["game_id"] for game in games] == list(range(51, 101))
    assert client.calls == [(40, "-added", 2), (40, "-added", 3)]
    assert games[0]["current_players"] is None
    assert len(service.get_games()) == 50
    assert all(game["developers"] == [] for game in games)


class FakeSteamTopClient:
    def __init__(self):
        self.calls = 0

    def get_most_played_games(self, limit: int):
        self.calls += 1
        assert limit == 100
        return [
            {
                "game_id": -730,
                "name": "Counter-Strike 2",
                "rating": None,
                "released": None,
                "genres": [],
                "platforms": ["PC (Steam)"],
                "metacritic": None,
                "ratings_count": None,
                "image": None,
                "steam_app_id": 730,
                "steam_lookup_status": "found",
                "current_players": 500,
                "live_rank": 1,
            }
        ]


def test_service_refreshes_the_live_top_games_for_home(tmp_path):
    service = GameService(
        FakeRawgClient(), GameDatabase(tmp_path / "games.db"), steam_client=FakeSteamTopClient()
    )

    result = service.refresh_live_top_games()

    assert result.saved == 1
    assert [game["name"] for game in service.get_live_top_games()] == ["Counter-Strike 2"]


class FakeDiscoveryClient(FakeRawgClient):
    def fetch_games(self, page_size: int, ordering: str | None = None, page: int = 1):
        assert page_size == 40
        assert ordering == "-added"
        assert page == 1
        return [
            {
                "id": 10,
                "name": "Popular game",
                "genres": [{"name": "Adventure"}],
                "platforms": [],
                "ratings_count": 100,
            }
        ]


def test_service_saves_rawg_discoveries_before_home_reads_them(tmp_path):
    service = GameService(FakeDiscoveryClient(), GameDatabase(tmp_path / "games.db"))

    result = service.refresh_catalog()

    assert result.saved == 1
    assert service.get_popular_games()[0]["genres"] == ["Adventure"]
    assert service.get_popular_games()[0]["developers"] == []
    assert service.get_popular_games()[0]["catalog_updated_at"].endswith("+07:00")


def test_catalog_default_refresh_interval_is_24_hours(tmp_path, monkeypatch):
    from datetime import datetime, timedelta
    from unittest.mock import Mock
    import src.services.game_service as module

    now = datetime.fromisoformat("2026-10-13T20:00:00+07:00")
    monkeypatch.setattr(module, "thailand_now", lambda: now)
    client = FakeDiscoveryClient()
    client.fetch_games = Mock(wraps=client.fetch_games)
    service = GameService(client, GameDatabase(tmp_path / "catalog-interval.db"))
    assert service.refresh_catalog().saved == 1
    now += timedelta(hours=23, minutes=59)
    assert service.refresh_catalog().skipped
    client.fetch_games.assert_called_once()
    now += timedelta(minutes=1)
    assert not service.refresh_catalog().skipped
    assert client.fetch_games.call_count == 2


def test_service_reuses_a_partial_live_snapshot_within_the_refresh_interval(tmp_path):
    steam_client = FakeSteamTopClient()
    service = GameService(FakeRawgClient(), GameDatabase(tmp_path / "games.db"), steam_client=steam_client)

    first = service.refresh_live_top_games()
    second = service.refresh_live_top_games()

    assert first.saved == 1
    assert second.skipped is True
    assert steam_client.calls == 1
