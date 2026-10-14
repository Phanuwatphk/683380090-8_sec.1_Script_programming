from src.utils.data_processing import process_game, process_games
import pytest


@pytest.mark.parametrize("ratings_count", [None, 0, 1])
def test_rawg_unrated_zero_is_missing_even_with_a_single_vote(ratings_count):
    assert process_game({"id": 42, "rating": 0, "ratings_count": ratings_count})["rating"] is None


def test_malformed_api_records_do_not_abort_normalization():
    games = process_games([None, "invalid", [], {"id": "abc"}, {"id": 7, "genres": [None, {"name": "Action"}], "developers": None}])
    assert len(games) == 1
    assert games[0]["genres"] == ["Action"]
    assert games[0]["developers"] == []


@pytest.mark.parametrize("value", ["abc", "", "NaN", "Infinity", float("inf"), -float("inf")])
def test_invalid_optional_numbers_are_missing_instead_of_crashing(value):
    game = process_game({"id": 7, "rating": value, "metacritic": value})
    assert game["rating"] is None
    assert game["metacritic"] is None


def test_process_game_normalizes_nested_rawg_fields():
    game = process_game(
        {
            "id": 42,
            "name": "Hades",
            "rating": "4.8",
            "released": "2020-09-17",
            "genres": [{"name": "Action"}, {"name": "Roguelike"}, {"name": "Action"}],
            "developers": [{"name": " Supergiant Games "}, {"name": "Supergiant Games"}],
            "platforms": [
                {"platform": {"name": "PC"}},
                {"platform": {"name": "Nintendo Switch"}},
                {"platform": {"name": "PC"}},
            ],
            "metacritic": 93,
            "ratings_count": 1200,
            "background_image": "https://example.test/hades.jpg",
        }
    )

    assert game == {
        "game_id": 42,
        "name": "Hades",
        "rating": 4.8,
        "released": "2020-09-17",
        "genres": ["Action", "Roguelike"],
        "developers": ["Supergiant Games"],
        "platforms": ["PC", "Nintendo Switch"],
        "metacritic": 93,
        "ratings_count": 1200,
        "image": "https://example.test/hades.jpg",
    }


def test_process_game_handles_missing_optional_values_safely():
    game = process_game({"id": "7", "name": None, "genres": None, "platforms": []})

    assert game is not None
    assert game["game_id"] == 7
    assert game["name"] == "Unknown game"
    assert game["genres"] == []
    assert game["platforms"] == []
    assert game["rating"] is None


def test_process_games_skips_records_without_a_game_id():
    assert process_games([{"name": "Missing ID"}, {"id": 3, "name": "Valid"}]) == [
        {
            "game_id": 3,
            "name": "Valid",
            "rating": None,
            "released": None,
            "genres": [],
            "developers": [],
            "platforms": [],
            "metacritic": None,
            "ratings_count": None,
            "image": None,
        }
    ]
