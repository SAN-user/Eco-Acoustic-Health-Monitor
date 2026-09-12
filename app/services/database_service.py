"""
Eco-Acoustic Health Monitor - SQLite Database Service
Provides persistent storage for audio analysis records, AST classifications,
threat detections, Module 4 wildlife predictions, and real-time alerts.
"""

import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_DIR = BASE_DIR / "data"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "eco_acoustic.db"


def get_db_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Establishes a connection to the SQLite database with row factory enabled."""
    target_path = Path(db_path) if db_path else DEFAULT_DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_database(db_path: Optional[Path] = None) -> bool:
    """
    Initializes the SQLite database schema if not already present.
    Safe to call multiple times on startup.
    """
    conn = get_db_connection(db_path)
    try:
        with conn:
            # 1. Create analyses table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    filename TEXT,
                    duration_sec REAL,
                    sample_rate INTEGER,
                    channels INTEGER,
                    ast_top_label TEXT,
                    ast_confidence REAL,
                    threat_detected INTEGER,
                    threat_label TEXT,
                    threat_confidence REAL,
                    wildlife_species TEXT,
                    wildlife_species_key TEXT,
                    wildlife_confidence REAL,
                    health_score INTEGER,
                    audio_path TEXT
                );
            """)
            
            # 2. Create alerts table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_id INTEGER,
                    timestamp TEXT NOT NULL,
                    alert_type TEXT,
                    message TEXT,
                    confidence REAL,
                    acknowledged INTEGER DEFAULT 0,
                    FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
                );
            """)
        return True
    finally:
        conn.close()


def save_analysis(analysis_data: Dict[str, Any], db_path: Optional[Path] = None) -> int:
    """
    Saves a real analysis result to the SQLite analyses table.
    Returns the newly inserted analysis ID.
    """
    conn = get_db_connection(db_path)
    try:
        ts = analysis_data.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with conn:
            cursor = conn.execute("""
                INSERT INTO analyses (
                    timestamp, filename, duration_sec, sample_rate, channels,
                    ast_top_label, ast_confidence, threat_detected, threat_label,
                    threat_confidence, wildlife_species, wildlife_species_key,
                    wildlife_confidence, health_score, audio_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                ts,
                analysis_data.get("filename"),
                analysis_data.get("duration_sec", 0.0),
                analysis_data.get("sample_rate", 16000),
                analysis_data.get("channels", 1),
                analysis_data.get("ast_top_label", "Unknown"),
                analysis_data.get("ast_confidence", 0.0),
                1 if analysis_data.get("threat_detected") else 0,
                analysis_data.get("threat_label", "None"),
                analysis_data.get("threat_confidence", 0.0),
                analysis_data.get("wildlife_species", "Dataset Required"),
                analysis_data.get("wildlife_species_key", "untrained"),
                analysis_data.get("wildlife_confidence", 0.0),
                analysis_data.get("health_score", 85),
                analysis_data.get("audio_path", "")
            ))
            return cursor.lastrowid
    finally:
        conn.close()


def save_alert(alert_data: Dict[str, Any], db_path: Optional[Path] = None) -> int:
    """
    Saves a real threat alert record linked to an analysis.
    Returns the inserted alert ID.
    """
    conn = get_db_connection(db_path)
    try:
        ts = alert_data.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with conn:
            cursor = conn.execute("""
                INSERT INTO alerts (
                    analysis_id, timestamp, alert_type, message, confidence, acknowledged
                ) VALUES (?, ?, ?, ?, ?, ?);
            """, (
                alert_data.get("analysis_id"),
                ts,
                alert_data.get("alert_type", "Threat Alert"),
                alert_data.get("message", "Potential acoustic threat detected."),
                alert_data.get("confidence", 0.0),
                1 if alert_data.get("acknowledged") else 0
            ))
            return cursor.lastrowid
    finally:
        conn.close()


def toggle_alert_acknowledgement(alert_id: int, db_path: Optional[Path] = None) -> bool:
    """Toggles the acknowledgement status of an alert."""
    conn = get_db_connection(db_path)
    try:
        with conn:
            cursor = conn.execute("SELECT acknowledged FROM alerts WHERE id = ?;", (alert_id,))
            row = cursor.fetchone()
            if not row:
                return False
            new_status = 0 if row["acknowledged"] == 1 else 1
            conn.execute("UPDATE alerts SET acknowledged = ? WHERE id = ?;", (new_status, alert_id))
            return True
    finally:
        conn.close()


def get_recent_analyses(limit: int = 50, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Retrieves recent analysis records sorted by newest first."""
    conn = get_db_connection(db_path)
    try:
        cursor = conn.execute("""
            SELECT * FROM analyses ORDER BY id DESC LIMIT ?;
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_all_alerts(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Retrieves all stored alerts joined with parent analysis info."""
    conn = get_db_connection(db_path)
    try:
        cursor = conn.execute("""
            SELECT 
                a.id AS alert_id,
                a.analysis_id,
                a.timestamp,
                a.alert_type,
                a.message,
                a.confidence,
                a.acknowledged,
                an.filename,
                an.health_score,
                an.audio_path
            FROM alerts a
            LEFT JOIN analyses an ON a.analysis_id = an.id
            ORDER BY a.id DESC;
        """)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_dashboard_stats(db_path: Optional[Path] = None) -> Dict[str, Any]:
    """Calculates real dashboard summary statistics from SQLite."""
    conn = get_db_connection(db_path)
    try:
        # Total analyses
        c_an = conn.execute("SELECT COUNT(*) AS cnt FROM analyses;").fetchone()
        total_analyses = c_an["cnt"] if c_an else 0

        # Total threats
        c_th = conn.execute("SELECT COUNT(*) AS cnt FROM analyses WHERE threat_detected = 1;").fetchone()
        total_threats = c_th["cnt"] if c_th else 0

        # Latest analysis
        c_latest = conn.execute("""
            SELECT health_score, wildlife_species, timestamp, filename
            FROM analyses ORDER BY id DESC LIMIT 1;
        """).fetchone()

        latest_health_score = c_latest["health_score"] if c_latest else None
        latest_wildlife = c_latest["wildlife_species"] if c_latest else None
        latest_filename = c_latest["filename"] if c_latest else None

        # Total alerts & unacknowledged
        c_al = conn.execute("SELECT COUNT(*) AS cnt FROM alerts;").fetchone()
        total_alerts = c_al["cnt"] if c_al else 0

        c_unack = conn.execute("SELECT COUNT(*) AS cnt FROM alerts WHERE acknowledged = 0;").fetchone()
        unack_alerts = c_unack["cnt"] if c_unack else 0

        return {
            "total_analyses": total_analyses,
            "total_threats": total_threats,
            "latest_health_score": latest_health_score,
            "latest_wildlife_species": latest_wildlife,
            "latest_filename": latest_filename,
            "total_alerts": total_alerts,
            "unacknowledged_alerts": unack_alerts
        }
    finally:
        conn.close()
