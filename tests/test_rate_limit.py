"""Tests for outbound Jev API rate limiting."""

from __future__ import annotations

from unittest.mock import MagicMock

import httpx
import pytest
from app.config.settings import Settings
from app.jev.client import JevClient, JevClientError
from app.jev.rate_limit import JevRateLimiter, RateLimitExceeded


def _settings(**overrides: object) -> Settings:
    base = {
        "_env_file": None,
        "JEV_API_KEY": "test-key",
        "RATE_LIMIT_ENABLED": True,
        "RATE_LIMIT_MAX_CALLS": 3,
        "RATE_LIMIT_WINDOW_HOURS": 5.0,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def test_rate_limiter_allows_up_to_max_then_blocks() -> None:
    limiter = JevRateLimiter(
        _settings(RATE_LIMIT_MAX_CALLS=3, RATE_LIMIT_WINDOW_HOURS=5)
    )
    limiter.acquire()
    limiter.acquire()
    limiter.acquire()
    with pytest.raises(RateLimitExceeded) as exc:
        limiter.acquire()
    assert exc.value.max_calls == 3
    assert exc.value.window_hours == 5.0


def test_rate_limiter_disabled_never_blocks() -> None:
    limiter = JevRateLimiter(_settings(RATE_LIMIT_ENABLED=False, RATE_LIMIT_MAX_CALLS=1))
    for _ in range(5):
        limiter.acquire()


def test_different_api_keys_have_separate_buckets() -> None:
    a = JevRateLimiter(_settings(JEV_API_KEY="key-a", RATE_LIMIT_MAX_CALLS=1))
    b = JevRateLimiter(_settings(JEV_API_KEY="key-b", RATE_LIMIT_MAX_CALLS=1))
    a.acquire()
    with pytest.raises(RateLimitExceeded):
        a.acquire()
    b.acquire()  # other API identity still allowed


def test_jev_client_decide_respects_rate_limit() -> None:
    settings = _settings(RATE_LIMIT_MAX_CALLS=2, RATE_LIMIT_WINDOW_HOURS=5)
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"answers": {}})
    )
    http = httpx.Client(transport=transport)
    client = JevClient(settings, client=http)

    client.decide({"model": "x"})
    client.decide({"model": "x"})
    with pytest.raises(JevClientError) as exc:
        client.decide({"model": "x"})
    assert exc.value.status_code == 429
    assert "rate limit" in str(exc.value).lower()


def test_jev_client_skips_http_when_rate_limited() -> None:
    settings = _settings(RATE_LIMIT_MAX_CALLS=1)
    mock_http = MagicMock(spec=httpx.Client)
    mock_http.post.return_value = httpx.Response(200, json={"ok": True})
    client = JevClient(settings, client=mock_http)

    client.decide({"model": "x"})
    with pytest.raises(JevClientError):
        client.decide({"model": "x"})
    assert mock_http.post.call_count == 1
