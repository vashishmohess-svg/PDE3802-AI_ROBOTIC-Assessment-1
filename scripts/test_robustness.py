"""Robustness and input-handling tests for the prediction application.

This script tests the prediction application with various edge cases,
invalid inputs, and failure scenarios to ensure robust behavior.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from office_item_classifier.predictor import (
    OfficeItemPredictor,
    PredictionResult,
)
from office_item_classifier.image_preprocessing import (
    ImagePreprocessingError,
)


PROJECT_ROOT = Path(__file__).parent.parent

MODEL_PATH = PROJECT_ROOT / "results" / "selected_model" / "rbf_c10_hog_svm.joblib"


def test_valid_image_file():
    """Test classification of a valid image file."""
    print("\nTest 1: Valid image file")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    image_path = PROJECT_ROOT / "dataset" / "train" / "Bottle" / "00001_jpg.rf.7d50e7e57d941fdcb0df860c2245e619.jpg"
    
    result = predictor.predict_image_file(image_path)
    
    assert result.status == "success", f"Expected success, got {result.status}"
    assert result.predicted_class is not None, "Expected a predicted class"
    assert result.input_source == "image_file", "Expected image_file source"
    assert result.error_message is None, "Expected no error message"
    
    print(f"[PASS] Valid image classified successfully")
    print(f"  Predicted class: {result.predicted_class}")
    print(f"  Status: {result.status}")


def test_missing_file():
    """Test handling of a non-existent file."""
    print("\nTest 2: Missing file")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    non_existent_path = PROJECT_ROOT / "non_existent_image.jpg"
    
    result = predictor.predict_image_file(non_existent_path)
    
    assert result.status == "failure", f"Expected failure, got {result.status}"
    assert result.predicted_class is None, "Expected no predicted class on failure"
    assert result.error_message is not None, "Expected an error message"
    assert "not found" in result.error_message.lower(), "Expected 'not found' in error"
    
    print(f"[PASS] Missing file handled correctly")
    print(f"  Status: {result.status}")
    print(f"  Error: {result.error_message}")


def test_unsupported_format():
    """Test handling of unsupported image format."""
    print("\nTest 3: Unsupported image format")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    
    # Create a temporary file with unsupported extension
    temp_file = PROJECT_ROOT / "test_temp.txt"
    temp_file.write_text("Not an image")
    
    try:
        result = predictor.predict_image_file(temp_file)
        
        assert result.status == "failure", f"Expected failure, got {result.status}"
        assert result.predicted_class is None, "Expected no predicted class on failure"
        assert result.error_message is not None, "Expected an error message"
        
        print(f"[PASS] Unsupported format handled correctly")
        print(f"  Status: {result.status}")
        print(f"  Error: {result.error_message}")
    finally:
        if temp_file.exists():
            temp_file.unlink()


def test_directory_instead_of_file():
    """Test handling when a directory path is provided instead of a file."""
    print("\nTest 4: Directory instead of file")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    dir_path = PROJECT_ROOT / "dataset"
    
    result = predictor.predict_image_file(dir_path)
    
    assert result.status == "failure", f"Expected failure, got {result.status}"
    assert result.predicted_class is None, "Expected no predicted class on failure"
    assert result.error_message is not None, "Expected an error message"
    
    print(f"[PASS] Directory path handled correctly")
    print(f"  Status: {result.status}")
    print(f"  Error: {result.error_message}")


def test_valid_camera_frame():
    """Test classification of a valid camera frame (simulated)."""
    print("\nTest 5: Valid camera frame")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    
    # Create a simulated camera frame (128x128 grayscale)
    frame = np.random.randint(0, 255, (128, 128), dtype=np.uint8)
    
    result = predictor.predict_camera_frame(frame)
    
    assert result.status == "success", f"Expected success, got {result.status}"
    assert result.predicted_class is not None, "Expected a predicted class"
    assert result.input_source == "camera_frame", "Expected camera_frame source"
    assert result.error_message is None, "Expected no error message"
    
    print(f"[PASS] Valid camera frame classified successfully")
    print(f"  Predicted class: {result.predicted_class}")
    print(f"  Status: {result.status}")


def test_empty_camera_frame():
    """Test handling of an empty camera frame."""
    print("\nTest 6: Empty camera frame")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    
    # Create an empty frame
    empty_frame = np.array([], dtype=np.uint8)
    
    result = predictor.predict_camera_frame(empty_frame)
    
    assert result.status == "failure", f"Expected failure, got {result.status}"
    assert result.predicted_class is None, "Expected no predicted class on failure"
    assert result.error_message is not None, "Expected an error message"
    
    print(f"[PASS] Empty frame handled correctly")
    print(f"  Status: {result.status}")
    print(f"  Error: {result.error_message}")


def test_wrong_dtype_frame():
    """Test handling of frame with wrong data type."""
    print("\nTest 7: Wrong data type frame")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    
    # Create a frame with float32 instead of uint8
    wrong_frame = np.random.rand(128, 128).astype(np.float32)
    
    result = predictor.predict_camera_frame(wrong_frame)
    
    assert result.status == "failure", f"Expected failure, got {result.status}"
    assert result.predicted_class is None, "Expected no predicted class on failure"
    assert result.error_message is not None, "Expected an error message"
    
    print(f"[PASS] Wrong dtype handled correctly")
    print(f"  Status: {result.status}")
    print(f"  Error: {result.error_message}")


def test_bgr_camera_frame():
    """Test handling of BGR color camera frame."""
    print("\nTest 8: BGR color camera frame")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    
    # Create a BGR frame (simulating OpenCV camera output)
    bgr_frame = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    
    result = predictor.predict_camera_frame(bgr_frame)
    
    assert result.status == "success", f"Expected success, got {result.status}"
    assert result.predicted_class is not None, "Expected a predicted class"
    
    print(f"[PASS] BGR frame converted and classified successfully")
    print(f"  Predicted class: {result.predicted_class}")
    print(f"  Status: {result.status}")


def test_bgra_camera_frame():
    """Test handling of BGRA color camera frame."""
    print("\nTest 9: BGRA color camera frame")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    
    # Create a BGRA frame
    bgra_frame = np.random.randint(0, 255, (128, 128, 4), dtype=np.uint8)
    
    result = predictor.predict_camera_frame(bgra_frame)
    
    assert result.status == "success", f"Expected success, got {result.status}"
    assert result.predicted_class is not None, "Expected a predicted class"
    
    print(f"[PASS] BGRA frame converted and classified successfully")
    print(f"  Predicted class: {result.predicted_class}")
    print(f"  Status: {result.status}")


def test_invalid_frame_shape():
    """Test handling of frame with invalid shape."""
    print("\nTest 10: Invalid frame shape")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    
    # Create a frame with wrong number of dimensions
    invalid_frame = np.random.randint(0, 255, (128, 128, 128, 3), dtype=np.uint8)
    
    result = predictor.predict_camera_frame(invalid_frame)
    
    assert result.status == "failure", f"Expected failure, got {result.status}"
    assert result.predicted_class is None, "Expected no predicted class on failure"
    assert result.error_message is not None, "Expected an error message"
    
    print(f"[PASS] Invalid shape handled correctly")
    print(f"  Status: {result.status}")
    print(f"  Error: {result.error_message}")


def test_model_info():
    """Test that model information is accessible."""
    print("\nTest 11: Model information")
    print("-" * 60)
    
    predictor = OfficeItemPredictor(MODEL_PATH)
    
    info = predictor.model_info
    class_names = predictor.class_names
    
    assert info["kernel"] == "rbf", "Expected RBF kernel"
    assert info["C"] == 10.0, "Expected C=10.0"
    assert info["probability"] == False, "Expected probability disabled"
    assert len(class_names) == 8, "Expected 8 classes"
    
    print(f"[PASS] Model information accessible")
    print(f"  Kernel: {info['kernel']}")
    print(f"  C: {info['C']}")
    print(f"  Classes: {len(class_names)}")


def run_all_tests():
    """Run all robustness tests."""
    print("=" * 70)
    print("STEP 7: ROBUSTNESS AND INPUT-HANDLING TESTS")
    print("=" * 70)
    
    tests = [
        test_valid_image_file,
        test_missing_file,
        test_unsupported_format,
        test_directory_instead_of_file,
        test_valid_camera_frame,
        test_empty_camera_frame,
        test_wrong_dtype_frame,
        test_bgr_camera_frame,
        test_bgra_camera_frame,
        test_invalid_frame_shape,
        test_model_info,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as exc:
            print(f"[FAIL] FAILED: {exc}")
            failed += 1
        except Exception as exc:
            print(f"[ERROR] ERROR: {exc}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 70)
    
    if failed == 0:
        print("\n[PASS] All robustness tests passed!")
    else:
        print(f"\n[FAIL] {failed} test(s) failed.")
    
    return failed == 0


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as exc:
        print(f"\nFatal error during testing: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
