import textwrap
import streamlit as st

def render_stat_card(title: str, value: str, subtext: str = "", icon: str = "🌳"):
    """
    Renders a statistics card with top indicator bar, icon, value and subtext.
    """
    html = textwrap.dedent(f"""
    <div class="eco-stat-card">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="eco-stat-title">{title}</span>
                <span style="font-size: 1.25rem;">{icon}</span>
            </div>
            <div class="eco-stat-value">{value}</div>
        </div>
        <div class="eco-stat-sub" style="color: #94A3B8;">
            {subtext}
        </div>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)

def render_quick_action_card(title: str, description: str, icon: str = "⚡", button_label: str = "Open", key: str = None) -> bool:
    """
    Renders a quick action card with a clickable trigger button.
    """
    with st.container():
        st.markdown(
            textwrap.dedent(f"""
            <div class="eco-quick-action" style="background: #14201C; border: 1px solid #243630; border-radius: 12px; padding: 1.1rem; text-align: center;">
                <div class="eco-quick-icon" style="font-size: 1.8rem; margin-bottom: 0.35rem;">{icon}</div>
                <div class="eco-quick-title" style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">{title}</div>
                <div style="font-size: 0.775rem; color: #94A3B8; margin-top: 0.25rem; margin-bottom: 0.75rem;">
                    {description}
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
        return st.button(button_label, key=key, use_container_width=True, type="secondary")

def render_species_card(name: str, confidence: int, time_str: str, icon: str = "🦜"):
    """
    Renders a species detection card.
    """
    html = textwrap.dedent(f"""
    <div class="eco-card" style="padding: 1rem 1.25rem; display: flex; align-items: center; justify-content: space-between; background: #14201C; border: 1px solid #243630; border-radius: 12px;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 1.8rem;">{icon}</div>
            <div>
                <div style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">{name}</div>
                <div style="font-size: 0.775rem; color: #94A3B8;">Detected at {time_str}</div>
            </div>
        </div>
        <div style="text-align: right;">
            <span class="eco-badge eco-badge-safe">{confidence}% Match</span>
        </div>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)

def render_threat_card(threat_type: str, priority: str, zone: str, time_str: str, icon: str = "⚠"):
    """
    Renders an environmental threat alert card.
    """
    badge_class = "eco-badge-threat" if priority in ["High", "Critical"] else "eco-badge-warning"
    html = textwrap.dedent(f"""
    <div class="eco-card" style="padding: 1rem 1.25rem; border-left: 4px solid #EF4444; background: #14201C; border-top: 1px solid #243630; border-right: 1px solid #243630; border-bottom: 1px solid #243630; border-radius: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.4rem;">{icon}</span>
                <div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">{threat_type} Detected</div>
                    <div style="font-size: 0.775rem; color: #94A3B8;">{zone} • {time_str}</div>
                </div>
            </div>
            <span class="eco-badge {badge_class}">{priority}</span>
        </div>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)
