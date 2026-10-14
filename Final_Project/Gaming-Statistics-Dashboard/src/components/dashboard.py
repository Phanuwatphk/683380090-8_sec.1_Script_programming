"""Presentation layer for the Gaming Statistics dashboard."""

from __future__ import annotations

from collections import defaultdict
from html import escape
from typing import Any, Callable
from urllib.parse import urlencode

import streamlit as st
if __package__ and __package__.startswith("src."):
    from src.api.rawg_api import RawgApiError
    from src.database.database import DatabaseError
    from src.services.game_service import GameService
    from src.utils.time_utils import format_thailand_timestamp
    from src.components.styles import apply_dashboard_styles
    from src.components.statistics_page import render_statistics_page
else:  # Supports imports when Streamlit runs src/app.py as a script.
    from api.rawg_api import RawgApiError
    from database.database import DatabaseError
    from services.game_service import GameService
    from utils.time_utils import format_thailand_timestamp
    from components.styles import apply_dashboard_styles
    from components.statistics_page import render_statistics_page


NAVIGATION = (
    ("home", "Home"),
    ("games", "Game Library"),
    ("search", "Search"),
    ("genres", "Genres"),
    ("top_rated", "Top Rated"),
    ("players", "Live Players"),
    ("statistics", "Statistics"),
)
GAMES_PER_PAGE = 50
LIBRARY_WIDGET_KEYS = (
    "library-genres", "library-platforms", "library-minimum-rating",
    "library-release-years", "library-sort-by", "library-sort-order",
)


def render_dashboard(game_service: GameService) -> None:
    """Render dashboard pages using data supplied by GameService."""
    apply_dashboard_styles()
    _initialize_navigation_state()
    should_scroll_to_top = st.session_state.pop("scroll_to_top", False)
    # Keep the counter across runs so consecutive resets have different scripts.
    scroll_request_id = st.session_state.get("scroll_request_id", 0)
    _render_sidebar()

    page = st.session_state.dashboard_page
    if page == "home":
        _render_home(game_service)
    elif page == "games":
        _render_games_page(game_service)
    elif page == "search":
        _render_search_page(game_service)
    elif page == "genres":
        _render_genres_page(game_service)
    elif page == "top_rated":
        _render_top_rated_page(game_service)
    elif page == "players":
        _render_players_page(game_service)
    elif page == "statistics":
        _page_heading("Statistics", "Explore descriptive statistics, distributions, and game comparisons.")
        render_statistics_page(
            game_service.get_games(),
            live_games=game_service.get_live_top_games(),
        )
    elif page == "detail":
        _render_detail_page(game_service)

    if should_scroll_to_top:
        _render_scroll_reset(scroll_request_id)


def _initialize_navigation_state() -> None:
    st.session_state.setdefault("dashboard_page", "home")
    st.session_state.setdefault("selected_game_id", None)
    requested_genre = st.query_params.pop("genre", None)
    if requested_genre:
        st.session_state.dashboard_page = "genres"
        st.session_state.selected_genre = requested_genre
        st.session_state[f"pagination-genre-{requested_genre}"] = 1
        _scroll_to_top()


def _render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand">Gaming Statistics</div>'
            '<div class="sidebar-label">Game discovery dashboard</div>',
            unsafe_allow_html=True,
        )
        st.caption("Game data: [RAWG](https://rawg.io) · Players: [Steam](https://store.steampowered.com/charts/mostplayed)")
        st.divider()

        for page, label in NAVIGATION:
            if st.button(
                label,
                key=f"navigation-{page}",
                type="primary" if st.session_state.dashboard_page == page else "secondary",
                width="stretch",
            ):
                _go_to(page)


