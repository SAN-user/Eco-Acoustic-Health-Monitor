"""
EcoSense AI - Dynamic CSS Injection Engine
Injects professional dark forest environmental monitoring styles into Streamlit.
"""

import streamlit as st
from app.styles.theme import ThemeTokens

def load_custom_css(dark_mode: bool = True):
    """
    Injects global custom CSS into the Streamlit session.
    Default mode is dark forest environmental aesthetic.
    """
    bg_color = ThemeTokens.DARK_BG if dark_mode else ThemeTokens.LIGHT_BG
    card_bg = ThemeTokens.DARK_CARD_BG if dark_mode else ThemeTokens.LIGHT_CARD_BG
    text_primary = ThemeTokens.DARK_TEXT_PRIMARY if dark_mode else ThemeTokens.LIGHT_TEXT_PRIMARY
    text_muted = ThemeTokens.DARK_TEXT_MUTED if dark_mode else ThemeTokens.LIGHT_TEXT_MUTED
    border_color = ThemeTokens.DARK_BORDER if dark_mode else ThemeTokens.LIGHT_BORDER

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* Global Reset & Dark Forest Canvas */
    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_primary} !important;
    }}

    /* Main Content Container Padding & Constraint */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1240px !important;
    }}

    /* Hide Default Header, Footer & Streamlit Brand Elements */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    [data-testid="stSidebarNav"] {{
        display: none !important;
    }}

    /* Streamlit Sidebar Customization */
    [data-testid="stSidebar"] {{
        background-color: {ThemeTokens.DARK_SIDEBAR_BG if dark_mode else ThemeTokens.LIGHT_BG} !important;
        border-right: 1px solid {border_color} !important;
    }}

    [data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        border-radius: 10px;
        text-align: left;
        padding: 0.6rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }}

    /* Professional Environmental Card Container */
    .eco-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: {ThemeTokens.CARD_SHADOW};
        margin-bottom: 1.25rem;
    }}

    /* Metric / Stat Card Styling */
    .eco-stat-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 1.25rem 1.25rem;
        box-shadow: {ThemeTokens.CARD_SHADOW};
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }}

    .eco-stat-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, {ThemeTokens.FOREST_GREEN}, {ThemeTokens.EMERALD_GREEN});
    }}

    .eco-stat-title {{
        font-size: 0.8rem;
        font-weight: 700;
        color: {text_muted};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}

    .eco-stat-value {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {text_primary};
        line-height: 1.1;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }}

    .eco-stat-sub {{
        font-size: 0.825rem;
        font-weight: 500;
        color: {ThemeTokens.EMERALD_GREEN};
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }}

    /* Page Headers */
    .eco-header {{
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid {border_color};
    }}

    .eco-title {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {text_primary};
        letter-spacing: -0.025em;
        margin-bottom: 0.25rem;
    }}

    .eco-subtitle {{
        font-size: 0.925rem;
        color: {text_muted};
    }}

    /* System Online Status Indicator Badge */
    .system-status-online {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        font-size: 0.775rem;
        font-weight: 700;
        letter-spacing: 0.03em;
    }}

    .system-status-dot {{
        width: 8px;
        height: 8px;
        background-color: #34D399;
        border-radius: 50%;
        box-shadow: 0 0 8px #34D399;
    }}

    /* Status Badges */
    .eco-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.775rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }}

    .eco-badge-safe {{
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }}

    .eco-badge-warning {{
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }}

    .eco-badge-threat {{
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }}

    .eco-badge-info {{
        background-color: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.35);
    }}

    /* Polished Streamlit Buttons */
    div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #059669, #10B981) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.4rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }}

    div.stButton > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #047857, #059669) !important;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.45) !important;
        transform: translateY(-1px) !important;
    }}

    div.stButton > button[kind="secondary"] {{
        background-color: {card_bg} !important;
        color: {text_primary} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.4rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }}

    div.stButton > button[kind="secondary"]:hover {{
        border-color: {ThemeTokens.EMERALD_GREEN} !important;
        color: {ThemeTokens.EMERALD_GREEN} !important;
        background-color: rgba(16, 185, 129, 0.08) !important;
    }}

    /* Custom Streamlit Metric & Expander Tweaks */
    [data-testid="stMetricValue"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        color: {text_primary} !important;
    }}

    .stExpander {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
