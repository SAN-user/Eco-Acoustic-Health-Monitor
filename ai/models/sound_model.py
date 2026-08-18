"""
Eco-Acoustic Health Monitor - AI Model Loader
Loads and manages the pretrained Audio Spectrogram Transformer (AST) model
and Hugging Face feature extractor.
"""

from typing import Tuple, Any, Optional
import torch
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

# Model Checkpoint Identifier
MODEL_ID = "MIT/ast-finetuned-audioset-10-10-0.4593"

# Singleton global cache
_FEATURE_EXTRACTOR: Optional[Any] = None
_MODEL: Optional[Any] = None

def get_ast_model_and_extractor() -> Tuple[Any, Any]:
    """
    Loads and returns the pretrained AST feature extractor and classification model.
    Uses singleton caching to avoid reloading weights across multiple inference calls.
    
    Returns:
        Tuple[AutoFeatureExtractor, AutoModelForAudioClassification]: Feature extractor and PyTorch model.
    """
    global _FEATURE_EXTRACTOR, _MODEL
    
    if _FEATURE_EXTRACTOR is not None and _MODEL is not None:
        return _FEATURE_EXTRACTOR, _MODEL

    try:
        # Load Hugging Face Feature Extractor and AST Model
        feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL_ID)
        model = AutoModelForAudioClassification.from_pretrained(MODEL_ID)
        model.eval()  # Set to evaluation mode
        
        _FEATURE_EXTRACTOR = feature_extractor
        _MODEL = model
        
        return feature_extractor, model
    except Exception as e:
        raise RuntimeError(f"Failed to load AST pretrained model '{MODEL_ID}': {str(e)}")
