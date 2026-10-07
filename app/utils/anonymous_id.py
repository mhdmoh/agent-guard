"""Anonymous browser identity for primary rate-limit buckets.

Streamlit can *read* request cookies via ``st.context.cookies`` but has no
supported API for app code to emit ``Set-Cookie`` with ``HttpOnly``. The
opaque UUID is therefore persisted with ``document.cookie`` (readable by JS,
``SameSite=Lax``, ``Secure`` in production). That is acceptable here: the
value is not an auth credential — IP abuse limits still apply if cookies are
cleared or forged. Client-supplied values are accepted only when they are
valid UUID strings.
"""

from __future__ import annotations

import re
import uuid
from typing import Any

ANON_COOKIE_NAME = "jev_anon_id"
_SESSION_KEY = "_jev_anon_id"
_COOKIE_WRITTEN_KEY = "_jev_anon_id_cookie_written"
_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def generate_anonymous_id() -> str:
    """Cryptographically secure anonymous browser id (UUID v4)."""
    return str(uuid.uuid4())


def is_valid_anonymous_id(value: str | None) -> bool:
    if not value or not isinstance(value, str):
        return False
    return bool(_UUID_RE.match(value.strip()))


def normalize_anonymous_id(value: str | None) -> str | None:
    if not is_valid_anonymous_id(value):
        return None
    assert value is not None
    return str(uuid.UUID(value.strip()))


def ensure_anonymous_id(
    *,
    cookie_name: str = ANON_COOKIE_NAME,
    cookie_max_age_seconds: int = 60 * 60 * 24 * 365,
    secure: bool = False,
    cookies: dict[str, str] | None = None,
    session_state: Any | None = None,
    persist_cookie: bool = True,
) -> str:
    """Return a stable anonymous id, minting + persisting a cookie when needed.

    Resolution order: session cache → request cookie → new UUID v4.
    """
    state = session_state
    if state is None:
        try:
            import streamlit as st

            state = st.session_state
        except Exception:  # noqa: BLE001
            state = None

    cookie_map = cookies if cookies is not None else _cookies_from_streamlit()
    from_cookie = normalize_anonymous_id(cookie_map.get(cookie_name))

    if state is not None:
        cached = normalize_anonymous_id(state.get(_SESSION_KEY))
        if cached:
            needs_write = persist_cookie and (
                from_cookie != cached or not state.get(_COOKIE_WRITTEN_KEY)
            )
            if needs_write:
                _persist_cookie(
                    cached,
                    cookie_name=cookie_name,
                    max_age_seconds=cookie_max_age_seconds,
                    secure=secure,
                )
                state[_COOKIE_WRITTEN_KEY] = True
            return cached

    if from_cookie:
        if state is not None:
            state[_SESSION_KEY] = from_cookie
            state[_COOKIE_WRITTEN_KEY] = True
        return from_cookie

    new_id = generate_anonymous_id()
    if state is not None:
        state[_SESSION_KEY] = new_id
    if persist_cookie:
        _persist_cookie(
            new_id,
            cookie_name=cookie_name,
            max_age_seconds=cookie_max_age_seconds,
            secure=secure,
        )
        if state is not None:
            state[_COOKIE_WRITTEN_KEY] = True
    return new_id


def _cookies_from_streamlit() -> dict[str, str]:
    try:
        import streamlit as st

        return {str(k): str(v) for k, v in st.context.cookies.items()}
    except Exception:  # noqa: BLE001
        return {}


def _persist_cookie(
    value: str,
    *,
    cookie_name: str,
    max_age_seconds: int,
    secure: bool,
) -> None:
    """Set the cookie in the browser via a tiny HTML component."""
    try:
        import streamlit.components.v1 as components
    except Exception:  # noqa: BLE001
        return

    safe_name = cookie_name.replace("\\", "\\\\").replace('"', '\\"')
    safe_value = value.replace("\\", "\\\\").replace('"', '\\"')
    secure_attr = "; Secure" if secure else ""
    script = f"""
<script>
(function () {{
  var name = "{safe_name}";
  var value = "{safe_value}";
  var maxAge = {int(max_age_seconds)};
  document.cookie = name + "=" + value
    + "; Path=/"
    + "; Max-Age=" + maxAge
    + "; SameSite=Lax{secure_attr}";
}})();
</script>
"""
    components.html(script, height=0)
