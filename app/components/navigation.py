"""
EcoSense AI - Navigation Components
Includes Sidebar Desktop Navigation, TopBar Header, and Page Title Headers.
"""

import streamlit as st
from app.config import SIDEBAR_NAV_ITEMS, APP_NAME, APP_TAGLINE, APP_VERSION
from app.state.session_state import get_state, set_state
from app.state.router import navigate_to, logout_user, get_current_page
from app.utils.formatters import format_current_date

def render_sidebar():
    """
    Renders the fixed sidebar with logo branding, nav items, and user session footer.
    """
    with st.sidebar:
        # Branding Header
        st.markdown(
            f"""
            <div style="padding: 0.5rem 0 1rem 0; text-align: center;">
                <div style="font-size: 2.2rem; margin-bottom: 0.25rem;">🌳</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #1E4D2B; letter-spacing: -0.02em;">{APP_NAME}</div>
                <div style="font-size: 0.725rem; color: #64748B; margin-top: 0.15rem;">{APP_TAGLINE}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        current_page = get_current_page()

        # Navigation Items
        st.markdown('<div style="font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Menu</div>', unsafe_allow_html=True)

        for item in SIDEBAR_NAV_ITEMS:
            key = item["key"]
            label = f"{item['icon']}  {item['label']}"
            is_active = (current_page == key)

            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
                if current_page != key:
                    navigate_to(key)

        st.divider()

        # Bottom Session & Theme Controls
        dark_mode = get_state("dark_mode", False)
        theme_label = "☀️ Light Mode" if dark_mode else "🌙 Dark Mode"
        if st.button(theme_label, key="sidebar_theme_toggle", use_container_width=True):
            set_state("dark_mode", not dark_mode)
            st.rerun()

        if st.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
            logout_user()

        st.markdown(
            f"""
            <div style="text-align: center; font-size: 0.725rem; color: #94A3B8; margin-top: 1rem;">
                {APP_NAME} v{APP_VERSION}<br>© 2026 Eco-Acoustic Tech
            </div>
            """,
            unsafe_allow_html=True
        )

def render_topbar():
    """
    Renders top navigation header with user greeting, current date, notification indicator, and user profile avatar.
    """
    user_info = get_state("user_profile", {})
    unread_count = sum(1 for n in get_state("notifications", []) if not n.get("read", False))

    col1, col2 = st.columns([3, 1], vertical_alignment="center")

    with col1:
        st.markdown(
            f"""
            <div>
                <div class="eco-greeting">Good Morning, {user_info.get('role', 'Officer')} 👋</div>
                <div class="eco-subtitle">📅 {format_current_date()} • {user_info.get('organization', 'Forest Department')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 1rem;">
                <div style="position: relative; background: #E8F5E9; padding: 0.5rem 0.75rem; border-radius: 12px; font-size: 1.1rem; cursor: pointer;">
                    🔔
                    {"<span style='position: absolute; top: -4px; right: -4px; background: #EF4444; color: white; font-size: 0.65rem; padding: 2px 6px; border-radius: 999px; font-weight: 800;'>" + str(unread_count) + "</span>" if unread_count > 0 else ""}
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; background: #F1F5F9; padding: 0.35rem 0.75rem; border-radius: 999px; font-weight: 700; font-size: 0.85rem;">
                    <span>{user_info.get('avatar', '🌲')}</span>
                    <span>{user_info.get('name', 'User')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_page_header(title: str, subtitle: str, breadcrumb: str = "Dashboard / Page"):
    """
    Standardized header present on every subpage according to UX Rule #9.
    """
    st.markdown(
        f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="font-size: 0.8rem; font-weight: 600; color: #2E7D32; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                📍 {breadcrumb}
            </div>
            <div style="font-size: 1.85rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">
                {title}
            </div>
            <div style="font-size: 0.95rem; color: #64748B; margin-top: 0.2rem;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
