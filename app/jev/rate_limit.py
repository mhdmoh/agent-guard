"""Configurable rate limiting for outbound Jev API calls (pyrate-limiter)."""

from __future__ import annotations

from pyrate_limiter import (
    AbstractBucket,
    BucketFactory,
    Duration,
    InMemoryBucket,
    Limiter,
    Rate,
    RateItem,
    WallClock,
)

from app.config.settings import Settings
from app.utils.logging import get_logger

logger = get_logger(__name__)


class RateLimitExceeded(Exception):
    """Raised when the configured Jev API call budget is exhausted."""

    def __init__(self, message: str, *, max_calls: int, window_hours: float) -> None:
        super().__init__(message)
        self.max_calls = max_calls
        self.window_hours = window_hours


class _PerKeyBucketFactory(BucketFactory):
    """One in-memory bucket per acquire() name (client IP).

    ``Limiter(Rate(...))`` uses SingleBucketFactory, which ignores the name and
    shares one global bucket — unsuitable for per-visitor limits.
    """

    def __init__(self, rates: list[Rate]) -> None:
        self._rates = rates
        self._clock = WallClock()
        self._buckets: dict[str, AbstractBucket] = {}

    def wrap_item(self, name: str, weight: int = 1) -> RateItem:
        return RateItem(name=name, timestamp=self._clock.now(), weight=weight)

    def get(self, item: RateItem) -> AbstractBucket:
        bucket = self._buckets.get(item.name)
        if bucket is None:
            bucket = self.create(InMemoryBucket, list(self._rates))
            self._buckets[item.name] = bucket
        return bucket


class JevRateLimiter:
    """Limits live Jev decide calls per visitor client IP."""

    def __init__(self, settings: Settings) -> None:
        self._enabled = settings.rate_limit_enabled
        self._max_calls = settings.rate_limit_max_calls
        self._window_hours = settings.rate_limit_window_hours
        window_ms = max(1, int(self._window_hours * Duration.HOUR))
        rates = [Rate(self._max_calls, window_ms)]
        self._limiter = Limiter(_PerKeyBucketFactory(rates))

    def acquire(self, client_ip: str | None = None) -> None:
        """Consume one permit for ``client_ip`` or raise RateLimitExceeded."""
        if not self._enabled:
            return
        bucket_key = _ip_bucket_key(client_ip)
        acquired = self._limiter.try_acquire(bucket_key, blocking=False)
        if not acquired:
            logger.warning(
                "jev_rate_limited key=%s max=%s window_h=%s",
                bucket_key,
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


def _ip_bucket_key(client_ip: str | None) -> str:
    ip = (client_ip or "").strip() or "unknown"
    return f"jev:ip:{ip}"
