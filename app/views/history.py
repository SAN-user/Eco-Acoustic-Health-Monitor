"""
Eco-Acoustic Health Monitor - Analysis History Screen
Reads and displays persistent real audio analysis records from the SQLite database.
"""

import textwrap
import streamlit as st
import pandas as pd
from app.components.navigation import render_page_header
from app.components.inputs import search_input
from app.services.database_service import get_recent_analyses

def render_history_page():
    """Renders real historical analysis records from SQLite with search capabilities."""
    render_page_header(
        title="Historical Analysis Records",
        subtitle="View, search, and review persisted audio analysis records from your soundscape monitoring.",
        breadcrumb="Dashboard / History"
    )

    records = get_recent_analyses(limit=100)

    if not records:
        st.markdown(
            textwrap.dedent("""
            <div style="text-align: center; padding: 3rem 1.5rem; background: #14201C; border: 1px solid #243630; border-radius: 14px; margin-top: 1rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎧</div>
                <div style="font-weight: 700; font-size: 1.15rem; color: #F8FAFC;">No analysis history available yet.</div>
                <div style="font-size: 0.875rem; color: #94A3B8; margin-top: 0.35rem;">
                    Upload a forest recording to begin acoustic monitoring.
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
        return

    # Prepare DataFrame
    formatted_rows = []
    for r in records:
        ast_conf_pct = r["ast_confidence"] * 100 if r["ast_confidence"] <= 1.0 else r["ast_confidence"]
        wf_conf_pct = r["wildlife_confidence"] * 100 if r["wildlife_confidence"] <= 1.0 else r["wildlife_confidence"]
        has_threat = bool(r["threat_detected"])
        threat_str = f"🔴 {r['threat_label']}" if has_threat else "🟢 SAFE"

        formatted_rows.append({
            "Date & Time": r["timestamp"],
            "Recording": r["filename"] or "Unknown",
            "Duration (s)": f"{r['duration_sec']:.1f}",
            "Wildlife Species": r["wildlife_species"],
            "Wildlife Confidence": f"{wf_conf_pct:.1f}%",
            "AST Sound Event": f"{r['ast_top_label']} ({ast_conf_pct:.1f}%)",
            "Threat Status": threat_str,
            "Health Score": f"{r['health_score']} / 100"
        })

    df = pd.DataFrame(formatted_rows)

    search_term = search_input(placeholder="Search by recording name, species, or status...")
    if search_term:
        mask = (
            df["Recording"].str.contains(search_term, case=False, na=False) |
            df["Wildlife Species"].str.contains(search_term, case=False, na=False) |
            df["AST Sound Event"].str.contains(search_term, case=False, na=False) |
            df["Threat Status"].str.contains(search_term, case=False, na=False)
        )
        df = df[mask]

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <div style="font-size: 0.9rem; font-weight: 700; color: #10B981;">
                Showing {len(df)} Persisted Database Analysis Records
            </div>
            <div style="font-size: 0.775rem; color: #94A3B8;">
                Source: <code>data/eco_acoustic.db</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date & Time": st.column_config.TextColumn("Date & Time", width="medium"),
            "Recording": st.column_config.TextColumn("Recording", width="medium"),
            "Wildlife Species": st.column_config.TextColumn("Wildlife Species", width="medium"),
            "Threat Status": st.column_config.TextColumn("Threat Status", width="small"),
            "Health Score": st.column_config.TextColumn("Health Score", width="small"),
        }
    )
