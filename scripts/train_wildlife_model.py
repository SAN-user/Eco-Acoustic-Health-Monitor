"""
Eco-Acoustic Health Monitor - Wildlife Model Training & Anti-Leakage Evaluation Pipeline
Extracts 46 Librosa acoustic features across 5s windowed segments, performs group-level
(recording_id) anti-leakage train/test splitting, trains a RandomForestClassifier, evaluates
out-of-sample metrics, and serializes payload to ai/models/wildlife_model.joblib.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

import joblib
import librosa
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GroupShuffleSplit

# Fix project python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ai.models.wildlife_model import (
    MODEL_SAVE_PATH,
    extract_acoustic_features,
    load_wildlife_model,
)

DATASET_DIR = BASE_DIR / "dataset"
FEATURE_CSV_PATH = DATASET_DIR / "extracted_features.csv"

# Segmenting hyperparameters
WINDOW_SEC = 5.0
HOP_SEC = 2.5
TARGET_SR = 16000

FEATURE_NAMES = [f"mfcc_mean_{i+1}" for i in range(20)] + \
                [f"mfcc_std_{i+1}" for i in range(20)] + \
                ["spectral_centroid_mean", "spectral_centroid_std",
                 "spectral_bandwidth_mean", "spectral_rolloff_mean",
                 "zero_crossing_rate_mean", "rms_energy_mean"]

EXPECTED_CLASSES = ["asian_koel", "bulbul", "house_crow", "myna", "peacock"]


def validate_and_extract_features() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Task 1 & 2: Validates dataset recordings, segments audio, extracts 46 features,
    and returns a DataFrame with parent recording_id tracking.
    """
    print("=" * 70)
    print("TASK 1 & 2: DATASET REVALIDATION & FEATURE EXTRACTION")
    print("=" * 70)

    if not DATASET_DIR.exists():
        raise FileNotFoundError(f"Dataset directory '{DATASET_DIR}' not found.")

    class_folders = [d for d in DATASET_DIR.iterdir() if d.is_dir() and d.name in EXPECTED_CLASSES]
    if len(class_folders) != 5:
        print(f"Warning: Found {len(class_folders)} class folders, expected 5.")

    validation_stats = {}
    feature_rows = []
    total_valid_recordings = 0
    total_failed_recordings = 0

    window_samples = int(WINDOW_SEC * TARGET_SR)
    hop_samples = int(HOP_SEC * TARGET_SR)

    for folder in sorted(class_folders):
        species_label = folder.name
        audio_files = sorted(list(folder.glob("*.mp3")) + list(folder.glob("*.wav")))
        
        valid_files = 0
        failed_files = 0

        print(f"\nProcessing Species Class: '{species_label}' ({len(audio_files)} audio files)...")

        for file_p in audio_files:
            rec_id = file_p.stem  # e.g., 'XC783988'
            try:
                # Load audio with 16kHz mono resampling
                y, sr = librosa.load(str(file_p), sr=TARGET_SR, mono=True)

                if y is None or len(y) < 2048:
                    print(f"   [!] Skipping '{file_p.name}': Audio signal too short ({len(y) if y is not None else 0} samples).")
                    failed_files += 1
                    continue

                y_norm = librosa.util.normalize(y)
                total_samples = len(y_norm)

                # Segment into 5-second windows (hop = 2.5s)
                if total_samples <= window_samples:
                    # Single segment for short clips
                    segments = [(0, total_samples)]
                else:
                    segments = []
                    start = 0
                    while start + window_samples <= total_samples:
                        segments.append((start, start + window_samples))
                        start += hop_samples

                file_segments_count = 0
                for seg_idx, (start, end) in enumerate(segments):
                    seg_waveform = y_norm[start:end]
                    if len(seg_waveform) < 2048:
                        continue

                    # Extract existing 46-dimensional feature vector
                    feat_vec, _ = extract_acoustic_features(seg_waveform, sr=sr)
                    if len(feat_vec) != 46:
                        continue

                    row = {
                        "recording_id": rec_id,
                        "species": species_label,
                        "filename": file_p.name,
                        "segment_index": seg_idx,
                        "start_sec": round(start / float(sr), 2),
                        "end_sec": round(end / float(sr), 2),
                    }
                    for f_name, f_val in zip(FEATURE_NAMES, feat_vec):
                        row[f_name] = float(f_val)

                    feature_rows.append(row)
                    file_segments_count += 1

                if file_segments_count > 0:
                    valid_files += 1
                else:
                    failed_files += 1

            except Exception as e:
                print(f"   [!] Corrupt or unreadable file '{file_p.name}': {e}")
                failed_files += 1

        validation_stats[species_label] = {
            "total_files": len(audio_files),
            "valid_files": valid_files,
            "failed_files": failed_files,
        }
        total_valid_recordings += valid_files
        total_failed_recordings += failed_files

    df_features = pd.DataFrame(feature_rows)
    df_features.to_csv(FEATURE_CSV_PATH, index=False)

    print("\n" + "-" * 70)
    print(f"[+] Feature Extraction Complete: {len(df_features)} total feature rows extracted.")
    print(f"[+] Extracted features saved to: {FEATURE_CSV_PATH}")
    print("-" * 70)

    summary_report = {
        "validation_stats": validation_stats,
        "total_valid_recordings": total_valid_recordings,
        "total_failed_recordings": total_failed_recordings,
        "total_feature_rows": len(df_features),
    }
    return df_features, summary_report


