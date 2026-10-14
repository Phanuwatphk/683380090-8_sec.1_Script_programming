"""Statistics charts and comparisons, using one prepared analysis frame."""

from __future__ import annotations

from typing import Any

import altair as alt
import pandas as pd
import streamlit as st

if __package__ and __package__.startswith("src."):
    from src.analysis import statistics as analysis
else:
    from analysis import statistics as analysis


def render_statistics_page(
    games: list[dict[str, Any]], live_games: list[dict[str, Any]] | None = None
) -> None:
    """Render the statistics route using already-loaded game records."""
    if not games:
        st.info("No data available. Add games through Search before viewing statistics.")
        return

    frame = analysis.games_to_dataframe(games)
    stats = analysis.descriptive_statistics(frame)

    metrics = (
        ("Average Rating", "mean"),
        ("Median Rating", "median"),
        ("Highest Rating", "max"),
        ("Lowest Rating", "min"),
        ("Rating standard deviation", "std"),
    )
    with st.container(key="statistics-metrics"):
        columns = st.columns(1 + len(metrics))
        columns[0].metric("Games Tracked", len(games))
        for column, (label, field) in zip(columns[1:], metrics):
            value = stats[field]
            column.metric(label, f"{value:.2f}" if value is not None else "N/A")

    st.subheader("Genre Distribution")
    genre_data = analysis.genre_frequency(games)
    if not genre_data.empty:
        genre_df = analysis.frequency_with_proportion(genre_data).head(10).rename(
            columns={"label": "Genre", "count": "Count", "proportion": "Share"}
        )

        genre_chart = (
            alt.Chart(genre_df)
            .mark_bar()
            .encode(
                x=alt.X("Genre:N", sort="-y"),
                y=alt.Y(
                    "Count:Q",
                    title="Games",
                ),
                tooltip=["Genre", "Count", alt.Tooltip("Share:Q", format=".1%")],
            )
        )

        _render_chart(genre_chart)
    else:
        st.info("No genre data available.")


    st.subheader("Platform Distribution")

    platform_data = analysis.platform_frequency(games)

    if not platform_data.empty:
        platform_df = analysis.frequency_with_proportion(platform_data).head(10).rename(
            columns={"label": "Platform", "count": "Count", "proportion": "Share"}
        )

        platform_chart = (
            alt.Chart(platform_df)
            .mark_bar()
            .encode(
                x=alt.X("Platform:N", sort="-y"),
                y=alt.Y(
                    "Count:Q",
                    title="Games",
                ),
                tooltip=["Platform", "Count", alt.Tooltip("Share:Q", format=".1%")] ,
            )
        )

        _render_chart(platform_chart)
    else:
        st.info("No platform data available.")


    st.subheader("Rating by Genre")

    rating_data = analysis.genre_rating_mean(frame).head(10)

    if not rating_data.empty:
        rating_df = rating_data.rename("Average Rating").reset_index()
        rating_df.columns = ["Genre", "Average Rating"]

        rating_chart = (
            alt.Chart(rating_df)
            .mark_bar()
            .encode(
                x=alt.X("Genre:N", sort="-y"),
                y=alt.Y(
                    "Average Rating:Q",
                    scale=alt.Scale(domain=[0, 5]),
                    title="Rating",
                ),
                tooltip=["Genre", "Average Rating"],
            )
        )

        _render_chart(rating_chart)
    else:
        st.info("No rating-by-genre data available.")


    st.subheader("Release Year Distribution")

    year_data = analysis.release_year_frequency(frame)

    if not year_data.empty:
        year_df = year_data.rename("Games").reset_index()
        year_df.columns = ["Year", "Games"]

        year_chart = (
            alt.Chart(year_df)
            .mark_line(point=True)
            .encode(
                x=alt.X("Year:O", title="Release Year"),
                y=alt.Y(
                    "Games:Q",
                    title="Games",
                ),
                tooltip=["Year", "Games"],
            )
        )

        _render_chart(year_chart)
    else:
        st.info("No release-year data available.")

    _render_metacritic_distribution(frame)
    _render_live_player_chart(live_games or [])

    game_names = sorted(game["name"] for game in games)

    col1, col2 = st.columns(2)
    with col1:
        game_a = st.selectbox("Game A", game_names, key="comparison-game-a")
    with col2:
        game_b = st.selectbox(
            "Game B",
            game_names,
            index=1 if len(game_names) > 1 else 0,
            key="comparison-game-b",
        )

    a = next(game for game in games if game["name"] == game_a)
    b = next(game for game in games if game["name"] == game_b)

    comparison = analysis.comparison_dataframe(a, b)

    st.dataframe(comparison, hide_index=True, width="stretch")



def _render_metacritic_distribution(games: analysis.GameData) -> None:
    st.subheader("Metacritic score distribution")
    scores = analysis.numeric_values(games, "metacritic")
    if scores.empty:
        st.info("No Metacritic data available.")
        return
    data = pd.DataFrame({"Metacritic score": scores})
    chart = (
        alt.Chart(data)
        .mark_bar(color="#845ec2")
        .encode(
            x=alt.X("Metacritic score:Q", bin=alt.Bin(maxbins=10), title="Metacritic score"),
            y=alt.Y("count():Q", title="Games"),
            tooltip=[alt.Tooltip("count():Q", title="Games")],
        )
    )
    _render_chart(chart)


def _render_live_player_chart(games: list[dict[str, Any]]) -> None:
    st.subheader("Top live Steam players")
    data = analysis.top_current_players(games)
    if data.empty:
        st.info("No live Steam-player data available.")
        return
    chart = (
        alt.Chart(data)
        .mark_bar(color="#00a6a6")
        .encode(
            x=alt.X("Game:N", sort="-y", title=None, axis=alt.Axis(labelAngle=-35)),
            y=alt.Y("Current Players:Q", title="Players"),
            tooltip=["Game", alt.Tooltip("Current Players:Q", format=",")],
        )
    )
    _render_chart(chart)


def _render_chart(chart: alt.Chart) -> None:
    """Keep statistics charts consistent with the dashboard's card surfaces."""
    with st.container(border=True):
        st.altair_chart(
            chart.configure(background="#ffffff")
            .configure_view(stroke=None)
            .configure_axis(labelColor="#61718a", titleColor="#3d506d", gridColor="#edf1f7")
            .configure_range(category=["#2563eb", "#5796e5", "#8ab7ee", "#102947"]),
            width="stretch",
        )
