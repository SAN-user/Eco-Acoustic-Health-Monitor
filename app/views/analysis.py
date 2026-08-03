"""
Eco-Acoustic Health Monitor - Audio Analysis Screen (Section 3.8 Placeholder UI)
"""

import streamlit as st
from app.components.navigation import render_page_header
from app.components.buttons import primary_button, secondary_button
from app.config import PAGE_REPORTS, PAGE_UPLOAD
from app.state.router import navigate_to

def render_analysis_page():
    """Renders the AI Analysis results page."""
    render_page_header(
        title="AI Soundscape Analysis Results",
        subtitle="Detailed wildlife classification, threat detection, and ecosystem health predictions.",
        breadcrumb="Dashboard / Audio Analysis"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="eco-card" style="text-align: center;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Top Species Detected</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #1E4D2B; margin: 0.5rem 0;">Indian Peacock</div>
                <span class="eco-badge eco-badge-healthy">96% AI Confidence</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="eco-card" style="text-align: center;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Threat Status</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #DC2626; margin: 0.5rem 0;">Chainsaw Detected</div>
                <span class="eco-badge eco-badge-critical">High Priority Alert</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="eco-card" style="text-align: center;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Forest Health Score</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #2E7D32; margin: 0.5rem 0;">94%</div>
                <span class="eco-badge eco-badge-healthy">Healthy Ecosystem</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700;'>💡 AI Recommendations</h3>", unsafe_allow_html=True)
    st.info("Chainsaw activity detected in Sector 4. Recommend dispatching forest patrol to verify logging compliance.")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if primary_button("Generate & Save Report →", key="btn_save_analysis_report", use_container_width=True):
            navigate_to(PAGE_REPORTS)

    with col_btn2:
        if secondary_button("Analyze Another Audio", key="btn_analyze_another", use_container_width=True):
            navigate_to(PAGE_UPLOAD)
