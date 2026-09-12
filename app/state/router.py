"""
EcoSense AI - Navigation Router & Route Guards
"""

import streamlit as st
from app.config import (
    PAGE_SPLASH,
    PAGE_LOGIN,
    PAGE_FORGOT_PASSWORD,
    PAGE_DASHBOARD,
)
from app.state.session_state import get_state, set_state

PUBLIC_PAGES = {PAGE_SPLASH, PAGE_LOGIN, PAGE_FORGOT_PASSWORD}

def navigate_to(page_key: str):
    """
    Transitions the application to the specified target page key.
    Reruns the Streamlit script to update UI immediately.
    """
    set_state("current_page", page_key)
    st.rerun()

def get_current_page() -> str:
    """Returns the current active page key."""
    return get_state("current_page", PAGE_SPLASH)

def is_authenticated() -> bool:
    """Checks whether prototype session access is active."""
    return bool(get_state("authenticated", False))

def enforce_route_guard() -> str:
    """
    Applies the prototype session-state gate for protected pages.
    If prototype access is inactive, redirects to the prototype access screen.
    Returns the resolved page key to display.
    """
    current_page = get_current_page()
    authenticated = is_authenticated()

    if not authenticated and current_page not in PUBLIC_PAGES:
        set_state("current_page", PAGE_LOGIN)
        return PAGE_LOGIN

    if authenticated and current_page in {PAGE_LOGIN, PAGE_FORGOT_PASSWORD}:
        set_state("current_page", PAGE_DASHBOARD)
        return PAGE_DASHBOARD

    return current_page

def login_user(email: str, remember: bool = False):
    """
    Starts prototype session access and routes to the Dashboard.
    """
    set_state("authenticated", True)
    set_state("remember_me", remember)
    navigate_to(PAGE_DASHBOARD)

def logout_user():
    """
    Clears prototype session access and routes back to the prototype access screen.
    """
    set_state("authenticated", False)
    navigate_to(PAGE_LOGIN)
