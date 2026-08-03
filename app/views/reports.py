"""
Eco-Acoustic Health Monitor - Reports Screen (Section 3.12 Placeholder UI)
"""

import streamlit as st
from app.components.navigation import render_page_header
from app.components.buttons import primary_button, secondary_button

def render_reports_page():
    """Renders report generation and export options."""
    render_page_header(
        title="Forest Soundscape Reports",
        subtitle="Generate comprehensive PDF and Excel summary reports for conservation audits.",
        breadcrumb="Dashboard / Reports"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="eco-card">
                <div style="font-size: 2rem;">📅</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin-top: 0.5rem;">Daily Summary Report</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 1rem;">Audio events for 03 August 2026</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if primary_button("Export PDF 📄", key="rep_daily_pdf"):
            st.toast("✅ Daily PDF Report generated successfully!")

    with c2:
        st.markdown(
            """
            <div class="eco-card">
                <div style="font-size: 2rem;">📊</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin-top: 0.5rem;">Weekly Health Audit</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 1rem;">7-day biodiversity trend report</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if primary_button("Export Excel 📊", key="rep_weekly_excel"):
            st.toast("✅ Weekly Excel Report exported successfully!")

    with c3:
        st.markdown(
            """
            <div class="eco-card">
                <div style="font-size: 2rem;">🗓️</div>
                <div style="font-weight: 700; font-size: 1.1rem; margin-top: 0.5rem;">Monthly Comprehensive</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 1rem;">Full month threat & biodiversity log</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if secondary_button("Generate PDF 📄", key="rep_monthly_pdf"):
            st.toast("✅ Monthly PDF Report queued!")
