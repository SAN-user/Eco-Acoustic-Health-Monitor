"""
EcoSense AI - Audio Player Component
Renders a preview audio player with file details.
"""

import streamlit as st
from app.utils.formatters import format_file_size, format_duration

def render_audio_player(filename: str, duration_sec: int, sample_rate_hz: int, file_size_bytes: int, audio_bytes=None):
    """
    Renders an audio preview card with audio waveform player controls.
    """
    st.markdown(
        f"""
        <div class="eco-card" style="padding: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 1.8rem;">🎵</span>
                    <div>
                        <div style="font-weight: 700; font-size: 1rem; color: #0F172A;">{filename}</div>
                        <div style="font-size: 0.8rem; color: #64748B;">
                            Duration: {format_duration(duration_sec)} • Sample Rate: {sample_rate_hz} Hz • Size: {format_file_size(file_size_bytes)}
                        </div>
                    </div>
                </div>
                <span class="eco-badge eco-badge-info">Ready for AI Analysis</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if audio_bytes:
        st.audio(audio_bytes)
    else:
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
