from __future__ import annotations

import pandas as pd

GameData = list[dict] | pd.DataFrame


def games_to_dataframe(games: GameData) -> pd.DataFrame:
    """Normalize records once, or reuse an already-prepared analysis frame."""
    if isinstance(games, pd.DataFrame):
        return games
    if not games:
        return pd.DataFrame()

    df = pd.DataFrame(games)

    for column in ["rating", "metacritic", "current_players"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "released" in df.columns:
        df["released"] = pd.to_datetime(df["released"], errors="coerce")
        df["release_year"] = df["released"].dt.year

    return df


def descriptive_statistics(games: GameData) -> dict:
    df = games_to_dataframe(games)

    if df.empty:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
            "std": None,
        }

    rating = df["rating"].dropna()

    if rating.empty:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
            "std": None,
        }

    return {
        "count": int(rating.count()),
        "mean": float(rating.mean()),
        "median": float(rating.median()),
        "min": float(rating.min()),
        "max": float(rating.max()),
        "std": float(rating.std()) if len(rating) > 1 else 0.0,
    }


def genre_frequency(games: list[dict]) -> pd.Series:
    values = [
        genre
        for game in games
        for genre in game.get("genres", [])
        if genre
    ]
    return pd.Series(values, dtype="string").value_counts().astype("int64")


def platform_frequency(games: list[dict]) -> pd.Series:
    values = [
        platform
        for game in games
        for platform in game.get("platforms", [])
        if platform
    ]
    return pd.Series(values, dtype="string").value_counts().astype("int64")


def genre_rating_mean(games: GameData) -> pd.Series:
    df = games_to_dataframe(games)
    if df.empty or "genres" not in df.columns:
        return pd.Series(dtype=float)

    exploded = df[["rating", "genres"]].explode("genres").dropna(subset=["rating", "genres"])
    return exploded.groupby("genres")["rating"].mean().sort_values(ascending=False)


def release_year_frequency(games: GameData) -> pd.Series:
    df = games_to_dataframe(games)
    if df.empty or "release_year" not in df.columns:
        return pd.Series(dtype=int)

    return df["release_year"].dropna().astype(int).value_counts().sort_index()

def frequency_with_proportion(values: pd.Series) -> pd.DataFrame:
    """Return frequency results with their share of all counted occurrences.

    Genre and platform are multi-value fields, so percentages use the total
    number of genre/platform assignments rather than the number of games.
    """
    if values.empty:
        return pd.DataFrame(columns=["label", "count", "proportion"])
    total = int(values.sum())
    frame = values.rename("count").reset_index()
    frame.columns = ["label", "count"]
    frame["count"] = pd.to_numeric(frame["count"], errors="coerce").astype("int64")
    frame["proportion"] = frame["count"] / total if total else 0.0
    return frame


def numeric_values(games: GameData, column: str) -> pd.Series:
    """Return valid numeric values for one stored game field."""
    df = games_to_dataframe(games)
    if df.empty or column not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df[column], errors="coerce").dropna()


def top_current_players(games: GameData, limit: int = 10) -> pd.DataFrame:
    """Return the games with the highest available live Steam-player reading."""
    df = games_to_dataframe(games)
    required = {"name", "current_players"}
    if df.empty or not required.issubset(df.columns):
        return pd.DataFrame(columns=["Game", "Current Players"])
    result = df[["name", "current_players"]].dropna(subset=["current_players"]).copy()
    result["current_players"] = result["current_players"].astype("int64")
    result = result.nlargest(limit, "current_players").rename(
        columns={"name": "Game", "current_players": "Current Players"}
    )
    return result.reset_index(drop=True)


def comparison_dataframe(first: dict, second: dict) -> pd.DataFrame:
    """Build the metric table used when comparing two selected games."""
    return pd.DataFrame(
        {
            "Metric": ["Rating", "Metacritic", "Steam Players"],
            first["name"]: [first.get("rating"), first.get("metacritic"), first.get("current_players")],
            second["name"]: [second.get("rating"), second.get("metacritic"), second.get("current_players")],
        }
    )
