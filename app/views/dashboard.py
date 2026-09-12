"""
Eco-Acoustic Health Monitor - Forest Soundscape Intelligence Dashboard
Professional environmental UI displaying real SQLite metrics, recent acoustic analysis, and trends.
"""

import textwrap
import streamlit as st
from app.config import PAGE_UPLOAD, PAGE_ANALYSIS, PAGE_REPORTS, PAGE_ALERTS
from app.state.router import navigate_to
from app.state.session_state import get_state
from app.components.navigation import render_topbar, render_page_header
from app.components.cards import render_stat_card, render_quick_action_card
from app.components.timeline import render_activity_timeline
from app.components.charts import (
    render_health_trend_chart,
    render_species_frequency_chart,
    render_threat_trend_chart
)
from app.utils.mock_data import (
    get_recent_activity,
    get_weekly_health_trend,
    get_species_frequency,
    get_threat_trend
)
from app.services.database_service import get_dashboard_stats, get_recent_analyses

def render_dashboard_page():
    """Renders the professional dark-forest home dashboard UI."""
    dark_mode = get_state("dark_mode", True)

    # 1. Top Navigation Bar & Title Header
    render_topbar()

    st.markdown(
        textwrap.dedent("""
        <div style="margin-bottom: 1.5rem; padding-bottom: 0.85rem; border-bottom: 1px solid #243630;">
            <div style="font-size: 0.775rem; font-weight: 700; color: #10B981; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.2rem;">
                🌿 ECO-ACOUSTIC HEALTH MONITOR
            </div>
            <div style="font-size: 1.85rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.025em;">
                Forest Soundscape Intelligence Dashboard
            </div>
            <div style="font-size: 0.875rem; color: #94A3B8; margin-top: 0.2rem;">
                Real-time overview of persistent bioacoustic analyses, threat alerts, and ecological indices.
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    # Fetch Real SQLite Database Statistics
    db_stats = get_dashboard_stats()
    recent_analyses = get_recent_analyses(limit=1)

    # 2. Four Primary Statistics KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    # Format Health Score emphasizing "/100 Forest Health"
    if db_stats['latest_health_score'] is not None:
        health_value = f"{db_stats['latest_health_score']} / 100"
        health_sub = "Forest Health Index"
    else:
        health_value = "N/A"
        health_sub = "No Analysis Yet"

    wildlife_str = db_stats['latest_wildlife_species'] if db_stats['latest_wildlife_species'] else "N/A"

    with col1:
        render_stat_card(
            title="Total Analyses",
            value=str(db_stats['total_analyses']),
            subtext="⚡ Stored SQLite Records",
            icon="🎧"
        )

    with col2:
        render_stat_card(
            title="Threat Alerts",
            value=str(db_stats['total_alerts']),
            subtext=f"🚨 Active Alerts: {db_stats['unacknowledged_alerts']}",
            icon="⚠️"
        )

    with col3:
        render_stat_card(
            title="Latest Health Score",
            value=health_value,
            subtext=health_sub,
            icon="🌲"
        )

    with col4:
        render_stat_card(
            title="Latest Wildlife",
            value=wildlife_str,
            subtext="5-Class Classifier Result",
            icon="🐦"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Latest Acoustic Analysis Section
    st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;'>📊 Latest Acoustic Analysis</h3>", unsafe_allow_html=True)

    if recent_analyses:
        latest = recent_analyses[0]
        has_threat = bool(latest.get("threat_detected", 0))

        if has_threat:
            badge_html = '<span class="eco-badge eco-badge-threat">🔴 THREAT DETECTED</span>'
        else:
            badge_html = '<span class="eco-badge eco-badge-safe">🟢 SAFE</span>'

        wildlife_conf = f" ({latest['wildlife_confidence']:.1f}%)" if latest.get('wildlife_confidence') else ""
        ast_conf = f" ({latest['ast_confidence']:.1f}%)" if latest.get('ast_confidence') else ""

        st.markdown(
            textwrap.dedent(f"""
            <div class="eco-card" style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #1F2D28; padding-bottom: 0.75rem;">
                    <div>
                        <div style="font-weight: 800; font-size: 1.1rem; color: #F8FAFC;">📁 {latest.get('filename', 'Unknown File')}</div>
                        <div style="font-size: 0.775rem; color: #94A3B8; margin-top: 0.15rem;">Processed: {latest.get('timestamp', 'N/A')}</div>
                    </div>
                    <div>
                        {badge_html}
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; text-align: left;">
                    <div style="background: #0B1311; padding: 0.75rem; border-radius: 10px; border: 1px solid #1F2D28;">
                        <div style="font-size: 0.725rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Wildlife Prediction</div>
                        <div style="font-size: 1rem; font-weight: 700; color: #34D399; margin-top: 0.2rem;">🐦 {latest.get('wildlife_species', 'N/A')}{wildlife_conf}</div>
                    </div>
                    <div style="background: #0B1311; padding: 0.75rem; border-radius: 10px; border: 1px solid #1F2D28;">
                        <div style="font-size: 0.725rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">AST Sound Event</div>
                        <div style="font-size: 1rem; font-weight: 700; color: #60A5FA; margin-top: 0.2rem;">🔊 {latest.get('ast_top_label', 'N/A')}{ast_conf}</div>
                    </div>
                    <div style="background: #0B1311; padding: 0.75rem; border-radius: 10px; border: 1px solid #1F2D28;">
                        <div style="font-size: 0.725rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Threat Status</div>
                        <div style="font-size: 1rem; font-weight: 700; color: {'#F87171' if has_threat else '#34D399'}; margin-top: 0.2rem;">
                            {'⚠️ ' + str(latest.get('threat_label', 'Threat')) if has_threat else '🟢 No Threat Detected'}
                        </div>
                    </div>
                    <div style="background: #0B1311; padding: 0.75rem; border-radius: 10px; border: 1px solid #1F2D28;">
                        <div style="font-size: 0.725rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Health Score</div>
                        <div style="font-size: 1rem; font-weight: 800; color: #10B981; margin-top: 0.2rem;">🌲 {latest.get('health_score', 'N/A')} / 100</div>
                    </div>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            textwrap.dedent("""
            <div style="text-align: center; padding: 2.25rem 1rem; background: #14201C; border: 1px solid #243630; border-radius: 14px; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.4rem;">🎧</div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC;">No Analysis History Available Yet</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 0.25rem;">
                    Upload a forest recording from the <b>Upload Audio</b> page to perform your first acoustic soundscape analysis.
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Quick Action Controls
    st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;'>⚡ Quick Actions</h3>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if render_quick_action_card("Upload Audio", "Analyze new forest WAV/MP3 files", icon="📤", button_label="Upload Audio", key="qa_upload"):
            navigate_to(PAGE_UPLOAD)

    with q2:
        if render_quick_action_card("Start Analysis", "Run AI models on uploaded audio", icon="🔬", button_label="Start Analysis", key="qa_analyze"):
            navigate_to(PAGE_ANALYSIS)

    with q3:
        if render_quick_action_card("View Reports", "Export CSV summary reports", icon="📄", button_label="View Reports", key="qa_reports"):
            navigate_to(PAGE_REPORTS)

    with q4:
        if render_quick_action_card("View Alerts", "Review environmental threat alerts", icon="🔔", button_label="View Alerts", key="qa_alerts"):
            navigate_to(PAGE_ALERTS)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Illustrative Soundscape Analytics Section
    chart_col, activity_col = st.columns([2, 1])

    with chart_col:
        st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;'>📈 Illustrative Soundscape Analytics (Demo Data)</h3>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Forest Health Trend", "Species Frequency", "Threat Trends"])

        with tab1:
            render_health_trend_chart(get_weekly_health_trend(), dark_mode=dark_mode)

        with tab2:
            render_species_frequency_chart(get_species_frequency(), dark_mode=dark_mode)

        with tab3:
            render_threat_trend_chart(get_threat_trend(), dark_mode=dark_mode)

    with activity_col:
        st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;'>⏱ Activity Timeline (Demo Data)</h3>", unsafe_allow_html=True)
        render_activity_timeline(get_recent_activity())
