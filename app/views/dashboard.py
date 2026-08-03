"""
Eco-Acoustic Health Monitor - Main Home Dashboard (Section 3.5)
Overview of forest health metrics, quick actions, interactive Plotly charts, and recent activity timeline.
"""

import streamlit as st
from app.config import PAGE_UPLOAD, PAGE_ANALYSIS, PAGE_REPORTS, PAGE_ALERTS
from app.state.router import navigate_to
from app.state.session_state import get_state
from app.components.navigation import render_topbar
from app.components.cards import render_stat_card, render_quick_action_card
from app.components.timeline import render_activity_timeline
from app.components.charts import (
    render_health_trend_chart,
    render_species_frequency_chart,
    render_threat_trend_chart
)
from app.utils.mock_data import (
    get_dashboard_stats,
    get_recent_activity,
    get_weekly_health_trend,
    get_species_frequency,
    get_threat_trend
)

def render_dashboard_page():
    """Renders the complete home dashboard UI."""
    dark_mode = get_state("dark_mode", False)

    # 1. Top Navigation Bar & Greeting
    render_topbar()
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Four Primary Statistics Cards (PRD Section 3.5)
    stats = get_dashboard_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            title="Forest Health Score",
            value=f"{stats['health_score']}%",
            subtext=f"🟢 Status: {stats['health_status']}",
            icon="🌳"
        )

    with col2:
        render_stat_card(
            title="Species Detected",
            value=str(stats['species_detected']),
            subtext=f"📈 {stats['species_change']}",
            icon="🦜"
        )

    with col3:
        render_stat_card(
            title="Threats Today",
            value=str(stats['threats_today']),
            subtext=f"🚨 {stats['threats_status']}",
            icon="⚠"
        )

    with col4:
        render_stat_card(
            title="Total Analyses",
            value=str(stats['total_analyses']),
            subtext=f"⚡ {stats['analyses_change']}",
            icon="📊"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Quick Action Cards (PRD Section 3.5)
    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 700; color: #1E4D2B;'>⚡ Quick Actions</h3>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if render_quick_action_card("Upload Audio", "Analyze new forest WAV/MP3 files", icon="📤", button_label="Upload Now", key="qa_upload"):
            navigate_to(PAGE_UPLOAD)

    with q2:
        if render_quick_action_card("Start Analysis", "Run AST model on uploaded audio", icon="🔬", button_label="Analyze", key="qa_analyze"):
            navigate_to(PAGE_ANALYSIS)

    with q3:
        if render_quick_action_card("View Reports", "Export PDF & Excel summary reports", icon="📄", button_label="View Reports", key="qa_reports"):
            navigate_to(PAGE_REPORTS)

    with q4:
        if render_quick_action_card("View Alerts", "Inspect 2 active environmental threats", icon="🔔", button_label="View Alerts", key="qa_alerts"):
            navigate_to(PAGE_ALERTS)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Interactive Plotly Charts & Activity Timeline
    chart_col, activity_col = st.columns([2, 1])

    with chart_col:
        st.markdown("<h3 style='font-size: 1.25rem; font-weight: 700; color: #1E4D2B;'>📈 Soundscape Analytics</h3>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Forest Health Trend", "Species Frequency", "Threat Trends"])

        with tab1:
            render_health_trend_chart(get_weekly_health_trend(), dark_mode=dark_mode)

        with tab2:
            render_species_frequency_chart(get_species_frequency(), dark_mode=dark_mode)

        with tab3:
            render_threat_trend_chart(get_threat_trend(), dark_mode=dark_mode)

    with activity_col:
        st.markdown("<h3 style='font-size: 1.25rem; font-weight: 700; color: #1E4D2B;'>⏱ Recent Activity</h3>", unsafe_allow_html=True)
        render_activity_timeline(get_recent_activity())
