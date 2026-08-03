"""
EcoSense AI - Structured Mock Datasets for Frontend Prototyping
"""

import pandas as pd

def get_dashboard_stats():
    """Returns top metric cards data as specified in prompt PRD Section 3.5."""
    return {
        "health_score": 94,
        "health_status": "Healthy",
        "species_detected": 28,
        "species_change": "+4 this week",
        "threats_today": 2,
        "threats_status": "1 High Priority",
        "total_analyses": 156,
        "analyses_change": "+12 today"
    }

def get_recent_activity():
    """Returns recent acoustic detection activity timeline."""
    return [
        {
            "id": 1,
            "icon": "🦜",
            "title": "Indian Peacock Detected",
            "type": "Species",
            "time": "09:15 AM",
            "confidence": 96,
            "status": "healthy"
        },
        {
            "id": 2,
            "icon": "⚠",
            "title": "Chainsaw Operation Detected",
            "type": "Threat",
            "time": "10:22 AM",
            "confidence": 91,
            "status": "critical"
        },
        {
            "id": 3,
            "icon": "🐦",
            "title": "Asian Koel Detected",
            "type": "Species",
            "time": "11:04 AM",
            "confidence": 94,
            "status": "healthy"
        },
        {
            "id": 4,
            "icon": "🐘",
            "title": "Indian Elephant Trumpet Identified",
            "type": "Species",
            "time": "01:30 PM",
            "confidence": 98,
            "status": "healthy"
        },
        {
            "id": 5,
            "icon": "🚨",
            "title": "Gunshot Sound Detected",
            "type": "Threat",
            "time": "02:15 PM",
            "confidence": 88,
            "status": "critical"
        }
    ]

def get_weekly_health_trend():
    """Returns 7-day Forest Health score trend DataFrame."""
    return pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Health Score (%)": [91, 93, 89, 94, 92, 95, 94],
        "Target Baseline": [90, 90, 90, 90, 90, 90, 90]
    })

def get_species_frequency():
    """Returns species detection count distribution DataFrame."""
    return pd.DataFrame({
        "Species": ["Indian Peacock", "Asian Koel", "Malabar Squirrel", "Great Hornbill", "Indian Elephant"],
        "Detections": [42, 38, 29, 21, 15]
    })

def get_threat_trend():
    """Returns threat detections trend DataFrame."""
    return pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Chainsaws": [0, 1, 0, 2, 1, 0, 1],
        "Gunshots": [0, 0, 1, 0, 0, 1, 1],
        "Vehicles": [1, 2, 0, 1, 3, 1, 0]
    })

def get_active_alerts():
    """Returns list of environmental threat alerts."""
    return [
        {
            "id": "ALT-101",
            "type": "Chainsaw",
            "zone": "Zone A - Sector 4",
            "priority": "High Priority",
            "severity": "High",
            "time": "10:32 AM",
            "reviewed": False,
            "confidence": "91%"
        },
        {
            "id": "ALT-102",
            "type": "Gunshot",
            "zone": "Zone C - Sector 12",
            "priority": "Critical",
            "severity": "Critical",
            "time": "02:15 PM",
            "reviewed": False,
            "confidence": "88%"
        },
        {
            "id": "ALT-103",
            "type": "Heavy Vehicle",
            "zone": "Zone B - Perimeter Road",
            "priority": "Medium Priority",
            "severity": "Medium",
            "time": "Yesterday",
            "reviewed": True,
            "confidence": "85%"
        }
    ]

def get_history_records():
    """Returns analysis history records DataFrame."""
    return pd.DataFrame([
        {
            "Date": "2026-08-03 10:22",
            "Audio Name": "forest_recording_sectorA.wav",
            "Species": "Indian Peacock",
            "Threat": "Chainsaw Detected",
            "Health Score": "89%",
            "Status": "Alert Flagged"
        },
        {
            "Date": "2026-08-03 09:15",
            "Audio Name": "morning_birds_sectorB.wav",
            "Species": "Asian Koel",
            "Threat": "None",
            "Health Score": "96%",
            "Status": "Normal"
        },
        {
            "Date": "2026-08-02 16:40",
            "Audio Name": "river_bank_soundscape.wav",
            "Species": "Great Hornbill",
            "Threat": "None",
            "Health Score": "95%",
            "Status": "Normal"
        },
        {
            "Date": "2026-08-02 14:10",
            "Audio Name": "perimeter_check_02.mp3",
            "Species": "Malabar Squirrel",
            "Threat": "Heavy Vehicle",
            "Health Score": "91%",
            "Status": "Reviewed"
        }
    ])
