"""Streamlit entry point for the Gaming Statistics Dashboard."""

from __future__ import annotations

import os
from datetime import timedelta

import streamlit as st

if __package__:
    from .config import catalog_refresh_interval, live_refresh_interval, resolve_database_path
    from .api.rawg_api import RawgApiClient, RawgApiError
    from .api.steam_api import SteamApiError
    from .components.dashboard import render_dashboard
    from .database.database import DatabaseError, GameDatabase
    from .services.game_service import GameService
else:  # `streamlit run src/app.py` executes this module as a script.
    from config import catalog_refresh_interval, live_refresh_interval, resolve_database_path
    from api.rawg_api import RawgApiClient, RawgApiError
    from api.steam_api import SteamApiError
    from components.dashboard import render_dashboard
    from database.database import DatabaseError, GameDatabase
    from services.game_service import GameService

def build_game_service() -> GameService:
    """Create the dependencies used by the dashboard for this application run."""
    # Load .env before resolving the database override it may contain.
    api_client = RawgApiClient()
    return GameService(api_client, GameDatabase(resolve_database_path()))


def _refresh_dashboard_data(
    game_service: GameService, live_interval: timedelta, catalog_interval: timedelta,
) -> None:
    """Check snapshot age on each rerun; the service reuses fresh shared data."""
    try:
        with st.spinner("Updating game discoveries and Steam live players..."):
            st.session_state.catalog_refresh_result = game_service.refresh_catalog(catalog_interval)
        st.session_state.pop("catalog_refresh_error", None)
    except RawgApiError as error:
        st.session_state.catalog_refresh_error = str(error)
    try:
        with st.spinner("Updating game discoveries and Steam live players..."):
            st.session_state.home_refresh_result = game_service.refresh_live_top_games(live_interval)
        st.session_state.pop("home_refresh_error", None)
    except SteamApiError as error:
        # Preserve the last successful SQLite snapshot if Steam is temporarily unavailable.
        st.session_state.home_refresh_error = str(error)


def main() -> None:
    """Configure Streamlit and render the dashboard."""
    st.set_page_config(page_title="Gaming Statistics", layout="wide")
    try:
        game_service = build_game_service()
        if os.getenv("GAMING_DASHBOARD_SKIP_REFRESH") != "1":
            _refresh_dashboard_data(game_service, live_refresh_interval(), catalog_refresh_interval())
        if error := st.session_state.get("home_refresh_error"):
            st.warning(f"Showing the last saved Steam ranking: {error}")
        if error := st.session_state.get("catalog_refresh_error"):
            st.warning(f"Showing the last saved game catalogue: {error}")
        render_dashboard(game_service)
    except DatabaseError as error:
        st.error(str(error))


if __name__ == "__main__":
    main()
