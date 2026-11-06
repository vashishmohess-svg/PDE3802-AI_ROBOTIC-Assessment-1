
from __future__ import annotations

import csv
import hashlib
import json
import math
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
from sklearn.svm import SVC

# Reuse the approved RBF dataset loader and HOG implementation.
import compare_rbf_models as rbf


PROJECT_ROOT = rbf.PROJECT_ROOT

MODEL_DIR = PROJECT_ROOT / "results" / "selected_model"

MODEL_PATH = MODEL_DIR / "rbf_c10_hog_svm.joblib"

METADATA_PATH = MODEL_DIR / "verification_metadata.json"

METRICS_PATH = MODEL_DIR / "validation_metrics.json"

REPORT_JSON_PATH = (
    MODEL_DIR / "validation_classification_report.json"
)

REPORT_CSV_PATH = (
    MODEL_DIR / "validation_classification_report.csv"
)

MATRIX_PATH = MODEL_DIR / "validation_confusion_matrix.csv"

PREDICTIONS_PATH = MODEL_DIR / "validation_predictions.csv"

SELECTED_CANDIDATE = "rbf_c10"
SELECTED_C = 10.0

EXPECTED_ACCURACY = 0.7256637168141593
EXPECTED_MACRO_F1 = 0.6831491956946296


def require(condition: bool, message: str) -> None:
    """Raise a clear error when a verification check fails."""
    if not condition:
        raise RuntimeError(message)


def verify_nested_values(
    actual,
    expected,
    location: str = "report",
) -> None:
    """Compare nested JSON values, allowing tiny float differences."""

    if isinstance(expected, dict):
        require(
            isinstance(actual, dict),
            f"{location}: expected a JSON object.",
        )

        require(
            set(actual) == set(expected),
            f"{location}: JSON keys do not match.",
        )

        for key in expected:
            verify_nested_values(
                actual[key],
                expected[key],
                f"{location}.{key}",
            )

    elif isinstance(expected, list):
        require(
            isinstance(actual, list)
            and len(actual) == len(expected),
            f"{location}: list length mismatch.",
        )

        for index, (actual_item, expected_item) in enumerate(
            zip(actual, expected)
        ):
            verify_nested_values(
                actual_item,
                expected_item,
                f"{location}[{index}]",
            )

    elif isinstance(expected, bool):
        require(
            actual is expected,
            f"{location}: Boolean value mismatch.",
        )

    elif isinstance(expected, (int, float)):
        require(
            isinstance(actual, (int, float))
            and math.isclose(
                float(actual),
                float(expected),
                rel_tol=0,
                abs_tol=1e-12,
            ),
            f"{location}: numerical value mismatch.",
        )

    else:
        require(
            actual == expected,
            f"{location}: value mismatch.",
        )


def read_saved_confusion_matrix() -> np.ndarray:
    """Read and validate the saved eight-class confusion matrix."""

    with MATRIX_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.reader(handle))

    require(
        len(rows) == len(rbf.CLASS_ORDER) + 1,
        "Confusion matrix has an unexpected number of rows.",
    )

    require(
        rows[0] == [
            "Actual / Predicted",
            *rbf.CLASS_ORDER,
        ],
        "Confusion matrix column order is incorrect.",
    )

    require(
        [row[0] for row in rows[1:]] == rbf.CLASS_ORDER,
        "Confusion matrix row order is incorrect.",
    )

    matrix = np.asarray(
        [
            [int(value) for value in row[1:]]
            for row in rows[1:]
        ],
        dtype=int,
    )

    require(
        matrix.shape == (8, 8),
        "Confusion matrix must have shape 8 x 8.",
    )

    require(
        int(matrix.sum()) == rbf.VALIDATION_COUNT,
        "Confusion matrix does not total 226 predictions.",
    )

    return matrix


