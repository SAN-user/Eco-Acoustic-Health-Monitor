import textwrap
import streamlit as st

def render_activity_timeline(activity_items: list):
    """
    Renders a vertical activity timeline showing acoustic events.
    """
    timeline_html = '<div style="display: flex; flex-direction: column; gap: 0.85rem;">\n'

    for item in activity_items:
        icon = item.get("icon", "🔔")
        title = item.get("title", "")
        time = item.get("time", "")
        status = item.get("status", "healthy")
        confidence = item.get("confidence", 90)

        badge_class = "eco-badge-critical" if status == "critical" else "eco-badge-healthy"

        timeline_html += textwrap.dedent(f"""<div style="display: flex; align-items: center; justify-content: space-between; padding: 0.85rem 1rem; background: rgba(248, 250, 252, 0.7); border: 1px solid #E2E8F0; border-radius: 12px;">
<div style="display: flex; align-items: center; gap: 0.85rem;">
<span style="font-size: 1.4rem;">{icon}</span>
<div>
<div style="font-weight: 700; font-size: 0.925rem; color: #0F172A;">{title}</div>
<div style="font-size: 0.775rem; color: #64748B;">{time} • Confidence {confidence}%</div>
</div>
</div>
<span class="eco-badge {badge_class}">{status.upper()}</span>
</div>""").strip() + "\n"

    timeline_html += '</div>'
    st.markdown(timeline_html, unsafe_allow_html=True)
