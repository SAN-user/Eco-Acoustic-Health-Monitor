"""
EcoSense AI - Dynamic CSS Injection Engine
Injects modern Apple / Material 3 glassmorphism styles into Streamlit.
"""

import streamlit as st
from app.styles.theme import ThemeTokens

def load_custom_css(dark_mode: bool = False):
    """
    Injects global custom CSS into the Streamlit session.
    """
    bg_color = ThemeTokens.DARK_BG if dark_mode else ThemeTokens.LIGHT_BG
    card_bg = ThemeTokens.DARK_CARD_BG if dark_mode else ThemeTokens.LIGHT_CARD_BG
    text_primary = ThemeTokens.DARK_TEXT_PRIMARY if dark_mode else ThemeTokens.LIGHT_TEXT_PRIMARY
    text_muted = ThemeTokens.DARK_TEXT_MUTED if dark_mode else ThemeTokens.LIGHT_TEXT_MUTED
    border_color = ThemeTokens.DARK_BORDER if dark_mode else ThemeTokens.LIGHT_BORDER

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* Global reset & typography */
    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_primary} !important;
    }}

    /* Main Container Padding */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }}

    /* Hide Default Header, Footer & Auto Multipage Nav */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    [data-testid="stSidebarNav"] {{
        display: none !important;
    }}

    /* Streamlit Sidebar Customization */
    [data-testid="stSidebar"] {{
        background-color: {card_bg} !important;
        border-right: 1px solid {border_color} !important;
    }}

    [data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        border-radius: 12px;
        text-align: left;
        padding: 0.65rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }}

    /* Custom Glassmorphism Card Utility */
    .eco-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: {ThemeTokens.CARD_SHADOW};
        margin-bottom: 1.25rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .eco-card:hover {{
        box-shadow: {ThemeTokens.HOVER_SHADOW};
        transform: translateY(-2px);
    }}

    /* Stat Card Styling */
    .eco-stat-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        box-shadow: {ThemeTokens.CARD_SHADOW};
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        position: relative;
        overflow: hidden;
    }}

    .eco-stat-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, {ThemeTokens.FOREST_GREEN}, {ThemeTokens.LEAF_ACCENT});
    }}

    .eco-stat-title {{
        font-size: 0.875rem;
        font-weight: 600;
        color: {text_muted};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }}

    .eco-stat-value {{
        font-size: 2.25rem;
        font-weight: 800;
        color: {text_primary};
        line-height: 1.1;
        margin-bottom: 0.35rem;
    }}

    .eco-stat-sub {{
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }}

    /* Header Component */
    .eco-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.75rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid {border_color};
    }}

    .eco-greeting {{
        font-size: 1.75rem;
        font-weight: 800;
        color: {text_primary};
        letter-spacing: -0.02em;
    }}

    .eco-subtitle {{
        font-size: 0.95rem;
        color: {text_muted};
        margin-top: 0.25rem;
    }}

    /* Quick Action Card */
    .eco-quick-action {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.25s ease;
        box-shadow: {ThemeTokens.CARD_SHADOW};
    }}

    .eco-quick-action:hover {{
        border-color: {ThemeTokens.EMERALD_GREEN};
        background: {ThemeTokens.LIGHT_MINT if not dark_mode else '#1E293B'};
        transform: translateY(-3px);
    }}

    .eco-quick-icon {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }}

    .eco-quick-title {{
        font-weight: 700;
        font-size: 1rem;
        color: {text_primary};
    }}

    /* Status Pills */
    .eco-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}

    .eco-badge-healthy {{
        background-color: #E8F5E9;
        color: #2E7D32;
        border: 1px solid #C8E6C9;
    }}

    .eco-badge-warning {{
        background-color: #FEF3C7;
        color: #D97706;
        border: 1px solid #FDE68A;
    }}

    .eco-badge-critical {{
        background-color: #FEE2E2;
        color: #DC2626;
        border: 1px solid #FCA5A5;
    }}

    .eco-badge-info {{
        background-color: #E0F2FE;
        color: #0284C7;
        border: 1px solid #BAE6FD;
    }}

    /* Splash Screen Overlay */
    .eco-splash-box {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, {ThemeTokens.FOREST_GREEN} 0%, {ThemeTokens.EMERALD_GREEN} 100%);
        color: white;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(30, 77, 43, 0.25);
        margin: 2rem auto;
        max-width: 650px;
    }}

    /* Custom Streamlit Button Styling Override */
    div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {ThemeTokens.FOREST_GREEN}, {ThemeTokens.EMERALD_GREEN}) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }}

    div.stButton > button[kind="primary"]:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(46, 125, 50, 0.35) !important;
    }}

    div.stButton > button[kind="secondary"] {{
        background-color: {card_bg} !important;
        color: {ThemeTokens.EMERALD_GREEN} !important;
        border: 1.5px solid {ThemeTokens.EMERALD_GREEN} !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 700 !important;
        transition: all 0.2s ease-in-out !important;
    }}

    div.stButton > button[kind="secondary"]:hover {{
        background-color: {ThemeTokens.LIGHT_MINT if not dark_mode else '#1E293B'} !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