def verify_classification_reports(
    expected_report: dict,
) -> None:
    """Verify both saved JSON and CSV classification reports."""

    saved_json = json.loads(
        REPORT_JSON_PATH.read_text(encoding="utf-8")
    )

    verify_nested_values(
        saved_json,
        expected_report,
        "classification_report",
    )

    with REPORT_CSV_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    require(
        len(rows) == len(rbf.CLASS_ORDER),
        "Classification CSV must contain exactly 8 classes.",
    )

    for class_name, row in zip(rbf.CLASS_ORDER, rows):
        require(
            row["class"] == class_name,
            "Classification CSV class order is incorrect.",
        )

        values = expected_report[class_name]

        for field in ("precision", "recall", "f1-score"):
            require(
                math.isclose(
                    float(row[field]),
                    float(values[field]),
                    rel_tol=0,
                    abs_tol=1e-12,
                ),
                f"Classification CSV mismatch: "
                f"{class_name} {field}.",
            )

        require(
            int(row["support"]) == int(values["support"]),
            f"Classification CSV support mismatch: {class_name}.",
        )


def main() -> None:
    print("=== SELECTED RBF MODEL INDEPENDENT VERIFICATION ===")

    # 1. Verify that all expected files exist.
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
        require(
            path.is_file() and path.stat().st_size > 0,
            f"Required artifact missing or empty: {path}",
        )

    print("[PASS] All seven selected-model artifacts exist.")

    # 2. Reload the permanent model.
    print("\n=== RELOAD PERMANENT MODEL ===")

    bundle = joblib.load(MODEL_PATH)

    require(
        isinstance(bundle, dict),
        "Saved model bundle is not a dictionary.",
    )

    expected_bundle_keys = {
        "model",
        "class_names",
        "model_name",
        "svm",
        "preprocessing",
        "hog",
        "manifest_sha256",
    }

    require(
        set(bundle) == expected_bundle_keys,
        "Saved model bundle structure is incorrect.",
    )

    model = bundle["model"]

    require(
        isinstance(model, SVC),
        "Reloaded model is not an sklearn SVC.",
    )

    print("[PASS] Permanent Joblib model successfully reloaded.")

    # 3. Verify saved and actual SVC parameters.
    expected_svm = rbf.candidate_parameters(SELECTED_C)

    require(
        bundle["svm"] == expected_svm,
        "Saved SVM configuration does not match RBF C=10.",
    )

    actual_parameters = model.get_params(deep=False)

    require(
        actual_parameters.get("kernel") == "rbf",
        "Incorrect model kernel.",
    )

    require(
        actual_parameters.get("C") == SELECTED_C,
        "Incorrect model C value.",
    )

    require(
        actual_parameters.get("gamma") == "scale",
        "Incorrect model gamma.",
    )

    require(
        actual_parameters.get("class_weight") is None,
        "Incorrect actual SVC class_weight.",
    )

    require(
        actual_parameters.get("decision_function_shape") == "ovr",
        "Incorrect decision function shape.",
    )

    # Scikit-learn 1.9+ can report "deprecated" for this
    # disabled parameter when calling get_params().
    require(
        actual_parameters.get("probability") in (
            False,
            "deprecated",
        ),
        "Probability estimates may be enabled.",
    )

    require(
        bundle["svm"]["probability"] is False,
        "Saved training configuration must explicitly disable probability.",
    )

    require(
        list(bundle["class_names"]) == rbf.CLASS_ORDER,
        "Saved model class order is incorrect.",
    )

    require(
        set(model.classes_) == set(rbf.CLASS_ORDER),
        "Trained model classes do not match the approved classes.",
    )

    print("[PASS] RBF C=10 configuration verified.")
    print("[PASS] All eight model classes verified.")
    print("[PASS] Probability estimates remain disabled.")

    # 4. Verify manifest identity.
    manifest_bytes = rbf.MANIFEST_PATH.read_bytes()

    manifest_sha256 = hashlib.sha256(
        manifest_bytes.replace(b"\r\n", b"\n")
    ).hexdigest().upper()

    require(
        manifest_sha256 == rbf.EXPECTED_MANIFEST_SHA256,
        "Current approved manifest hash mismatch.",
    )

    require(
        bundle["manifest_sha256"] == manifest_sha256,
        "Model bundle manifest hash mismatch.",
    )

    print("[PASS] Approved manifest identity verified.")

    # 5. Verify preprocessing and HOG configuration.
    expected_preprocessing = {
        "orientation": "EXIF transpose",
        "colour": "grayscale",
        "image_size": [128, 128],
        "resize_interpolation": "cv2.INTER_AREA",
    }

    expected_hog = {
        "window_size": list(rbf.HOG_WIN_SIZE),
        "block_size": list(rbf.HOG_BLOCK_SIZE),
        "block_stride": list(rbf.HOG_BLOCK_STRIDE),
        "cell_size": list(rbf.HOG_CELL_SIZE),
        "bins": rbf.HOG_BINS,
        "feature_count": rbf.EXPECTED_HOG_FEATURES,
    }

    require(
        bundle["preprocessing"] == expected_preprocessing,
        "Preprocessing configuration mismatch.",
    )

    require(
        bundle["hog"] == expected_hog,
        "HOG configuration mismatch.",
    )

    require(
        model.n_features_in_ == rbf.EXPECTED_HOG_FEATURES,
        "Model input feature count is incorrect.",
    )

    print("[PASS] Preprocessing and HOG configuration verified.")

    # 6. Verify execution metadata and metrics.
    metadata = json.loads(
        METADATA_PATH.read_text(encoding="utf-8")
    )

    metrics = json.loads(
        METRICS_PATH.read_text(encoding="utf-8")
    )

    require(
        metadata["selected_candidate"] == SELECTED_CANDIDATE,
        "Metadata selected candidate mismatch.",
    )

    require(
        metadata["manifest_sha256"] == manifest_sha256,
        "Metadata manifest hash mismatch.",
    )

    require(
        metadata["training_images"] == rbf.TRAINING_COUNT
        and metadata["validation_images"] == rbf.VALIDATION_COUNT,
        "Metadata split counts mismatch.",
    )

    require(
        metadata["test_images_used"] == 0
        and metadata["held_out_test_accessed"] is False,
        "Metadata indicates held-out test access.",
    )

    require(
        metadata["independent_test_evaluation_performed"] is False,
        "Independent test evaluation must not have occurred.",
    )

    require(
        metadata["class_order"] == rbf.CLASS_ORDER,
        "Metadata class ordering mismatch.",
    )

    require(
        metrics["selected_candidate"] == SELECTED_CANDIDATE,
        "Metrics selected candidate mismatch.",
    )

    require(
        metrics["training_images"] == rbf.TRAINING_COUNT
        and metrics["validation_images"] == rbf.VALIDATION_COUNT,
        "Metrics split counts mismatch.",
    )

    require(
        metrics["test_images_used"] == 0
        and metrics["independent_test_evaluation_performed"] is False,
        "Metrics indicate held-out test access.",
    )


    print("[PASS] Metadata and held-out test safeguards verified.")

    # 7. Load validation images only.
    print("\n=== RECREATE VALIDATION PREDICTIONS ===")

    validation = rbf.load_split_images(
        rbf.MANIFEST_PATH,
        rbf.DATASET_ROOT,
        "valid",
    )

    require(
        len(validation.labels) == rbf.VALIDATION_COUNT
        and len(validation.images) == rbf.VALIDATION_COUNT
        and len(validation.paths) == rbf.VALIDATION_COUNT,
        "Validation split size mismatch.",
    )

    y_actual = np.asarray(validation.labels).astype(str)

    X_valid = rbf.extract_hog_features(validation.images)

    require(
        X_valid.shape == (
            rbf.VALIDATION_COUNT,
            rbf.EXPECTED_HOG_FEATURES,
        ),
        "Validation feature shape mismatch.",
    )

    predictions = model.predict(X_valid).astype(str)

    require(
        len(predictions) == rbf.VALIDATION_COUNT,
        "Unexpected number of validation predictions.",
    )

    print("[PASS] Exactly 226 validation images loaded.")
    print("[PASS] No training or test split requested.")
    print("[PASS] Validation HOG features recreated.")

    # 8. Compare every prediction with the saved prediction record.
    with PREDICTIONS_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as handle:
        saved_predictions = list(csv.DictReader(handle))

    require(
        len(saved_predictions) == rbf.VALIDATION_COUNT,
        "Saved prediction CSV must contain 226 records.",
    )

    for index, (actual, predicted, image_path, saved) in enumerate(
        zip(
            y_actual,
            predictions,
            validation.paths,
            saved_predictions,
        )
    ):
        require(
            int(saved["validation_index"]) == index + 1,
            f"Validation index mismatch at row {index + 1}.",
        )

        require(
            saved["image_filename"] == Path(image_path).name,
            f"Image filename mismatch at row {index + 1}.",
        )

        require(
            saved["actual_class"] == str(actual),
            f"Actual class mismatch at row {index + 1}.",
        )

        require(
            saved["predicted_class"] == str(predicted),
            f"Predicted class mismatch at row {index + 1}.",
        )

        require(
            saved["correct"].lower() == str(
                actual == predicted
            ).lower(),
            f"Correctness field mismatch at row {index + 1}.",
        )

    print("[PASS] All 226 saved predictions reproduced exactly.")

    # 9. Independently calculate classification metrics.
    accuracy = float(
        accuracy_score(y_actual, predictions)
    )

    macro_f1 = float(
        f1_score(
            y_actual,
            predictions,
            labels=rbf.CLASS_ORDER,
            average="macro",
            zero_division=0,
        )
    )

    matrix = confusion_matrix(
        y_actual,
        predictions,
        labels=rbf.CLASS_ORDER,
    )

    report = classification_report(
        y_actual,
        predictions,
        labels=rbf.CLASS_ORDER,
        target_names=rbf.CLASS_ORDER,
        output_dict=True,
        zero_division=0,
    )

    # Compare against the previous approved RBF experiment.
    require(
        math.isclose(
            accuracy,
            EXPECTED_ACCURACY,
            rel_tol=0,
            abs_tol=1e-12,
        ),
        "Recreated accuracy does not match approved RBF C=10 result.",
    )

    require(
        math.isclose(
            macro_f1,
            EXPECTED_MACRO_F1,
            rel_tol=0,
            abs_tol=1e-12,
        ),
        "Recreated macro-F1 does not match approved RBF C=10 result.",
    )

    require(
        math.isclose(
            accuracy,
            float(metrics["validation_accuracy"]),
            rel_tol=0,
            abs_tol=1e-12,
        ),
        "Accuracy does not match saved verification metrics.",
    )

    require(
        math.isclose(
            macro_f1,
            float(metrics["validation_macro_f1"]),
            rel_tol=0,
            abs_tol=1e-12,
        ),
        "Macro-F1 does not match saved verification metrics.",
    )

    print("[PASS] Validation accuracy reproduced:", f"{accuracy:.6f}")
    print("[PASS] Validation macro-F1 reproduced:", f"{macro_f1:.6f}")

    # 10. Verify confusion matrix and classification reports.
    saved_matrix = read_saved_confusion_matrix()

    require(
        np.array_equal(matrix, saved_matrix),
        "Saved confusion matrix does not match recreated predictions.",
    )

    verify_classification_reports(report)

    print("[PASS] Saved confusion matrix reproduced exactly.")
    print("[PASS] Saved CSV and JSON classification reports verified.")

    # 11. Verify support-vector count and serialized size.
    support_vector_count = int(
        model.support_vectors_.shape[0]
    )

    require(
        support_vector_count == metrics["support_vector_count"],
        "Support-vector count mismatch.",
    )

    actual_model_size = MODEL_PATH.stat().st_size

    require(
        actual_model_size == metrics["model_size_bytes"],
        "Saved model size differs from recorded model size.",
    )

    print("[PASS] Support vectors:", support_vector_count)
    print("[PASS] Saved model size:", actual_model_size, "bytes")

    print("\n=== SELECTED MODEL VERIFICATION COMPLETE ===")
    print("[PASS] Permanent model reload successful.")
    print("[PASS] SVM configuration and manifest identity verified.")
    print("[PASS] All 226 validation predictions reproduced.")
    print("[PASS] Accuracy, macro-F1 and confusion matrix reproduced.")
    print("[PASS] Classification reports verified.")
    print("[PASS] Model size and support-vector count verified.")
    print("[PASS] No held-out test images accessed.")


if __name__ == "__main__":
    main()
