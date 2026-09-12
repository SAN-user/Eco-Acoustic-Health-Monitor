"""
Eco-Acoustic Health Monitor - Reports Screen
Displays active audio analysis results and provides SQLite CSV export options.
"""

import textwrap
import streamlit as st
import pandas as pd
from app.components.navigation import render_page_header
from app.state.session_state import get_state
from app.utils.formatters import format_file_size, format_duration
from app.services.database_service import get_recent_analyses

def render_reports_page():
    """Renders persistent SQLite reports and CSV export options."""
    render_page_header(
        title="Monitoring Reports",
        subtitle="Export historical acoustic monitoring results stored in the system.",
        breadcrumb="Dashboard / Reports"
    )

    db_records = get_recent_analyses(limit=500)
    db_count = len(db_records)

    # 1. Main Report Card
    st.markdown(
        textwrap.dedent(f"""
        <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #1F2D28; padding-bottom: 0.75rem;">
                <div>
                    <div style="font-weight: 800; font-size: 1.15rem; color: #F8FAFC;">📊 System Monitoring Records Export</div>
                    <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 0.2rem;">SQLite Database Persistence Status</div>
                </div>
                <span class="eco-badge eco-badge-safe">{db_count} Analyses Available</span>
            </div>

            <div style="font-size: 0.9rem; font-weight: 600; color: #F8FAFC; margin-bottom: 0.5rem;">Exported CSV Includes:</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.6rem; font-size: 0.85rem; color: #34D399; margin-bottom: 1.25rem;">
                <div>✓ Recording metadata (Sample rate, duration)</div>
                <div>✓ Wildlife classifications (5-class RF model)</div>
                <div>✓ AST sound events (AudioSet classes)</div>
                <div>✓ Threat detections (Chainsaw, gunfire, vehicle)</div>
                <div>✓ Ecosystem health scores (Heuristic index)</div>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    if db_records:
        df_db = pd.DataFrame(db_records)
        csv_db_data = df_db.to_csv(index=False).encode('utf-8')

        st.download_button(
            label=f"Download CSV Report ({db_count} Persisted Records) 📥",
            data=csv_db_data,
            file_name="eco_acoustic_monitoring_report.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    else:
        st.markdown(
            textwrap.dedent("""
            <div style="text-align: center; padding: 2.5rem 1.5rem; background: #14201C; border: 1px solid #243630; border-radius: 14px; margin-bottom: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #F8FAFC;">No Reports Available</div>
                <div style="font-size: 0.875rem; color: #94A3B8; margin-top: 0.35rem;">
                    Complete an analysis to generate monitoring records.
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

    # 2. Active Session Summary Export Section
    meta = get_state("uploaded_audio_metadata")
    prep_data = get_state("preprocessed_audio")
    analysis_results = get_state("analysis_results")
    wildlife_results = get_state("wildlife_results")

    has_active_analysis = bool(
        (analysis_results and isinstance(analysis_results, dict) and analysis_results.get("predicted_class"))
        or (meta and isinstance(meta, dict) and meta.get("filename"))
    )

    if has_active_analysis:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;'>⚡ Active Session Single-File Report</h3>", unsafe_allow_html=True)

        filename = (meta.get("filename") if meta else None) or (prep_data.get("filename") if prep_data else "Unknown")
        file_format = meta.get("format", "N/A") if meta else "N/A"
        duration_sec = meta.get("duration_sec") if meta else (prep_data.get("duration") if prep_data else None)
        sample_rate = meta.get("sample_rate_hz") if meta else (prep_data.get("sample_rate") if prep_data else None)

        ast_class = analysis_results.get("predicted_class", "N/A") if analysis_results else "N/A"
        ast_conf_pct = analysis_results.get("confidence_pct", 0.0) if analysis_results else 0.0
        threat_info = analysis_results.get("threat_status", {}) if analysis_results else {}
        has_threat = threat_info.get("has_threat", False)

        health_score = max(35, 95 - 35) if has_threat else min(98, max(75, int(75 + ast_conf_pct * 0.2)))
        predicted_species = wildlife_results.get("predicted_species", "N/A") if wildlife_results else "N/A"

        report_dict = {
            "Metric": ["Filename", "Format", "Duration (s)", "Sample Rate (Hz)", "AST Detection", "AST Confidence (%)", "Threat Detected", "Health Score", "Predicted Wildlife"],
            "Value": [filename, file_format, duration_sec, sample_rate, ast_class, round(ast_conf_pct, 2), has_threat, health_score, predicted_species]
        }
        df_active = pd.DataFrame(report_dict)
        csv_active_data = df_active.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Active Session Summary (CSV) 📄",
            data=csv_active_data,
            file_name="eco_acoustic_active_session.csv",
            mime="text/csv",
            use_container_width=True
        )
