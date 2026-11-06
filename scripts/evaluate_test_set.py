"""Final held-out test evaluation for the selected model.

This script evaluates the selected HOG + RBF SVM model on the held-out
test dataset that was reserved for Step 6. It generates accuracy,
macro-F1, confusion matrix, and error analysis.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from office_item_classifier.dataset import (
    CLASS_NAMES,
    MANIFEST_RELATIVE_PATH,
    EXPECTED_PROPOSED_COUNTS,
    ImageRecord,
    load_manifest,
)
from office_item_classifier.features import extract_hog_features
from office_item_classifier.image_preprocessing import preprocess_pil_image


PROJECT_ROOT = Path(__file__).parent.parent

MANIFEST_PATH = PROJECT_ROOT / MANIFEST_RELATIVE_PATH

DATASET_ROOT = PROJECT_ROOT / "dataset"

MODEL_PATH = PROJECT_ROOT / "results" / "selected_model" / "rbf_c10_hog_svm.joblib"

RESULTS_DIR = PROJECT_ROOT / "results" / "test_evaluation"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_test_records() -> list[ImageRecord]:
    """Load test split records from the approved manifest."""
    records = load_manifest(MANIFEST_PATH, DATASET_ROOT)
    
    test_records = [
        record for record in records
        if record.proposed_split == "test"
    ]
    
    expected_count = EXPECTED_PROPOSED_COUNTS["test"]
    
    if len(test_records) != expected_count:
        raise RuntimeError(
            f"Expected {expected_count} test records, found {len(test_records)}."
        )
    
    # Verify test image files exist
    missing = [
        record.source_path
        for record in test_records
        if not record.source_path.is_file()
    ]
    
    if missing:
        raise FileNotFoundError(
            f"{len(missing)} test image files are missing."
        )
    
    return test_records


def load_test_images_and_labels(records: list[ImageRecord]) -> tuple[np.ndarray, np.ndarray]:
    """Load and preprocess all test images."""
    images = []
    labels = []
    
    for record in records:
        try:
            with record.source_path.open("rb") as f:
                from PIL import Image
                image = Image.open(f)
                preprocessed = preprocess_pil_image(image)
                images.append(preprocessed)
                labels.append(record.class_name)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load test image {record.source_path}: {exc}"
            ) from exc
    
    images_array = np.stack(images, axis=0)
    labels_array = np.asarray(labels, dtype=str)
    
    return images_array, labels_array


def evaluate_test_set():
    """Run the final held-out test evaluation."""
    print("=" * 70)
    print("STEP 6: FINAL HELD-OUT TEST EVALUATION")
    print("=" * 70)
    
    # Load test records
    print("\n1. Loading test records from approved manifest...")
    test_records = load_test_records()
    print(f"   Loaded {len(test_records)} test records.")
    
    # Load test images
    print("\n2. Loading and preprocessing test images...")
    test_images, test_labels = load_test_images_and_labels(test_records)
    print(f"   Loaded {len(test_images)} test images.")
    print(f"   Image shape: {test_images.shape}")
    print(f"   Labels shape: {test_labels.shape}")
    
    # Extract HOG features
    print("\n3. Extracting HOG features...")
    test_features = extract_hog_features(test_images)
    print(f"   Feature matrix shape: {test_features.shape}")
    
    # Load the trained model
    print("\n4. Loading trained model...")
    model_dict = joblib.load(MODEL_PATH)
    model = model_dict["model"]
    print(f"   Model loaded from: {MODEL_PATH}")
    print(f"   Model type: {type(model)}")
    print(f"   Kernel: {model_dict['svm']['kernel']}")
    print(f"   C: {model_dict['svm']['C']}")
    
    # Make predictions
    print("\n5. Running predictions on test set...")
    predictions = model.predict(test_features)
    print(f"   Generated {len(predictions)} predictions.")
    
    # Calculate metrics
    print("\n6. Calculating evaluation metrics...")
    accuracy = accuracy_score(test_labels, predictions)
    macro_f1 = f1_score(test_labels, predictions, average="macro")
    
    print(f"   Test accuracy: {accuracy:.6f}")
    print(f"   Test macro-F1: {macro_f1:.6f}")
    
    # Generate classification report
    print("\n7. Generating classification report...")
    class_report = classification_report(
        test_labels,
        predictions,
        target_names=CLASS_NAMES,
        output_dict=True,
    )
    
    # Generate confusion matrix
    print("\n8. Generating confusion matrix...")
    conf_matrix = confusion_matrix(test_labels, predictions, labels=CLASS_NAMES)
    
    # Save results
    print("\n9. Saving results...")
    
    # Save metrics
    metrics = {
        "test_accuracy": float(accuracy),
        "test_macro_f1": float(macro_f1),
        "n_test_images": len(test_images),
        "model_path": str(MODEL_PATH),
        "manifest_path": str(MANIFEST_PATH),
    }
    
    metrics_path = RESULTS_DIR / "test_metrics.json"
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"   Saved metrics to: {metrics_path}")
    
    # Save classification report (JSON)
    report_json_path = RESULTS_DIR / "test_classification_report.json"
    with report_json_path.open("w", encoding="utf-8") as f:
        json.dump(class_report, f, indent=2)
    print(f"   Saved classification report (JSON) to: {report_json_path}")
    
    # Save classification report (CSV)
    report_csv_path = RESULTS_DIR / "test_classification_report.csv"
    with report_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Class", "Precision", "Recall", "F1-Score", "Support"])
        for class_name in CLASS_NAMES:
            metrics_dict = class_report[class_name]
            writer.writerow([
                class_name,
                metrics_dict["precision"],
                metrics_dict["recall"],
                metrics_dict["f1-score"],
                metrics_dict["support"],
            ])
        # Add averages
        writer.writerow([])
        writer.writerow(["Macro avg", class_report["macro avg"]["precision"],
                        class_report["macro avg"]["recall"],
                        class_report["macro avg"]["f1-score"],
                        class_report["macro avg"]["support"]])
        writer.writerow(["Weighted avg", class_report["weighted avg"]["precision"],
                        class_report["weighted avg"]["recall"],
                        class_report["weighted avg"]["f1-score"],
                        class_report["weighted avg"]["support"]])
    print(f"   Saved classification report (CSV) to: {report_csv_path}")
    
    # Save confusion matrix (CSV)
    matrix_csv_path = RESULTS_DIR / "test_confusion_matrix.csv"
    with matrix_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Actual / Predicted"] + list(CLASS_NAMES))
        for i, class_name in enumerate(CLASS_NAMES):
            writer.writerow([class_name] + conf_matrix[i].tolist())
    print(f"   Saved confusion matrix (CSV) to: {matrix_csv_path}")
    
    # Save predictions with labels
    predictions_path = RESULTS_DIR / "test_predictions.csv"
    with predictions_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Image Path", "True Label", "Predicted Label", "Correct"])
        for record, pred in zip(test_records, predictions):
            correct = record.class_name == pred
            writer.writerow([str(record.source_path), record.class_name, pred, correct])
    print(f"   Saved predictions to: {predictions_path}")
    
    # Error analysis
    print("\n10. Error analysis...")
    incorrect_indices = np.where(predictions != test_labels)[0]
    n_incorrect = len(incorrect_indices)
    print(f"   Incorrect predictions: {n_incorrect} / {len(test_images)} ({n_incorrect/len(test_images)*100:.2f}%)")
    
    if n_incorrect > 0:
        print("\n   Top error patterns:")
        error_counts = {}
        for idx in incorrect_indices:
            true_label = test_labels[idx]
            pred_label = predictions[idx]
            key = f"{true_label} -> {pred_label}"
            error_counts[key] = error_counts.get(key, 0) + 1
        
        sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        for error, count in sorted_errors[:10]:
            print(f"      {error}: {count}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Test accuracy: {accuracy:.6f}")
    print(f"Test macro-F1: {macro_f1:.6f}")
    print(f"Total test images: {len(test_images)}")
    print(f"Correct predictions: {len(test_images) - n_incorrect}")
    print(f"Incorrect predictions: {n_incorrect}")
    print("=" * 70)
    print(f"\nResults saved to: {RESULTS_DIR}")
    print("\nEvaluation complete.")


if __name__ == "__main__":
    try:
        evaluate_test_set()
    except Exception as exc:
        print(f"\nError during test evaluation: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
