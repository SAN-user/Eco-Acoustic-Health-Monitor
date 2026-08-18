"""
Verification Script for Module 4 (Wildlife Feature Profiling, Model Training Engine, and Ecosystem Assessment)
"""

import sys
import os
import shutil
import math
import struct
import wave
import numpy as np
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai.models.wildlife_model import (
    extract_acoustic_features,
    train_wildlife_model,
    load_wildlife_model
)
from ai.inference.wildlife_classifier import run_wildlife_inference

def create_synthetic_sound_file(filepath: Path, freq: float, duration_sec: float = 1.0, sr: int = 16000):
    """Creates a synthetic single-frequency PCM WAV file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    n_samples = int(duration_sec * sr)
    amplitude = 15000
    with wave.open(str(filepath), 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        frames = bytearray()
        for i in range(n_samples):
            t = float(i) / sr
            val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
            frames.extend(struct.pack('<h', val))
        f.writeframes(frames)

def main():
    print("--- Starting Module 4 Unit & Functional Verification ---")

    # 1. Dataset Audit Check
    dataset_dir = ROOT_DIR / "dataset"
    print(f"Auditing local dataset folder: {dataset_dir}")
    audit_res = train_wildlife_model(dataset_dir)
    print("Audit Result on empty dataset:", audit_res)
    assert audit_res["trained"] == False, "Expected dataset audit trained=False for empty dataset"
    assert audit_res["num_classes"] == 0
    print("✅ Test 1: Empty dataset discovery audit passed.")

    # 2. Test Real Acoustic Feature Extraction on 16kHz Waveform
    dummy_waveform = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 16000)).astype(np.float32)
    feat_vec, metrics = extract_acoustic_features(dummy_waveform, sr=16000)
    print(f"\nExtracted Feature Vector length: {len(feat_vec)}")
    print("Readable Acoustic Metrics:", metrics)
    assert len(feat_vec) == 46, f"Expected 46 features, got {len(feat_vec)}"
    assert metrics["spectral_centroid_hz"] > 0
    assert metrics["spectral_bandwidth_hz"] > 0
    print("✅ Test 2: Librosa acoustic feature extraction passed.")

    # 3. Test Untrained Inference Behavior (Current Dataset State)
    uploads_dir = ROOT_DIR / "uploads"
    upload_files = list(uploads_dir.glob("*.wav")) + list(uploads_dir.glob("*.mp3"))
    if upload_files:
        test_audio = upload_files[0]
    else:
        test_audio = ROOT_DIR / "scratch" / "test_audio" / "stereo_44100hz_test.wav"

    print(f"\nRunning Module 4 inference on active file: {test_audio.name}")
    inf_res = run_wildlife_inference(test_audio)
    print("Inference Output (Untrained State):")
    print(f"  - Model Status: {inf_res['model_status']}")
    print(f"  - Predicted Species: {inf_res['predicted_species']}")
    print(f"  - Spectral Centroid: {inf_res['acoustic_profile']['spectral_centroid_hz']} Hz")
    print(f"  - Spectral Bandwidth: {inf_res['acoustic_profile']['spectral_bandwidth_hz']} Hz")
    assert inf_res["model_trained"] == False
    assert inf_res["predicted_species"] == "Dataset Required"
    print("✅ Test 3: Untrained model fallback & real acoustic profiling passed.")

    # 4. Verify Training & Model Persistence Pipeline using Synthetic Multi-class Data (Isolated in scratch)
    synth_dir = ROOT_DIR / "scratch" / "test_synth_dataset"
    synth_model_path = ROOT_DIR / "scratch" / "synth_model.joblib"
    
    try:
        # Create 2 synthetic classes: 'synth_peacock' (1200Hz) and 'synth_elephant' (300Hz)
        create_synthetic_sound_file(synth_dir / "synth_peacock" / "sample1.wav", freq=1200.0)
        create_synthetic_sound_file(synth_dir / "synth_peacock" / "sample2.wav", freq=1250.0)
        create_synthetic_sound_file(synth_dir / "synth_peacock" / "sample3.wav", freq=1180.0)
        create_synthetic_sound_file(synth_dir / "synth_elephant" / "sample1.wav", freq=300.0)
        create_synthetic_sound_file(synth_dir / "synth_elephant" / "sample2.wav", freq=320.0)
        create_synthetic_sound_file(synth_dir / "synth_elephant" / "sample3.wav", freq=280.0)

        print(f"\nVerifying training pipeline on synthetic multi-class folder: {synth_dir}")
        train_res = train_wildlife_model(synth_dir, model_save_path=synth_model_path)
        print("Training Result:", train_res)
        assert train_res["trained"] == True
        assert train_res["num_classes"] == 2
        assert synth_model_path.exists(), "Model file joblib was not serialized"

        # Verify inference with trained synthetic model
        synth_inf = run_wildlife_inference(test_audio, model_path=synth_model_path)
        print("Inference Result (Trained Synthetic Model):")
        print(f"  - Model Status: {synth_inf['model_status']}")
        print(f"  - Predicted Species: {synth_inf['predicted_species']}")
        print(f"  - Confidence: {synth_inf['confidence_pct']}%")
        assert synth_inf["model_trained"] == True
        assert 0.0 <= synth_inf["confidence"] <= 1.0
        print("✅ Test 4: Model training, serialization, and inference pipeline passed.")

    finally:
        # Clean up scratch test artifacts
        if synth_dir.exists():
            shutil.rmtree(synth_dir, ignore_errors=True)
        if synth_model_path.exists():
            os.remove(synth_model_path)

    # 5. Test Error Handling (Missing audio / single class)
    single_class_dir = ROOT_DIR / "scratch" / "test_single_class"
    try:
        create_synthetic_sound_file(single_class_dir / "single_class" / "sample1.wav", freq=440.0)
        single_res = train_wildlife_model(single_class_dir)
        assert single_res["trained"] == False
        print("  ✅ Single class error handling passed.")
    finally:
        if single_class_dir.exists():
            shutil.rmtree(single_class_dir, ignore_errors=True)

    print("\n🎉 ALL MODULE 4 UNIT AND FUNCTIONAL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
