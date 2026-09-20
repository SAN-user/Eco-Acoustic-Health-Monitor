"""
ESP32 Sensor Audio Service

Detects newly transferred ESP32 WAV recordings
inside the application's uploads directory.
"""

from pathlib import Path
from typing import Optional, Tuple

from app.config import UPLOADS_DIR
from app.services.audio_service import extract_audio_metadata


SENSOR_PREFIX = "esp32_"
SENSOR_EXTENSION = ".wav"


def find_latest_sensor_audio() -> Optional[Path]:
    """
    Finds the newest ESP32-generated WAV file.
    """

    uploads_dir = Path(UPLOADS_DIR)

    if not uploads_dir.exists():
        return None

    sensor_files = list(
        uploads_dir.glob(f"{SENSOR_PREFIX}*{SENSOR_EXTENSION}")
    )

    if not sensor_files:
        return None

    return max(
        sensor_files,
        key=lambda path: path.stat().st_mtime
    )


def get_sensor_audio_metadata(
    audio_path: Path
) -> dict:
    """
    Extract metadata from an ESP32 sensor WAV file.
    """

    return extract_audio_metadata(
        file_source=audio_path,
        filename=audio_path.name,
        file_size_bytes=audio_path.stat().st_size
    )


def get_latest_sensor_recording() -> Optional[Tuple[Path, dict]]:
    """
    Returns the latest ESP32 recording and its metadata.

    Returns:
        (audio_path, metadata)
        or None if no sensor recording exists.
    """

    audio_path = find_latest_sensor_audio()

    if audio_path is None:
        return None

    metadata = get_sensor_audio_metadata(audio_path)

    return audio_path, metadata