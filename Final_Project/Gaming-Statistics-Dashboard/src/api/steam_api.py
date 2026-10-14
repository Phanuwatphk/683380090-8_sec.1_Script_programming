"""Small client for Steam's public store and current-player endpoints."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from typing import Any

import requests


STEAM_STORE_SEARCH_URL = "https://store.steampowered.com/api/storesearch/"
STEAM_CURRENT_PLAYERS_URL = (
    "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
)
STEAM_TOP_GAMES_URL = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
STEAM_APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails/"


class SteamApiError(RuntimeError):
    """Raised when a Steam request cannot provide a trustworthy result."""


class SteamConnectionError(SteamApiError):
    """Raised when Steam cannot be reached; retrying every game would be wasteful."""


class SteamApiClient:
    """Resolve a Steam app ID and read its current Steam player count."""

    def __init__(
        self, session: requests.Session | None = None, timeout: int = 5, max_workers: int = 8
    ) -> None:
        self.session = session or requests.Session()
        self.timeout = timeout
        self.max_workers = max_workers

    def find_app_id(self, game_name: str) -> int | None:
        """Return an exact Steam-store name match, never a speculative match."""
        payload = self._get_json(
            STEAM_STORE_SEARCH_URL,
            {"term": game_name, "l": "english", "cc": "us"},
        )
        items = payload.get("items")
        if not isinstance(items, list):
            raise SteamApiError("Steam Store ส่งรูปแบบข้อมูลที่ไม่คาดไว้")

        expected_name = _normalized_name(game_name)
        for item in items:
            # Steam Store currently calls purchasable games ``app``.  Retain
            # ``game`` too because older responses and mocks may use it.
            if not isinstance(item, dict) or item.get("type") not in {"app", "game"}:
                continue
            app_id = item.get("id")
            if _normalized_name(item.get("name")) == expected_name and isinstance(app_id, int):
                return app_id
        return None

    def get_current_players(self, app_id: int) -> int | None:
        """Read the number of people currently active in one Steam app."""
        payload = self._get_json(STEAM_CURRENT_PLAYERS_URL, {"appid": app_id})
        response = payload.get("response")
        if not isinstance(response, dict):
            raise SteamApiError("Steam ส่งรูปแบบข้อมูลจำนวนผู้เล่นที่ไม่คาดไว้")
        player_count = response.get("player_count")
        if isinstance(player_count, int) and player_count >= 0:
            return player_count
        return None

    def get_most_played_games(self, limit: int = 50) -> list[dict[str, Any]]:
        """Return Steam's current top games with exact current-player readings."""
        if not 1 <= limit <= 100:
            raise ValueError("จำนวนเกมยอดนิยมต้องอยู่ระหว่าง 1 ถึง 100")
        payload = self._get_json(STEAM_TOP_GAMES_URL, {})
        response = payload.get("response")
        ranks = response.get("ranks") if isinstance(response, dict) else None
        if not isinstance(ranks, list):
            raise SteamApiError("Steam ส่งอันดับเกมที่ไม่คาดไว้")

        # A Steam chart can include non-game apps.  Read a few extra ranks so
        # the dashboard still has the requested number of actual games after filtering.
        candidate_limit = min(len(ranks), limit + 10)
        ranked_apps = [
            item
            for item in ranks[:candidate_limit]
            if isinstance(item, dict)
            and isinstance(item.get("appid"), int)
            and isinstance(item.get("rank"), int)
        ]
        if not ranked_apps:
            raise SteamApiError("Steam ไม่พบอันดับเกมในขณะนี้")

        app_ids = [item["appid"] for item in ranked_apps]
        details = self._fetch_many(app_ids, self._get_app_detail)
        player_counts = self._fetch_many(app_ids, self.get_current_players)
        games = []
        for item in ranked_apps:
            app_id = item["appid"]
            detail = details.get(app_id)
            player_count = player_counts.get(app_id)
            if not detail or player_count is None:
                continue
            games.append(
                {
                    # Steam App IDs are kept negative so they cannot collide
                    # with RAWG's positive game IDs in the same SQLite table.
                    "game_id": -app_id,
                    "name": detail["name"],
                    "rating": None,
                    "released": None,
                    "genres": detail["genres"],
                    "platforms": ["PC (Steam)"],
                    "metacritic": None,
                    "ratings_count": None,
                    "image": detail.get("image"),
                    "steam_app_id": app_id,
                    "steam_lookup_status": "found",
                    "current_players": player_count,
                    "live_rank": item["rank"],
                }
            )
        if not games:
            raise SteamApiError("Steam ไม่ส่งข้อมูลผู้เล่นสำหรับอันดับเกม")
        return games[:limit]

    def _get_app_detail(self, app_id: int) -> dict[str, Any] | None:
        payload = self._get_json(
            STEAM_APP_DETAILS_URL, {"appids": app_id, "l": "english", "cc": "us"}
        )
        entry = payload.get(str(app_id))
        if not isinstance(entry, dict) or not entry.get("success"):
            return None
        data = entry.get("data")
        if not isinstance(data, dict) or data.get("type") != "game":
            return None
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            return None
        image = data.get("header_image")
        genres = data.get("genres")
        return {
            "name": name.strip(),
            "image": image if isinstance(image, str) else None,
            "genres": [
                genre["description"].strip()
                for genre in genres
                if isinstance(genre, dict) and isinstance(genre.get("description"), str)
            ]
            if isinstance(genres, list)
            else [],
        }

    def _fetch_many(self, app_ids: list[int], fetcher: Any) -> dict[int, Any]:
        """Fetch independent Steam records concurrently so Home does not stall."""
        results: dict[int, Any] = {}
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(app_ids))) as executor:
            futures = {executor.submit(fetcher, app_id): app_id for app_id in app_ids}
            for future in as_completed(futures):
                app_id = futures[future]
                try:
                    results[app_id] = future.result()
                except SteamApiError:
                    continue
        return results

    def _get_json(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
        except requests.Timeout as error:
            raise SteamConnectionError("การเชื่อมต่อ Steam หมดเวลา") from error
        except requests.ConnectionError as error:
            raise SteamConnectionError("ไม่สามารถเชื่อมต่อ Steam ได้") from error
        except requests.HTTPError as error:
            raise SteamApiError("Steam ตอบกลับด้วยข้อผิดพลาด HTTP") from error
        except requests.RequestException as error:
            raise SteamApiError("เกิดข้อผิดพลาดขณะเรียก Steam") from error
        except ValueError as error:
            raise SteamApiError("Steam ส่งข้อมูลที่ไม่ใช่ JSON") from error
        if not isinstance(payload, dict):
            raise SteamApiError("Steam ส่งรูปแบบข้อมูลที่ไม่คาดไว้")
        return payload


def _normalized_name(value: Any) -> str:
    """Compare titles conservatively while ignoring punctuation and whitespace."""
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())
