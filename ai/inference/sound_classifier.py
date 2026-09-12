"""
Eco-Acoustic Health Monitor - AI Inference Engine
Runs pretrained Audio Spectrogram Transformer (AST) classification on 16kHz audio waveforms,
computes sigmoid AudioSet probabilities, categorizes detected acoustic events,
and measures inference latency.
"""

import time
from pathlib import Path
from typing import Dict, Any, List, Union
import numpy as np
import torch

from ai.preprocessing import preprocess_audio_pipeline
from ai.models.sound_model import get_ast_model_and_extractor

# Category mapping definitions based on AudioSet labels
THREAT_KEYWORDS = {
    "chainsaw": ("Potential Threat Detected", "critical", "Chainsaw activity detected"),
    "gunshot": ("Critical Potential Threat Detected", "critical", "Gunshot or gunfire impulse sound detected"),
    "gunfire": ("Critical Potential Threat Detected", "critical", "Gunfire sound detected"),
    "explosion": ("Critical Potential Threat Detected", "critical", "Explosive sound detected"),
    "engine": ("Potential Anthropogenic Sound", "warning", "Engine or vehicle operation detected"),
    "vehicle": ("Potential Anthropogenic Sound", "warning", "Vehicle noise detected"),
    "motorcycle": ("Potential Anthropogenic Sound", "warning", "Motorized vehicle noise detected"),
    "truck": ("Potential Anthropogenic Sound", "warning", "Heavy vehicle activity detected"),
}

WILDLIFE_KEYWORDS = ["bird", "animal", "wild", "natural", "rain", "wind", "fowl", "rooster", "crow", "frog", "bark"]

# Keep each AST call below the feature extractor's 1,024-frame limit. At 16 kHz,
# a 10-second waveform produces fewer than 1,024 10 ms feature frames.
AST_CHUNK_DURATION_SEC = 10.0


def split_waveform_into_ast_chunks(
    waveform: np.ndarray,
    sample_rate: int,
    chunk_duration_sec: float = AST_CHUNK_DURATION_SEC
) -> List[np.ndarray]:
    """Splits a mono waveform into contiguous AST-safe chunks.

    Clips no longer than one chunk are returned unchanged so existing short-audio
    inference continues to use the same extractor/model call as before.
    """
    samples_per_chunk = int(sample_rate * chunk_duration_sec)
    if samples_per_chunk <= 0:
        raise ValueError("AST chunk duration must produce at least one sample.")

    if len(waveform) <= samples_per_chunk:
        return [waveform]

    return [waveform[start:start + samples_per_chunk] for start in range(0, len(waveform), samples_per_chunk)]


def classify_audioset_category(label: str) -> str:
    """Classifies an AudioSet label into Wildlife/Environmental, Potential Threat, or Other."""
    lbl_lower = label.lower()
    for kw in THREAT_KEYWORDS:
        if kw in lbl_lower:
            return "Potential Threat"
    for kw in WILDLIFE_KEYWORDS:
        if kw in lbl_lower:
            return "Wildlife / Environmental"
    return "Other / Ambient"


def evaluate_threat_status(top_predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates threat status transparently based strictly on actual top AudioSet class detections.
    Does not claim real-world certainty; uses transparent language ('Potential Threat Detected').
    """
    for pred in top_predictions:
        label_lower = pred["class"].lower()
        prob = pred["probability"]

        for kw, (status_title, badge_type, desc) in THREAT_KEYWORDS.items():
            if kw in label_lower and prob > 0.05:  # At least 5% model score
                return {
                    "has_threat": True,
                    "status_title": f"{status_title}: {pred['class']}",
                    "badge_type": badge_type,
                    "detected_class": pred["class"],
                    "probability_pct": pred["pct"],
                    "description": f"Model output detected {pred['class']} with score {pred['pct']:.1f}%. Recommend field inspection."
                }

    # Default to Natural / Normal soundscape if no threat detected in top predictions
    return {
        "has_threat": False,
        "status_title": "Natural Soundscape Detected",
        "badge_type": "healthy",
        "detected_class": "Natural Ambient Sound",
        "probability_pct": top_predictions[0]["pct"] if top_predictions else 0.0,
        "description": "No chainsaw, gunshot, or motorized threat signals detected in top model outputs."
    }


def run_ast_inference(
    file_path_or_preprocessed: Union[str, Path, Dict[str, Any]],
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Executes AST inference using the pretrained model MIT/ast-finetuned-audioset-10-10-0.4593.
    
    Args:
        file_path_or_preprocessed: Path to audio file or preprocessed dict from Module 2.
        top_k: Number of top AudioSet predictions to return (default: 5).
        
    Returns:
        Dict containing top predicted class, confidence, top_k list, threat status, and latency.
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

    # 2. Get AST Model and Feature Extractor Singleton
    feature_extractor, model = get_ast_model_and_extractor()

    # 3. Split recordings longer than one AST-safe window. Short recordings stay
    # on the original one-call path. Each chunk is independently featurized and
    # classified using the unchanged AST model and sigmoid multi-label outputs.
    waveform_chunks = split_waveform_into_ast_chunks(waveform, sample_rate)
    chunk_probabilities = []

    with torch.no_grad():
        for waveform_chunk in waveform_chunks:
            inputs = feature_extractor(
                waveform_chunk,
                sampling_rate=sample_rate,
                return_tensors="pt"
            )
            outputs = model(**inputs)
            chunk_probabilities.append(torch.sigmoid(outputs.logits[0]).cpu().numpy())

    # 4. Aggregate chunk-level sigmoid vectors with per-label max pooling. This
    # preserves the strongest detection for each AudioSet label anywhere in the
    # recording instead of diluting short events across quiet chunks.
    probabilities = np.max(np.stack(chunk_probabilities), axis=0)

    # 5. Extract Top-K AudioSet Classes
    top_k_indices = probabilities.argsort()[-top_k:][::-1]
    
    id2label = model.config.id2label

    top_predictions: List[Dict[str, Any]] = []
    for idx in top_k_indices:
        class_name = id2label.get(int(idx), f"Class {idx}")
        prob = float(probabilities[idx])
        category = classify_audioset_category(class_name)
        
        top_predictions.append({
            "class_id": int(idx),
            "class": class_name,
            "probability": round(prob, 4),
            "pct": round(prob * 100, 2),
            "category": category
        })

    elapsed_time = round(time.time() - start_time, 3)

    top_pred = top_predictions[0]
    threat_eval = evaluate_threat_status(top_predictions)

    return {
        "file_path": file_path_str,
        "model_id": "MIT/ast-finetuned-audioset-10-10-0.4593",
        "predicted_class": top_pred["class"],
        "confidence": top_pred["probability"],
        "confidence_pct": top_pred["pct"],
        "category": top_pred["category"],
        "top_5_predictions": top_predictions,
        "threat_status": threat_eval,
        "inference_time_sec": elapsed_time
    }
