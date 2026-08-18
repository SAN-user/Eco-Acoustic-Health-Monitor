"""
Eco-Acoustic Health Monitor - Audio Service
Provides safe audio file persistence and metadata extraction for WAV and MP3 files.
"""

import io
import os
import re
import wave
from pathlib import Path
from typing import Dict, Any, Union, Optional
import mutagen

# Supported Audio Formats
SUPPORTED_EXTENSIONS = {".wav", ".mp3"}

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a filename to prevent path traversal and shell injection vulnerabilities.
    Only allows alphanumeric characters, underscores, hyphens, and dots.
    """
    # Extract only the base name (strip any folder paths)
    base_name = os.path.basename(filename)
    
    # Strip dangerous characters
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', base_name)
    
    # Ensure extension is intact and lowercase
    ext = Path(safe_name).suffix.lower()
    name_without_ext = Path(safe_name).stem
    
    if not name_without_ext or name_without_ext == "_":
        name_without_ext = "audio_recording"
        
    return f"{name_without_ext}{ext}"


def get_unique_filepath(target_dir: Path, safe_filename: str) -> Path:
    """
    Generates a non-conflicting filepath in target_dir by appending incremental counter if needed.
    """
    target_dir = Path(target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = target_dir / safe_filename
    
    # Prevent path traversal outside target_dir
    try:
        resolved = file_path.resolve()
        if not str(resolved).startswith(str(target_dir)):
            raise ValueError("Path traversal attempt detected.")
    except Exception as e:
        raise ValueError(f"Invalid target file path: {e}")
        
    if not file_path.exists():
        return file_path
        
    stem = file_path.stem
    ext = file_path.suffix
    counter = 1
    
    while True:
        candidate = target_dir / f"{stem}_{counter}{ext}"
        if not candidate.exists():
            return candidate
        counter += 1


def save_audio_file(uploaded_file, target_dir: Path) -> Path:
    """
    Saves an uploaded file safely to the specified target directory.
    
    Args:
        uploaded_file: Streamlit UploadedFile or file-like object with .name and .getbuffer()/.read()
        target_dir: Path to directory where file should be saved
        
    Returns:
        Path: Absolute path to the saved file
    """
    if not uploaded_file:
        raise ValueError("No audio file provided.")
        
    raw_name = getattr(uploaded_file, "name", "uploaded_audio.wav")
    safe_name = sanitize_filename(raw_name)
    
    ext = Path(safe_name).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported audio format '{ext}'. Allowed formats: WAV, MP3.")
        
    save_path = get_unique_filepath(target_dir, safe_name)
    
    try:
        # Get bytes from UploadedFile or file object
        if hasattr(uploaded_file, "getbuffer"):
            content = uploaded_file.getbuffer()
        elif hasattr(uploaded_file, "getvalue"):
            content = uploaded_file.getvalue()
        elif hasattr(uploaded_file, "read"):
            uploaded_file.seek(0)
            content = uploaded_file.read()
            uploaded_file.seek(0)
        else:
            raise ValueError("Invalid file object structure.")
            
        with open(save_path, "wb") as f:
            f.write(content)
            
        return save_path
    except Exception as e:
        raise IOError(f"Failed to save audio file to disk: {str(e)}")


def extract_audio_metadata(
    file_source: Union[bytes, io.BytesIO, Path, str, Any],
    filename: Optional[str] = None,
    file_size_bytes: Optional[int] = None
) -> Dict[str, Any]:
    """
    Extracts audio metadata (format, duration, sample rate, channels, bitrate, size) from WAV or MP3 files.
    
    Args:
        file_source: File path, BytesIO, UploadedFile, or raw bytes
        filename: Optional override filename
        file_size_bytes: Optional override size in bytes
        
    Returns:
        Dict containing extracted audio metadata keys.
    """
    # Resolve filename & size
    if hasattr(file_source, "name") and not filename:
        filename = file_source.name
    elif isinstance(file_source, (str, Path)) and not filename:
        filename = Path(file_source).name
    elif not filename:
        filename = "recording.wav"
        
    safe_name = sanitize_filename(filename)
    ext = Path(safe_name).suffix.lower()
    audio_format = ext.lstrip(".").upper()
    
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported audio extension '{ext}'. Only WAV and MP3 are supported.")

    # Get file content in BytesIO or Path
    file_bytes: Optional[bytes] = None
    saved_path_str: Optional[str] = None
    
    if isinstance(file_source, (str, Path)):
        file_path = Path(file_source)
        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found at: {file_path}")
        saved_path_str = str(file_path.resolve())
        file_size_bytes = file_size_bytes or file_path.stat().st_size
        with open(file_path, "rb") as f:
            file_bytes = f.read()
    elif hasattr(file_source, "getvalue"):
        file_bytes = file_source.getvalue()
        file_size_bytes = file_size_bytes or len(file_bytes)
    elif hasattr(file_source, "getbuffer"):
        file_bytes = bytes(file_source.getbuffer())
        file_size_bytes = file_size_bytes or len(file_bytes)
    elif isinstance(file_source, bytes):
        file_bytes = file_source
        file_size_bytes = file_size_bytes or len(file_bytes)
    elif hasattr(file_source, "read"):
        file_source.seek(0)
        file_bytes = file_source.read()
        file_source.seek(0)
        file_size_bytes = file_size_bytes or len(file_bytes)
    else:
        raise ValueError("Unrecognized audio file source.")

    if not file_bytes or len(file_bytes) == 0:
        raise ValueError("Audio file is empty (0 bytes).")

    duration_sec: float = 0.0
    sample_rate_hz: int = 0
    channels: int = 1
    bitrate: Optional[int] = None

    # Extraction Logic for WAV
    if ext == ".wav":
        try:
            wav_buffer = io.BytesIO(file_bytes)
            with wave.open(wav_buffer, "rb") as wav_file:
                channels = wav_file.getnchannels()
                sample_rate_hz = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                sampwidth = wav_file.getsampwidth()
                
                if sample_rate_hz > 0:
                    duration_sec = n_frames / float(sample_rate_hz)
                if sample_rate_hz > 0 and channels > 0:
                    bitrate = int(sample_rate_hz * channels * sampwidth * 8)
        except Exception as e_wav:
            # Fallback to mutagen if standard wave parser fails (e.g. non-PCM header)
            try:
                mutagen_file = mutagen.File(io.BytesIO(file_bytes))
                if mutagen_file and mutagen_file.info:
                    duration_sec = getattr(mutagen_file.info, "length", 0.0)
                    sample_rate_hz = getattr(mutagen_file.info, "sample_rate", 0)
                    channels = getattr(mutagen_file.info, "channels", 1)
                    bitrate = getattr(mutagen_file.info, "bitrate", None)
                else:
                    raise ValueError(f"Corrupt or invalid WAV audio file: {e_wav}")
            except Exception as e_mut:
                raise ValueError(f"Could not parse WAV audio file: {e_wav} | mutagen: {e_mut}")

    # Extraction Logic for MP3
    elif ext == ".mp3":
        try:
            mutagen_file = mutagen.File(io.BytesIO(file_bytes))
            if mutagen_file is None or not hasattr(mutagen_file, "info") or mutagen_file.info is None:
                raise ValueError("Mutagen could not parse MP3 audio header.")
                
            info = mutagen_file.info
            duration_sec = float(getattr(info, "length", 0.0))
            sample_rate_hz = int(getattr(info, "sample_rate", 0))
            channels = int(getattr(info, "channels", 1))
            bitrate = getattr(info, "bitrate", None)
            if bitrate is not None:
                bitrate = int(bitrate)
        except Exception as e_mp3:
            raise ValueError(f"Could not parse MP3 metadata: {e_mp3}")

    if duration_sec <= 0:
        raise ValueError("Unable to determine audio duration. File may be corrupted.")

    return {
        "filename": safe_name,
        "file_path": saved_path_str,
        "format": audio_format,
        "size_bytes": file_size_bytes or len(file_bytes),
        "duration_sec": round(duration_sec, 2),
        "sample_rate_hz": sample_rate_hz,
        "channels": channels,
        "bitrate": bitrate
    }