def run_anti_leakage_training_and_eval(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Task 3 & 4 & 5 & 6 & 8: Executes Recording-Level Anti-Leakage Train/Test split,
    trains 5-class RandomForestClassifier, evaluates on test set, and serializes model.
    """
    print("\n" + "=" * 70)
    print("TASK 3 & 4 & 5 & 6 & 8: ANTI-LEAKAGE SPLIT, 5-CLASS TRAINING & EVALUATION")
    print("=" * 70)

    X = df[FEATURE_NAMES].values.astype(np.float32)
    y = df["species"].values
    groups = df["recording_id"].values

    classes = sorted(list(np.unique(y)))

    # Task 8 Verification: Check for exactly 5 classes including 'myna'
    assert len(classes) == 5, f"CRITICAL ERROR: Expected 5 classes, got {len(classes)} ({classes})"
    assert "myna" in classes, "CRITICAL ERROR: 'myna' is missing from dataset classes!"
    print(f"[+] 5-Class Verification Passed: Trained classes = {classes}")

    # Task 3: Recording-level GroupShuffleSplit (80% train / 20% test, random_state=42)
    gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    train_groups = set(groups[train_idx])
    test_groups = set(groups[test_idx])

    # STRICT ANTI-LEAKAGE ASSERTION
    overlap = train_groups.intersection(test_groups)
    assert len(overlap) == 0, f"CRITICAL DATA LEAKAGE ERROR! Overlapping recording IDs: {overlap}"
    print(f"[+] Strict Anti-Leakage Verification Passed: 0 overlapping recording IDs between train and test.")

    # Calculate per-class recording counts for train and test
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]

    train_recs_per_class = train_df.groupby("species")["recording_id"].nunique().to_dict()
    test_recs_per_class = test_df.groupby("species")["recording_id"].nunique().to_dict()

    train_segs_per_class = train_df.groupby("species").size().to_dict()
    test_segs_per_class = test_df.groupby("species").size().to_dict()

    print("\nRecording and Segment Distribution:")
    print(f"• Train Recordings: {len(train_groups)} | Test Recordings: {len(test_groups)}")
    print(f"• Train Segments:   {len(X_train)} | Test Segments:   {len(X_test)}")
    
    print("\nPer-Class Recording & Segment Split Breakdown:")
    for cls in classes:
        tr_r = train_recs_per_class.get(cls, 0)
        te_r = test_recs_per_class.get(cls, 0)
        tr_s = train_segs_per_class.get(cls, 0)
        te_s = test_segs_per_class.get(cls, 0)
        print(f"  - {cls:<15}: Train = {tr_r} recs ({tr_s} segs) | Test = {te_r} recs ({te_s} segs)")

    # Task 4: Train RandomForestClassifier(n_estimators=100, random_state=42)
    print("\n[*] Training RandomForestClassifier(n_estimators=100, random_state=42) on training set...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    train_pred = clf.predict(X_train)
    train_acc = accuracy_score(y_train, train_pred)

    # Task 5: Evaluate strictly on held-out test set
    test_pred = clf.predict(X_test)
    test_acc = accuracy_score(y_test, test_pred)
    macro_prec = precision_score(y_test, test_pred, average="macro", zero_division=0)
    macro_rec = recall_score(y_test, test_pred, average="macro", zero_division=0)
    macro_f1 = f1_score(y_test, test_pred, average="macro", zero_division=0)

    test_report = classification_report(y_test, test_pred, target_names=classes, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, test_pred, labels=classes)

    print("\n" + "=" * 70)
    print("FINAL 5-CLASS HELD-OUT TEST EVALUATION METRICS")
    print("=" * 70)
    print(f"• Training Set Accuracy (Fit Check): {train_acc * 100:.2f}%")
    print(f"• Test Set Out-of-Sample Accuracy:  {test_acc * 100:.2f}%")
    print(f"• Macro Precision:                   {macro_prec * 100:.2f}%")
    print(f"• Macro Recall:                      {macro_rec * 100:.2f}%")
    print(f"• Macro F1-Score:                    {macro_f1 * 100:.2f}%")

    print("\nPer-Class Metrics on Held-out Test Set:")
    for cls_name in classes:
        metrics = test_report.get(cls_name, {})
        p = metrics.get("precision", 0.0) * 100
        r = metrics.get("recall", 0.0) * 100
        f = metrics.get("f1-score", 0.0) * 100
        s = metrics.get("support", 0)
        print(f"  - {cls_name:<15}: Precision={p:5.2f}%, Recall={r:5.2f}%, F1={f:5.2f}% (Support={s} segments)")

    print("\nConfusion Matrix (Rows: True, Cols: Predicted):")
    print(f"Order: {classes}")
    print(cm)

    # Task 6: Serialize payload to ai/models/wildlife_model.joblib
    payload = {
        "model": clf,
        "classes": classes,
        "num_features": X.shape[1],
        "feature_names": FEATURE_NAMES,
        "train_accuracy": float(train_acc),
        "test_accuracy": float(test_acc),
        "macro_precision": float(macro_prec),
        "macro_recall": float(macro_rec),
        "macro_f1": float(macro_f1),
        "classification_report": test_report,
        "confusion_matrix": cm.tolist(),
        "train_recordings_count": len(train_groups),
        "test_recordings_count": len(test_groups),
        "train_segments_count": len(X_train),
        "test_segments_count": len(X_test),
        "train_recs_per_class": train_recs_per_class,
        "test_recs_per_class": test_recs_per_class,
        "train_segs_per_class": train_segs_per_class,
        "test_segs_per_class": test_segs_per_class,
        "train_recording_ids": list(train_groups),
        "test_recording_ids": list(test_groups),
    }

    MODEL_SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, MODEL_SAVE_PATH)
    print(f"\n[+] Serialized trained 5-class model payload to: {MODEL_SAVE_PATH}")

    return {
        "classes": classes,
        "train_accuracy": train_acc,
        "test_accuracy": test_acc,
        "macro_precision": macro_prec,
        "macro_recall": macro_rec,
        "macro_f1": macro_f1,
        "classification_report": test_report,
        "confusion_matrix": cm.tolist(),
        "train_recordings_count": len(train_groups),
        "test_recordings_count": len(test_groups),
        "train_segments_count": len(X_train),
        "test_segments_count": len(X_test),
        "train_recs_per_class": train_recs_per_class,
        "test_recs_per_class": test_recs_per_class,
        "train_segs_per_class": train_segs_per_class,
        "test_segs_per_class": test_segs_per_class,
        "test_recording_ids": list(test_groups),
    }


def sanity_check_inference(test_recording_ids: List[str]):
    """
    Task 7: Reloads serialized joblib model and runs inference on a held-out test recording.
    """
    print("\n" + "=" * 70)
    print("TASK 7: RE-LOAD MODEL & INFERENCE SANITY TEST")
    print("=" * 70)

    model_payload = load_wildlife_model(MODEL_SAVE_PATH)
    if not model_payload or "model" not in model_payload:
        raise RuntimeError("Failed to load serialized model payload.")

    clf = model_payload["model"]
    classes = model_payload["classes"]
    print(f"[+] Loaded joblib model successfully. Known classes ({len(classes)}): {classes}")

    # Pick first test recording ID from dataset
    test_rec_id = test_recording_ids[0]
    target_file = None
    target_species = None

    for root, _, files in os.walk(DATASET_DIR):
        for f in files:
            if test_rec_id in f and (f.endswith(".mp3") or f.endswith(".wav")):
                target_file = Path(root) / f
                target_species = Path(root).name
                break

    if target_file and target_file.exists():
        print(f"   Held-out test audio file: {target_file.name} (True species: '{target_species}')")
        y, sr = librosa.load(str(target_file), sr=TARGET_SR, mono=True)
        y_norm = librosa.util.normalize(y)

        # Extract 46 features
        feat_vector, readable_metrics = extract_acoustic_features(y_norm, sr=sr)

        # Execute prediction
        probs = clf.predict_proba([feat_vector])[0]
        top_idx = int(np.argmax(probs))
        pred_species = classes[top_idx]
        conf_pct = float(probs[top_idx]) * 100

        print(f"   Model Prediction: '{pred_species}' ({conf_pct:.2f}% Confidence)")
        print(f"   All Class Probabilities: {dict(zip(classes, [round(p, 4) for p in probs]))}")
        print(f"   Extracted Acoustic Profile: Spectral Centroid = {readable_metrics['spectral_centroid_hz']} Hz, RMS = {readable_metrics['rms_energy']:.5f}")
        print("[+] Sanity test inference executed successfully.")
        return {
            "test_file": target_file.name,
            "true_species": target_species,
            "predicted_species": pred_species,
            "confidence_pct": conf_pct,
            "all_probabilities": dict(zip(classes, [round(float(p), 4) for p in probs]))
        }
    else:
        print("   [!] Could not locate test audio file for sanity check.")
        return None


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    # Step 1 & 2: Dataset Revalidation & Feature Extraction
    df_features, summary_report = validate_and_extract_features()

    # Step 3, 4, 5, 6, 8: Anti-leakage Training & 5-Class Evaluation
    eval_results = run_anti_leakage_training_and_eval(df_features)

    # Step 7: Sanity test inference on held-out test recording
    sanity_res = sanity_check_inference(eval_results["test_recording_ids"])

    print("\n" + "=" * 70)
    print("STEP 2B COMPLETE: 5-CLASS WILDLIFE CLASSIFICATION PIPELINE EXECUTED CLEANLY")
    print("=" * 70)


if __name__ == "__main__":
    main()
