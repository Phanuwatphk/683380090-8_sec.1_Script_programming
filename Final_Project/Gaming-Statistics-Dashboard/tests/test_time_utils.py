from src.utils.time_utils import format_thailand_timestamp


def test_format_thailand_timestamp_converts_utc_to_ict():
    assert format_thailand_timestamp("2026-09-22T18:17:06.590359+00:00") == "2026-09-23 01:17:06 UTC+7"


def test_format_thailand_timestamp_preserves_thailand_timestamp():
    assert format_thailand_timestamp("2026-09-23T01:17:06+07:00") == "2026-09-23 01:17:06 UTC+7"


def test_format_thailand_timestamp_treats_legacy_naive_values_as_utc():
    assert format_thailand_timestamp("2026-09-22T18:17:06") == "2026-09-23 01:17:06 UTC+7"
