"""
Eco-Acoustic Health Monitor - Upload Audio Screen (Section 3.6 Placeholder UI)
"""

import streamlit as st
from app.components.navigation import render_page_header
from app.components.audio_player import render_audio_player
from app.components.buttons import primary_button, secondary_button
from app.config import SUPPORTED_AUDIO_FORMATS, MAX_AUDIO_SIZE_MB, PAGE_ANALYSIS
from app.state.router import navigate_to
from app.state.session_state import set_state

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
            st.success(f"✅ Selected `{audio_file.name}` ({audio_file.size // 1024} KB)")
            render_audio_player(
                filename=audio_file.name,
                duration_sec=18,
                sample_rate_hz=22050,
                file_size_bytes=audio_file.size,
                audio_bytes=audio_file
            )

            c1, c2 = st.columns(2)
            with c1:
                if primary_button("Start AI Analysis →", key="btn_start_analysis", use_container_width=True):
                    set_state("uploaded_audio_file", audio_file.name)
                    navigate_to(PAGE_ANALYSIS)
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
