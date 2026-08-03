"""
Eco-Acoustic Health Monitor - Forgot Password Screen (Section 3.4)
"""

import streamlit as st
from app.config import APP_NAME, PAGE_LOGIN
from app.state.router import navigate_to

def render_forgot_password_page():
    """Renders the forgot password screen."""
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])

    with col2:
        st.markdown(
            f"""
            <div class="eco-card" style="padding: 2rem; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔑</div>
                <h2 style="font-size: 1.5rem; font-weight: 800; color: #1E4D2B; margin-bottom: 0.25rem;">Reset Your Password</h2>
                <div style="font-size: 0.875rem; color: #64748B;">
                    Enter your registered email address to receive password reset instructions.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("forgot_pwd_form"):
            email = st.text_input("Registered Email Address", placeholder="officer@forest.gov.in")
            submitted = st.form_submit_button("Send Reset Link", use_container_width=True, type="primary")

            if submitted:
                if not email.strip() or "@" not in email:
                    st.error("⚠️ Please enter a valid registered email address.")
                else:
                    st.success(f"✅ Reset link sent successfully to `{email}`! Check your inbox.")

        if st.button("← Back to Login", key="back_to_login_btn", use_container_width=True, type="secondary"):
            navigate_to(PAGE_LOGIN)
