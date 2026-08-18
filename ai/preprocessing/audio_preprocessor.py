"""
Eco-Acoustic Health Monitor - Audio Preprocessing Engine
Handles loading, resampling (16kHz), mono conversion, peak normalization,
and Mel Spectrogram generation using Librosa.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Union
import numpy as np
import librosa

# Default Signal Processing Hyperparameters
DEFAULT_TARGET_SR = 16000  # Hz
DEFAULT_N_FFT = 2048       # FFT window size
DEFAULT_HOP_LENGTH = 512   # Frame hop size
DEFAULT_N_MELS = 128       # Mel frequency bands

def load_and_resample(file_path: Union[str, Path], target_sr: int = DEFAULT_TARGET_SR) -> Tuple[np.ndarray, int]:
    """
    Loads an audio file and resamples it to target_sr.
    
    Args:
        file_path: Path to the input audio file.
        target_sr: Desired sampling rate in Hz (default: 16000 Hz).
        
    Returns:
        Tuple[np.ndarray, int]: Audio signal array and target sample rate.
    """
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Audio file does not exist at: {path}")
        
    try:
        # Load audio with librosa preserving multi-channel initially to detect stereo/mono
        signal, sr = librosa.load(str(path), sr=target_sr, mono=False)
    except Exception as e:
        raise ValueError(f"Failed to load/decode audio file '{path.name}': {str(e)}")
        
    if signal is None or signal.size == 0:
        raise ValueError(f"Loaded audio signal from '{path.name}' is empty (0 samples).")
        
    return signal, sr


def convert_to_mono(signal: np.ndarray) -> np.ndarray:
    """
    Converts multi-channel (stereo) audio signal to a single 1D mono channel array.
    
    Args:
        signal: Audio array (1D for mono, 2D for multi-channel).
        
    Returns:
        np.ndarray: 1D float32 mono signal array.
    """
    if signal.ndim == 1:
        return signal.astype(np.float32)
        
    # Convert multi-channel to mono
    mono_signal = librosa.to_mono(signal)
    return mono_signal.astype(np.float32)


def normalize_audio(signal: np.ndarray) -> np.ndarray:
    """
    Normalizes audio signal to peak amplitude range [-1.0, 1.0].
    
    Args:
        signal: 1D float32 audio signal array.
        
    Returns:
        np.ndarray: Normalized 1D float32 signal array.
    """
    if signal.size == 0:
        return signal
        
    # Librosa utility for peak normalization
    norm_signal = librosa.util.normalize(signal)
    return norm_signal.astype(np.float32)


def generate_mel_spectrogram(
    signal: np.ndarray,
    sr: int = DEFAULT_TARGET_SR,
    n_fft: int = DEFAULT_N_FFT,
    hop_length: int = DEFAULT_HOP_LENGTH,
    n_mels: int = DEFAULT_N_MELS
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates Mel Spectrogram and converts power to log-scale decibels (dB).
    
    Args:
        signal: 1D normalized mono audio signal.
        sr: Sample rate in Hz.
        n_fft: FFT window length.
        hop_length: Hop length between frames.
        n_mels: Number of Mel frequency bins.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: (raw_mel_spectrogram, spectrogram_db)
    """
    if signal.ndim != 1:
        raise ValueError("Mel Spectrogram generation requires a 1D mono audio signal.")
        
    if len(signal) < n_fft:
        raise ValueError(
            f"Audio signal is too short ({len(signal)} samples) for N_FFT window size of {n_fft}. "
            f"Minimum required duration is {n_fft / sr:.3f} seconds."
        )

    # Calculate Mel Spectrogram
    mel_spec = librosa.feature.melspectrogram(
        y=signal,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels
    )
    
    # Convert power spectrogram to dB scale
    spectrogram_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    return mel_spec, spectrogram_db


def preprocess_audio_pipeline(
    file_path: Union[str, Path],
    target_sr: int = DEFAULT_TARGET_SR,
    n_fft: int = DEFAULT_N_FFT,
    hop_length: int = DEFAULT_HOP_LENGTH,
    n_mels: int = DEFAULT_N_MELS
) -> Dict[str, Any]:
    """
    Executes the complete audio preprocessing pipeline:
      load -> resample (16kHz) -> convert to mono -> normalize -> generate Mel spectrogram (dB)
      
    Args:
        file_path: Path to the input audio file.
        target_sr: Target sample rate in Hz (default: 16000 Hz).
        n_fft: FFT window size (default: 2048).
        hop_length: Frame hop size (default: 512).
        n_mels: Number of Mel frequency bins (default: 128).
        
    Returns:
        Dict containing preprocessed audio tensors, metadata, and spectrogram matrix.
    """
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Missing audio file at: {path}")

    # 1. Load and Resample to 16,000 Hz
    raw_signal, sr = load_and_resample(path, target_sr=target_sr)
    
    # Track initial channels for metadata report
    initial_channels = 1 if raw_signal.ndim == 1 else raw_signal.shape[0]

    # 2. Convert to Mono
    mono_signal = convert_to_mono(raw_signal)

    # 3. Peak Normalization
    normalized_signal = normalize_audio(mono_signal)

    # 4. Generate Mel Spectrogram (Power & dB)
    mel_spec, spec_db = generate_mel_spectrogram(
        signal=normalized_signal,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels
    )

    duration_sec = len(normalized_signal) / float(sr)

    return {
        "file_path": str(path),
        "filename": path.name,
        "waveform": normalized_signal,
        "sample_rate": sr,
        "duration": round(duration_sec, 2),
        "initial_channels": initial_channels,
        "is_mono": True,
        "mel_spectrogram": mel_spec,
        "spectrogram_db": spec_db,
        "n_mels": n_mels,
        "n_fft": n_fft,
        "hop_length": hop_length,
        "num_frames": spec_db.shape[1]
    }
