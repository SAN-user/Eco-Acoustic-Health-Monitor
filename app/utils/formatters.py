"""
EcoSense AI - Data Formatting Utilities
"""

from datetime import datetime

def format_current_date() -> str:
    """Returns formatted current date e.g. Monday, 03 August 2026."""
    return datetime.now().strftime("%A, %d %B %Y")

def format_percentage(value: float) -> str:
    """Formats float/int to percentage string e.g. 94%."""
    return f"{int(round(value))}%"

def format_file_size(size_bytes: int) -> str:
    """Formats bytes to human readable string (KB, MB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def format_duration(seconds: int) -> str:
    """Formats duration in seconds to MM:SS format."""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def get_health_status(score: int) -> tuple[str, str]:
    """
    Returns (status_text, status_badge_type) based on Forest Health Score.
    """
    if score >= 90:
        return "Healthy", "healthy"
    elif score >= 70:
        return "Moderate Risk", "warning"
    else:
        return "Critical Threat", "critical"
