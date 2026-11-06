"""Prediction application for office-item classification.

This script provides a command-line interface for classifying office items
using the trained HOG + RBF SVM model. It supports both image file input
and standard camera input.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from office_item_classifier.predictor import (
    OfficeItemPredictor,
    PredictionResult,
)


def print_result(result: PredictionResult) -> None:
    """Print prediction result in a user-friendly format."""
    print("\n" + "=" * 60)
    print("CLASSIFICATION RESULT")
    print("=" * 60)
    print(f"Input source: {result.input_source}")
    print(f"Status: {result.status.upper()}")

    if result.status == "success":
        print(f"Predicted class: {result.predicted_class}")
        if result.confidence is not None:
            print(f"Confidence: {result.confidence:.4f}")
        else:
            print("Confidence: Not provided by the selected model")
    else:
        print(f"Error: {result.error_message}")

    print("=" * 60 + "\n")


def run_image_file_mode(predictor: OfficeItemPredictor, image_path: str) -> None:
    """Classify a single image file."""
    print(f"Classifying image: {image_path}")
    result = predictor.predict_image_file(image_path)
    print_result(result)


def run_camera_mode(predictor: OfficeItemPredictor, camera_index: int = 0) -> None:
    """Classify frames from a standard camera."""
    print("\nOpening camera...")
    print("Press 'q' to quit, 'c' to capture and classify a frame.")
    print("=" * 60)

    cap = None
    try:
        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            print(f"Error: Could not open camera at index {camera_index}")
            print("Please check that a camera is connected and the index is correct.")
            return

        print(f"Camera opened successfully (index {camera_index})")
        print("Displaying live preview...")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame from camera")
                break

            # Display the frame
            cv2.imshow("Office Item Classifier - Live Preview", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\nQuitting camera mode...")
                break
            elif key == ord('c'):
                print("\nCapturing and classifying frame...")
                result = predictor.predict_camera_frame(frame)
                print_result(result)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as exc:
        print(f"\nError in camera mode: {exc}")
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        print("Camera resources released.")


def main() -> int:
    """Main entry point for the prediction application."""
    parser = argparse.ArgumentParser(
        description="Office Item Classification Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Classify an image file
  python scripts/predict_app.py --image path/to/image.jpg

  # Use camera for classification
  python scripts/predict_app.py --camera

  # Use specific camera index
  python scripts/predict_app.py --camera --camera-index 1
        """
    )

    parser.add_argument(
        "--image",
        type=str,
        help="Path to an image file to classify",
    )

    parser.add_argument(
        "--camera",
        action="store_true",
        help="Use camera for live classification",
    )

    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Camera index to use (default: 0)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="results/selected_model/rbf_c10_hog_svm.joblib",
        help="Path to the trained model file",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.image and not args.camera:
        parser.print_help()
        print("\nError: Please specify either --image or --camera")
        return 1

    if args.image and args.camera:
        parser.print_help()
        print("\nError: Please specify only one of --image or --camera")
        return 1

    # Load the model
    print("Loading trained model...")
    print(f"Model path: {args.model}")
    print("=" * 60)

    try:
        predictor = OfficeItemPredictor(args.model)
        print("Model loaded successfully.")
        print(f"Model info: {predictor.model_info}")
        print(f"Supported classes: {', '.join(predictor.class_names)}")
        print("=" * 60)
    except Exception as exc:
        print(f"Error loading model: {exc}")
        return 1

    # Run the appropriate mode
    try:
        if args.image:
            run_image_file_mode(predictor, args.image)
        else:
            run_camera_mode(predictor, args.camera_index)

        return 0

    except Exception as exc:
        print(f"\nUnexpected error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