def _render_home(game_service: GameService) -> None:
    games = st.session_state.get("home-page-games")
    if games is None:
        games = game_service.get_popular_games(limit=GAMES_PER_PAGE)
    live_games = game_service.get_live_top_games()
    _page_heading("Popular Games", "Popular and widely played games saved from the latest RAWG discovery update.")

    if not games:
        _render_empty_state("Popular games are unavailable", "Refresh the page to request the latest game discovery snapshot.")
        return
    current_players = [game["current_players"] for game in live_games if game["current_players"] is not None]
    latest_update = max((game["players_updated_at"] or "" for game in live_games), default="")
    _render_top_player_stat(sum(current_players), latest_update)
    st.markdown("### Popular games")
    _render_remote_paginated_game_grid(
        games,
        page_key="home",
        columns_per_row=4,
        key_prefix="home",
        fetch_page=lambda page: game_service.import_catalog_page(
            page, page_size=GAMES_PER_PAGE
        ),
    )


def _render_games_page(game_service: GameService) -> None:
    games = game_service.get_games()
    _page_heading("Game Library", "Browse, filter, and compare your saved games.")
    if not games:
        _render_empty_state("Your library is empty", "Use Search to add games and build your collection.")
        return

    with st.container(border=True, key="library-filters"):
        games = _render_collection_filters(games)
        sort_column, order_column = st.columns(2)
        with sort_column:
            sort_by = st.selectbox(
                "Sort by", ["Rating", "Release Date", "Name"], key="library-sort-by",
            )
        with order_column:
            sort_order = st.selectbox(
                "Order", ["Descending", "Ascending"], key="library-sort-order",
            )

    games = _sort_games(games, sort_by, descending=sort_order == "Descending")
    if not games:
        _render_empty_state("No matching games", "Try broadening the genre, platform, or rating filters.")
        return

    st.caption(f"{len(games):,} games · Sorted by {sort_by.lower()} ({sort_order.lower()})")
    _render_paginated_game_grid(games, page_key="games", key_prefix="games")


