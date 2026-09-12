"""
Eco-Acoustic Health Monitor - Wildlife Model Training & Feature Extraction
Provides Librosa acoustic feature extraction, dataset folder discovery,
RandomForest model training, and joblib serialization.
"""

import os
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List, Union
import numpy as np
import librosa
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

MODEL_SAVE_PATH = Path(__file__).resolve().parent / "wildlife_model.joblib"


def extract_acoustic_features(waveform: np.ndarray, sr: int = 16000) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Extracts 46 acoustic features (20 MFCC means, 20 MFCC stds, Spectral Centroid Mean/Std,
    Bandwidth Mean, Rolloff Mean, Zero Crossing Rate Mean, RMS Energy Mean) from a 1D mono waveform.
    
    Args:
        waveform: 1D float32 normalized mono audio signal.
        sr: Sampling rate in Hz (default: 16000).
        
    Returns:
        Tuple[np.ndarray, Dict[str, float]]: Feature vector array and human-readable metrics dict.
    """
    if waveform.ndim != 1 or len(waveform) == 0:
        raise ValueError("Feature extraction requires a non-empty 1D mono waveform.")

    # 1. MFCCs (20 coefficients)
    mfccs = librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=20)
    mfcc_means = np.mean(mfccs, axis=1)
    mfcc_stds = np.std(mfccs, axis=1)

    # 2. Spectral Centroid
    centroid = librosa.feature.spectral_centroid(y=waveform, sr=sr)
    centroid_mean = float(np.mean(centroid))
    centroid_std = float(np.std(centroid))

    # 3. Spectral Bandwidth
    bandwidth = librosa.feature.spectral_bandwidth(y=waveform, sr=sr)
    bandwidth_mean = float(np.mean(bandwidth))

    # 4. Spectral Rolloff
    rolloff = librosa.feature.spectral_rolloff(y=waveform, sr=sr)
    rolloff_mean = float(np.mean(rolloff))

    # 5. Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y=waveform)
    zcr_mean = float(np.mean(zcr))

    # 6. RMS Energy
    rms = librosa.feature.rms(y=waveform)
    rms_mean = float(np.mean(rms))

    # Concatenate into 46-dimensional feature vector
    feature_vector = np.concatenate([
        mfcc_means,
        mfcc_stds,
        [centroid_mean, centroid_std, bandwidth_mean, rolloff_mean, zcr_mean, rms_mean]
    ]).astype(np.float32)

    readable_metrics = {
        "spectral_centroid_hz": round(centroid_mean, 2),
        "spectral_centroid_std": round(centroid_std, 2),
        "spectral_bandwidth_hz": round(bandwidth_mean, 2),
        "spectral_rolloff_hz": round(rolloff_mean, 2),
        "zero_crossing_rate": round(zcr_mean, 5),
        "rms_energy": round(rms_mean, 5),
        "mfcc_base": round(float(mfcc_means[0]), 2)
    }

    return feature_vector, readable_metrics


def train_wildlife_model(
    dataset_dir: Union[str, Path],
    model_save_path: Path = MODEL_SAVE_PATH
) -> Dict[str, Any]:
    """
    Scans dataset_dir for class subfolders, segments audio into 5s windows,
    extracts 46 Librosa features, executes GroupShuffleSplit anti-leakage split by recording_id,
    trains a RandomForestClassifier, and serializes payload to joblib.
    """
    dir_path = Path(dataset_dir).resolve()
    if not dir_path.exists():
        return {
            "trained": False,
            "reason": f"Dataset directory '{dir_path}' does not exist.",
            "num_classes": 0,
            "classes": []
        }

    class_folders = [d for d in dir_path.iterdir() if d.is_dir()]
    feature_rows = []

    window_samples = int(5.0 * 16000)
    hop_samples = int(2.5 * 16000)

    for folder in sorted(class_folders):
        species_label = folder.name
        audio_files = sorted(list(folder.glob("*.wav")) + list(folder.glob("*.mp3")))

        for file_p in audio_files:
            rec_id = file_p.stem
            try:
                y, sr = librosa.load(str(file_p), sr=16000, mono=True)
                if y is None or len(y) < 2048:
                    continue

                y_norm = librosa.util.normalize(y)
                total_samples = len(y_norm)

                if total_samples <= window_samples:
                    segments = [(0, total_samples)]
                else:
                    segments = []
                    start = 0
                    while start + window_samples <= total_samples:
                        segments.append((start, start + window_samples))
                        start += hop_samples

                for start_sample, end_sample in segments:
                    seg_w = y_norm[start_sample:end_sample]
                    if len(seg_w) < 2048:
                        continue
                    feat, _ = extract_acoustic_features(seg_w, sr=sr)
                    if len(feat) == 46:
                        feature_rows.append({
                            "recording_id": rec_id,
                            "species": species_label,
                            "features": feat
                        })
            except Exception:
                continue

    num_classes = len(set(r["species"] for r in feature_rows))
    num_recordings = len(set(r["recording_id"] for r in feature_rows))

    if num_classes < 2 or num_recordings < 4:
        return {
            "trained": False,
            "reason": f"Insufficient dataset classes. Found {num_classes} classes and {num_recordings} unique recordings. Multi-class wildlife classification requires at least 2 labeled species folders with audio samples.",
            "num_classes": num_classes,
            "classes": list(set(r["species"] for r in feature_rows)),
            "num_samples": len(feature_rows)
        }

    X = np.array([r["features"] for r in feature_rows], dtype=np.float32)
    y = np.array([r["species"] for r in feature_rows])
    groups = np.array([r["recording_id"] for r in feature_rows])

    # Anti-leakage GroupShuffleSplit by recording_id
    from sklearn.model_selection import GroupShuffleSplit
    gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    train_acc = float(accuracy_score(y_train, clf.predict(X_train)))
    test_acc = float(accuracy_score(y_test, clf.predict(X_test)))

    payload = {
        "model": clf,
        "classes": list(clf.classes_),
        "num_features": X.shape[1],
        "train_accuracy": train_acc,
        "test_accuracy": test_acc
    }

    model_save_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, model_save_path)

    return {
        "trained": True,
        "model_path": str(model_save_path),
        "num_classes": num_classes,
        "classes": list(clf.classes_),
        "num_samples": len(feature_rows),
        "train_accuracy_pct": round(train_acc * 100, 2),
        "test_accuracy_pct": round(test_acc * 100, 2)
    }


def load_wildlife_model(model_path: Path = MODEL_SAVE_PATH) -> Optional[Dict[str, Any]]:
    """Loads saved wildlife classification model payload if available."""
    path = Path(model_path).resolve()
    if not path.exists():
        return None
    try:
        return joblib.load(path)
    except Exception:
        return None
