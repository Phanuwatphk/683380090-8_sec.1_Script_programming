"""RAWG Video Games Database API client."""

from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

if __package__ and __package__.startswith("src."):
    from src.config import PROJECT_ROOT
else:
    from config import PROJECT_ROOT


RAWG_GAMES_URL = "https://api.rawg.io/api/games"
RAWG_MAX_PAGE_SIZE = 40


class RawgApiError(RuntimeError):
    """Base error for failures while retrieving game data from RAWG."""


class RawgConfigurationError(RawgApiError):
    """Raised when the application has no RAWG API key configured."""


class RawgApiClient:
    """Fetch a page of game records from RAWG without exposing HTTP to the UI."""

    def __init__(
        self,
        api_key: str | None = None,
        session: requests.Session | None = None,
        timeout: int = 15,
    ) -> None:
        # Resolve the project's configuration explicitly so the app works even
        # when Streamlit is launched from a different working directory.
        load_dotenv(PROJECT_ROOT / ".env")
        self.api_key = api_key if api_key is not None else os.getenv("RAWG_API_KEY", "")
        self.session = session or requests.Session()
        self.timeout = timeout

    def fetch_games(
        self, page_size: int = 20, ordering: str | None = None, page: int = 1
    ) -> list[dict[str, Any]]:
        """Return RAWG's default game listing or raise a user-friendly API error."""
        return self._fetch_games(
            page_size, search_term=None, require_results=True, ordering=ordering, page=page
        )

    def search_games(
        self, search_term: str, page_size: int = 20, page: int = 1
    ) -> list[dict[str, Any]]:
        """Search RAWG by title; an unmatched title is a valid empty result."""
        term = search_term.strip()
        if not term:
            return []
        return self._fetch_games(
            page_size, search_term=term, require_results=False, ordering=None, page=page
        )

    def fetch_game_details(self, game_id: int) -> dict[str, Any]:
        """Fetch detail-only metadata, including the developer studios."""
        payload = self._request_json(f"{RAWG_GAMES_URL}/{game_id}", {})
        if payload.get("id") != game_id:
            raise RawgApiError("RAWG API ส่งรูปแบบรายละเอียดเกมที่ไม่คาดไว้")
        return payload

    def _request_json(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        """Apply the same authentication, transport and JSON checks everywhere."""
        if not self.api_key.strip():
            raise RawgConfigurationError(
                "ไม่พบ RAWG API key: กรุณาตั้งค่า RAWG_API_KEY ในไฟล์ .env หรือ environment"
            )
        try:
            response = self.session.get(
                url,
                params={"key": self.api_key.strip(), **params},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.Timeout as error:
            raise RawgApiError("การเชื่อมต่อ RAWG API หมดเวลา กรุณาลองใหม่") from error
        except requests.ConnectionError as error:
            raise RawgApiError("ไม่สามารถเชื่อมต่อ RAWG API ได้ กรุณาตรวจสอบอินเทอร์เน็ต") from error
        except requests.HTTPError as error:
            status_code = error.response.status_code if error.response is not None else None
            if status_code in {401, 403}:
                message = "RAWG API key ไม่ถูกต้องหรือไม่มีสิทธิ์ใช้งาน"
            else:
                message = f"RAWG API ตอบกลับด้วย HTTP {status_code or 'error'}"
            raise RawgApiError(message) from error
        except requests.RequestException as error:
            raise RawgApiError("เกิดข้อผิดพลาดขณะเรียก RAWG API") from error
        try:
            payload = response.json()
        except ValueError as error:
            raise RawgApiError("RAWG API ส่งข้อมูลที่ไม่ใช่ JSON") from error
        if not isinstance(payload, dict):
            raise RawgApiError("RAWG API ส่งรูปแบบข้อมูลที่ไม่คาดไว้")
        return payload

    def _fetch_games(
        self,
        page_size: int,
        search_term: str | None,
        require_results: bool,
        ordering: str | None,
        page: int,
    ) -> list[dict[str, Any]]:
        if not 1 <= page_size <= 100:
            raise ValueError("จำนวนเกมที่ดึงต้องอยู่ระหว่าง 1 ถึง 100")
        if page < 1:
            raise ValueError("หน้าข้อมูลต้องเริ่มที่ 1")

        games: list[dict[str, Any]] = []
        # RAWG page offsets depend on ``page_size``. For a multi-request
        # result, keep every request at RAWG's maximum of 40 records so page
        # 2 always follows page 1 instead of overlapping it.
        for api_page in range(page, page + (page_size - 1) // RAWG_MAX_PAGE_SIZE + 1):
            requested_size = (
                page_size if page_size <= RAWG_MAX_PAGE_SIZE else RAWG_MAX_PAGE_SIZE
            )
            params = {"page_size": requested_size}
            if search_term:
                params["search"] = search_term
            if ordering:
                params["ordering"] = ordering
            if api_page > 1:
                params["page"] = api_page
            payload = self._request_json(RAWG_GAMES_URL, params)
            if not isinstance(payload.get("results"), list):
                raise RawgApiError("RAWG API ส่งรูปแบบข้อมูลที่ไม่คาดไว้")
            page_games = payload["results"]
            games.extend(page_games)
            if len(page_games) < requested_size:
                break

        if not games and require_results:
            raise RawgApiError("RAWG API ไม่พบข้อมูลเกมสำหรับคำขอนี้")
        return games[:page_size]
