"""
Eco-Acoustic Health Monitor - Splash Screen
"""

import textwrap
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
            textwrap.dedent(f"""
            <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); border-radius: 20px; padding: 3.5rem 2rem; text-align: center; color: #FFFFFF; box-shadow: 0 15px 35px rgba(5, 150, 105, 0.25);">
                <div style="font-size: 3.8rem; margin-bottom: 0.5rem; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));">🌲</div>
                <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 0.25rem; color: #FFFFFF; letter-spacing: -0.02em;">{APP_NAME}</h1>
                <div style="font-size: 1.05rem; font-weight: 600; opacity: 0.95; margin-bottom: 0.4rem;">{APP_SUBTITLE}</div>
                <div style="font-size: 0.875rem; opacity: 0.85; font-style: italic; margin-bottom: 1.5rem;">"{APP_TAGLINE}"</div>
                
                <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                    <div style="background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); padding: 0.35rem 0.85rem; border-radius: 999px; font-size: 0.775rem; font-weight: 700;">
                        ● AI System Online
                    </div>
                </div>
                
                <div style="font-size: 0.775rem; opacity: 0.8;">Version {APP_VERSION} • Academic Prototype</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        target_page = PAGE_DASHBOARD if is_authenticated() else PAGE_LOGIN
        target_label = "Enter Dashboard →" if is_authenticated() else "Proceed to Prototype Access →"

        if primary_button(target_label, key="splash_enter_btn", use_container_width=True):
            navigate_to(target_page)
