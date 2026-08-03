"""
Eco-Acoustic Health Monitor - Forest Health Screen (Section 3.9 Placeholder UI)
"""

import streamlit as st
from app.components.navigation import render_page_header
from app.components.meters import render_health_meter
from app.components.charts import render_health_trend_chart
from app.utils.mock_data import get_weekly_health_trend
from app.state.session_state import get_state

def render_forest_health_page():
    """Renders ecosystem health overview."""
    dark_mode = get_state("dark_mode", False)
    render_page_header(
        title="Forest Ecosystem Health Overview",
        subtitle="Comprehensive bio-acoustic indicators, biodiversity indices, and environmental stability ratings.",
        breadcrumb="Dashboard / Forest Health"
    )

    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown("<div class='eco-card'>", unsafe_allow_html=True)
        render_health_meter(94, "Healthy Ecosystem")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        render_health_trend_chart(get_weekly_health_trend(), dark_mode=dark_mode)
