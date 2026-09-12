"""
Eco-Acoustic Health Monitor - Forest Health Screen
"""

import textwrap
import streamlit as st
from app.components.navigation import render_page_header
from app.components.meters import render_health_meter
from app.components.charts import render_health_trend_chart
from app.utils.mock_data import get_weekly_health_trend
from app.state.session_state import get_state

def render_forest_health_page():
    """Renders ecosystem health overview."""
    dark_mode = get_state("dark_mode", True)
    render_page_header(
        title="Forest Ecosystem Health Overview",
        subtitle="Illustrative bio-acoustic indicators, biodiversity indices, and environmental stability ratings.",
        breadcrumb="Dashboard / Forest Health"
    )
    st.info(
        "**Demo / Illustrative Data** — The ecosystem score and health trend below are illustrative "
        "and are not derived from an uploaded recording."
    )

    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown(
            textwrap.dedent("""
            <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem;">
            """).strip(),
            unsafe_allow_html=True
        )
        render_health_meter(94, "Healthy Ecosystem")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        render_health_trend_chart(get_weekly_health_trend(), dark_mode=dark_mode)
