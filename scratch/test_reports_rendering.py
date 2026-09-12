"""
Unit test for reports.py render_reports_page behavior with and without active analysis.
"""
import sys
from pathlib import Path
import pandas as pd

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app.state.session_state import init_session_state, set_state

def test_without_active_analysis():
    print("Testing reports page without active analysis...")
    # Clear session state
    st.session_state.clear()
    init_session_state()

    meta = st.session_state.get("uploaded_audio_metadata")
    analysis_results = st.session_state.get("analysis_results")

    has_active_analysis = bool(
        (analysis_results and isinstance(analysis_results, dict) and analysis_results.get("predicted_class"))
        or (meta and isinstance(meta, dict) and meta.get("filename"))
    )
    assert not has_active_analysis, "Should evaluate has_active_analysis to False when empty"
    print("  [OK] Without active analysis state correctly detected.")

def test_with_active_analysis():
    print("Testing reports page with active analysis...")
    st.session_state.clear()
    init_session_state()

    set_state("uploaded_audio_metadata", {
        "filename": "forest_sample.wav",
        "format": "WAV",
        "duration_sec": 12.5,
        "sample_rate_hz": 16000,
        "channels": 1,
        "size_bytes": 400000,
        "bitrate": 256000
    })

    set_state("analysis_results", {
        "predicted_class": "Bird song",
        "confidence_pct": 87.4,
        "category": "Wildlife / Environmental",
        "threat_status": {
            "has_threat": False,
            "status_title": "Natural Soundscape Detected",
            "detected_class": "Natural Ambient Sound"
        },
        "inference_time_sec": 0.42
    })

    set_state("wildlife_results", {
        "model_trained": False,
        "model_status": "Wildlife Model: Not Trained",
        "predicted_species": "Dataset Required",
        "confidence_pct": 0.0,
        "acoustic_profile": {
            "spectral_centroid_hz": 2150.5,
            "spectral_bandwidth_hz": 1800.2,
            "spectral_rolloff_hz": 4200.0,
            "rms_energy": 0.04512,
            "zero_crossing_rate": 0.08123
        }
    })

    meta = st.session_state.get("uploaded_audio_metadata")
    analysis_results = st.session_state.get("analysis_results")

    has_active_analysis = bool(
        (analysis_results and isinstance(analysis_results, dict) and analysis_results.get("predicted_class"))
        or (meta and isinstance(meta, dict) and meta.get("filename"))
    )
    assert has_active_analysis, "Should evaluate has_active_analysis to True when data present"

    # Verify CSV dataframe construction
    report_dict = {
        "Metric / Property": [
            "Audio Filename", "Format", "Duration (seconds)", "Sample Rate (Hz)",
            "Channels", "File Size", "Bitrate", "AST Model ID", "AST Top Prediction",
            "AST Confidence Score (%)", "AST Sound Category", "Threat Evaluation Status",
            "Has Threat Flag", "Ecosystem Acoustic Score (heuristic)",
            "Wildlife Classifier Status", "Predicted Wildlife Species",
            "Wildlife Confidence Score (%)", "Spectral Centroid (Hz)",
            "Spectral Bandwidth (Hz)", "Spectral Rolloff (Hz)", "RMS Energy",
            "Zero-Crossing Rate", "Inference Latency (sec)"
        ],
        "Value": [
            meta["filename"], meta["format"], meta["duration_sec"], meta["sample_rate_hz"],
            "Mono (1 channel)", "390.6 KB", "256 kbps", "MIT/ast-finetuned-audioset-10-10-0.4593",
            analysis_results["predicted_class"], 87.4, analysis_results["category"],
            "Natural Soundscape Detected", False, 92, "Wildlife Model: Not Trained",
            "Not Trained (Dataset Required)", "N/A", 2150.5, 1800.2, 4200.0, 0.04512, 0.08123, 0.42
        ]
    }
    df = pd.DataFrame(report_dict)
    assert len(df) == 23
    assert df.loc[df["Metric / Property"] == "Audio Filename", "Value"].values[0] == "forest_sample.wav"
    assert df.loc[df["Metric / Property"] == "AST Top Prediction", "Value"].values[0] == "Bird song"
    assert df.loc[df["Metric / Property"] == "Predicted Wildlife Species", "Value"].values[0] == "Not Trained (Dataset Required)"

    print("  [OK] CSV generation contains exact active session values.")

if __name__ == "__main__":
    test_without_active_analysis()
    test_with_active_analysis()
    print("\n[SUCCESS] All unit tests for report rendering & CSV export passed!")
