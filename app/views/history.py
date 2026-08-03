"""
Eco-Acoustic Health Monitor - Analysis History Screen (Section 3.11 Placeholder UI)
"""

import streamlit as st
from app.components.navigation import render_page_header
from app.components.inputs import search_input
from app.utils.mock_data import get_history_records

def render_history_page():
    """Renders historical analysis records with search and filter capabilities."""
    render_page_header(
        title="Historical Analysis Records",
        subtitle="Search and review past audio analyses, detected species, threats, and health trends.",
        breadcrumb="Dashboard / History"
    )

    search_term = search_input(placeholder="Search audio recording name, species, or status...")

    df = get_history_records()

    if search_term:
        df = df[df["Audio Name"].str.contains(search_term, case=False) | df["Species"].str.contains(search_term, case=False)]

    st.dataframe(df, use_container_width=True, hide_index=True)
