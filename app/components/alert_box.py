"""
EcoSense AI - Alert Box Component
Renders severity alert banners (Critical, High, Medium, Low).
"""

import streamlit as st

def render_alert_box(message: str, severity: str = "Medium", title: str = None):
    """
    Renders a styled alert banner.
    severity: 'Critical', 'High', 'Medium', 'Low'
    """
    styles = {
        "Critical": {"bg": "#FEE2E2", "border": "#EF4444", "color": "#991B1B", "icon": "🚨"},
        "High": {"bg": "#FEF3C7", "border": "#F59E0B", "color": "#92400E", "icon": "⚠"},
        "Medium": {"bg": "#E0F2FE", "border": "#0284C7", "color": "#075985", "icon": "ℹ"},
        "Low": {"bg": "#E8F5E9", "border": "#2E7D32", "color": "#166534", "icon": "✅"}
    }
    cfg = styles.get(severity, styles["Medium"])
    heading = title if title else f"{severity} Priority Alert"

    html = f"""
    <div style="background-color: {cfg['bg']}; border-left: 4px solid {cfg['border']}; padding: 1rem 1.25rem; border-radius: 12px; margin-bottom: 1rem;">
        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
            <span style="font-size: 1.3rem;">{cfg['icon']}</span>
            <div>
                <div style="font-weight: 700; color: {cfg['color']}; font-size: 0.95rem;">{heading}</div>
                <div style="font-size: 0.875rem; color: {cfg['color']}; opacity: 0.9; margin-top: 0.2rem;">{message}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
