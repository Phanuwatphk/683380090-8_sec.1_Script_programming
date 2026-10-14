from src.analysis.statistics import (
    comparison_dataframe,
    frequency_with_proportion,
    numeric_values,
    top_current_players,
    descriptive_statistics,
    genre_frequency,
    platform_frequency,
    release_year_frequency,
)


def test_prepared_analysis_frame_matches_list_results_without_mutation():
    import pandas as pd
    from src.analysis.statistics import games_to_dataframe, genre_rating_mean

    games = sample_games()
    frame = games_to_dataframe(games)
    original = frame.copy(deep=True)
    assert descriptive_statistics(frame) == descriptive_statistics(games)
    pd.testing.assert_series_equal(genre_rating_mean(frame), genre_rating_mean(games))
    pd.testing.assert_series_equal(release_year_frequency(frame), release_year_frequency(games))
    pd.testing.assert_series_equal(numeric_values(frame, "metacritic"), numeric_values(games, "metacritic"))
    pd.testing.assert_frame_equal(frame, original)


def sample_games():
    return [
        {
            "name": "Game A",
            "rating": 4.0,
            "released": "2020-01-01",
            "genres": ["Action", "RPG"],
            "platforms": ["PC"],
            "metacritic": 80,
        },
        {
            "name": "Game B",
            "rating": 5.0,
            "released": "2021-01-01",
            "genres": ["Action"],
            "platforms": ["PC", "PS5"],
            "metacritic": 90,
        },
        {
            "name": "Game C",
            "rating": 3.0,
            "released": "2021-01-01",
            "genres": ["RPG"],
            "platforms": ["PS5"],
            "metacritic": 70,
        },
    ]


def test_descriptive_statistics():
    stats = descriptive_statistics(sample_games())

    assert stats["count"] == 3
    assert stats["mean"] == 4.0
    assert stats["median"] == 4.0
    assert stats["min"] == 3.0
    assert stats["max"] == 5.0
    assert stats["std"] == 1.0


def test_genre_frequency():
    result = genre_frequency(sample_games())

    assert result["Action"] == 2
    assert result["RPG"] == 2


def test_platform_frequency():
    result = platform_frequency(sample_games())

    assert result["PC"] == 2
    assert result["PS5"] == 2


def test_release_year_frequency():
    result = release_year_frequency(sample_games())

    assert result[2020] == 1
    assert result[2021] == 2


def test_empty_statistics():
    stats = descriptive_statistics([])

    assert stats["count"] == 0
    assert stats["mean"] is None

def test_statistics_supports_proportions_numeric_values_and_player_ranking():
    games = sample_games()
    games[0]["current_players"] = 20
    games[1]["current_players"] = 100
    games[2]["current_players"] = None

    proportions = frequency_with_proportion(genre_frequency(games))
    assert proportions.loc[proportions["label"] == "Action", "proportion"].item() == 0.5
    assert numeric_values(games, "metacritic").tolist() == [80, 90, 70]
    assert top_current_players(games).to_dict("records") == [
        {"Game": "Game B", "Current Players": 100},
        {"Game": "Game A", "Current Players": 20},
    ]


def test_comparison_dataframe_uses_the_selected_games_values():
    comparison = comparison_dataframe(sample_games()[0], sample_games()[1])

    assert comparison.columns.tolist() == ["Metric", "Game A", "Game B"]
    assert comparison.iloc[0].tolist() == ["Rating", 4.0, 5.0]
