"""
Verification Script for Module 3 (Pretrained Audio Spectrogram Transformer - AST Inference)
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai.models.sound_model import get_ast_model_and_extractor
from ai.inference.sound_classifier import run_ast_inference, classify_audioset_category

def main():
    print("--- Starting Module 3 AST Model & Inference Verification ---")

    # 1. Test Model and Feature Extractor Loading
    print("Loading AST Model and Feature Extractor ('MIT/ast-finetuned-audioset-10-10-0.4593')...")
    start_load = time.time()
    feature_extractor, model = get_ast_model_and_extractor()
    load_time = time.time() - start_load
    print(f"✅ Model & Feature Extractor loaded successfully in {load_time:.2f} seconds.")
    assert feature_extractor is not None, "Feature Extractor is None"
    assert model is not None, "Model is None"
    assert hasattr(model.config, "id2label"), "Model missing id2label mapping"

    # 2. Test Audio File Selection from uploads/ or scratch/
    uploads_dir = ROOT_DIR / "uploads"
    upload_files = list(uploads_dir.glob("*.wav")) + list(uploads_dir.glob("*.mp3"))
    
    if upload_files:
        test_audio = upload_files[0]
    else:
        test_audio = ROOT_DIR / "scratch" / "test_audio" / "stereo_44100hz_test.wav"
        
    print(f"\nRunning AST inference on test audio file: {test_audio.name}")
    
    # 3. Execute AST Inference Pipeline
    res = run_ast_inference(test_audio, top_k=5)
    
    print("\n--- Module 3 Inference Output ---")
    print(f"File Path: {res['file_path']}")
    print(f"Model ID: {res['model_id']}")
    print(f"Top Predicted Class: {res['predicted_class']}")
    print(f"Confidence Score: {res['confidence']} ({res['confidence_pct']}%)")
    print(f"Inference Latency: {res['inference_time_sec']} seconds")
    print(f"Threat Evaluation: {res['threat_status']['status_title']} ({res['threat_status']['badge_type']})")
    
    print("\nTop 5 AudioSet Category Predictions:")
    for idx, item in enumerate(res["top_5_predictions"], start=1):
        print(f"  {idx}. {item['class']} -> {item['pct']:.2f}% ({item['category']})")

    # 4. Assertions and Validation
    assert res["predicted_class"] is not None and len(res["predicted_class"]) > 0
    assert 0.0 <= res["confidence"] <= 1.0, f"Invalid probability {res['confidence']}"
    assert len(res["top_5_predictions"]) == 5, f"Expected 5 predictions, got {len(res['top_5_predictions'])}"
    assert res["inference_time_sec"] > 0.0

    print("\n🎉 ALL MODULE 3 AST INFERENCE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
