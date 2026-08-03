"""
Eco-Acoustic Health Monitor - Active Alerts Screen (Section 3.10 Placeholder UI)
"""

import streamlit as st
from app.components.navigation import render_page_header
from app.components.cards import render_threat_card
from app.utils.mock_data import get_active_alerts

def render_alerts_page():
    """Renders active environmental threat alerts list."""
    render_page_header(
        title="Environmental Threat Alerts",
        subtitle="Real-time acoustic detection alerts requiring forest officer inspection.",
        breadcrumb="Dashboard / Alerts"
    )

    alerts = get_active_alerts()

    for alert in alerts:
        render_threat_card(
            threat_type=alert["type"],
            priority=alert["priority"],
            zone=alert["zone"],
            time_str=alert["time"],
            icon="🚨" if alert["priority"] == "Critical" else "⚠"
        )
