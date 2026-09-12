"""
Eco-Acoustic Health Monitor - User Profile Screen
"""

import textwrap
import streamlit as st
from app.components.navigation import render_page_header
from app.state.session_state import get_state

def render_profile_page():
    """Renders user profile information."""
    user = get_state("user_profile", {})
    render_page_header(
        title="Prototype Profile & Session",
        subtitle="Illustrative profile details shown for session-based prototype access.",
        breadcrumb="Dashboard / Profile"
    )

    st.info("**Prototype access** — This profile is illustrative session data, not an authenticated user account.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            textwrap.dedent(f"""
            <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; text-align: center; padding: 2rem 1.25rem;">
                <div style="font-size: 3.5rem;">{user.get('avatar', '🌲')}</div>
                <div style="font-weight: 800; font-size: 1.25rem; margin-top: 0.5rem; color: #F8FAFC;">{user.get('name', 'User')}</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 0.15rem;">{user.get('role', 'Officer')}</div>
                <div style="margin-top: 0.75rem;">
                    <span class="eco-badge eco-badge-safe">Prototype Session</span>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            textwrap.dedent(f"""
            <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.5rem;">
                <div style="font-weight: 700; font-size: 1.1rem; color: #F8FAFC; margin-bottom: 0.75rem;">Illustrative Profile Details</div>
                <div style="font-size: 0.875rem; color: #94A3B8; line-height: 1.8;">
                    • <b>Email Address:</b> <code>{user.get('email', 'officer@forest.gov.in')}</code><br>
                    • <b>Organization:</b> <span style="color: #F8FAFC;">{user.get('organization', 'Forest Department')}</span><br>
                    • <b>Role:</b> <span style="color: #F8FAFC;">{user.get('role', 'Field Wildlife Officer')}</span><br>
                    • <b>Last Active Session:</b> <span style="color: #F8FAFC;">{user.get('last_login', 'Active Session')}</span>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
