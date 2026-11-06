
from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import sklearn
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

# Reuse the approved RBF implementation so that the
# dataset loader, HOG extractor and configuration are identical.
import compare_rbf_models as rbf


PROJECT_ROOT = rbf.PROJECT_ROOT

OUTPUT_DIR = PROJECT_ROOT / "results" / "selected_model"

MODEL_PATH = OUTPUT_DIR / "rbf_c10_hog_svm.joblib"

METADATA_PATH = OUTPUT_DIR / "verification_metadata.json"

METRICS_PATH = OUTPUT_DIR / "validation_metrics.json"

REPORT_JSON_PATH = (
    OUTPUT_DIR / "validation_classification_report.json"
)

REPORT_CSV_PATH = (
    OUTPUT_DIR / "validation_classification_report.csv"
)

MATRIX_PATH = OUTPUT_DIR / "validation_confusion_matrix.csv"

PREDICTIONS_PATH = OUTPUT_DIR / "validation_predictions.csv"

SELECTED_CANDIDATE = "rbf_c10"
SELECTED_C = 10.0


def write_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, indent=2, allow_nan=False),
        encoding="utf-8",
    )


def verify_previous_experiment_summary() -> dict:
    """Check the approved RBF C=10 evidence before retraining."""

    summary_path = (
        PROJECT_ROOT
        / "results"
        / "model_comparison"
        / "rbf"
        / "comparison_summary.json"
    )

    if not summary_path.is_file():
        raise FileNotFoundError(summary_path)

    summary = json.loads(
        summary_path.read_text(encoding="utf-8")
    )

    matches = [
        row for row in summary
        if row.get("candidate") == SELECTED_CANDIDATE
    ]

    if len(matches) != 1:
        raise RuntimeError(
            "Expected exactly one RBF C=10 summary record."
        )

    result = matches[0]

    expected_values = {
        "kernel": "rbf",
        "C": SELECTED_C,
        "gamma": "scale",
        "class_weight": "none",
        "probability": False,
        "training_images": rbf.TRAINING_COUNT,
        "validation_images": rbf.VALIDATION_COUNT,
        "test_images_used": 0,
    }

    for key, expected in expected_values.items():
        if result.get(key) != expected:
            raise RuntimeError(
                f"Previous experiment summary mismatch: "
                f"{key}: expected {expected!r}, "
                f"received {result.get(key)!r}"
            )

    print("[PASS] Previous RBF C=10 experiment evidence verified.")

    return result


