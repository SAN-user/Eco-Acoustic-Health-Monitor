"""
EcoSense AI - Reusable Input Components
Includes text input, password field with toggle, search bar, dropdowns, and date pickers.
"""

import streamlit as st

def text_input(label: str, value: str = "", placeholder: str = "", key: str = None, type: str = "default") -> str:
    """
    Renders a standard text input field.
    """
    return st.text_input(
        label=label,
        value=value,
        placeholder=placeholder,
        key=key,
        type=type
    )

def password_input(label: str = "Password", key: str = "password_input") -> str:
    """
    Renders a password input field with show/hide toggle support.
    """
    show_password_key = f"{key}_show_toggle"
    if show_password_key not in st.session_state:
        st.session_state[show_password_key] = False

    col1, col2 = st.columns([5, 1], vertical_alignment="bottom")
    with col1:
        input_type = "default" if st.session_state[show_password_key] else "password"
        val = st.text_input(
            label=label,
            placeholder="••••••••",
            type=input_type,
            key=key
        )
    with col2:
        toggle_label = "🙈 Hide" if st.session_state[show_password_key] else "👁 Show"
        if st.button(toggle_label, key=f"{key}_toggle_btn", use_container_width=True):
            st.session_state[show_password_key] = not st.session_state[show_password_key]
            st.rerun()

    return val

def search_input(placeholder: str = "Search species, threats, or recordings...", key: str = "search_field") -> str:
    """
    Renders a search input field with search icon.
    """
    return st.text_input(
        label="🔍 Search",
        placeholder=placeholder,
        key=key,
        label_visibility="collapsed"
    )

def select_dropdown(label: str, options: list, default_index: int = 0, key: str = None):
    """
    Renders a styled selectbox dropdown.
    """
    return st.selectbox(
        label=label,
        options=options,
        index=default_index,
        key=key
    )
