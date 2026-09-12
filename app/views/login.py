"""
Eco-Acoustic Health Monitor - Login Screen
"""

import textwrap
import re
import streamlit as st
from app.config import APP_NAME, APP_VERSION, PAGE_FORGOT_PASSWORD
from app.state.router import login_user, navigate_to
from app.components.buttons import primary_button

def validate_email(email: str) -> bool:
    """Basic regex format validation for email address."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def render_login_page():
    """Renders the login screen UI."""
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])

    with col2:
        st.markdown(
            textwrap.dedent(f"""
            <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 2.25rem 1.5rem; text-align: center; margin-bottom: 1.25rem;">
                <div style="font-size: 2.8rem; margin-bottom: 0.4rem;">🌲</div>
                <h2 style="font-size: 1.6rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.25rem;">Welcome to {APP_NAME}</h2>
                <div style="font-size: 0.85rem; color: #94A3B8;">
                    Demo application access for the forest soundscape monitoring prototype
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

        st.info("**Prototype access** — Email format and a non-empty password are checked only to start a session. No account credentials are verified, persisted, or sent to a backend.")

        email = st.text_input("Email Address (prototype)", value="officer@forest.gov.in", placeholder="officer@forest.gov.in", key="login_email_input")

        col_pwd, col_chk = st.columns([3, 1], vertical_alignment="bottom")
        with col_pwd:
            show_pwd = st.session_state.get("login_show_pwd", False)
            password = st.text_input(
                "Password (prototype)",
                value="forest2026",
                placeholder="••••••••",
                type="default" if show_pwd else "password",
                key="login_pwd_input"
            )
        with col_chk:
            if st.button("👁 Show" if not show_pwd else "🙈 Hide", key="toggle_login_pwd"):
                st.session_state["login_show_pwd"] = not show_pwd
                st.rerun()

        remember_me = st.checkbox("Remember this prototype session on this device", value=True, key="login_remember_chk")

        st.markdown("<br>", unsafe_allow_html=True)

        if primary_button("Continue to Dashboard →", key="login_submit_btn", use_container_width=True):
            if not email.strip():
                st.error("⚠️ Please enter your email address.")
            elif not validate_email(email):
                st.error("⚠️ Please enter a valid email address (e.g. officer@forest.gov.in).")
            elif not password.strip():
                st.error("⚠️ Password cannot be empty.")
            else:
                st.success("✅ Prototype session access enabled. Navigating to Dashboard...")
                login_user(email.strip(), remember_me)

        col_left, col_right = st.columns(2)
        with col_left:
            if st.button("Forgot Password?", key="forgot_pwd_nav_btn", use_container_width=True, type="secondary"):
                navigate_to(PAGE_FORGOT_PASSWORD)

        st.markdown(
            textwrap.dedent(f"""
            <div style="text-align: center; font-size: 0.775rem; color: #64748B; margin-top: 2rem;">
                Demo application access • {APP_NAME} v{APP_VERSION}
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
