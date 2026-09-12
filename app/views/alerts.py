"""
Eco-Acoustic Health Monitor - Environmental Threat Alerts Screen
Reads and displays persistent real acoustic threat alerts from the SQLite database.
"""

import textwrap
import streamlit as st
from app.components.navigation import render_page_header
from app.services.database_service import get_all_alerts, toggle_alert_acknowledgement

def render_alerts_page():
    """Renders active environmental threat alerts list from SQLite."""
    render_page_header(
        title="Environmental Threat Alerts",
        subtitle="Real-time acoustic threat detections, chainsaws, gunshots, and vehicle activity alerts.",
        breadcrumb="Dashboard / Alerts"
    )

    alerts = get_all_alerts()

    if not alerts:
        st.markdown(
            textwrap.dedent("""
            <div style="text-align: center; padding: 3rem 1.5rem; background: #14201C; border: 1px solid #243630; border-radius: 14px; margin-top: 1rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🟢</div>
                <div style="font-weight: 700; font-size: 1.15rem; color: #34D399;">No Active Alerts</div>
                <div style="font-size: 0.875rem; color: #94A3B8; margin-top: 0.35rem;">
                    Your stored analyses currently contain no detected anthropogenic threats.
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
        return

    st.markdown(
        f"""
        <div style="font-size: 0.9rem; font-weight: 700; color: #F87171; margin-bottom: 1rem;">
            ⚠️ Found {len(alerts)} Persistent Threat Alert Records:
        </div>
        """,
        unsafe_allow_html=True
    )

    for alert in alerts:
        a_id = alert["alert_id"]
        ack = alert["acknowledged"]
        conf_pct = alert["confidence"] * 100 if alert["confidence"] <= 1.0 else alert["confidence"]
        badge_cls = "eco-badge-safe" if ack else "eco-badge-threat"
        ack_label = "ACKNOWLEDGED" if ack else "UNACKNOWLEDGED"

        st.markdown(
            textwrap.dedent(f"""
            <div class="eco-card" style="margin-bottom: 1rem; border-left: 4px solid {'#10B981' if ack else '#EF4444'}; background: #14201C; border-top: 1px solid #243630; border-right: 1px solid #243630; border-bottom: 1px solid #243630; border-radius: 12px; padding: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-weight: 800; font-size: 1.05rem; color: {'#34D399' if ack else '#F87171'};">
                            ⚠️ THREAT DETECTED: {alert['alert_type']}
                        </div>
                        <div style="font-size: 0.875rem; color: #F8FAFC; margin-top: 0.35rem;">
                            {alert['message']}
                        </div>
                        <div style="font-size: 0.775rem; color: #94A3B8; margin-top: 0.5rem;">
                            🕒 <b>Timestamp:</b> {alert['timestamp']} &nbsp;|&nbsp; 📄 <b>Recording:</b> <code>{alert.get('filename', 'N/A')}</code> &nbsp;|&nbsp; ⚡ <b>Confidence:</b> {conf_pct:.1f}%
                        </div>
                    </div>
                    <span class="eco-badge {badge_cls}">{ack_label}</span>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

        # Acknowledgement Button
        btn_label = "Mark as Resolved / Acknowledged" if not ack else "Re-open Alert"
        if st.button(btn_label, key=f"btn_ack_{a_id}"):
            toggle_alert_acknowledgement(a_id)
            st.rerun()
