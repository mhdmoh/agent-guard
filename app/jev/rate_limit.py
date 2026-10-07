"""Configurable rate limiting for outbound Jev API calls (pyrate-limiter)."""

from __future__ import annotations

from hashlib import sha256

from pyrate_limiter import Duration, Limiter, Rate

from app.config.settings import Settings
from app.utils.logging import get_logger

logger = get_logger(__name__)


class RateLimitExceeded(Exception):
    """Raised when the configured Jev API call budget is exhausted."""

    def __init__(self, message: str, *, max_calls: int, window_hours: float) -> None:
        super().__init__(message)
        self.max_calls = max_calls
        self.window_hours = window_hours


class JevRateLimiter:
    """Limits live Jev decide calls for a given API identity."""

    def __init__(self, settings: Settings) -> None:
        self._enabled = settings.rate_limit_enabled
        self._max_calls = settings.rate_limit_max_calls
        self._window_hours = settings.rate_limit_window_hours
        self._bucket_key = _api_bucket_key(settings)
        window_ms = max(1, int(self._window_hours * Duration.HOUR))
        self._limiter = Limiter(Rate(self._max_calls, window_ms))

    def acquire(self) -> None:
        """Consume one permit or raise RateLimitExceeded (non-blocking)."""
        if not self._enabled:
            return
        acquired = self._limiter.try_acquire(self._bucket_key, blocking=False)
        if not acquired:
            logger.warning(
                "jev_rate_limited key=%s max=%s window_h=%s",
                self._bucket_key,
                self._max_calls,
                self._window_hours,
            )
            raise RateLimitExceeded(
                f"Jev API rate limit exceeded: "
                f"{self._max_calls} call(s) per {self._window_hours:g} hour(s). "
                "Try again later.",
                max_calls=self._max_calls,
                window_hours=self._window_hours,
            )


def _api_bucket_key(settings: Settings) -> str:
    """Stable key for 'the same API' — base URL + API key fingerprint."""
    key = settings.jev_api_key.strip() or "anonymous"
    digest = sha256(key.encode("utf-8")).hexdigest()[:12]
    return f"jev:{settings.jev_base_url}:{digest}"
