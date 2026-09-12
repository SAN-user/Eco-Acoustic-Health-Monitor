"""
Eco-Acoustic Health Monitor - Audio Analysis Screen
Displays real uploaded audio metadata, Librosa audio preprocessing metrics,
interactive Mel Spectrogram, Hugging Face AudioSpectrogramTransformer (AST) sound classification,
and Module 4 Wildlife Acoustic Feature Profiling & Ecosystem Assessment.
"""

import textwrap
from pathlib import Path
import streamlit as st
import numpy as np
import plotly.express as px
from app.components.navigation import render_page_header
from app.components.buttons import primary_button, secondary_button
from app.config import PAGE_REPORTS, PAGE_UPLOAD, UPLOADS_DIR
from app.state.router import navigate_to
from app.state.session_state import get_state, set_state
from app.services.audio_service import extract_audio_metadata
from app.utils.formatters import format_file_size, format_duration
from ai.preprocessing import preprocess_audio_pipeline
from ai.inference import run_ast_inference, run_wildlife_inference

def render_analysis_page():
    """Renders the AI Analysis results page."""
    render_page_header(
        title="AI Soundscape Analysis Results",
        subtitle="Detailed wildlife classification, threat detection, and ecosystem health predictions.",
        breadcrumb="Dashboard / Audio Analysis"
    )

    # 1. Retrieve Real Uploaded Audio Metadata (with auto-fallback to uploads dir)
    meta = get_state("uploaded_audio_metadata")
    if not meta or not meta.get("file_path") or not Path(meta["file_path"]).exists():
        # Auto-fallback: check uploads directory for existing saved recording
        if UPLOADS_DIR.exists():
            upload_files = list(UPLOADS_DIR.glob("*.wav")) + list(UPLOADS_DIR.glob("*.mp3"))
            if upload_files:
                target_file = upload_files[0]
                try:
                    meta = extract_audio_metadata(
                        file_source=target_file,
                        filename=target_file.name,
                        file_size_bytes=target_file.stat().st_size
                    )
                    meta["file_path"] = str(target_file.resolve())
                    set_state("uploaded_audio_metadata", meta)
                    set_state("uploaded_audio_file", target_file.name)
                except Exception:
                    meta = None

    prep_data = get_state("preprocessed_audio")
    analysis_results = get_state("analysis_results")
    wildlife_results = get_state("wildlife_results")

    if meta and meta.get("file_path"):
        file_path = meta["file_path"]
        channels_str = "Stereo" if meta.get("channels") == 2 else "Mono" if meta.get("channels") == 1 else str(meta.get("channels"))
        bitrate_str = f"{meta['bitrate'] // 1000} kbps" if meta.get("bitrate") else "N/A"

        st.markdown(
            textwrap.dedent(f"""
            <div class="eco-card" style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem; margin-bottom: 1.25rem;">
                <div style="font-weight: 800; font-size: 1.15rem; color: #F8FAFC; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
                    <span>🎵 Active Soundscape File: {meta.get('filename', 'Unknown')}</span>
                    <span class="eco-badge eco-badge-info">Ready for Inference</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.75rem; font-size: 0.85rem; color: #94A3B8;">
                    <div><b style="color: #F8FAFC;">Format:</b> {meta.get('format', 'N/A').upper()}</div>
                    <div><b style="color: #F8FAFC;">Duration:</b> {format_duration(int(round(meta.get('duration_sec', 0))))} ({meta.get('duration_sec')}s)</div>
                    <div><b style="color: #F8FAFC;">Sample Rate:</b> {meta.get('sample_rate_hz')} Hz</div>
                    <div><b style="color: #F8FAFC;">Channels:</b> {channels_str}</div>
                    <div><b style="color: #F8FAFC;">File Size:</b> {format_file_size(meta.get('size_bytes', 0))}</div>
                    <div><b style="color: #F8FAFC;">Bitrate:</b> {bitrate_str}</div>
                </div>
                <div style="font-size: 0.775rem; color: #64748B; margin-top: 0.75rem; word-break: break-all; background: #0B1311; padding: 0.4rem 0.75rem; border-radius: 8px;">
                    📁 <b>Audio File Location:</b> <code>{file_path}</code>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

        # 2. Run / Cache Audio Preprocessing Pipeline (Module 2)
        if not prep_data or prep_data.get("file_path") != file_path:
            with st.spinner("⚡ Running Librosa audio preprocessing (16kHz Mono Resampling & Mel Spectrogram)..."):
                try:
                    prep_data = preprocess_audio_pipeline(file_path, target_sr=16000)
                    set_state("preprocessed_audio", prep_data)
                except Exception as e:
                    st.error(f"❌ Audio Preprocessing Pipeline Failed: {str(e)}")
                    prep_data = None

        # 3. Run / Cache Module 3 AST AI Model Inference
        if not analysis_results or analysis_results.get("file_path") != file_path:
            with st.spinner("🤖 Running Hugging Face AST Model Inference (MIT/ast-finetuned-audioset)..."):
                try:
                    analysis_results = run_ast_inference(prep_data if prep_data else file_path, top_k=5)
                    set_state("analysis_results", analysis_results)
                except Exception as e_ast:
                    st.error(f"❌ AST AI Model Inference Failed: {str(e_ast)}")
                    analysis_results = None

        # 4. Run / Cache Module 4 Wildlife Feature Extraction & Classifier
        if not wildlife_results or str(Path(wildlife_results.get("file_path", "")).resolve()) != str(Path(file_path).resolve()):
            with st.spinner("🌿 Extracting Module 4 Acoustic Features & Checking 5-Class Wildlife Model..."):
                try:
                    wildlife_results = run_wildlife_inference(prep_data if prep_data else file_path)
                    set_state("wildlife_results", wildlife_results)
                except Exception as e_w:
                    st.error(f"❌ Module 4 Feature Extraction Failed: {str(e_w)}")
                    wildlife_results = None

        # Compute Ecosystem Health Score (100% UNCHANGED calculation)
        if analysis_results:
            ast_conf_pct = float(analysis_results.get("confidence_pct", 0.0))
            threat_info = analysis_results.get("threat_status", {})
            health_score = max(35, 95 - 35) if threat_info.get("has_threat") else min(98, max(75, int(75 + ast_conf_pct * 0.2)))
        else:
            health_score = 85

        # 5. Top 4 Result KPI Cards
        st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;'>🎯 Primary Analysis Summary</h3>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)

        with r1:
            st.markdown(
                textwrap.dedent(f"""
                <div class="eco-stat-card" style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem; text-align: center;">
                    <div style="font-size: 0.775rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">🌲 Ecosystem Health</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: {'#F87171' if health_score < 70 else '#10B981'}; margin: 0.3rem 0; line-height: 1;">
                        {health_score} <span style="font-size: 1.1rem; color: #94A3B8; font-weight: 600;">/ 100</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8;">Forest Health Index</div>
                </div>
                """).strip(),
                unsafe_allow_html=True
            )

        with r2:
            w_name = wildlife_results.get("predicted_species", "N/A") if wildlife_results else "N/A"
            w_pct = f"{wildlife_results.get('confidence_pct', 0.0):.0f}%" if wildlife_results and wildlife_results.get('confidence_pct') else ""
            st.markdown(
                textwrap.dedent(f"""
                <div class="eco-stat-card" style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem; text-align: center;">
                    <div style="font-size: 0.775rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">🐦 Wildlife Prediction</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #34D399; margin: 0.4rem 0; line-height: 1.2;">
                        {w_name}
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8;">Confidence: <b style="color: #F8FAFC;">{w_pct}</b></div>
                </div>
                """).strip(),
                unsafe_allow_html=True
            )

        with r3:
            ast_name = analysis_results.get("predicted_class", "N/A") if analysis_results else "N/A"
            ast_pct = f"{analysis_results.get('confidence_pct', 0.0):.0f}%" if analysis_results else ""
            st.markdown(
                textwrap.dedent(f"""
                <div class="eco-stat-card" style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem; text-align: center;">
                    <div style="font-size: 0.775rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">🔊 Sound Event (AST)</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #60A5FA; margin: 0.4rem 0; line-height: 1.2;">
                        {ast_name}
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8;">Confidence: <b style="color: #F8FAFC;">{ast_pct}</b></div>
                </div>
                """).strip(),
                unsafe_allow_html=True
            )

        with r4:
            has_threat = analysis_results.get("threat_status", {}).get("has_threat", False) if analysis_results else False
            threat_label = analysis_results.get("threat_status", {}).get("detected_class", "SAFE") if analysis_results else "SAFE"
            st.markdown(
                textwrap.dedent(f"""
                <div class="eco-stat-card" style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem; text-align: center;">
                    <div style="font-size: 0.775rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">⚠️ Threat Status</div>
                    <div style="font-size: 1.2rem; font-weight: 800; color: {'#F87171' if has_threat else '#34D399'}; margin: 0.4rem 0; line-height: 1.2;">
                        {'🔴 ' + threat_label.upper() if has_threat else '🟢 SAFE'}
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8;">
                        {'Anthropogenic Alert' if has_threat else 'Natural Soundscape'}
                    </div>
                </div>
                """).strip(),
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 6. Prominent Mel Spectrogram Section
        if prep_data:
            st.markdown(
                textwrap.dedent("""
                <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem; margin-bottom: 1.5rem;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.25rem;">
                        📊 Acoustic Spectrogram
                    </div>
                    <div style="font-size: 0.825rem; color: #94A3B8; margin-bottom: 1rem;">
                        Real 128-band Log-Mel Spectrogram computed from 16,000 Hz resampled mono audio signal using Librosa.
                    </div>
                """).strip(),
                unsafe_allow_html=True
            )

            try:
                spec_db = prep_data["spectrogram_db"]
                num_frames = spec_db.shape[1]
                n_mels = spec_db.shape[0]

                time_axis = np.linspace(0, prep_data["duration"], num_frames)
                mel_axis = np.arange(1, n_mels + 1)

                fig = px.imshow(
                    spec_db,
                    x=time_axis,
                    y=mel_axis,
                    labels=dict(x="Time (seconds)", y="Mel Frequency Bins (1 - 128)", color="Intensity (dB)"),
                    color_continuous_scale="Viridis",
                    origin="lower",
                    aspect="auto"
                )
                fig.update_layout(
                    margin=dict(l=40, r=40, t=30, b=40),
                    height=320,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", color="#94A3B8")
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e_plot:
                st.warning(f"Could not render Mel Spectrogram plot: {str(e_plot)}")

            st.markdown("</div>", unsafe_allow_html=True)

        # 7. Wildlife Classifier & Probability Distribution Section
        if wildlife_results and wildlife_results.get("model_trained"):
            w_top = wildlife_results.get("top_predictions", [])
            st.markdown(
                textwrap.dedent("""
                <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem; margin-bottom: 1.5rem;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.2rem;">
                        🌿 Wildlife Acoustic Probability Distribution
                    </div>
                    <div style="font-size: 0.825rem; color: #94A3B8; margin-bottom: 1rem;">
                        <i>Model supports five target acoustic classes.</i> Predicted probabilities for bioacoustic soundscape profiles:
                    </div>
                """).strip(),
                unsafe_allow_html=True
            )

            for item in w_top:
                sp_disp = item["species"]
                pct_val = item["pct"]
                st.markdown(
                    textwrap.dedent(f"""
                    <div style="margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.875rem; margin-bottom: 0.25rem;">
                            <span style="font-weight: 600; color: #F8FAFC;">{sp_disp}</span>
                            <span style="font-weight: 700; color: #10B981;">{pct_val:.1f}%</span>
                        </div>
                        <div style="background: #0B1311; border: 1px solid #243630; height: 10px; border-radius: 5px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #059669, #10B981); height: 100%; width: {min(100, max(2, pct_val))}%;"></div>
                        </div>
                    </div>
                    """).strip(),
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        # 8. AST Environmental Sound Classification Section
        if analysis_results:
            top_class = analysis_results["predicted_class"]
            confidence_pct = analysis_results["confidence_pct"]
            threat_info = analysis_results["threat_status"]
            top_5 = analysis_results["top_5_predictions"]

            st.markdown(
                textwrap.dedent(f"""
                <div style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem; margin-bottom: 1.5rem;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.25rem;">
                        🤖 AST Environmental Sound Classification
                    </div>
                    <div style="font-size: 0.825rem; color: #94A3B8; margin-bottom: 1rem;">
                        General AudioSet classification powered by Hugging Face <code>MIT/ast-finetuned-audioset</code>.
                    </div>
                """).strip(),
                unsafe_allow_html=True
            )

            if threat_info["has_threat"]:
                st.markdown(
                    textwrap.dedent(f"""
                    <div style="background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                        <div style="font-weight: 800; color: #F87171; font-size: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                            🚨 Anthropogenic Threat Detected: {threat_info['detected_class']}
                        </div>
                        <div style="font-size: 0.825rem; color: #FCA5A5; margin-top: 0.25rem;">
                            Confidence: {threat_info.get('confidence_pct', 0.0):.1f}% • AST threat signal detected in forest soundscape.
                        </div>
                    </div>
                    """).strip(),
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    textwrap.dedent("""
                    <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                        <div style="font-weight: 800; color: #34D399; font-size: 0.95rem; display: flex; align-items: center; gap: 0.5rem;">
                            🟢 No anthropogenic threat signal detected
                        </div>
                        <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 0.25rem;">
                            *Note: A safe status indicates no strong anthropogenic threat frequencies matched the target classes in this audio window; it does not guarantee total absence of unmonitored human activity.*
                        </div>
                    </div>
                    """).strip(),
                    unsafe_allow_html=True
                )

            st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.6rem;'>Top 5 AudioSet Categories:</div>", unsafe_allow_html=True)
            for item in top_5:
                category_badge = "eco-badge-threat" if item["category"] == "Potential Threat" else "eco-badge-safe" if item["category"] == "Wildlife / Environmental" else "eco-badge-info"
                st.markdown(
                    textwrap.dedent(f"""
                    <div style="background: #0B1311; border: 1px solid #243630; border-radius: 8px; padding: 0.6rem 0.85rem; margin-bottom: 0.4rem; display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 0.6rem;">
                            <span style="font-weight: 600; font-size: 0.875rem; color: #F8FAFC;">{item['class']}</span>
                            <span class="eco-badge {category_badge}">{item['category']}</span>
                        </div>
                        <span style="font-weight: 700; font-size: 0.875rem; color: #10B981;">{item['pct']:.2f}% Score</span>
                    </div>
                    """).strip(),
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        # Footnote
        st.markdown(
            textwrap.dedent("""
            <div style="font-size: 0.775rem; color: #64748B; line-height: 1.5; margin-bottom: 1.5rem; background: #0F1A17; border: 1px solid #243630; padding: 0.85rem 1rem; border-radius: 10px;">
                ℹ️ <b>Ecosystem Acoustic Score (heuristic):</b> This project-specific heuristic metric is derived from the top AudioSet classification confidence and threat status. It is not a scientifically validated ecological health index.
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

        # 9. Persist Real Analysis & Threat Alert to SQLite Database (Task 3 & 11)
        if meta and analysis_results and wildlife_results:
            last_saved_path = get_state("last_saved_db_file_path")
            if last_saved_path != file_path:
                try:
                    from app.services.database_service import save_analysis, save_alert
                    threat_info = analysis_results.get("threat_status", {})
                    ast_conf_pct = float(analysis_results.get("confidence_pct", 0.0))
                    calculated_health_score = max(35, 95 - 35) if threat_info.get("has_threat") else min(98, max(75, int(75 + ast_conf_pct * 0.2)))
                    analysis_db_payload = {
                        "filename": meta.get("filename", "audio.wav"),
                        "duration_sec": meta.get("duration_sec", 0.0),
                        "sample_rate": meta.get("sample_rate_hz", 16000),
                        "channels": meta.get("channels", 1),
                        "ast_top_label": analysis_results.get("predicted_class", "Unknown"),
                        "ast_confidence": round(ast_conf_pct / 100.0, 4),
                        "threat_detected": 1 if threat_info.get("has_threat") else 0,
                        "threat_label": threat_info.get("detected_class", "None"),
                        "threat_confidence": round(float(threat_info.get("confidence_pct", 0.0)) / 100.0, 4),
                        "wildlife_species": wildlife_results.get("predicted_species", "Model File Missing / Untrained"),
                        "wildlife_species_key": wildlife_results.get("raw_species_key", "untrained"),
                        "wildlife_confidence": float(wildlife_results.get("confidence", 0.0)),
                        "health_score": calculated_health_score,
                        "audio_path": file_path
                    }
                    inserted_analysis_id = save_analysis(analysis_db_payload)
                    # Create real alert record if threat is detected
                    if threat_info.get("has_threat"):
                        alert_db_payload = {
                            "analysis_id": inserted_analysis_id,
                            "alert_type": f"Threat Detected: {threat_info.get('detected_class', 'Acoustic Threat')}",
                            "message": f"Acoustic threat '{threat_info.get('detected_class')}' detected with {threat_info.get('confidence_pct', 0.0):.1f}% confidence in soundscape '{meta.get('filename')}'",
                            "confidence": round(float(threat_info.get("confidence_pct", 0.0)) / 100.0, 4),
                            "acknowledged": 0
                        }
                        save_alert(alert_db_payload)
                    set_state("last_saved_db_file_path", file_path)
                except Exception as e_db:
                    st.warning(f"Note: Could not save analysis to local SQLite database: {str(e_db)}")

    else:
        st.markdown(
            textwrap.dedent("""
            <div style="text-align: center; padding: 3rem 1.5rem; background: #14201C; border: 1px solid #243630; border-radius: 14px; margin-bottom: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎧</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #F8FAFC;">No Audio Recording Analyzed Yet</div>
                <div style="font-size: 0.875rem; color: #94A3B8; margin-top: 0.35rem;">
                    Upload a forest recording from the <b>Upload Audio</b> page to view real-time preprocessing, Mel Spectrogram, AST sound classification, and Module 4 Wildlife profiling.
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if primary_button("View & Export Report →", key="btn_save_analysis_report", use_container_width=True):
            navigate_to(PAGE_REPORTS)

    with col_btn2:
        if secondary_button("Analyze Another Audio", key="btn_analyze_another", use_container_width=True):
            navigate_to(PAGE_UPLOAD)
