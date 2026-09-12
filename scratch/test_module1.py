"""
Verification Script for Module 1 (Audio Service, File Saving, and Metadata Extraction)
"""

import sys
import struct
import math
import wave
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.audio_service import (
    sanitize_filename,
    get_unique_filepath,
    save_audio_file,
    extract_audio_metadata
)

def create_synthetic_wav(filepath: Path, duration_sec: float = 3.5, sample_rate: int = 44100, channels: int = 1):
    """Creates a valid PCM WAV audio file with a 440 Hz sine wave tone."""
    n_samples = int(duration_sec * sample_rate)
    amplitude = 16000 # 16-bit audio
    frequency = 440.0
    
    with wave.open(str(filepath), 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2) # 2 bytes = 16-bit
        wav_file.setframerate(sample_rate)
        
        frames = bytearray()
        for i in range(n_samples):
            t = float(i) / sample_rate
            value = int(amplitude * math.sin(2.0 * math.pi * frequency * t))
            sample_bytes = struct.pack('<h', value)
            frames.extend(sample_bytes * channels)
            
        wav_file.writeframes(frames)

class MockUploadedFile:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._data = data
        self.size = len(data)
        
    def getbuffer(self):
        return self._data
        
    def getvalue(self):
        return self._data

def main():
    print("--- Starting Module 1 Unit & Functional Verification ---")
    
    # 1. Test filename sanitization
    test_names = [
        ("../../etc/passwd", "passwd"),
        ("../test sound file.WAV", "test_sound_file.wav"),
        ("forest-recording#1!.mp3", "forest-recording_1_.mp3")
    ]
    for raw, expected_contains in test_names:
        sanitized = sanitize_filename(raw)
        print(f"Sanitized '{raw}' -> '{sanitized}'")
        assert expected_contains.lower() in sanitized.lower(), f"Sanitization failed for {raw}"
    print("✅ Filename sanitization passed.")

    # 2. Create synthetic WAV file
    test_dir = ROOT_DIR / "scratch" / "test_audio"
    test_dir.mkdir(parents=True, exist_ok=True)
    
    wav_path = test_dir / "sample_44100_stereo.wav"
    create_synthetic_wav(wav_path, duration_sec=4.0, sample_rate=44100, channels=2)
    print(f"Generated synthetic WAV file: {wav_path} (Size: {wav_path.stat().st_size} bytes)")
    
    # 3. Test Metadata Extraction on WAV Path
    meta_wav = extract_audio_metadata(wav_path)
    print("Extracted WAV Metadata:", meta_wav)
    assert meta_wav["format"] == "WAV", f"Expected WAV, got {meta_wav['format']}"
    assert meta_wav["sample_rate_hz"] == 44100, f"Expected 44100 Hz, got {meta_wav['sample_rate_hz']}"
    assert meta_wav["channels"] == 2, f"Expected 2 channels, got {meta_wav['channels']}"
    assert abs(meta_wav["duration_sec"] - 4.0) < 0.1, f"Expected ~4.0s, got {meta_wav['duration_sec']}"
    print("✅ WAV Metadata extraction passed.")

    # 4. Test File Persistence via save_audio_file
    with open(wav_path, "rb") as f:
        mock_file = MockUploadedFile("forest_sensor_alpha.wav", f.read())
        
    uploads_dir = ROOT_DIR / "uploads"
    saved_path = save_audio_file(mock_file, uploads_dir)
    print(f"Saved audio file to: {saved_path}")
    assert saved_path.exists(), "Saved file does not exist on disk"
    assert "forest_sensor_alpha" in saved_path.name, f"Unexpected filename: {saved_path.name}"
    print("✅ File persistence & safe saving passed.")

    # 5. Test Unique Filepath Collision Prevention
    saved_path_2 = save_audio_file(mock_file, uploads_dir)
    print(f"Saved duplicate audio file to: {saved_path_2}")
    assert saved_path_2.name != saved_path.name, "Duplicate file overwrote previous file!"
    import re
    assert re.search(r"_\d+\.wav$", saved_path_2.name), "Collision counter suffix not added!"
    print("✅ Unique filepath collision prevention passed.")

    # 6. Test Error Handling (Invalid extension, empty file, corrupt content)
    try:
        extract_audio_metadata(b"", filename="empty.wav")
        assert False, "Should have raised ValueError for empty file"
    except ValueError as e:
        print(f"✅ Empty file validation caught: {e}")

    try:
        extract_audio_metadata(b"INVALID DATA", filename="corrupt.wav")
        assert False, "Should have raised ValueError for corrupt WAV data"
    except ValueError as e:
        print(f"✅ Corrupt WAV validation caught: {e}")

    try:
        extract_audio_metadata(b"INVALID DATA", filename="test.txt")
        assert False, "Should have raised ValueError for unsupported format"
    except ValueError as e:
        print(f"✅ Unsupported format validation caught: {e}")

    print("\n🎉 ALL MODULE 1 UNIT AND ERROR HANDLING TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
