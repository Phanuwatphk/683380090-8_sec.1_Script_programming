from datetime import timedelta

import pytest

from src import config


@pytest.mark.parametrize("value, expected", [("abc", 24), ("", 24), ("0", 0), ("-1", 0), ("48", 48)])
def test_catalog_setting_does_not_change_steam_interval(monkeypatch, value, expected):
    monkeypatch.setenv("CATALOG_REFRESH_HOURS", value)
    monkeypatch.setenv("PLAYER_REFRESH_MINUTES", "15")
    assert config.catalog_refresh_interval() == timedelta(hours=expected)
    assert config.live_refresh_interval() == timedelta(minutes=15)


def test_application_loads_env_before_resolving_relative_database_from_other_cwd(tmp_path, monkeypatch):
    from src.api import rawg_api
    from src.app import build_game_service

    (tmp_path / ".env").write_text("RAWG_API_KEY=test-key\nGAMING_DASHBOARD_DB=data/env.db\n")
    other_directory = tmp_path / "elsewhere"
    other_directory.mkdir()
    monkeypatch.chdir(other_directory)
    monkeypatch.setattr(config, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(rawg_api, "PROJECT_ROOT", tmp_path)
    # Record the environment override so dotenv changes are restored after this test.
    monkeypatch.setenv("GAMING_DASHBOARD_DB", "placeholder")
    monkeypatch.delenv("GAMING_DASHBOARD_DB")
    monkeypatch.setenv("RAWG_API_KEY", "test-key")
    service = build_game_service()
    assert service.database.database_path == tmp_path / "data/env.db"
    assert service.database.database_path.exists()
    assert not (other_directory / "data").exists()
