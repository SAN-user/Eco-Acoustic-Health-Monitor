"""
Eco-Acoustic Health Monitor - User Profile Screen (Section 3.15 Placeholder UI)
"""

import streamlit as st
from app.components.navigation import render_page_header
from app.state.session_state import get_state

def render_profile_page():
    """Renders user profile information."""
    user = get_state("user_profile", {})
    render_page_header(
        title="Officer Profile & Identity",
        subtitle="Manage personal credentials, organization details, and access authorization.",
        breadcrumb="Dashboard / Profile"
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            f"""
            <div class="eco-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 4rem;">{user.get('avatar', '🌲')}</div>
                <div style="font-weight: 800; font-size: 1.35rem; margin-top: 0.5rem; color: #1E4D2B;">{user.get('name')}</div>
                <div style="font-size: 0.9rem; color: #64748B;">{user.get('role')}</div>
                <span class="eco-badge eco-badge-healthy" style="margin-top: 0.75rem;">Active Session</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("<div class='eco-card'>", unsafe_allow_html=True)
        st.subheader("Officer Details")
        st.write(f"• **Email Address**: `{user.get('email')}`")
        st.write(f"• **Organization**: {user.get('organization')}")
        st.write(f"• **Role Privileges**: {user.get('role')}")
        st.write(f"• **Last Active Login**: {user.get('last_login')}")
        st.markdown("</div>", unsafe_allow_html=True)
