"""
Eco-Acoustic Health Monitor - Settings Screen
"""

import textwrap
import streamlit as st
from app.components.navigation import render_page_header
from app.state.session_state import get_state, set_state

def render_settings_page():
    """Renders application settings options."""
    render_page_header(
        title="Application Settings",
        subtitle="Manage appearance, notification preferences, and system configurations.",
        breadcrumb="Dashboard / Settings"
    )

    st.markdown(
        textwrap.dedent("""
        <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="font-weight: 700; font-size: 1.1rem; color: #F8FAFC; margin-bottom: 0.75rem;">🎨 Appearance Theme</div>
        """).strip(),
        unsafe_allow_html=True
    )
    dark_mode = st.toggle("Enable Dark Forest Theme", value=get_state("dark_mode", True))

    if dark_mode != get_state("dark_mode", True):
        set_state("dark_mode", dark_mode)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        textwrap.dedent("""
        <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="font-weight: 700; font-size: 1.1rem; color: #F8FAFC; margin-bottom: 0.25rem;">🔔 Notification Preferences</div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 1rem;">
                <i>Prototype UI controls — External SMS/Email dispatching is not connected in this version.</i>
            </div>
        """).strip(),
        unsafe_allow_html=True
    )
    st.checkbox("Alert on Chainsaw Detections (Prototype Control)", value=True)
    st.checkbox("Alert on Gunshot Detections (Prototype Control)", value=True)
    st.checkbox("Daily Forest Health Digest Email (Prototype Control)", value=False)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        textwrap.dedent("""
        <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.5rem;">
            <div style="font-weight: 700; font-size: 1.1rem; color: #F8FAFC; margin-bottom: 0.75rem;">🌐 System Information</div>
            <div style="font-size: 0.875rem; color: #94A3B8; line-height: 1.8;">
                • Engine Version: <b style="color: #F8FAFC;">v1.0.0</b><br>
                • AST AI Model: <b style="color: #F8FAFC;">Audio Spectrogram Transformer (MIT/ast-finetuned-audioset)</b><br>
                • Wildlife Model: <b style="color: #F8FAFC;">5-Class Random Forest (46 Librosa Features)</b><br>
                • Architecture: <b style="color: #F8FAFC;">Streamlit Direct Pipeline (PyTorch + Librosa)</b><br>
                • Database Persistence: <b style="color: #10B981;">SQLite3 (data/eco_acoustic.db)</b>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )
