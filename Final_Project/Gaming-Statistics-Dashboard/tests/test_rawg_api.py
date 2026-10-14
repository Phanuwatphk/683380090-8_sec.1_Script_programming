from unittest.mock import Mock

import pytest
import requests

from src.api.rawg_api import RawgApiClient, RawgApiError, RawgConfigurationError


def test_fetch_game_details_reads_developer_studios():
    response = Mock()
    response.json.return_value = {"id": 42, "developers": [{"name": "Supergiant Games"}]}
    session = Mock()
    session.get.return_value = response
    client = RawgApiClient(api_key="test-key", session=session)

    assert client.fetch_game_details(42)["developers"] == [{"name": "Supergiant Games"}]
    session.get.assert_called_once_with(
        "https://api.rawg.io/api/games/42", params={"key": "test-key"}, timeout=15
    )


@pytest.mark.parametrize("payload", [[], {"detail": "Not found"}, {"id": 99}])
def test_fetch_game_details_rejects_invalid_or_mismatched_game(payload):
    response = Mock()
    response.json.return_value = payload
    session = Mock()
    session.get.return_value = response
    with pytest.raises(RawgApiError):
        RawgApiClient(api_key="test-key", session=session).fetch_game_details(42)


def test_fetch_games_returns_rawg_results_without_live_request():
    response = Mock()
    response.json.return_value = {"results": [{"id": 1, "name": "Portal 2"}]}
    session = Mock()
    session.get.return_value = response
    client = RawgApiClient(api_key="test-key", session=session)

    assert client.fetch_games(10) == [{"id": 1, "name": "Portal 2"}]
    session.get.assert_called_once()


def test_fetch_games_rejects_missing_api_key():
    with pytest.raises(RawgConfigurationError, match="RAWG_API_KEY"):
        RawgApiClient(api_key="", session=Mock()).fetch_games()


def test_search_games_sends_title_and_allows_an_empty_result():
    response = Mock()
    response.json.return_value = {"results": []}
    session = Mock()
    session.get.return_value = response
    client = RawgApiClient(api_key="test-key", session=session)

    assert client.search_games("Minecraft", 10) == []
    assert session.get.call_args.kwargs["params"] == {
        "key": "test-key",
        "page_size": 10,
        "search": "Minecraft",
    }


def test_fetch_games_requests_a_later_rawg_page():
    response = Mock()
    response.json.return_value = {"results": [{"id": 101, "name": "Later game"}]}
    session = Mock()
    session.get.return_value = response
    client = RawgApiClient(api_key="test-key", session=session)

    assert client.fetch_games(10, ordering="-added", page=2) == [
        {"id": 101, "name": "Later game"}
    ]
    assert session.get.call_args.kwargs["params"] == {
        "key": "test-key",
        "page_size": 10,
        "ordering": "-added",
        "page": 2,
    }


def test_fetch_games_uses_fixed_rawg_page_sizes_for_a_large_result():
    responses = []
    for page in range(1, 4):
        response = Mock()
        first_id = (page - 1) * 40 + 1
        response.json.return_value = {
            "results": [{"id": game_id, "name": f"Game {game_id}"} for game_id in range(first_id, first_id + 40)]
        }
        responses.append(response)
    session = Mock()
    session.get.side_effect = responses
    client = RawgApiClient(api_key="test-key", session=session)

    games = client.fetch_games(100)

    assert [game["id"] for game in games] == list(range(1, 101))
    assert [call.kwargs["params"] for call in session.get.call_args_list] == [
        {"key": "test-key", "page_size": 40},
        {"key": "test-key", "page_size": 40, "page": 2},
        {"key": "test-key", "page_size": 40, "page": 3},
    ]


def test_fetch_games_converts_http_error_to_clear_error():
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError(
        response=Mock(status_code=403)
    )
    session = Mock()
    session.get.return_value = response

    with pytest.raises(RawgApiError, match="API key"):
        RawgApiClient(api_key="bad-key", session=session).fetch_games()


def test_fetch_games_converts_network_failure_to_clear_error():
    session = Mock()
    session.get.side_effect = requests.ConnectionError("offline")

    with pytest.raises(RawgApiError, match="เชื่อมต่อ"):
        RawgApiClient(api_key="test-key", session=session).fetch_games()


@pytest.mark.parametrize("payload", [{"results": []}, {"unexpected": []}, []])
def test_fetch_games_handles_empty_or_unexpected_response(payload):
    response = Mock()
    response.json.return_value = payload
    session = Mock()
    session.get.return_value = response

    with pytest.raises(RawgApiError):
        RawgApiClient(api_key="test-key", session=session).fetch_games()