def main() -> None:
    print("=== SELECTED MODEL TRAINING ===")
    print("Candidate:", SELECTED_CANDIDATE)
    print("Kernel: RBF")
    print("C:", SELECTED_C)
    print('Gamma: "scale"')
    print("Class weight: None")
    print("Probability estimates: disabled")

    # Verify the previously approved experiment.
    previous_result = verify_previous_experiment_summary()

    # Verify the approved manifest.
    if not rbf.MANIFEST_PATH.is_file():
        raise FileNotFoundError(rbf.MANIFEST_PATH)

    manifest_bytes = rbf.MANIFEST_PATH.read_bytes()

    manifest_sha256 = hashlib.sha256(
        manifest_bytes.replace(b"\r\n", b"\n")
    ).hexdigest().upper()

    if manifest_sha256 != rbf.EXPECTED_MANIFEST_SHA256:
        raise RuntimeError(
            "Approved manifest SHA-256 mismatch."
        )

    print("[PASS] Approved manifest SHA-256 verified.")

    # Load only the approved training and validation splits.
    print("\n=== LOAD APPROVED TRAINING DATA ===")

    training = rbf.load_split_images(
        rbf.MANIFEST_PATH,
        rbf.DATASET_ROOT,
        "train",
    )

    print("Training images:", len(training.labels))

    if len(training.labels) != rbf.TRAINING_COUNT:
        raise RuntimeError("Expected 812 training images.")

    print("\n=== LOAD APPROVED VALIDATION DATA ===")

    validation = rbf.load_split_images(
        rbf.MANIFEST_PATH,
        rbf.DATASET_ROOT,
        "valid",
    )

    print("Validation images:", len(validation.labels))

    if len(validation.labels) != rbf.VALIDATION_COUNT:
        raise RuntimeError("Expected 226 validation images.")

    # Check the approved class set.
    y_train = np.asarray(training.labels).astype(str)
    y_valid = np.asarray(validation.labels).astype(str)

    if set(y_train) != set(rbf.CLASS_ORDER):
        raise RuntimeError("Unexpected training class labels.")

    if set(y_valid) != set(rbf.CLASS_ORDER):
        raise RuntimeError("Unexpected validation class labels.")

    # Ensure that training and validation paths do not overlap.
    train_paths = {
        path.resolve() for path in training.paths
    }

    valid_paths = {
        path.resolve() for path in validation.paths
    }

    if not train_paths.isdisjoint(valid_paths):
        raise RuntimeError(
            "Training and validation images overlap."
        )

    print("[PASS] Training and validation paths are disjoint.")
    print("[PASS] No test split requested.")

    # Extract the same approved HOG features.
    print("\n=== EXTRACT APPROVED HOG FEATURES ===")

    feature_started = time.perf_counter()

    X_train = rbf.extract_hog_features(training.images)
    X_valid = rbf.extract_hog_features(validation.images)

    feature_seconds = time.perf_counter() - feature_started

    expected_train_shape = (
        rbf.TRAINING_COUNT,
        rbf.EXPECTED_HOG_FEATURES,
    )

    expected_valid_shape = (
        rbf.VALIDATION_COUNT,
        rbf.EXPECTED_HOG_FEATURES,
    )

    if X_train.shape != expected_train_shape:
        raise RuntimeError(
            f"Unexpected training feature shape: {X_train.shape}"
        )

    if X_valid.shape != expected_valid_shape:
        raise RuntimeError(
            f"Unexpected validation feature shape: {X_valid.shape}"
        )

    if not (
        np.isfinite(X_train).all()
        and np.isfinite(X_valid).all()
    ):
        raise RuntimeError("Non-finite HOG features detected.")

    print("Training HOG shape:", X_train.shape)
    print("Validation HOG shape:", X_valid.shape)
    print("[PASS] HOG feature extraction verified.")

    # Build and fit the selected RBF SVM.
    print("\n=== TRAIN SELECTED RBF MODEL ===")

    parameters = rbf.candidate_parameters(SELECTED_C)
    model = rbf.create_rbf_model(SELECTED_C)

    actual_parameters = model.get_params(deep=False)

    if (
        actual_parameters.get("kernel") != "rbf"
        or actual_parameters.get("C") != SELECTED_C
        or actual_parameters.get("gamma") != "scale"
        or actual_parameters.get("class_weight") is not None
        or actual_parameters.get("decision_function_shape") != "ovr"
        or parameters.get("probability") is not False
    ):
        raise RuntimeError(
            "Selected SVM configuration is incorrect."
        )

    fit_started = time.perf_counter()

    # Fit on training images only.
    model.fit(X_train, y_train)

    fit_seconds = time.perf_counter() - fit_started

    print("Fit time:", f"{fit_seconds:.4f} seconds")
    print("Support vectors:", model.support_vectors_.shape[0])

    # Evaluate only on validation images.
    print("\n=== VALIDATION EVALUATION ===")

    predictions = model.predict(X_valid)

    accuracy = float(
        accuracy_score(y_valid, predictions)
    )

    macro_f1 = float(
        f1_score(
            y_valid,
            predictions,
            labels=rbf.CLASS_ORDER,
            average="macro",
            zero_division=0,
        )
    )

    matrix = confusion_matrix(
        y_valid,
        predictions,
        labels=rbf.CLASS_ORDER,
    )

    report = classification_report(
        y_valid,
        predictions,
        labels=rbf.CLASS_ORDER,
        target_names=rbf.CLASS_ORDER,
        output_dict=True,
        zero_division=0,
    )

    # Compare retrained metrics with the approved RBF experiment.
    if not math.isclose(
        accuracy,
        float(previous_result["validation_accuracy"]),
        rel_tol=0,
        abs_tol=1e-12,
    ):
        raise RuntimeError(
            "Retrained accuracy does not reproduce "
            "the approved RBF C=10 result."
        )

    if not math.isclose(
        macro_f1,
        float(previous_result["validation_macro_f1"]),
        rel_tol=0,
        abs_tol=1e-12,
    ):
        raise RuntimeError(
            "Retrained macro-F1 does not reproduce "
            "the approved RBF C=10 result."
        )

    # Verify the original experiment confusion matrix.
    previous_matrix_path = (
        PROJECT_ROOT
        / "results"
        / "model_comparison"
        / "rbf"
        / "confusion_matrices"
        / "rbf_c10.csv"
    )

    with previous_matrix_path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as handle:
        previous_rows = list(csv.reader(handle))

    if (
        not previous_rows
        or previous_rows[0][1:] != rbf.CLASS_ORDER
        or [row[0] for row in previous_rows[1:]]
        != rbf.CLASS_ORDER
    ):
        raise RuntimeError(
            "Previous RBF confusion matrix has an invalid class order."
        )

    previous_matrix = np.asarray(
        [
            [int(value) for value in row[1:]]
            for row in previous_rows[1:]
        ],
        dtype=int,
    )

    if not np.array_equal(matrix, previous_matrix):
        raise RuntimeError(
            "Retrained confusion matrix does not match "
            "the original RBF C=10 experiment."
        )

    print(f"Validation accuracy: {accuracy:.6f}")
    print(f"Validation macro-F1: {macro_f1:.6f}")
    print("[PASS] Accuracy reproduced.")
    print("[PASS] Macro-F1 reproduced.")
    print("[PASS] All 226 confusion-matrix predictions reproduced.")

    # Construct the permanent model bundle.
    preprocessing = {
        "orientation": "EXIF transpose",
        "colour": "grayscale",
        "image_size": [128, 128],
        "resize_interpolation": "cv2.INTER_AREA",
    }

    hog_configuration = {
        "window_size": list(rbf.HOG_WIN_SIZE),
        "block_size": list(rbf.HOG_BLOCK_SIZE),
        "block_stride": list(rbf.HOG_BLOCK_STRIDE),
        "cell_size": list(rbf.HOG_CELL_SIZE),
        "bins": rbf.HOG_BINS,
        "feature_count": rbf.EXPECTED_HOG_FEATURES,
    }

    bundle = {
        "model": model,
        "class_names": list(rbf.CLASS_ORDER),
        "model_name": "HOG + RBF SVM C=10.0",
        "svm": parameters,
        "preprocessing": preprocessing,
        "hog": hog_configuration,
        "manifest_sha256": manifest_sha256,
    }

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Permanent, uncompressed Joblib model, protocol 5.
    saved_paths = joblib.dump(
        bundle,
        MODEL_PATH,
        compress=0,
        protocol=5,
    )

    model_size_bytes = sum(
        Path(path).stat().st_size
        for path in saved_paths
    )

    if not MODEL_PATH.is_file() or model_size_bytes <= 0:
        raise RuntimeError(
            "Permanent selected model was not saved correctly."
        )

    print("\n[PASS] Permanent selected model saved.")
    print("Model path:", MODEL_PATH)
    print("Model size:", model_size_bytes, "bytes")

    # Save validation metrics.
    metrics = {
        "selected_candidate": SELECTED_CANDIDATE,
        "kernel": "rbf",
        "C": SELECTED_C,
        "gamma": "scale",
        "class_weight": "none",
        "probability": False,
        "validation_accuracy": accuracy,
        "validation_macro_f1": macro_f1,
        "fit_seconds": float(fit_seconds),
        "feature_extraction_seconds": float(feature_seconds),
        "model_size_bytes": int(model_size_bytes),
        "support_vector_count": int(model.support_vectors_.shape[0]),
        "training_images": rbf.TRAINING_COUNT,
        "validation_images": rbf.VALIDATION_COUNT,
        "test_images_used": 0,
        "independent_test_evaluation_performed": False,
        "reproduced_previous_accuracy": True,
        "reproduced_previous_macro_f1": True,
        "reproduced_previous_confusion_matrix": True,
    }

    write_json(METRICS_PATH, metrics)

    write_json(
        REPORT_JSON_PATH,
        report,
    )

    # Save class-wise CSV report.
    report_fields = [
        "class",
        "precision",
        "recall",
        "f1-score",
        "support",
    ]

    with REPORT_CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=report_fields,
        )
        writer.writeheader()

        for class_name in rbf.CLASS_ORDER:
            values = report[class_name]
            writer.writerow({
                "class": class_name,
                "precision": values["precision"],
                "recall": values["recall"],
                "f1-score": values["f1-score"],
                "support": int(values["support"]),
            })

    # Save the reproduced confusion matrix.
    with MATRIX_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "Actual / Predicted",
            *rbf.CLASS_ORDER,
        ])

        for class_name, row in zip(
            rbf.CLASS_ORDER,
            matrix,
        ):
            writer.writerow([
                class_name,
                *row.tolist(),
            ])

    # Save all validation predictions for traceability.
    with PREDICTIONS_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "validation_index",
                "image_filename",
                "actual_class",
                "predicted_class",
                "correct",
            ],
        )

        writer.writeheader()

        for index, (actual, predicted, image_path) in enumerate(
            zip(
                y_valid,
                predictions,
                validation.paths,
            )
        ):
            writer.writerow({
                "validation_index": index + 1,
                "image_filename": Path(image_path).name,
                "actual_class": str(actual),
                "predicted_class": str(predicted),
                "correct": bool(actual == predicted),
            })

    metadata = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "selected_candidate": SELECTED_CANDIDATE,
        "model_path": str(
            MODEL_PATH.relative_to(PROJECT_ROOT)
        ),
        "manifest_path": str(
            rbf.MANIFEST_PATH.relative_to(PROJECT_ROOT)
        ),
        "manifest_sha256": manifest_sha256,
        "python_version": __import__("sys").version.split()[0],
        "scikit_learn_version": sklearn.__version__,
        "numpy_version": np.__version__,
        "joblib_version": joblib.__version__,
        "training_images": rbf.TRAINING_COUNT,
        "validation_images": rbf.VALIDATION_COUNT,
        "test_images_used": 0,
        "held_out_test_accessed": False,
        "class_order": list(rbf.CLASS_ORDER),
        "preprocessing": preprocessing,
        "hog_configuration": hog_configuration,
        "svm_configuration": parameters,
        "selection_basis": (
            "Jointly selected after comparing five approved "
            "Linear and RBF SVM candidates using validation data."
        ),
        "grouped_cross_validation_performed": False,
        "independent_test_evaluation_performed": False,
    }

    write_json(
        METADATA_PATH,
        metadata,
    )

    # Verify all required output artifacts.
    required_files = [
        MODEL_PATH,
        METADATA_PATH,
        METRICS_PATH,
        REPORT_JSON_PATH,
        REPORT_CSV_PATH,
        MATRIX_PATH,
        PREDICTIONS_PATH,
    ]

    for path in required_files:
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(
                f"Required artifact missing or empty: {path}"
            )

    print("\n=== SELECTED MODEL TRAINING COMPLETE ===")
    print("[PASS] RBF C=10.0 trained using training images only.")
    print("[PASS] Validation metrics match the approved experiment.")
    print("[PASS] Confusion matrix matches the approved experiment.")
    print("[PASS] Permanent Joblib model saved.")
    print("[PASS] Validation predictions and reports saved.")
    print("[PASS] No held-out test images accessed.")
    print("\nArtifacts directory:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
