"""
Eco-Acoustic AI Preprocessing Package
Provides Librosa-based audio loading, 16kHz resampling, mono conversion,
peak normalization, and Mel Spectrogram generation.
"""

from ai.preprocessing.audio_preprocessor import (
    load_and_resample,
    convert_to_mono,
    normalize_audio,
    generate_mel_spectrogram,
    preprocess_audio_pipeline,
    DEFAULT_TARGET_SR,
    DEFAULT_N_FFT,
    DEFAULT_HOP_LENGTH,
    DEFAULT_N_MELS
)

__all__ = [
    "load_and_resample",
    "convert_to_mono",
    "normalize_audio",
    "generate_mel_spectrogram",
    "preprocess_audio_pipeline",
    "DEFAULT_TARGET_SR",
    "DEFAULT_N_FFT",
    "DEFAULT_HOP_LENGTH",
    "DEFAULT_N_MELS"
]
