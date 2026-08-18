"""
Eco-Acoustic AI Models Package
Provides Wildlife-Specific RandomForest model training, feature extraction, and model loading.
"""

from ai.models.wildlife_model import (
    extract_acoustic_features,
    train_wildlife_model,
    load_wildlife_model,
    MODEL_SAVE_PATH
)

__all__ = [
    "extract_acoustic_features",
    "train_wildlife_model",
    "load_wildlife_model",
    "MODEL_SAVE_PATH"
]
