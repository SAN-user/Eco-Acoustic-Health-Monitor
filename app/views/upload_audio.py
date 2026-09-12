"""
Eco-Acoustic Health Monitor - Upload Audio Screen
Handles file validation, audio persistence, and metadata extraction.
"""

import textwrap
from pathlib import Path
import streamlit as st
from app.components.navigation import render_page_header
from app.components.audio_player import render_audio_player
from app.components.buttons import primary_button, secondary_button
from app.config import (
    SUPPORTED_AUDIO_FORMATS,
    MAX_AUDIO_SIZE_MB,
    MAX_AUDIO_DURATION_SEC,
    PAGE_ANALYSIS,
    UPLOADS_DIR
)
from app.state.router import navigate_to
from app.state.session_state import set_state
from app.services.audio_service import extract_audio_metadata, save_audio_file

def render_upload_audio_page():
    """Renders the audio upload UI page."""
    render_page_header(
        title="Analyze Forest Soundscape",
        subtitle="Upload an audio recording to identify environmental sounds, wildlife activity, and potential anthropogenic threats.",
        breadcrumb="Dashboard / Upload Audio"
    )

    # Visual Workflow Bar
    st.markdown(
        textwrap.dedent("""
        <div style="background: #14201C; border: 1px solid #243630; border-radius: 12px; padding: 0.85rem 1.25rem; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-around; font-size: 0.85rem; font-weight: 700; color: #94A3B8;">
                <div style="color: #10B981; display: flex; align-items: center; gap: 0.4rem;">
                    <span style="background: #10B981; color: #0B1311; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem;">1</span>
                    UPLOAD RECORDING
                </div>
                <div style="color: #64748B;">➔</div>
                <div style="display: flex; align-items: center; gap: 0.4rem;">
                    <span style="background: #243630; color: #94A3B8; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem;">2</span>
                    LIBROSA PREPROCESS
                </div>
                <div style="color: #64748B;">➔</div>
                <div style="display: flex; align-items: center; gap: 0.4rem;">
                    <span style="background: #243630; color: #94A3B8; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem;">3</span>
                    AST & WILDLIFE AI
                </div>
                <div style="color: #64748B;">➔</div>
                <div style="display: flex; align-items: center; gap: 0.4rem;">
                    <span style="background: #243630; color: #94A3B8; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem;">4</span>
                    HEALTH INDEX & SQLITE
                </div>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            textwrap.dedent(f"""
            <div style="background: #14201C; border: 2px dashed #10B981; border-radius: 14px; text-align: center; padding: 2.25rem 1.5rem; margin-bottom: 1rem;">
                <div style="font-size: 2.8rem; margin-bottom: 0.4rem;">📥</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #F8FAFC;">Select or Drag & Drop Forest Audio Files</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 0.35rem;">
                    Supported Formats: <b style="color: #10B981;">WAV • MP3</b> &nbsp;|&nbsp; Max Size: <b>{MAX_AUDIO_SIZE_MB} MB</b> &nbsp;|&nbsp; Max Duration: <b>10 Mins</b>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

        audio_file = st.file_uploader(
            "Choose audio file",
            type=SUPPORTED_AUDIO_FORMATS,
            help="Select a forest soundscape recording to analyze.",
            label_visibility="collapsed"
        )

        if audio_file:
            # 1. Size Validation
            max_size_bytes = MAX_AUDIO_SIZE_MB * 1024 * 1024
            if audio_file.size > max_size_bytes:
                st.error(
                    f"❌ File size ({audio_file.size / (1024*1024):.1f} MB) exceeds "
                    f"maximum allowed limit of {MAX_AUDIO_SIZE_MB} MB."
                )
                return

            # 2. Extension Validation
            ext = Path(audio_file.name).suffix.lower().lstrip(".")
            if ext not in SUPPORTED_AUDIO_FORMATS:
                st.error(f"❌ Unsupported file format '{ext}'. Allowed formats: WAV, MP3.")
                return

            # 3. Real Metadata Extraction
            try:
                metadata = extract_audio_metadata(
                    file_source=audio_file,
                    filename=audio_file.name,
                    file_size_bytes=audio_file.size
                )
            except Exception as e:
                st.error(f"❌ Audio Metadata Extraction Failed: {str(e)}")
                return

            # 4. Duration Validation
            if metadata["duration_sec"] > MAX_AUDIO_DURATION_SEC:
                st.error(
                    f"❌ Audio duration ({metadata['duration_sec']:.2f} seconds) exceeds "
                    f"the maximum allowed limit of {MAX_AUDIO_DURATION_SEC} seconds (10 minutes)."
                )
                return

            st.success(f"✅ Selected `{metadata['filename']}` ({audio_file.size // 1024} KB)")

            # Render Audio Player with real metadata
            render_audio_player(
                filename=metadata["filename"],
                duration_sec=int(round(metadata["duration_sec"])),
                sample_rate_hz=metadata["sample_rate_hz"],
                file_size_bytes=metadata["size_bytes"],
                audio_bytes=audio_file
            )

            c1, c2 = st.columns(2)
            with c1:
                if primary_button("Start AI Analysis →", key="btn_start_analysis", use_container_width=True):
                    try:
                        # Save file to uploads directory safely
                        saved_path = save_audio_file(audio_file, UPLOADS_DIR)
                        metadata["file_path"] = str(saved_path)

                        # Update Session State with full metadata dictionary
                        set_state("uploaded_audio_file", metadata["filename"])
                        set_state("uploaded_audio_metadata", metadata)

                        # Navigate to Analysis screen
                        navigate_to(PAGE_ANALYSIS)
                    except Exception as err:
                        st.error(f"❌ Failed to save uploaded file: {str(err)}")

            with c2:
                if secondary_button("Cancel Upload", key="btn_cancel_upload", use_container_width=True):
                    st.rerun()

    with col2:
        st.markdown(
            textwrap.dedent("""
            <div class="eco-card" style="background: #14201C; border: 1px solid #243630; border-radius: 14px; padding: 1.25rem;">
                <div style="font-weight: 700; font-size: 0.95rem; color: #10B981; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.4rem;">
                    📋 Acoustic Analysis Pipeline
                </div>
                <ul style="font-size: 0.825rem; color: #94A3B8; padding-left: 1.1rem; line-height: 1.6; margin-bottom: 0;">
                    <li style="margin-bottom: 0.4rem;">Audio is resampled to <b>16,000 Hz mono</b> via Librosa.</li>
                    <li style="margin-bottom: 0.4rem;">Computes <b>128-band Log-Mel Spectrogram</b> for AST sound classification.</li>
                    <li style="margin-bottom: 0.4rem;">Extracts <b>46 acoustic features</b> (MFCCs, spectral centroid, roll-off, ZCR, RMS).</li>
                    <li style="margin-bottom: 0.4rem;">Evaluates <b>5-class wildlife Random Forest</b> model.</li>
                    <li style="margin-bottom: 0.4rem;">Computes <b>Ecosystem Health Score</b> & persists results to SQLite.</li>
                </ul>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
