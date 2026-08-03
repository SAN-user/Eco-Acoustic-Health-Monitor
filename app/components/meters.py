"""
EcoSense AI - Gauge and Confidence Meters
"""

import streamlit as st

def render_health_meter(score: int, status_text: str = "Healthy"):
    """
    Renders a visual Forest Health Score gauge.
    """
    if score >= 90:
        color = "#2E7D32"
    elif score >= 70:
        color = "#F59E0B"
    else:
        color = "#DC2626"

    html = f"""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="position: relative; width: 140px; height: 140px; margin: 0 auto; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: conic-gradient({color} 0% {score}%, #E2E8F0 {score}% 100%);">
            <div style="width: 110px; height: 110px; border-radius: 50%; background: white; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <span style="font-size: 2rem; font-weight: 800; color: {color}; line-height: 1;">{score}%</span>
                <span style="font-size: 0.75rem; font-weight: 700; color: #64748B; margin-top: 2px;">{status_text}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_confidence_meter(confidence: int):
    """
    Renders a prediction confidence progress meter with status color.
    90-100%: Green
    70-89%: Yellow
    <70%: Red
    """
    if confidence >= 90:
        color = "#2E7D32"
        label = "High Confidence"
    elif confidence >= 70:
        color = "#F59E0B"
        label = "Medium Confidence"
    else:
        color = "#DC2626"
        label = "Low Confidence"

    st.markdown(f"**Confidence Level**: `{confidence}%` ({label})")
    st.progress(confidence / 100.0)
