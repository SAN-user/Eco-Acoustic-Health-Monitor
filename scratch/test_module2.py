"""
Verification Script for Module 2 (Audio Preprocessing & Mel Spectrogram Pipeline)
"""

import sys
import math
import struct
import wave
from pathlib import Path
import numpy as np

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai.preprocessing.audio_preprocessor import (
    load_and_resample,
    convert_to_mono,
    normalize_audio,
    generate_mel_spectrogram,
    preprocess_audio_pipeline
)

def create_test_wav(filepath: Path, duration_sec: float = 3.0, sample_rate: int = 44100, channels: int = 2):
    """Generates a stereo test WAV file with a dual frequency tone."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    n_samples = int(duration_sec * sample_rate)
    amplitude = 15000
    
    with wave.open(str(filepath), 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        frames = bytearray()
        for i in range(n_samples):
            t = float(i) / sample_rate
            # Channel 1: 440Hz, Channel 2: 880Hz
            ch1 = int(amplitude * math.sin(2.0 * math.pi * 440.0 * t))
            ch2 = int(amplitude * math.sin(2.0 * math.pi * 880.0 * t))
            frames.extend(struct.pack('<hh', ch1, ch2))
            
        wav_file.writeframes(frames)

def main():
    print("--- Starting Module 2 Unit & Functional Verification ---")

    # 1. Create Test WAV File
    test_dir = ROOT_DIR / "scratch" / "test_audio"
    wav_path = test_dir / "stereo_44100hz_test.wav"
    create_test_wav(wav_path, duration_sec=3.0, sample_rate=44100, channels=2)
    print(f"Generated test WAV file: {wav_path}")

    # 2. Test Step-by-Step Preprocessing Functions
    # Step A: Load & Resample
    raw_sig, sr = load_and_resample(wav_path, target_sr=16000)
    print(f"Loaded signal shape: {raw_sig.shape}, Sample Rate: {sr} Hz")
    assert sr == 16000, f"Expected 16000 Hz target sample rate, got {sr}"
    assert raw_sig.shape[0] == 2, "Expected stereo signal (2 channels)"

    # Step B: Convert to Mono
    mono_sig = convert_to_mono(raw_sig)
    print(f"Mono signal shape: {mono_sig.shape}")
    assert mono_sig.ndim == 1, "Expected 1D mono array"
    assert len(mono_sig) == raw_sig.shape[1], "Sample count mismatch after mono conversion"

    # Step C: Normalize Audio
    norm_sig = normalize_audio(mono_sig)
    print(f"Normalized signal range: min={norm_sig.min():.3f}, max={norm_sig.max():.3f}")
    assert abs(norm_sig.max()) <= 1.0, "Signal peak exceeds 1.0"
    assert norm_sig.dtype == np.float32, "Expected float32 dtype"

    # Step D: Mel Spectrogram Generation
    mel_spec, spec_db = generate_mel_spectrogram(norm_sig, sr=16000, n_fft=2048, hop_length=512, n_mels=128)
    print(f"Mel Spectrogram shape: {mel_spec.shape}, dB Spectrogram shape: {spec_db.shape}")
    assert mel_spec.shape[0] == 128, f"Expected 128 Mel frequency bins, got {mel_spec.shape[0]}"
    assert spec_db.shape == mel_spec.shape, "Power and dB spectrogram shape mismatch"
    assert not np.isnan(spec_db).any(), "Spectrogram contains NaN values"
    print("✅ Step-by-step audio preprocessor functions passed.")

    # 3. Test Full Pipeline Execution
    prep_res = preprocess_audio_pipeline(wav_path, target_sr=16000)
    print("\nFull Pipeline Output Summary:")
    print(f"  - Filename: {prep_res['filename']}")
    print(f"  - Sample Rate: {prep_res['sample_rate']} Hz")
    print(f"  - Duration: {prep_res['duration']} s")
    print(f"  - Initial Channels: {prep_res['initial_channels']} -> Is Mono: {prep_res['is_mono']}")
    print(f"  - Waveform length: {len(prep_res['waveform'])} samples")
    print(f"  - Spectrogram dB shape: {prep_res['spectrogram_db'].shape} (Mels: {prep_res['n_mels']}, Frames: {prep_res['num_frames']})")
    
    assert prep_res["sample_rate"] == 16000
    assert prep_res["n_mels"] == 128
    assert prep_res["n_fft"] == 2048
    assert prep_res["hop_length"] == 512
    assert abs(prep_res["duration"] - 3.0) < 0.1
    print("✅ Full preprocessing pipeline test passed.")

    # 4. Test with Real Files in uploads/ if existing
    uploads_dir = ROOT_DIR / "uploads"
    if uploads_dir.exists():
        upload_files = list(uploads_dir.glob("*.wav")) + list(uploads_dir.glob("*.mp3"))
        if upload_files:
            real_file = upload_files[0]
            print(f"\nTesting pipeline on real uploaded file: {real_file.name}")
            real_res = preprocess_audio_pipeline(real_file)
            print(f"  - Sample Rate: {real_res['sample_rate']} Hz")
            print(f"  - Spectrogram shape: {real_res['spectrogram_db'].shape}")
            assert real_res["sample_rate"] == 16000
            assert real_res["spectrogram_db"].shape[0] == 128
            print(f"✅ Real upload preprocessing passed for '{real_file.name}'.")

    # 5. Error Handling Tests
    print("\nTesting Pipeline Error Handling:")
    # Missing File
    try:
        preprocess_audio_pipeline(ROOT_DIR / "non_existent.wav")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        print(f"  ✅ Missing file caught: {e}")

    # Short audio file (< n_fft=2048 samples)
    tiny_wav = test_dir / "tiny.wav"
    create_test_wav(tiny_wav, duration_sec=0.02, sample_rate=16000, channels=1) # ~320 samples
    try:
        preprocess_audio_pipeline(tiny_wav)
        assert False, "Should have raised ValueError for audio clip too short"
    except ValueError as e:
        print(f"  ✅ Short audio file error caught: {e}")

    print("\n🎉 ALL MODULE 2 TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
