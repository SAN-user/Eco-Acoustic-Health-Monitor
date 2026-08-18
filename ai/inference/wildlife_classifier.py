"""
Eco-Acoustic Health Monitor - Wildlife Classifier & Ecosystem Assessment Engine
Performs real Librosa acoustic feature extraction, executes wildlife species prediction if a trained model exists,
or returns transparent real acoustic profiles when the model is untrained.
"""

import time
from pathlib import Path
from typing import Dict, Any, Union, Optional
import numpy as np

from ai.preprocessing import preprocess_audio_pipeline
from ai.models.wildlife_model import extract_acoustic_features, load_wildlife_model, MODEL_SAVE_PATH

def run_wildlife_inference(
    file_path_or_preprocessed: Union[str, Path, Dict[str, Any]],
    model_path: Path = MODEL_SAVE_PATH
) -> Dict[str, Any]:
    """
    Executes Module 4 Wildlife Feature Extraction & Classification.
    
    Args:
        file_path_or_preprocessed: File path or Module 2 preprocessed output dict.
        model_path: Path to serialized wildlife classifier joblib model.
        
    Returns:
        Dict containing model training status, real acoustic feature profile,
        predicted species (if trained), confidence, and latency.
    """
    start_time = time.time()

    # 1. Retrieve 16kHz Mono Waveform from Module 2 pipeline
    if isinstance(file_path_or_preprocessed, dict) and "waveform" in file_path_or_preprocessed:
        waveform = file_path_or_preprocessed["waveform"]
        sample_rate = file_path_or_preprocessed["sample_rate"]
        file_path_str = file_path_or_preprocessed.get("file_path", "")
    else:
        file_path = Path(file_path_or_preprocessed)
        file_path_str = str(file_path.resolve())
        prep_data = preprocess_audio_pipeline(file_path, target_sr=16000)
        waveform = prep_data["waveform"]
        sample_rate = prep_data["sample_rate"]

    # 2. Extract 45 Real Librosa Acoustic Features
    feat_vector, readable_metrics = extract_acoustic_features(waveform, sr=sample_rate)

    # 3. Check for Trained Local Model
    model_payload = load_wildlife_model(model_path)
    elapsed_time = round(time.time() - start_time, 3)

    if model_payload is not None and "model" in model_payload:
        # Trained Model Available
        clf = model_payload["model"]
        classes = model_payload["classes"]

        probs = clf.predict_proba([feat_vector])[0]
        top_idx = int(np.argmax(probs))

        top_predictions = []
        for c_name, p_val in zip(classes, probs):
            top_predictions.append({
                "species": c_name,
                "probability": round(float(p_val), 4),
                "pct": round(float(p_val) * 100, 2)
            })

        top_predictions.sort(key=lambda x: x["probability"], reverse=True)

        return {
            "file_path": file_path_str,
            "model_trained": True,
            "model_status": "Wildlife Model: Trained & Active",
            "model_name": "RandomForest Wildlife Classifier",
            "predicted_species": top_predictions[0]["species"],
            "confidence": top_predictions[0]["probability"],
            "confidence_pct": top_predictions[0]["pct"],
            "top_predictions": top_predictions,
            "known_classes": classes,
            "acoustic_profile": readable_metrics,
            "inference_latency_sec": elapsed_time,
            "notice": "Predictions generated using trained local Random Forest model."
        }
    else:
        # Untrained Model (Dataset Currently Empty / Insufficient)
        return {
            "file_path": file_path_str,
            "model_trained": False,
            "model_status": "Wildlife Model: Not Trained",
            "model_name": "RandomForest Wildlife Classifier (Pending Dataset)",
            "predicted_species": "Dataset Required",
            "confidence": 0.0,
            "confidence_pct": 0.0,
            "top_predictions": [],
            "known_classes": [],
            "acoustic_profile": readable_metrics,
            "inference_latency_sec": elapsed_time,
            "notice": "The dataset/ directory contains 0 labeled class folders. Domain-specific wildlife species classification requires labeled audio folders (e.g., dataset/peacock/*.wav)."
        }
