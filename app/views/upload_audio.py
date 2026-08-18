"""
Eco-Acoustic Health Monitor - Upload Audio Screen
Handles file validation, audio persistence, and metadata extraction.
"""

from pathlib import Path
import streamlit as st
from app.components.navigation import render_page_header
from app.components.audio_player import render_audio_player
from app.components.buttons import primary_button, secondary_button
from app.config import (
    SUPPORTED_AUDIO_FORMATS,
    MAX_AUDIO_SIZE_MB,
    PAGE_ANALYSIS,
    UPLOADS_DIR
)
from app.state.router import navigate_to
from app.state.session_state import set_state
from app.services.audio_service import extract_audio_metadata, save_audio_file

def render_upload_audio_page():
    """Renders the audio upload UI page."""
    render_page_header(
        title="Upload Forest Audio Recording",
        subtitle="Select or drag and drop WAV or MP3 audio recordings collected from acoustic sensors.",
        breadcrumb="Dashboard / Upload Audio"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            f"""
            <div class="eco-card" style="border: 2px dashed #4CAF50; text-align: center; padding: 2.5rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">📥</div>
                <div style="font-weight: 700; font-size: 1.1rem;">Drag & Drop Forest Audio Files</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.25rem;">
                    Supported Formats: <b>WAV, MP3</b> • Max File Size: <b>{MAX_AUDIO_SIZE_MB} MB</b>
                </div>
            </div>
            """,
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
            """
            <div class="eco-card">
                <div style="font-weight: 700; font-size: 1rem; color: #1E4D2B; margin-bottom: 0.5rem;">📋 Upload Guidelines</div>
                <ul style="font-size: 0.85rem; color: #64748B; padding-left: 1.2rem; line-height: 1.6;">
                    <li>Ensure clear acoustic quality without excessive wind clipping.</li>
                    <li>Audio recordings should be mono or stereo at 16kHz-44.1kHz.</li>
                    <li>Files up to 10 minutes will be processed through AST AI pipeline.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
