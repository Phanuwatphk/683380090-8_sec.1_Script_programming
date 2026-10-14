from unittest.mock import Mock

import pytest
import requests

from src.api.steam_api import SteamApiClient, SteamApiError, SteamConnectionError


def test_find_app_id_uses_only_an_exact_game_match():
    response = Mock()
    response.json.return_value = {
        "items": [
            {"id": 999, "name": "Portal Stories: Mel", "type": "app"},
            {"id": 620, "name": "Portal 2", "type": "app"},
        ]
    }
    session = Mock()
    session.get.return_value = response

    assert SteamApiClient(session=session).find_app_id("Portal 2") == 620


def test_get_current_players_returns_public_steam_count():
    response = Mock()
    response.json.return_value = {"response": {"player_count": 12345}}
    session = Mock()
    session.get.return_value = response

    assert SteamApiClient(session=session).get_current_players(620) == 12345


def test_steam_client_handles_connection_failure():
    session = Mock()
    session.get.side_effect = requests.ConnectionError("offline")

    with pytest.raises(SteamConnectionError, match="เชื่อมต่อ"):
        SteamApiClient(session=session).find_app_id("Portal 2")


def test_steam_client_rejects_unexpected_player_response():
    response = Mock()
    response.json.return_value = {"unexpected": True}
    session = Mock()
    session.get.return_value = response

    with pytest.raises(SteamApiError):
        SteamApiClient(session=session).get_current_players(620)


def test_steam_client_builds_live_top_games_from_chart_and_player_data():
    chart_response = Mock()
    chart_response.json.return_value = {
        "response": {"ranks": [{"appid": 730, "rank": 1}, {"appid": 570, "rank": 2}]}
    }
    detail_one = Mock()
    detail_one.json.return_value = {
        "730": {"success": True, "data": {"type": "game", "name": "Counter-Strike 2"}}
    }
    detail_two = Mock()
    detail_two.json.return_value = {
        "570": {"success": True, "data": {"type": "game", "name": "Dota 2"}}
    }
    players_one = Mock()
    players_one.json.return_value = {"response": {"player_count": 500}}
    players_two = Mock()
    players_two.json.return_value = {"response": {"player_count": 400}}
    session = Mock()
    session.get.side_effect = [chart_response, detail_one, detail_two, players_one, players_two]

    games = SteamApiClient(session=session, max_workers=1).get_most_played_games(2)

    assert [(game["name"], game["current_players"], game["live_rank"]) for game in games] == [
        ("Counter-Strike 2", 500, 1),
        ("Dota 2", 400, 2),
    ]
