"""
EcoSense AI - Reusable Button Components
Includes Primary, Secondary, Danger, and Icon buttons.
"""

import streamlit as st

def primary_button(label: str, key: str = None, use_container_width: bool = True, disabled: bool = False) -> bool:
    """
    Renders a primary forest-green action button.
    """
    return st.button(
        label=label,
        key=key,
        type="primary",
        use_container_width=use_container_width,
        disabled=disabled
    )

def secondary_button(label: str, key: str = None, use_container_width: bool = True, disabled: bool = False) -> bool:
    """
    Renders a secondary bordered button.
    """
    return st.button(
        label=label,
        key=key,
        type="secondary",
        use_container_width=use_container_width,
        disabled=disabled
    )

def danger_button(label: str, key: str = None, use_container_width: bool = True, disabled: bool = False) -> bool:
    """
    Renders a red danger button for destructive actions.
    """
    return st.button(
        label=f"🚨 {label}",
        key=key,
        use_container_width=use_container_width,
        disabled=disabled
    )

def icon_button(icon: str, label: str, key: str = None) -> bool:
    """
    Renders an icon button with label.
    """
    return st.button(
        label=f"{icon} {label}",
        key=key,
        use_container_width=False
    )