def _render_collection_filters(games: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Render collection filters and return games matching every selected value."""
    genre_options = sorted({genre for game in games for genre in game["genres"]})
    platform_options = sorted({platform for game in games for platform in game["platforms"]})
    release_years = sorted(year for game in games if (year := _release_year(game)) is not None)
    ratings = [game["rating"] for game in games if game["rating"] is not None]

    genre_column, platform_column, rating_column, year_column = st.columns(4)
    with genre_column:
        selected_genres = st.multiselect("Genre", genre_options, placeholder="All genres", key="library-genres")
    with platform_column:
        selected_platforms = st.multiselect("Platform", platform_options, placeholder="All platforms", key="library-platforms")
    with rating_column:
        minimum_rating = st.number_input("Minimum rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1, disabled=not ratings, key="library-minimum-rating")
    with year_column:
        if release_years and release_years[0] != release_years[-1]:
            selected_years = st.slider(
                "Release year", min_value=release_years[0], max_value=release_years[-1],
                value=(release_years[0], release_years[-1]),
                key="library-release-years",
            )
        else:
            st.text_input("Release year", value=str(release_years[0]) if release_years else "Unavailable", disabled=True)
            selected_years = (release_years[0], release_years[0]) if release_years else None

    return _filter_games(games, selected_genres, selected_platforms, minimum_rating, selected_years if release_years else None)


def _filter_games(
    games: list[dict[str, Any]],
    selected_genres: list[str] | tuple[str, ...] = (),
    selected_platforms: list[str] | tuple[str, ...] = (),
    minimum_rating: float = 0.0,
    release_year_range: tuple[int, int] | None = None,
) -> list[dict[str, Any]]:
    """Return games that satisfy all collection-filter conditions."""
    return [
        game for game in games
        if (not selected_genres or set(selected_genres).intersection(game["genres"]))
        and (not selected_platforms or set(selected_platforms).intersection(game["platforms"]))
        and (minimum_rating == 0 or (game["rating"] is not None and game["rating"] >= minimum_rating))
        and (release_year_range is None or (_release_year(game) is not None and release_year_range[0] <= _release_year(game) <= release_year_range[1]))
    ]


def _release_year(game: dict[str, Any]) -> int | None:
    released = game.get("released") or ""
    try:
        return int(released[:4])
    except (TypeError, ValueError):
        return None


def _sort_games(games: list[dict[str, Any]], sort_by: str, descending: bool = True) -> list[dict[str, Any]]:
    """Sort the library consistently, keeping missing values at the end."""
    if sort_by == "Name":
        return sorted(games, key=lambda game: game["name"].lower(), reverse=descending)
    field = "rating" if sort_by == "Rating" else "released"
    available = [game for game in games if game[field] is not None]
    missing = [game for game in games if game[field] is None]
    return sorted(available, key=lambda game: game[field], reverse=descending) + missing


def _render_search_page(game_service: GameService) -> None:
    _page_heading("Search Games", "Search your library first; missing games are fetched and saved automatically.")
    with st.form("game-search"):
        search_term = st.text_input(
            "Game title", placeholder="For example: Hades, Portal, or Minecraft"
        )
        submitted = st.form_submit_button("Search", type="primary")
    if submitted and search_term.strip():
        try:
            with st.spinner("Searching games..."):
                local_results = game_service.search_games(search_term)
                st.session_state.search_results_remote = not bool(local_results)
                st.session_state.search_results_games = (
                    game_service.search_and_import_games(
                        search_term, page_size=GAMES_PER_PAGE
                    )
                    if st.session_state.search_results_remote
                    else local_results
                )
                st.session_state.search_results_term = search_term.strip()
                st.session_state.search_results_page = 1
                st.session_state["remote-pagination-search-results"] = 1
        except (RawgApiError, DatabaseError, ValueError) as error:
            st.error(str(error))
            return

    active_term = st.session_state.get("search_results_term", "")
    if not search_term.strip() and not active_term:
        _render_empty_state("Ready to search", "Enter a game title above to see results.")
        return
    if not active_term:
        return
    games = st.session_state.search_results_games
    if not games:
        _render_empty_state("No matching games", f'No games matched “{active_term}”.')
        return
    st.caption(f'Results for “{active_term}” · {len(games)} game(s)')
    if st.session_state.get("search_results_remote", False):
        _render_remote_paginated_game_grid(
            games,
            page_key="search-results",
            columns_per_row=1,
            key_prefix="search",
            fetch_page=lambda page: game_service.import_search_page(
                active_term, page, page_size=GAMES_PER_PAGE
            ),
        )
    else:
        _render_paginated_game_grid(
            games, page_key="search-results", columns_per_row=1, key_prefix="search"
        )


def _render_genres_page(game_service: GameService) -> None:
    _page_heading("Genres", "Explore the games in your library by genre.")
    grouped_games: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for game in game_service.get_games():
        for genre in game["genres"]:
            grouped_games[genre].append(game)

    if not grouped_games:
        _render_empty_state("No genre data yet", "Add games through Search to start exploring genres.")
        return
    selected_genre = st.session_state.get("selected_genre")
    if selected_genre and selected_genre not in grouped_games:
        st.info(f'No saved games found for “{selected_genre}”. Browse the genres below.')
    for genre in sorted(grouped_games, key=lambda genre: (genre != selected_genre, genre)):
        with st.expander(
            f"{genre} · {len(grouped_games[genre])} game(s)",
            expanded=genre == selected_genre,
        ):
            _render_paginated_game_grid(
                grouped_games[genre],
                page_key=f"genre-{genre}",
                columns_per_row=3,
                key_prefix=f"genre-{genre}",
            )


def _render_top_rated_page(game_service: GameService) -> None:
    _page_heading("Top Rated Games", "The highest-rated games in your saved library.")
    games = _sort_by_rating(game_service.get_games())
    if not games:
        _render_empty_state("Your library is empty", "Use Search to add games and view their ratings.")
        return
    _render_paginated_game_grid(
        games, page_key="top-rated", key_prefix="top-rated", show_rank=True
    )


def _render_players_page(game_service: GameService) -> None:
    _page_heading("Live Players", "Steam's latest Top 100 games by current active player count.")
    games = game_service.get_live_top_games()
    if not games:
        _render_empty_state(
            "Live Steam data is unavailable",
            "Refresh the page to request the latest ranking snapshot.",
        )
        return
    latest_update = max(game["players_updated_at"] or "" for game in games)
    if latest_update:
        st.caption(f"Last updated: {_display_timestamp(latest_update)}")
    _render_paginated_game_grid(games, page_key="players", key_prefix="players", show_rank=True)

def _render_detail_page(game_service: GameService) -> None:
    game_id = st.session_state.selected_game_id
    try:
        game = game_service.get_game_details(game_id)
    except RawgApiError as error:
        st.warning(f"Developer information could not be loaded: {error}")
        game = game_service.get_game_details(game_id, fetch_developers=False)
    if game is None:
        _render_empty_state("Game not found", "This game may have been removed from the library.")
        if st.button("← Back to Games"):
            _return_from_details()
        return

    if st.button("← Back to Games"):
        _return_from_details()
    _page_heading(game["name"], "Everything you need to know at a glance.")

    if game["image"]:
        st.markdown(
            f'<img class="detail-cover" src="{escape(str(game["image"]), quote=True)}" '
            f'alt="Cover for {escape(game["name"], quote=True)}">',
            unsafe_allow_html=True,
        )

    st.markdown("### Game Information")
    fields = (
        ("Rating", f'{game["rating"]:.2f} / 5' if game["rating"] is not None else "N/A"),
        ("Steam players now", f'{game["current_players"]:,}' if game["current_players"] is not None else "N/A"),
        ("Release date", game["released"] or "–"),
        ("Metacritic", game["metacritic"] if game["metacritic"] is not None else "–"),
    )
    stat_cards = "".join(
        f'<div class="detail-panel"><div class="detail-label">{escape(label)}</div>'
        f'<div class="detail-value">{escape(str(value))}</div></div>'
        for label, value in fields
    )
    platforms = "".join(f'<span class="platform-tag">{escape(platform)}</span>' for platform in game["platforms"])
    genres = "".join(_genre_link(genre) for genre in game["genres"])
    developers = "".join(
        f'<span class="platform-tag">{escape(developer)}</span>'
        for developer in game.get("developers", [])
    )
    st.markdown(
        f'<div class="detail-stats">{stat_cards}</div>'
        '<div class="detail-taxonomy">'
        '<section class="detail-section"><h3>Platforms</h3><div class="detail-tags">'
        f'{platforms or "<span class=detail-empty>No platform data available.</span>"}</div></section>'
        '<section class="detail-section"><h3>Genres</h3><div class="detail-tags">'
        f'{genres or "<span class=detail-empty>No genre data available.</span>"}</div></section>'
        '<section class="detail-section detail-developers"><h3>Developers</h3><div class="detail-tags">'
        f'{developers or "<span class=detail-empty>No developer data available.</span>"}</div></section></div>',
        unsafe_allow_html=True,
    )


def _render_game_grid(
    games: list[dict[str, Any]],
    columns_per_row: int = 3,
    key_prefix: str = "games",
    show_rank: bool = False,
    rank_start: int = 1,
) -> None:
    for start in range(0, len(games), columns_per_row):
        columns = st.columns(columns_per_row)
        for offset, (column, game) in enumerate(zip(columns, games[start : start + columns_per_row])):
            with column:
                rank = rank_start + start + offset if show_rank else None
                _render_game_card(game, f"{key_prefix}-{start + offset}", rank)


def _render_paginated_game_grid(
    games: list[dict[str, Any]],
    page_key: str,
    columns_per_row: int = 3,
    key_prefix: str = "games",
    show_rank: bool = False,
) -> None:
    """Render exactly up to 50 games and page through the remaining local records."""
    total_pages = max(1, (len(games) + GAMES_PER_PAGE - 1) // GAMES_PER_PAGE)
    state_key = f"pagination-{page_key}"
    current_page = min(st.session_state.get(state_key, 1), total_pages)
    st.session_state[state_key] = current_page
    start = (current_page - 1) * GAMES_PER_PAGE
    cards_container = st.empty()
    with cards_container.container():
        _render_game_grid(
            games[start : start + GAMES_PER_PAGE],
            columns_per_row=columns_per_row,
            key_prefix=f"{key_prefix}-page-{current_page}",
            show_rank=show_rank,
            rank_start=start + 1,
        )
    if total_pages == 1:
        return

    previous_column, page_column, next_column = st.columns((1, 2, 1))
    with previous_column:
        if st.button("← Previous", key=f"{state_key}-previous", disabled=current_page == 1):
            cards_container.empty()
            st.session_state[state_key] = current_page - 1
            _scroll_to_top()
            st.rerun()
    with page_column:
        st.markdown(f"<p style='text-align:center'>Page {current_page} of {total_pages}</p>", unsafe_allow_html=True)
    with next_column:
        if st.button("Next →", key=f"{state_key}-next", disabled=current_page == total_pages):
            cards_container.empty()
            st.session_state[state_key] = current_page + 1
            _scroll_to_top()
            st.rerun()


def _render_remote_paginated_game_grid(
    games: list[dict[str, Any]],
    page_key: str,
    fetch_page: Callable[[int], list[dict[str, Any]]],
    columns_per_row: int = 3,
    key_prefix: str = "games",
) -> None:
    """Render one 50-game API page and load another only after navigation."""
    state_key = f"remote-pagination-{page_key}"
    current_page = st.session_state.get(state_key, 1)
    cards_container = st.empty()
    with cards_container.container():
        _render_game_grid(
            games[:GAMES_PER_PAGE],
            columns_per_row=columns_per_row,
            key_prefix=f"{key_prefix}-page-{current_page}",
            rank_start=(current_page - 1) * GAMES_PER_PAGE + 1,
        )

    previous_column, page_column, next_column = st.columns((1, 2, 1))
    with previous_column:
        previous = st.button("← Previous", key=f"{state_key}-previous", disabled=current_page == 1)
    with page_column:
        st.markdown(f"<p style='text-align:center'>Page {current_page}</p>", unsafe_allow_html=True)
    with next_column:
        next_page = st.button(
            "Next →", key=f"{state_key}-next", disabled=len(games) < GAMES_PER_PAGE
        )

    requested_page = current_page - 1 if previous else current_page + 1 if next_page else None
    if requested_page is None or requested_page == current_page:
        return
    try:
        with st.spinner("Loading games..."):
            page_games = fetch_page(requested_page)
    except (RawgApiError, DatabaseError, ValueError) as error:
        st.error(str(error))
        return
    if not page_games:
        st.info("No more games available.")
        return
    cards_container.empty()
    st.session_state[state_key] = requested_page
    st.session_state[f"{page_key}-page-games"] = page_games
    if page_key == "search-results":
        st.session_state.search_results_games = page_games
        st.session_state.search_results_page = requested_page
    elif page_key == "home":
        st.session_state["home-page-games"] = page_games
    _scroll_to_top()
    st.rerun()


def _render_top_player_stat(total_players: int, latest_update: str) -> None:
    """Render the sole Home KPI: active players across Steam's Top 100."""
    updated_note = (
        f"Last updated {_display_timestamp(latest_update)}" if latest_update else "Update time unavailable"
    )
    st.markdown(
        '<div class="hero-stat">'
        '<div class="hero-stat-label">Players in the Steam Top 100</div>'
        f'<div class="hero-stat-value">{total_players:,}</div>'
        f'<div class="hero-stat-note">{escape(updated_note)}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_game_card(game: dict[str, Any], key_prefix: str, rank: int | None = None) -> None:
    if game["image"]:
        cover = (
            f'<img class="game-cover" loading="lazy" src="{escape(str(game["image"]), quote=True)}" '
            f'alt="Cover for {escape(str(game["name"]), quote=True)}">'
        )
    else:
        cover = '<div class="game-cover game-cover--empty">No cover image available</div>'

    rank_text = f"#{rank} · " if rank is not None else ""
    rating = f"Rating {game['rating']:.1f}" if game["rating"] is not None else ""
    summary = f"{rank_text}{rating}" or "Steam"
    players = (
        f"{game['current_players']:,} players online"
        if game["current_players"] is not None
        else "Player count unavailable"
    )
    tags = "".join(_genre_link(genre) for genre in game["genres"][:2]) or '<span class="tag tag--muted">Uncategorized</span>'
    st.markdown(
        f'<div class="game-tile">{cover}<div class="game-card"><div class="game-name" title="{escape(game["name"], quote=True)}">{escape(game["name"])}</div>'
        f'<div class="game-meta">{summary}</div>'
        f'<div class="game-meta">{players}</div><div class="game-tags">{tags}</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button("View Details", key=f"detail-{key_prefix}-{game['game_id']}", width="stretch"):
        st.session_state.selected_game_id = game["game_id"]
        _go_to("detail")


def _render_empty_state(title: str, message: str) -> None:
    st.markdown(
        f'<div class="empty-state"><h3>{escape(title)}</h3><p>{escape(message)}</p></div>',
        unsafe_allow_html=True,
    )


def _genre_link(genre: str) -> str:
    """Link a genre chip to the matching section of the Genres page."""
    href = escape(f"?{urlencode({'genre': genre})}", quote=True)
    return f'<a class="tag genre-link" href="{href}" target="_self">{escape(genre)}</a>'


def _page_heading(title: str, subtitle: str) -> None:
    st.markdown(
        '<header class="page-heading"><div class="page-kicker">Gaming Statistics</div>'
        f'<h1 class="page-title">{escape(title)}</h1>'
        f'<p class="page-subtitle">{escape(subtitle)}</p></header>',
        unsafe_allow_html=True,
    )


def _sort_by_rating(games: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(games, key=lambda game: game["rating"] if game["rating"] is not None else -1, reverse=True)


def _display_timestamp(value: str) -> str:
    """Display timestamps in Thailand time, to second precision."""
    return format_thailand_timestamp(value)


def _go_to(page: str) -> None:
    if page == "detail" and st.session_state.dashboard_page != "detail":
        st.session_state.detail_origin = st.session_state.dashboard_page
        # Streamlit removes widget state when its page is no longer rendered.
        st.session_state.detail_library_state = {
            key: st.session_state[key]
            for key in LIBRARY_WIDGET_KEYS if key in st.session_state
        }
    st.session_state.dashboard_page = page
    _scroll_to_top()
    st.rerun()


def _return_from_details() -> None:
    """Return to the originating collection with its existing browsing state."""
    origin = st.session_state.get("detail_origin", "games")
    if origin not in {page for page, _ in NAVIGATION}:
        origin = "games"
    if origin == "games":
        for key, value in st.session_state.get("detail_library_state", {}).items():
            st.session_state[key] = value
    _go_to(origin)

def _scroll_to_top() -> None:
    """Schedule a unique top-of-page viewport reset for the following run."""
    st.session_state.scroll_to_top = True
    st.session_state.scroll_request_id = st.session_state.get("scroll_request_id", 0) + 1

def _render_scroll_reset(scroll_request_id: int) -> None:
    """Reset the viewport once when the navigation script mounts in the DOM."""
    st.html(
        """
        <script>
        // Unique request token: __SCROLL_REQUEST_ID__.  A changing script body makes Streamlit remount it on every page change.
        (() => {
            const scrollToTop = () => {
                try {
                    const main = document.querySelector("section[data-testid=stMain]");
                    const containers = new Set([
                        document.scrollingElement,
                        document.documentElement,
                        document.body,
                        ...document.querySelectorAll(
                            "section[data-testid=stMain], [data-testid=stAppViewContainer], .stApp"
                        ),
                    ]);

                    for (let element = main; element; element = element.parentElement) {
                        containers.add(element);
                    }

                    for (const container of containers) {
                        if (container) {
                            container.scrollTop = 0;
                            container.scrollLeft = 0;
                        }
                    }

                    const activeElement = document.activeElement;
                    if (
                        activeElement &&
                        typeof activeElement.blur === "function"
                    ) {
                        activeElement.blur();
                    }

                    window.scrollTo({ top: 0, left: 0, behavior: "auto" });
                } catch (_) {
                    window.scrollTo({ top: 0, left: 0, behavior: "auto" });
                }
            };

            scrollToTop();
        })();
        </script>
        """.replace("__SCROLL_REQUEST_ID__", str(scroll_request_id)),
        unsafe_allow_javascript=True,
    )
