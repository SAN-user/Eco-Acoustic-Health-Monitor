"""
EcoSense AI - Dialog & Modal Component Wrappers (Section 4.22)
"""

import streamlit as st

def confirm_action_dialog(title: str, message: str, action_label: str = "Confirm", cancel_label: str = "Cancel", key: str = "modal") -> bool:
    """
    Renders an inline confirmation dialog.
    """
    with st.expander(f"⚠️ {title}", expanded=True):
        st.write(message)
        col1, col2 = st.columns(2)
        with col1:
            cancelled = st.button(cancel_label, key=f"{key}_cancel", use_container_width=True, type="secondary")
        with col2:
            confirmed = st.button(action_label, key=f"{key}_confirm", use_container_width=True, type="primary")

        if confirmed:
            return True
        return False
