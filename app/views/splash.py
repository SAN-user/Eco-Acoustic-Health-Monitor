"""
Eco-Acoustic Health Monitor - Splash Screen (Section 3.2)
"""

import streamlit as st
from app.config import APP_NAME, APP_SUBTITLE, APP_TAGLINE, APP_VERSION, PAGE_LOGIN, PAGE_DASHBOARD
from app.state.router import navigate_to, is_authenticated
from app.components.buttons import primary_button

def render_splash_page():
    """Renders the splash screen."""
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            f"""
            <div class="eco-splash-box">
                <div style="font-size: 4rem; margin-bottom: 0.5rem; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2));">🌳</div>
                <h1 style="font-size: 2.25rem; font-weight: 800; margin-bottom: 0.25rem; color: white;">{APP_NAME}</h1>
                <div style="font-size: 1.1rem; font-weight: 600; opacity: 0.95; margin-bottom: 0.5rem;">{APP_SUBTITLE}</div>
                <div style="font-size: 0.9rem; opacity: 0.8; font-style: italic; margin-bottom: 1.5rem;">"{APP_TAGLINE}"</div>
                
                <div style="width: 80%; background: rgba(255,255,255,0.2); height: 6px; border-radius: 999px; overflow: hidden; margin-bottom: 1.5rem;">
                    <div style="width: 100%; height: 100%; background: white; animation: splash-progress 2s ease-in-out infinite;"></div>
                </div>
                
                <div style="font-size: 0.8rem; opacity: 0.85; margin-top: 0.5rem;">Version {APP_VERSION} • Production Build</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        target_page = PAGE_DASHBOARD if is_authenticated() else PAGE_LOGIN
        target_label = "Enter Dashboard →" if is_authenticated() else "Proceed to Login →"

        if primary_button(target_label, key="splash_enter_btn", use_container_width=True):
            navigate_to(target_page)
