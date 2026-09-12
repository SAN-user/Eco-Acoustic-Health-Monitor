import textwrap
import streamlit as st
from app.config import SIDEBAR_NAV_ITEMS, APP_NAME, APP_TAGLINE, APP_VERSION
from app.state.session_state import get_state, set_state
from app.state.router import navigate_to, logout_user, get_current_page
from app.utils.formatters import format_current_date

def render_sidebar():
    """
    Renders the fixed sidebar with dark forest branding, nav items, system online status, and session controls.
    """
    with st.sidebar:
        # Branding Header
        st.markdown(
            textwrap.dedent(f"""
            <div style="padding: 0.75rem 0.5rem 1rem 0.5rem; text-align: center;">
                <div style="font-size: 2.2rem; margin-bottom: 0.35rem; line-height: 1;">🌲</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em; line-height: 1.2;">
                    ECO-ACOUSTIC<br><span style="color: #10B981; font-weight: 700;">Health Monitor</span>
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.4rem; font-weight: 500;">
                    Intelligent Forest Soundscape Analysis
                </div>
                <div style="margin-top: 0.75rem; display: flex; justify-content: center;">
                    <div class="system-status-online">
                        <span class="system-status-dot"></span>
                        AI System Online
                    </div>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

        st.divider()

        current_page = get_current_page()

        # Navigation Menu Header
        st.markdown('<div style="font-size: 0.725rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.6rem; padding-left: 0.2rem;">Navigation</div>', unsafe_allow_html=True)

        for item in SIDEBAR_NAV_ITEMS:
            key = item["key"]
            label = f"{item['icon']}  {item['label']}"
            is_active = (current_page == key)

            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
                if current_page != key:
                    navigate_to(key)

        st.divider()

        # Theme & Logout Controls
        dark_mode = get_state("dark_mode", True)
        theme_label = "☀️ Light Theme" if dark_mode else "🌙 Forest Dark Theme"
        if st.button(theme_label, key="sidebar_theme_toggle", use_container_width=True):
            set_state("dark_mode", not dark_mode)
            st.rerun()

        if st.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
            logout_user()

        st.markdown(
            textwrap.dedent(f"""
            <div style="text-align: center; font-size: 0.725rem; color: #64748B; margin-top: 1rem; font-weight: 500;">
                {APP_NAME} v{APP_VERSION}<br>© 2026 Eco-Acoustic Monitoring System
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

def render_topbar():
    """
    Renders top navigation bar with user greeting, date, and status indicators.
    """
    user_info = get_state("user_profile", {})
    unread_count = sum(1 for n in get_state("notifications", []) if not n.get("read", False))

    col1, col2 = st.columns([3, 1], vertical_alignment="center")

    with col1:
        st.markdown(
            textwrap.dedent(f"""
            <div style="padding: 0.25rem 0;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;">
                    Good Morning, {user_info.get('role', 'Officer')} 👋
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 0.15rem; font-weight: 500;">
                    📅 {format_current_date()} • {user_info.get('organization', 'Forest Conservation Dept')}
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            textwrap.dedent(f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 0.85rem;">
                <div style="position: relative; background: #14201C; border: 1px solid #243630; padding: 0.45rem 0.75rem; border-radius: 10px; font-size: 1.1rem; cursor: pointer;">
                    🔔
                    {"<span style='position: absolute; top: -5px; right: -5px; background: #EF4444; color: white; font-size: 0.65rem; padding: 2px 5px; border-radius: 999px; font-weight: 800;'>" + str(unread_count) + "</span>" if unread_count > 0 else ""}
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; background: #14201C; border: 1px solid #243630; padding: 0.35rem 0.75rem; border-radius: 999px; font-weight: 600; font-size: 0.85rem; color: #F8FAFC;">
                    <span>{user_info.get('avatar', '🌲')}</span>
                    <span>{user_info.get('name', 'User')}</span>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

def render_page_header(title: str, subtitle: str, breadcrumb: str = "Dashboard / Page"):
    """
    Standardized header present on subpages with clean typography and breadcrumbs.
    """
    st.markdown(
        textwrap.dedent(f"""
        <div style="margin-bottom: 1.5rem; padding-bottom: 0.85rem; border-bottom: 1px solid #243630;">
            <div style="font-size: 0.775rem; font-weight: 700; color: #10B981; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">
                📍 {breadcrumb}
            </div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.025em;">
                {title}
            </div>
            <div style="font-size: 0.9rem; color: #94A3B8; margin-top: 0.2rem; font-weight: 500;">
                {subtitle}
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )
