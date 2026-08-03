"""
EcoSense AI - Configuration & Metadata Constants
"""

import os
from pathlib import Path

# Application Metadata
APP_NAME = "Eco-Acoustic Health Monitor"
APP_SUBTITLE = "Intelligent Forest Soundscape Platform"
APP_TAGLINE = "Intelligent Forest Soundscape Analysis"
APP_VERSION = "1.0.0"
COMPANY_NAME = "Eco-Acoustic Technologies"

# Directory Paths
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
UPLOADS_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"
AI_DIR = BASE_DIR / "ai"

# Create directories if they do not exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Audio Upload Constraints
MAX_AUDIO_SIZE_MB = 100
MAX_AUDIO_DURATION_SEC = 600  # 10 minutes prototype limit
SUPPORTED_AUDIO_FORMATS = ["wav", "mp3"]

# Navigation Page Keys
PAGE_SPLASH = "splash"
PAGE_LOGIN = "login"
PAGE_FORGOT_PASSWORD = "forgot_password"
PAGE_DASHBOARD = "dashboard"
PAGE_UPLOAD = "upload_audio"
PAGE_ANALYSIS = "analysis"
PAGE_FOREST_HEALTH = "forest_health"
PAGE_ALERTS = "alerts"
PAGE_HISTORY = "history"
PAGE_REPORTS = "reports"
PAGE_SETTINGS = "settings"
PAGE_PROFILE = "profile"

# Navigation Items for Sidebar (Icon, Label, Route Key)
SIDEBAR_NAV_ITEMS = [
    {"icon": "🏠", "label": "Dashboard", "key": PAGE_DASHBOARD},
    {"icon": "📤", "label": "Upload Audio", "key": PAGE_UPLOAD},
    {"icon": "📊", "label": "Analysis", "key": PAGE_ANALYSIS},
    {"icon": "🌳", "label": "Forest Health", "key": PAGE_FOREST_HEALTH},
    {"icon": "🔔", "label": "Alerts", "key": PAGE_ALERTS},
    {"icon": "📜", "label": "History", "key": PAGE_HISTORY},
    {"icon": "📄", "label": "Reports", "key": PAGE_REPORTS},
    {"icon": "⚙", "label": "Settings", "key": PAGE_SETTINGS},
    {"icon": "👤", "label": "Profile", "key": PAGE_PROFILE},
]

# User Roles
ROLE_FOREST_OFFICER = "Forest Officer"
ROLE_RESEARCHER = "Wildlife Researcher"
ROLE_ADMIN = "Forest Dept Administrator"
ROLE_ENV_ORG = "Environmental Organization"

# Default Mock User
DEFAULT_USER = {
    "name": "Alex Rivera",
    "email": "alex.rivera@forest.gov.in",
    "role": ROLE_FOREST_OFFICER,
    "organization": "National Forest Conservation Service",
    "avatar": "🌲",
    "last_login": "Today at 08:30 AM"
}
