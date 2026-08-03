"""
Phase 1 Automated Verification Script
Tests importability and execution of all Eco-Acoustic Health Monitor components and views.
"""

import sys
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

def test_imports():
    print("Testing core imports...")
    import app.config as config
    assert config.APP_NAME == "Eco-Acoustic Health Monitor"
    print("  [OK] app.config")

    import app.styles.theme as theme
    import app.styles.style_loader as style_loader
    print("  [OK] app.styles")

    import app.state.session_state as session_state
    import app.state.router as router
    print("  [OK] app.state")

    import app.utils.formatters as formatters
    import app.utils.mock_data as mock_data
    print("  [OK] app.utils")

    import app.components.buttons as buttons
    import app.components.cards as cards
    import app.components.inputs as inputs
    import app.components.charts as charts
    import app.components.meters as meters
    import app.components.timeline as timeline
    import app.components.navigation as navigation
    import app.components.status_chips as status_chips
    import app.components.alert_box as alert_box
    import app.components.audio_player as audio_player
    import app.components.skeleton as skeleton
    import app.components.dialogs as dialogs
    print("  [OK] app.components (all 12 reusable UI modules)")

    import app.views.splash as splash
    import app.views.login as login
    import app.views.forgot_password as forgot_password
    import app.views.dashboard as dashboard
    import app.views.upload_audio as upload_audio
    import app.views.analysis as analysis
    import app.views.forest_health as forest_health
    import app.views.alerts as alerts
    import app.views.history as history
    import app.views.reports as reports
    import app.views.settings as settings
    import app.views.profile as profile
    print("  [OK] app.views (all 12 screen views)")

    import app.main as main_entry
    print("  [OK] app.main entrypoint")

    print("\n[SUCCESS] All imports, views, and navigation components resolved with 0 errors!")

if __name__ == "__main__":
    test_imports()
