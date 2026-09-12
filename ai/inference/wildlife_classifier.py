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

# Human-readable species display names mapping
SPECIES_DISPLAY_NAMES = {
    "asian_koel": "Asian Koel",
    "bulbul": "Red-vented Bulbul",
    "house_crow": "House Crow",
    "myna": "Hill Myna",
    "peacock": "Indian Peafowl / Peacock",
}


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

    # 2. Extract 46 Real Librosa Acoustic Features
    feat_vector, readable_metrics = extract_acoustic_features(waveform, sr=sample_rate)

    # 3. Check for Trained Local Model
    model_payload = load_wildlife_model(model_path)
    elapsed_time = round(time.time() - start_time, 3)

    if model_payload is not None and "model" in model_payload:
        clf = model_payload["model"]
        classes = model_payload["classes"]

        # Feature Order & Count Verification
        num_expected = model_payload.get("num_features", 46)
        if len(feat_vector) != num_expected:
            raise ValueError(f"Feature count mismatch: Extracted {len(feat_vector)} features, model expected {num_expected}.")

        probs = clf.predict_proba([feat_vector])[0]

        top_predictions = []
        for c_name, p_val in zip(classes, probs):
            disp_name = SPECIES_DISPLAY_NAMES.get(c_name, c_name)
            top_predictions.append({
                "species_key": c_name,
                "species": disp_name,
                "probability": round(float(p_val), 4),
                "pct": round(float(p_val) * 100, 2)
            })

        top_predictions.sort(key=lambda x: x["probability"], reverse=True)

        top_key = top_predictions[0]["species_key"]
        top_disp = top_predictions[0]["species"]

        display_classes = [SPECIES_DISPLAY_NAMES.get(c, c) for c in classes]

        return {
            "file_path": file_path_str,
            "model_trained": True,
            "model_status": "Wildlife Model: Trained & Active (5 Classes)",
            "model_name": "RandomForest 5-Class Wildlife Classifier",
            "raw_species_key": top_key,
            "predicted_species": top_disp,
            "confidence": top_predictions[0]["probability"],
            "confidence_pct": top_predictions[0]["pct"],
            "top_predictions": top_predictions,
            "known_classes": classes,
            "display_classes": display_classes,
            "acoustic_profile": readable_metrics,
            "inference_latency_sec": elapsed_time,
            "notice": "Predictions generated using trained Random Forest model. Note: This model classifies ONLY five target acoustic classes (Asian Koel, Red-vented Bulbul, House Crow, Hill Myna, Indian Peafowl / Peacock)."
        }
    else:
        # Untrained Model Fallback
        return {
            "file_path": file_path_str,
            "model_trained": False,
            "model_status": "Wildlife Model: Not Trained",
            "model_name": "RandomForest Wildlife Classifier (Pending Model)",
            "raw_species_key": "untrained",
            "predicted_species": "Model File Missing / Untrained",
            "confidence": 0.0,
            "confidence_pct": 0.0,
            "top_predictions": [],
            "known_classes": [],
            "display_classes": [],
            "acoustic_profile": readable_metrics,
            "inference_latency_sec": elapsed_time,
            "notice": f"Model file '{model_path.name}' could not be loaded. Please ensure the model file is trained and available."
        }
