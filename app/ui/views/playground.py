"""Interactive AgentGuard playground — lazy-inits gateway on first visit."""

from __future__ import annotations

from functools import lru_cache

import streamlit as st

from app.config.settings import Settings, get_settings
from app.guard.gateway import AgentGuard
from app.guard.models import AgentRun
from app.ui.components.render import (
    render_composer,
    render_playground_header,
    render_run,
)
from app.ui.styles import inject_styles
from app.utils.client_ip import visitor_client_ip
from app.utils.logging import setup_logging


@lru_cache
def _settings() -> Settings:
    return get_settings()


@st.cache_resource(show_spinner=False)
def get_guard() -> AgentGuard:
    settings = _settings()
    setup_logging(settings.log_level)
    return AgentGuard(settings)


def render_playground() -> None:
    """Interactive console. Initializes Jev/AgentGuard only when this page runs."""
    inject_styles()

    try:
        settings = _settings()
        setup_logging(settings.log_level)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Configuration error: {exc}")
        st.stop()

    guard = get_guard()
    home = st.session_state.get("page_home")
    render_playground_header(
        demo_mode=guard.demo_mode,
        jev_model=settings.jev_model,
        home_page=home,
    )

    if "current_run" not in st.session_state:
        st.session_state.current_run = None
    if "pending_human" not in st.session_state:
        st.session_state.pending_human = None
    if "sync_request" in st.session_state:
        st.session_state.request_draft = st.session_state.sync_request
        del st.session_state.sync_request

    with st.sidebar:
        st.markdown("**Playground**")
        st.caption("Interactive AgentGuard console")
        st.divider()
        st.caption("POLICY")
        st.markdown(
            f"Auto-execute when risk ≤ `{settings.auto_execute_max_risk}` "
            f"and safe ≥ `{settings.auto_execute_min_safe}`"
        )
        st.markdown(f"Block when risk ≥ `{settings.block_min_risk}`")
        st.caption(f"policy v{settings.policy_version}")
        st.divider()
        st.caption("NOTE")
        st.write(
            "Jev produces typed signals. AgentGuard applies deterministic policy. "
            "Tools are sandboxed demos."
        )
        if home is not None:
            st.page_link(home, label="← Back to overview", width="stretch")
        if st.button("Clear run", use_container_width=True):
            st.session_state.current_run = None
            st.session_state.pending_human = None
            st.rerun()

    request, should_run = render_composer()
    if should_run and request:
        st.session_state.sync_request = request
        client_ip = visitor_client_ip(settings.trusted_proxy_cidrs)
        with st.spinner("Agent → Jev → Policy…"):
            st.session_state.current_run = guard.run(request, client_ip=client_ip)
        st.session_state.pending_human = None
        st.rerun()

    current: AgentRun | None = st.session_state.current_run
    pending = st.session_state.pending_human
    if current is not None and pending in {"approve", "reject"}:
        st.session_state.current_run = guard.resolve_confirmation(
            current,
            approved=pending == "approve",
        )
        st.session_state.pending_human = None
        st.rerun()

    if st.session_state.current_run is not None:
        render_run(st.session_state.current_run)
