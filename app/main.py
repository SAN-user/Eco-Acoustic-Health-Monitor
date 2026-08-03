"""
Eco-Acoustic Health Monitor
Main Streamlit Application Entrypoint
"""

import sys
from pathlib import Path

# Fix python path for Streamlit execution
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Eco-Acoustic Health Monitor",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Imports & Dependencies
from app.config import (
    PAGE_SPLASH,
    PAGE_LOGIN,
    PAGE_FORGOT_PASSWORD,
    PAGE_DASHBOARD,
    PAGE_UPLOAD,
    PAGE_ANALYSIS,
    PAGE_FOREST_HEALTH,
    PAGE_ALERTS,
    PAGE_HISTORY,
    PAGE_REPORTS,
    PAGE_SETTINGS,
    PAGE_PROFILE,
)
from app.styles.style_loader import load_custom_css
from app.state.session_state import init_session_state, get_state, get_flash
from app.state.router import enforce_route_guard
from app.components.navigation import render_sidebar

# View imports
from app.views.splash import render_splash_page
from app.views.login import render_login_page
from app.views.forgot_password import render_forgot_password_page
from app.views.dashboard import render_dashboard_page
from app.views.upload_audio import render_upload_audio_page
from app.views.analysis import render_analysis_page
from app.views.forest_health import render_forest_health_page
from app.views.alerts import render_alerts_page
from app.views.history import render_history_page
from app.views.reports import render_reports_page
from app.views.settings import render_settings_page
from app.views.profile import render_profile_page

def main():
    # Initialize Session State
    init_session_state()

    # Route Guard & Active Page Resolution
    active_page = enforce_route_guard()

    # Load Glassmorphism Custom Theme
    dark_mode = get_state("dark_mode", False)
    load_custom_css(dark_mode=dark_mode)

    # Flash Messages
    flash = get_flash()
    if flash:
        cat = flash.get("category", "info")
        msg = flash.get("message", "")
        if cat == "error":
            st.error(msg)
        elif cat == "success":
            st.success(msg)
        else:
            st.info(msg)

    # Router Dispatching
    if active_page == PAGE_SPLASH:
        render_splash_page()

    elif active_page == PAGE_LOGIN:
        render_login_page()

    elif active_page == PAGE_FORGOT_PASSWORD:
        render_forgot_password_page()

    else:
        # Render Sidebar for Protected Application Routes
        render_sidebar()

        # Render Active Screen into Main Content Area
        if active_page == PAGE_DASHBOARD:
            render_dashboard_page()
        elif active_page == PAGE_UPLOAD:
            render_upload_audio_page()
        elif active_page == PAGE_ANALYSIS:
            render_analysis_page()
        elif active_page == PAGE_FOREST_HEALTH:
            render_forest_health_page()
        elif active_page == PAGE_ALERTS:
            render_alerts_page()
        elif active_page == PAGE_HISTORY:
            render_history_page()
        elif active_page == PAGE_REPORTS:
            render_reports_page()
        elif active_page == PAGE_SETTINGS:
            render_settings_page()
        elif active_page == PAGE_PROFILE:
            render_profile_page()

if __name__ == "__main__":
    main()