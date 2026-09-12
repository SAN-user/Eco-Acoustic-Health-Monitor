"""
Eco-Acoustic Health Monitor - Forgot Password Screen
"""

import textwrap
import streamlit as st
from app.config import APP_NAME, PAGE_LOGIN
from app.state.router import navigate_to

def render_forgot_password_page():
    """Renders the forgot password screen."""
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])

    with col2:
        st.markdown(
            textwrap.dedent(f"""
            <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 2rem 1.5rem; text-align: center; margin-bottom: 1.25rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.4rem;">🔑</div>
                <h2 style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.25rem;">Prototype Access Notice</h2>
                <div style="font-size: 0.85rem; color: #94A3B8;">
                    Password reset is not available because this prototype does not authenticate accounts or send email.
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

        st.info("**Prototype access** uses session state only. No registered accounts, password-reset links, or email delivery are configured.")

        if st.button("← Back to Login", key="back_to_login_btn", use_container_width=True, type="secondary"):
            navigate_to(PAGE_LOGIN)
