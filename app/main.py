"""Streamlit entrypoint — landing + playground navigation."""

from __future__ import annotations

import streamlit as st

from app.ui.views.landing import render_landing
from app.ui.views.playground import render_playground


def main() -> None:
    st.set_page_config(
        page_title="AgentGuard — AI Agent Safety Gateway",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            "About": (
                "AgentGuard — an engineering experiment exploring typed AI decisions, "
                "deterministic policy, and safe tool execution for AI agents."
            ),
        },
    )

    home = st.Page(
        render_landing,
        title="Home",
        default=True,
    )
    playground = st.Page(
        render_playground,
        title="Playground",
        url_path="playground",
    )

    # Share Page objects so views can render st.page_link without re-creating pages.
    st.session_state["page_home"] = home
    st.session_state["page_playground"] = playground

    st.navigation([home, playground], position="hidden").run()


if __name__ == "__main__":
    main()
