"""
EcoSense AI - Session State Manager
Maintains single-source-of-truth in Streamlit's st.session_state without state duplication.
"""

import streamlit as st
from app.config import DEFAULT_USER, PAGE_SPLASH, PAGE_LOGIN, PAGE_DASHBOARD

def init_session_state():
    """
    Initializes all session state keys with default values if not already present.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "current_page" not in st.session_state:
        st.session_state.current_page = PAGE_SPLASH

    if "user_profile" not in st.session_state:
        st.session_state.user_profile = DEFAULT_USER.copy()

    if "remember_me" not in st.session_state:
        st.session_state.remember_me = False

    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    if "notifications" not in st.session_state:
        st.session_state.notifications = [
            {"id": 1, "title": "Chainsaw Detected", "time": "10:22 AM", "priority": "High", "read": False},
            {"id": 2, "title": "Indian Peacock Identified", "time": "09:15 AM", "priority": "Low", "read": False},
            {"id": 3, "title": "Weekly Health Report Ready", "time": "Yesterday", "priority": "Medium", "read": True},
        ]

    if "flash_message" not in st.session_state:
        st.session_state.flash_message = None

    if "uploaded_audio_file" not in st.session_state:
        st.session_state.uploaded_audio_file = None

    if "uploaded_audio_metadata" not in st.session_state:
        st.session_state.uploaded_audio_metadata = None

    if "analysis_in_progress" not in st.session_state:
        st.session_state.analysis_in_progress = False

def get_state(key: str, default=None):
    """Safe getter for session state keys."""
    return st.session_state.get(key, default)

def set_state(key: str, value):
    """Safe setter for session state keys."""
    st.session_state[key] = value

def set_flash(message: str, category: str = "info"):
    """Sets a temporary alert message to be shown across page navigation."""
    st.session_state.flash_message = {"message": message, "category": category}

def get_flash():
    """Retrieves and clears the current flash message."""
    msg = st.session_state.get("flash_message", None)
    st.session_state.flash_message = None
    return msg
