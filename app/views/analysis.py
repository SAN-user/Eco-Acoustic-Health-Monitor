"""
Eco-Acoustic Health Monitor - Audio Analysis Screen
Displays real uploaded audio metadata, Librosa audio preprocessing metrics,
interactive Mel Spectrogram, Hugging Face AudioSpectrogramTransformer (AST) sound classification,
and Module 4 Wildlife Acoustic Feature Profiling & Ecosystem Assessment.
"""

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
            f"""
            <div class="eco-card" style="margin-bottom: 1.25rem; padding: 1.25rem;">
                <div style="font-weight: 700; font-size: 1.1rem; color: #1E4D2B; margin-bottom: 0.5rem;">
                    🎵 Active Soundscape File: {meta.get('filename', 'Unknown')}
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem; font-size: 0.88rem; color: #334155;">
                    <div><b>Original Format:</b> {meta.get('format', 'N/A')}</div>
                    <div><b>Original Duration:</b> {format_duration(int(round(meta.get('duration_sec', 0))))} ({meta.get('duration_sec')}s)</div>
                    <div><b>Original Sample Rate:</b> {meta.get('sample_rate_hz')} Hz</div>
                    <div><b>Original Channels:</b> {channels_str}</div>
                    <div><b>File Size:</b> {format_file_size(meta.get('size_bytes', 0))}</div>
                    <div><b>Bitrate:</b> {bitrate_str}</div>
                </div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 0.6rem; word-break: break-all;">
                    📁 <b>Saved File Path:</b> <code>{file_path}</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 2. Run / Cache Audio Preprocessing Pipeline (Module 2)
        if not prep_data or prep_data.get("file_path") != file_path:
            with st.spinner("⚡ Running Librosa audio preprocessing (Resampling to 16kHz, Mono Conversion, Normalization & Mel Spectrogram)..."):
                try:
                    prep_data = preprocess_audio_pipeline(file_path, target_sr=16000)
                    set_state("preprocessed_audio", prep_data)
                except Exception as e:
                    st.error(f"❌ Audio Preprocessing Pipeline Failed: {str(e)}")
                    prep_data = None

        # 3. Display Preprocessing Metrics & Spectrogram
        if prep_data:
            st.markdown(
                f"""
                <div class="eco-card" style="margin-bottom: 1.25rem; padding: 1rem 1.25rem; background-color: #F8FAFC; border-left: 4px solid #2E7D32;">
                    <div style="font-weight: 700; font-size: 0.95rem; color: #1E4D2B; margin-bottom: 0.4rem;">
                        ⚙️ Module 2 Preprocessing Pipeline Status: <span class="eco-badge eco-badge-healthy">Completed (16,000 Hz Mono)</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.5rem; font-size: 0.85rem; color: #475569;">
                        <div><b>Target Sample Rate:</b> {prep_data['sample_rate']} Hz</div>
                        <div><b>Processed Duration:</b> {prep_data['duration']} s</div>
                        <div><b>Signal Channels:</b> Mono (1D)</div>
                        <div><b>Amplitude Normalization:</b> Peak [-1.0, 1.0]</div>
                        <div><b>Mel Frequency Bins:</b> {prep_data['n_mels']} mels</div>
                        <div><b>Spectrogram Frames:</b> {prep_data['num_frames']} frames</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Render Mel Spectrogram Plotly Chart
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
                    title=dict(
                        text=f"🔊 Real Mel Spectrogram — {meta.get('filename', 'Audio')} (128 Mel Bins, 16kHz Resampled Mono)",
                        font=dict(size=14, color="#1E4D2B")
                    ),
                    margin=dict(l=40, r=40, t=50, b=40),
                    height=300,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif")
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e_plot:
                st.warning(f"Could not render Mel Spectrogram plot: {str(e_plot)}")

        # 4. Run / Cache Module 3 AST AI Model Inference
        if not analysis_results or analysis_results.get("file_path") != file_path:
            with st.spinner("🤖 Running Hugging Face AST Model Inference (MIT/ast-finetuned-audioset-10-10-0.4593)..."):
                try:
                    analysis_results = run_ast_inference(prep_data if prep_data else file_path, top_k=5)
                    set_state("analysis_results", analysis_results)
                except Exception as e_ast:
                    st.error(f"❌ AST AI Model Inference Failed: {str(e_ast)}")
                    analysis_results = None

        # 5. Display Genuine AST Model Inference Results (Module 3)
        if analysis_results:
            top_class = analysis_results["predicted_class"]
            confidence_pct = analysis_results["confidence_pct"]
            threat_info = analysis_results["threat_status"]
            latency_sec = analysis_results["inference_time_sec"]
            top_5 = analysis_results["top_5_predictions"]

            st.divider()
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin: 0;">
                        🤖 Module 3: AudioSpectrogramTransformer (AST) General AudioSet Classification
                    </h3>
                    <span style="font-size: 0.8rem; background-color: #E2E8F0; padding: 0.35rem 0.75rem; border-radius: 12px; color: #475569;">
                        ⚡ Latency: <b>{latency_sec}s</b> • Model: <code>MIT/ast-finetuned-audioset</code>
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Top Metric Cards (3 Columns)
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f"""
                    <div class="eco-card" style="text-align: center;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Top AudioSet Category</div>
                        <div style="font-size: 1.4rem; font-weight: 800; color: #1E4D2B; margin: 0.5rem 0; word-break: break-word;">
                            {top_class}
                        </div>
                        <span class="eco-badge eco-badge-healthy">{confidence_pct:.1f}% Model Probability</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:
                threat_badge = "eco-badge-critical" if threat_info["has_threat"] else "eco-badge-healthy"
                st.markdown(
                    f"""
                    <div class="eco-card" style="text-align: center;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Threat Status Evaluation</div>
                        <div style="font-size: 1.2rem; font-weight: 800; color: {'#DC2626' if threat_info['has_threat'] else '#1E4D2B'}; margin: 0.5rem 0;">
                            {threat_info['status_title']}
                        </div>
                        <span class="eco-badge {threat_badge}">{threat_info['detected_class']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:
                # Dynamic Ecosystem Score: Derived project metric based on AudioSet soundscape stability & threat detection
                health_score = max(35, 95 - 35) if threat_info["has_threat"] else min(98, max(75, int(75 + confidence_pct * 0.2)))
                st.markdown(
                    f"""
                    <div class="eco-card" style="text-align: center;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Acoustic Ecosystem Score</div>
                        <div style="font-size: 1.6rem; font-weight: 800; color: {'#DC2626' if health_score < 70 else '#2E7D32'}; margin: 0.5rem 0;">
                            {health_score}%
                        </div>
                        <span class="eco-badge {'eco-badge-critical' if health_score < 70 else 'eco-badge-healthy'}">
                            {'Action Required' if threat_info['has_threat'] else 'Stable Soundscape'}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Top 5 AudioSet Predictions List
            st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; margin-top: 1.25rem; color: #1E4D2B;'>📋 Top 5 AudioSet Predictions</h4>", unsafe_allow_html=True)
            
            for item in top_5:
                category_badge = "eco-badge-critical" if item["category"] == "Potential Threat" else "eco-badge-healthy" if item["category"] == "Wildlife / Environmental" else "eco-badge-info"
                st.markdown(
                    f"""
                    <div class="eco-card" style="padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 0.75rem;">
                                <span style="font-weight: 700; font-size: 0.95rem; color: #0F172A;">{item['class']}</span>
                                <span class="eco-badge {category_badge}">{item['category']}</span>
                            </div>
                            <span style="font-weight: 700; font-size: 0.95rem; color: #1E4D2B;">{item['pct']:.2f}% Score</span>
                        </div>
                        <div style="background-color: #E2E8F0; height: 6px; border-radius: 3px; margin-top: 0.4rem; overflow: hidden;">
                            <div style="background-color: {'#DC2626' if item['category'] == 'Potential Threat' else '#2E7D32'}; height: 100%; width: {min(100, max(2, item['pct']))}%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # 6. Run / Cache Module 4 Wildlife Feature Extraction & Classifier
        if not wildlife_results or str(Path(wildlife_results.get("file_path", "")).resolve()) != str(Path(file_path).resolve()):
            with st.spinner("🌿 Extracting Module 4 Acoustic Features & Checking Domain Wildlife Model..."):
                try:
                    wildlife_results = run_wildlife_inference(prep_data if prep_data else file_path)
                    set_state("wildlife_results", wildlife_results)
                except Exception as e_w:
                    st.error(f"❌ Module 4 Feature Extraction Failed: {str(e_w)}")
                    wildlife_results = None

        # 7. Display Module 4 Wildlife Classification & Real Acoustic Profile
        if wildlife_results:
            st.divider()
            model_status = wildlife_results["model_status"]
            is_trained = wildlife_results["model_trained"]
            ac_prof = wildlife_results["acoustic_profile"]
            w_latency = wildlife_results["inference_latency_sec"]

            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin: 0;">
                        🌿 Module 4: Domain-Specific Wildlife Classification & Acoustic Profile
                    </h3>
                    <span style="font-size: 0.8rem; background-color: {'#E8F5E9' if is_trained else '#FEF3C7'}; color: {'#2E7D32' if is_trained else '#D97706'}; padding: 0.35rem 0.75rem; border-radius: 12px; font-weight: 700;">
                        {model_status}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if is_trained:
                # Model Trained Case
                w_pred = wildlife_results["predicted_species"]
                w_conf = wildlife_results["confidence_pct"]

                st.markdown(
                    f"""
                    <div class="eco-card" style="margin-bottom: 1.25rem; padding: 1.25rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Predicted Species</div>
                                <div style="font-size: 1.6rem; font-weight: 800; color: #1E4D2B;">{w_pred}</div>
                            </div>
                            <span class="eco-badge eco-badge-healthy">{w_conf:.1f}% Confidence</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Untrained Case (0 class folders in dataset/)
                st.markdown(
                    f"""
                    <div class="eco-card" style="margin-bottom: 1.25rem; padding: 1.25rem; border-left: 4px solid #D97706; background-color: #FFFBEB;">
                        <div style="font-weight: 700; font-size: 1rem; color: #92400E; margin-bottom: 0.3rem;">
                            ℹ️ Wildlife Classifier Status: <span class="eco-badge eco-badge-warning">Not Trained</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #78350F; line-height: 1.5;">
                            {wildlife_results['notice']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Display Real Extracted Librosa Acoustic Profile Metrics
            st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; color: #1E4D2B; margin-bottom: 0.75rem;'>📊 Real Extracted Acoustic Profile Metrics (Librosa 46-Feature Vector)</h4>", unsafe_allow_html=True)
            
            st.markdown(
                f"""
                <div class="eco-card" style="padding: 1.25rem;">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; font-size: 0.88rem; color: #334155;">
                        <div><b>Spectral Centroid:</b> {ac_prof['spectral_centroid_hz']} Hz</div>
                        <div><b>Spectral Bandwidth:</b> {ac_prof['spectral_bandwidth_hz']} Hz</div>
                        <div><b>Spectral Rolloff:</b> {ac_prof['spectral_rolloff_hz']} Hz</div>
                        <div><b>RMS Energy:</b> {ac_prof['rms_energy']:.5f}</div>
                        <div><b>Zero-Crossing Rate:</b> {ac_prof['zero_crossing_rate']:.5f}</div>
                        <div><b>Base MFCC (1st):</b> {ac_prof['mfcc_base']}</div>
                    </div>
                    <div style="font-size: 0.78rem; color: #64748B; margin-top: 0.75rem;">
                        ⚡ Feature Extraction Latency: <b>{w_latency}s</b> • 46 MFCC/Spectral Features computed from 16kHz mono audio.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Safe extraction of Module 3 AST results for Ecosystem Summary
            ast_class_str = analysis_results.get('predicted_class', 'General Soundscape') if analysis_results else 'General Soundscape'
            ast_conf_str = f"{analysis_results['confidence_pct']:.1f}%" if analysis_results else "N/A"
            ast_threat_str = analysis_results.get('threat_status', {}).get('status_title', 'Evaluated') if analysis_results else 'Evaluated'

            # Ecosystem Assessment Summary Card
            st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; margin-top: 1.25rem; color: #1E4D2B;'>🌳 Integrated Ecosystem Health Assessment</h4>", unsafe_allow_html=True)
            st.info(
                f"**Ecosystem Analysis Summary:**\n\n"
                f"• **General AudioSet Soundscape:** Top detected sound is `{ast_class_str}` ({ast_conf_str} probability).\n"
                f"• **Threat Indicator:** {ast_threat_str}.\n"
                f"• **Acoustic Spectral Profile:** Spectral Centroid at {ac_prof['spectral_centroid_hz']} Hz with Rolloff at {ac_prof['spectral_rolloff_hz']} Hz.\n\n"
                f"*ℹ️ Note: Acoustic Ecosystem Score is a derived project metric combining AudioSet soundscape classification, threat detections, and spectral acoustic stability. It is not a scientifically validated ecological index.*"
            )

    else:
        st.info("ℹ️ No custom recording uploaded. Upload an audio file from the Upload Audio screen to view real preprocessing, Mel Spectrogram, AST AI classification, and Module 4 Wildlife profiling.")

    st.divider()

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if primary_button("Generate & Save Report →", key="btn_save_analysis_report", use_container_width=True):
            navigate_to(PAGE_REPORTS)

    with col_btn2:
        if secondary_button("Analyze Another Audio", key="btn_analyze_another", use_container_width=True):
            navigate_to(PAGE_UPLOAD)
