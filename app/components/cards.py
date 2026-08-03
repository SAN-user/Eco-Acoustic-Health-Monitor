"""
EcoSense AI - Card Components
Provides Stat Cards, Quick Action Cards, Species Cards, Threat Cards, and Health Score Cards.
"""

import streamlit as st

def render_stat_card(title: str, value: str, subtext: str = "", icon: str = "🌳"):
    """
    Renders a statistics card with top indicator bar, icon, value and subtext.
    """
    html = f"""
    <div class="eco-stat-card">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="eco-stat-title">{title}</span>
                <span style="font-size: 1.25rem;">{icon}</span>
            </div>
            <div class="eco-stat-value">{value}</div>
        </div>
        <div class="eco-stat-sub" style="color: #64748B;">
            {subtext}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_quick_action_card(title: str, description: str, icon: str = "⚡", button_label: str = "Open", key: str = None) -> bool:
    """
    Renders a quick action card with a clickable trigger button.
    """
    with st.container():
        st.markdown(
            f"""
            <div class="eco-quick-action">
                <div class="eco-quick-icon">{icon}</div>
                <div class="eco-quick-title">{title}</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 0.25rem; margin-bottom: 0.75rem;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return st.button(button_label, key=key, use_container_width=True, type="secondary")

def render_species_card(name: str, confidence: int, time_str: str, icon: str = "🦜"):
    """
    Renders a species detection card.
    """
    html = f"""
    <div class="eco-card" style="padding: 1rem 1.25rem; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">{icon}</div>
            <div>
                <div style="font-weight: 700; font-size: 1rem;">{name}</div>
                <div style="font-size: 0.8rem; color: #64748B;">Detected at {time_str}</div>
            </div>
        </div>
        <div style="text-align: right;">
            <span class="eco-badge eco-badge-healthy">{confidence}% Match</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_threat_card(threat_type: str, priority: str, zone: str, time_str: str, icon: str = "⚠"):
    """
    Renders an environmental threat alert card.
    """
    badge_class = "eco-badge-critical" if priority in ["High", "Critical"] else "eco-badge-warning"
    html = f"""
    <div class="eco-card" style="padding: 1rem 1.25rem; border-left: 4px solid #DC2626;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <div>
                    <div style="font-weight: 700; font-size: 1rem; color: #1E293B;">{threat_type} Detected</div>
                    <div style="font-size: 0.8rem; color: #64748B;">{zone} • {time_str}</div>
                </div>
            </div>
            <span class="eco-badge {badge_class}">{priority}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
