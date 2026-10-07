"""Resolve the real client IP behind a trusted reverse proxy.

Production path: Browser → Nginx → Docker (127.0.0.1 publish) → Streamlit.

Nginx overwrites ``X-Real-IP`` with ``$remote_addr``. We only honour forwarded
headers when the immediate TCP peer is a configured trusted proxy; otherwise we
use the peer IP and ignore client-supplied ``X-Forwarded-For`` / ``X-Real-IP``.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from ipaddress import ip_address, ip_network

# Defaults cover loopback (local Nginx → published port) and Docker bridge peers.
DEFAULT_TRUSTED_PROXY_CIDRS = (
    "127.0.0.0/8",
    "::1/128",
    "172.16.0.0/12",
)


def parse_trusted_proxy_cidrs(value: str | Sequence[str] | None) -> tuple[str, ...]:
    if value is None:
        return DEFAULT_TRUSTED_PROXY_CIDRS
    if isinstance(value, str):
        parts = [p.strip() for p in value.split(",") if p.strip()]
        return tuple(parts) if parts else DEFAULT_TRUSTED_PROXY_CIDRS
    parts = [str(p).strip() for p in value if str(p).strip()]
    return tuple(parts) if parts else DEFAULT_TRUSTED_PROXY_CIDRS


def is_valid_ip(value: str) -> bool:
    try:
        ip_address(value.strip())
    except ValueError:
        return False
    return True


def is_trusted_proxy(peer_ip: str, trusted_cidrs: Sequence[str]) -> bool:
    try:
        peer = ip_address(peer_ip.strip())
    except ValueError:
        return False
    for cidr in trusted_cidrs:
        try:
            if peer in ip_network(cidr, strict=False):
                return True
        except ValueError:
            continue
    return False


def resolve_client_ip(
    *,
    peer_ip: str | None,
    headers: Mapping[str, str] | None = None,
    trusted_proxy_cidrs: Sequence[str] | None = None,
) -> str:
    """Return the client IP to use as a rate-limit bucket key.

    When the TCP peer is a trusted proxy, prefer ``X-Real-IP`` (set by our Nginx
    from ``$remote_addr``). Do not trust the left-hand client-controlled entries
    of ``X-Forwarded-For``; if ``X-Real-IP`` is absent, use only the *rightmost*
    ``X-Forwarded-For`` hop (the address our proxy appended/set).

    When the peer is not trusted, ignore forwarded headers entirely.
    """
    trusted = parse_trusted_proxy_cidrs(trusted_proxy_cidrs)
    peer = (peer_ip or "").strip() or None
    hdrs = _normalize_headers(headers)

    if peer is None or is_trusted_proxy(peer, trusted):
        real_ip = hdrs.get("x-real-ip")
        if real_ip and is_valid_ip(real_ip):
            return real_ip.strip()

        forwarded = hdrs.get("x-forwarded-for")
        if forwarded:
            # Rightmost hop is what the immediate trusted proxy observed/set.
            hops = [h.strip() for h in forwarded.split(",") if h.strip()]
            if hops and is_valid_ip(hops[-1]):
                return hops[-1]

    if peer and is_valid_ip(peer):
        return peer
    return "unknown"


def peer_ip_from_streamlit() -> str | None:
    """TCP peer IP as seen by Streamlit (Docker bridge or loopback)."""
    try:
        import streamlit as st

        # Public API maps loopback to None; treat that as local peer.
        ip = st.context.ip_address
        if ip is None:
            return "127.0.0.1"
        return str(ip)
    except Exception:  # noqa: BLE001 — safe outside a Streamlit script run
        return None


def headers_from_streamlit() -> dict[str, str]:
    try:
        import streamlit as st

        return {str(k): str(v) for k, v in st.context.headers.items()}
    except Exception:  # noqa: BLE001
        return {}


def visitor_client_ip(trusted_proxy_cidrs: Sequence[str] | str | None = None) -> str:
    """Resolve the current Streamlit visitor's client IP for rate limiting."""
    return resolve_client_ip(
        peer_ip=peer_ip_from_streamlit(),
        headers=headers_from_streamlit(),
        trusted_proxy_cidrs=parse_trusted_proxy_cidrs(trusted_proxy_cidrs),
    )


def _normalize_headers(headers: Mapping[str, str] | None) -> dict[str, str]:
    if not headers:
        return {}
    return {str(k).lower(): str(v).strip() for k, v in headers.items() if v is not None}
