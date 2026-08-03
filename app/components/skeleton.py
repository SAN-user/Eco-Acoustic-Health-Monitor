"""
EcoSense AI - Skeleton Loaders
Shows placeholder skeletons while data loads (Section 4.21).
"""

import streamlit as st

def render_card_skeleton(height: int = 120):
    """Renders a card skeleton placeholder."""
    html = f"""
    <div style="background: linear-gradient(90deg, #F1F5F9 25%, #E2E8F0 50%, #F1F5F9 75%); background-size: 200% 100%; animation: loading 1.5s infinite; border-radius: 16px; height: {height}px; margin-bottom: 1rem;"></div>
    <style>
    @keyframes loading {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)
