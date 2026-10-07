from app.ui.styles.landing import LANDING_CSS
from app.ui.styles.theme import APP_CSS

__all__ = ["APP_CSS", "LANDING_CSS", "inject_styles"]


def inject_styles() -> None:
    """Playground / console styles."""
    import streamlit as st

    st.markdown(APP_CSS, unsafe_allow_html=True)
