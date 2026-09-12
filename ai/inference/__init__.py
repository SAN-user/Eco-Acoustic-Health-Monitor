"""
Eco-Acoustic AI Inference Engine Package
Provides AST model inference, probability extraction, threat classification,
and Wildlife-Specific classification & feature profiling.
"""

try:
    from ai.inference.sound_classifier import (
        run_ast_inference,
        classify_audioset_category,
        evaluate_threat_status
    )
except ImportError:
    run_ast_inference = None
    classify_audioset_category = None
    evaluate_threat_status = None

from ai.inference.wildlife_classifier import run_wildlife_inference

__all__ = [
    "run_ast_inference",
    "classify_audioset_category",
    "evaluate_threat_status",
    "run_wildlife_inference"
]
