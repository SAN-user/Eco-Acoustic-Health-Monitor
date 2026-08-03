"""
Eco-Acoustic Health Monitor - Settings Screen (Section 3.14 Placeholder UI)
"""

import streamlit as st
from app.components.navigation import render_page_header
from app.state.session_state import get_state, set_state

def render_settings_page():
    """Renders application settings options."""
    render_page_header(
        title="Application Settings",
        subtitle="Manage appearance, notifications, language preferences, and system configurations.",
        breadcrumb="Dashboard / Settings"
    )

    st.markdown("<div class='eco-card'>", unsafe_allow_html=True)
    st.subheader("🎨 Appearance")
    dark_mode = st.toggle("Enable Dark Mode", value=get_state("dark_mode", False))

    if dark_mode != get_state("dark_mode", False):
        set_state("dark_mode", dark_mode)
        st.rerun()

    st.divider()

    st.subheader("🔔 Notification Preferences")
    st.checkbox("Alert on Chainsaw Detections", value=True)
    st.checkbox("Alert on Gunshot Detections", value=True)
    st.checkbox("Daily Forest Health Digest Email", value=False)

    st.divider()

    st.subheader("🌐 System Info")
    st.write("• Engine Version: **v1.0.0**")
    st.write("• Model Pipeline: **Audio Spectrogram Transformer (AST)**")
    st.write("• Backend Framework: **FastAPI + PyTorch**")
    st.markdown("</div>", unsafe_allow_html=True)
