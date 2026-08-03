"""
Eco-Acoustic Health Monitor - Login Screen (Section 3.3)
"""

import streamlit as st
import re
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
            f"""
            <div class="eco-card" style="padding: 2.5rem; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🌳</div>
                <h2 style="font-size: 1.75rem; font-weight: 800; color: #1E4D2B; margin-bottom: 0.25rem;">Welcome to {APP_NAME}</h2>
                <div style="font-size: 0.9rem; color: #64748B; margin-bottom: 1.75rem;">
                    Sign in to access your forest soundscape monitoring portal
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        email = st.text_input("Email Address", value="officer@forest.gov.in", placeholder="officer@forest.gov.in", key="login_email_input")

        col_pwd, col_chk = st.columns([3, 1], vertical_alignment="bottom")
        with col_pwd:
            show_pwd = st.session_state.get("login_show_pwd", False)
            password = st.text_input(
                "Password",
                value="forest2026",
                placeholder="••••••••",
                type="default" if show_pwd else "password",
                key="login_pwd_input"
            )
        with col_chk:
            if st.button("👁 Show" if not show_pwd else "🙈 Hide", key="toggle_login_pwd"):
                st.session_state["login_show_pwd"] = not show_pwd
                st.rerun()

        remember_me = st.checkbox("Remember Me on this device", value=True, key="login_remember_chk")

        st.markdown("<br>", unsafe_allow_html=True)

        if primary_button("Sign In →", key="login_submit_btn", use_container_width=True):
            if not email.strip():
                st.error("⚠️ Please enter your email address.")
            elif not validate_email(email):
                st.error("⚠️ Please enter a valid email address (e.g. officer@forest.gov.in).")
            elif not password.strip():
                st.error("⚠️ Password cannot be empty.")
            else:
                st.success("✅ Credentials verified. Navigating to Dashboard...")
                login_user(email.strip(), remember_me)

        col_left, col_right = st.columns(2)
        with col_left:
            if st.button("Forgot Password?", key="forgot_pwd_nav_btn", use_container_width=True, type="secondary"):
                navigate_to(PAGE_FORGOT_PASSWORD)

        st.markdown(
            f"""
            <div style="text-align: center; font-size: 0.8rem; color: #94A3B8; margin-top: 2rem;">
                Authorized Personnel Only • {APP_NAME} v{APP_VERSION}
            </div>
            """,
            unsafe_allow_html=True
        )
