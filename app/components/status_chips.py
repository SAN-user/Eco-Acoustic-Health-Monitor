"""
EcoSense AI - Status Chips Component
Renders pill-shaped status chips for Healthy, Threat, Analyzing, Completed, etc.
"""

import streamlit as st

def render_status_chip(status_text: str, category: str = "healthy"):
    """
    Renders a pill-shaped status chip.
    categories: 'healthy', 'warning', 'critical', 'info'
    """
    category_map = {
        "healthy": "eco-badge-healthy",
        "warning": "eco-badge-warning",
        "critical": "eco-badge-critical",
        "info": "eco-badge-info"
    }
    badge_class = category_map.get(category.lower(), "eco-badge-info")
    
    html = f"""
    <span class="eco-badge {badge_class}">
        {status_text}
    </span>
    """
    st.markdown(html, unsafe_allow_html=True)
