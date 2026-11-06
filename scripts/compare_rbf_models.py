
from __future__ import annotations

import csv
import hashlib
import json
import statistics
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import cv2
import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.svm import SVC

from office_item_classifier.dataset import (
    CLASS_NAMES,
    EXPECTED_MANIFEST_SHA256,
    load_split_images,
)
from office_item_classifier.features import (
    EXPECTED_HOG_FEATURES,
    HOG_BINS,
    HOG_BLOCK_SIZE,
    HOG_BLOCK_STRIDE,
    HOG_CELL_SIZE,
    HOG_WIN_SIZE,
    extract_hog_features,
)

# Approved project paths.
MANIFEST_PATH = (
    PROJECT_ROOT
    / "docs"
    / "evidence"
    / "step3.5.5J"
    / "step3.5.5K3_full_split_manifest_proposal.csv"
)

DATASET_ROOT = PROJECT_ROOT / "dataset"

OUTPUT_DIR = (
    PROJECT_ROOT / "results" / "model_comparison" / "rbf"
)

# Fixed approved class ordering.
CLASS_ORDER = list(CLASS_NAMES)

TRAINING_COUNT = 812
VALIDATION_COUNT = 226

# Member 1's exact approved candidate identifiers.
CANDIDATES = [
    ("rbf_c0_1", 0.1),
    ("rbf_c1", 1.0),
    ("rbf_c10", 10.0),
]

# Exact shared CSV/JSON comparison-summary fields.
SUMMARY_FIELDS = [
    "candidate",
    "kernel",
    "C",
    "gamma",
    "class_weight",
    "probability",
    "validation_accuracy",
    "validation_macro_f1",
    "fit_seconds",
    "prediction_median_ms_per_image",
    "model_size_bytes",
    "support_vector_count",
    "validation_images",
    "training_images",
    "test_images_used",
]


def candidate_parameters(c_value: float) -> dict:
    """Return one approved RBF SVM configuration."""
    return {
        "kernel": "rbf",
        "C": c_value,
        "gamma": "scale",
        "class_weight": None,
        "decision_function_shape": "ovr",
        "probability": False,
    }


def create_rbf_model(c_value: float) -> SVC:
    """Construct an approved RBF SVM without fitting it."""
    if c_value not in {0.1, 1.0, 10.0}:
        raise ValueError("Unapproved RBF C value.")

    return SVC(**candidate_parameters(c_value))


def write_json(path: Path, data) -> None:
    path.write_text(
        json.dumps(data, indent=2, allow_nan=False),
        encoding="utf-8",
    )


def write_csv(path: Path, rows: list[dict], fields: list) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="raise",
        )
        writer.writeheader()
        writer.writerows(rows)


def measure_prediction_time(
    model: SVC,
    features: np.ndarray,
    reference_predictions: np.ndarray,
) -> float:
    """
    One warm-up, followed by ten timed full-batch predictions.

    Return median milliseconds per image.
    HOG feature extraction is excluded.
    """
    count = len(reference_predictions)

    if count != VALIDATION_COUNT or len(features) != count:
        raise ValueError("Unexpected validation batch size.")

    # Warm-up prediction.
    warmup = model.predict(features)

    if not np.array_equal(warmup, reference_predictions):
        raise RuntimeError("Warm-up predictions are inconsistent.")

    elapsed_seconds = []

    for _ in range(10):
        started = time.perf_counter()
        repeated = model.predict(features)
        elapsed = time.perf_counter() - started

        if not np.array_equal(repeated, reference_predictions):
            raise RuntimeError("Timed predictions are inconsistent.")

        elapsed_seconds.append(elapsed)

    return float(
        statistics.median(elapsed_seconds)
        * 1000.0
        / count
    )


def measure_model_size(bundle: dict) -> int:
    """
    Measure the complete model bundle using uncompressed
    joblib serialization with protocol 5.

    Temporary serialized files are removed automatically.
    """
    with tempfile.TemporaryDirectory() as temporary_dir:
        destination = Path(temporary_dir) / "rbf_candidate.joblib"

        saved_paths = joblib.dump(
            bundle,
            destination,
            compress=0,
            protocol=5,
        )

        size_bytes = sum(
            Path(path).stat().st_size
            for path in saved_paths
        )

    if size_bytes <= 0:
        raise RuntimeError("Serialized model size is invalid.")

    return int(size_bytes)


def save_classification_report(
    candidate: str,
    report: dict,
) -> list[Path]:
    directory = OUTPUT_DIR / "reports"
    directory.mkdir(parents=True, exist_ok=True)

    rows = []

    for class_name in CLASS_ORDER:
        values = report[class_name]

        rows.append({
            "class": class_name,
            "precision": float(values["precision"]),
            "recall": float(values["recall"]),
            "f1-score": float(values["f1-score"]),
            "support": int(values["support"]),
        })

    csv_path = directory / f"{candidate}_report.csv"
    json_path = directory / f"{candidate}_report.json"

    write_csv(
        csv_path,
        rows,
        ["class", "precision", "recall", "f1-score", "support"],
    )
    write_json(json_path, report)

    return [csv_path, json_path]


def save_confusion_matrix(
    candidate: str,
    matrix: np.ndarray,
) -> list[Path]:
    directory = OUTPUT_DIR / "confusion_matrices"
    directory.mkdir(parents=True, exist_ok=True)

    if matrix.shape != (8, 8):
        raise RuntimeError("Expected an 8 x 8 confusion matrix.")

    if int(matrix.sum()) != VALIDATION_COUNT:
        raise RuntimeError("Confusion matrix total is incorrect.")

    csv_path = directory / f"{candidate}.csv"
    png_path = directory / f"{candidate}.png"

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.writer(handle)

        writer.writerow(["Actual / Predicted", *CLASS_ORDER])

        for class_name, row in zip(CLASS_ORDER, matrix):
            writer.writerow([
                class_name,
                *[int(value) for value in row],
            ])

    figure, axis = plt.subplots(figsize=(10, 8))

    axis.imshow(matrix, interpolation="nearest")

    axis.set_xticks(range(8))
    axis.set_yticks(range(8))
    axis.set_xticklabels(CLASS_ORDER, rotation=45, ha="right")
    axis.set_yticklabels(CLASS_ORDER)

    axis.set_xlabel("Predicted class")
    axis.set_ylabel("Actual class")
    axis.set_title(f"{candidate} - Validation Confusion Matrix")

    threshold = matrix.max() / 2.0

    for row_index in range(8):
        for column_index in range(8):
            value = int(matrix[row_index, column_index])

            axis.text(
                column_index,
                row_index,
                str(value),
                ha="center",
                va="center",
                color=(
                    "white"
                    if value > threshold
                    else "black"
                ),
            )

    figure.tight_layout()
    figure.savefig(png_path, dpi=150)
    plt.close(figure)

    return [csv_path, png_path]


def main() -> None:
    print("=== MEMBER 2 - RBF SVM MODEL COMPARISON ===")

    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(MANIFEST_PATH)

    if not DATASET_ROOT.is_dir():
        raise FileNotFoundError(DATASET_ROOT)

    if len(CLASS_ORDER) != 8:
        raise RuntimeError("Unexpected number of classes.")

    # Manifest metadata can be validated, but test image files
    # must never be opened during Step 4.
    manifest_bytes = MANIFEST_PATH.read_bytes()

    manifest_sha256 = hashlib.sha256(
        manifest_bytes.replace(b"\r\n", b"\n")
    ).hexdigest().upper()

    if manifest_sha256 != EXPECTED_MANIFEST_SHA256:
        raise RuntimeError("Approved manifest SHA-256 mismatch.")

    print("\nLoading approved training split...")
    training = load_split_images(
        MANIFEST_PATH,
        DATASET_ROOT,
        "train",
    )

    print("Loading approved validation split...")
    validation = load_split_images(
        MANIFEST_PATH,
        DATASET_ROOT,
        "valid",
    )

    if len(training.labels) != TRAINING_COUNT:
        raise RuntimeError("Expected 812 training images.")

    if len(validation.labels) != VALIDATION_COUNT:
        raise RuntimeError("Expected 226 validation images.")

    y_train = np.asarray(training.labels)
    y_valid = np.asarray(validation.labels)

    if set(y_train) != set(CLASS_ORDER):
        raise RuntimeError("Unexpected training labels.")

    if set(y_valid) != set(CLASS_ORDER):
        raise RuntimeError("Unexpected validation labels.")

    train_paths = {
        path.resolve() for path in training.paths
    }
    validation_paths = {
        path.resolve() for path in validation.paths
    }

    if not train_paths.isdisjoint(validation_paths):
        raise RuntimeError(
            "Training and validation paths overlap."
        )

    print("Training images:", len(y_train))
    print("Validation images:", len(y_valid))

    print("\nExtracting approved HOG features...")

    feature_started = time.perf_counter()

    X_train = extract_hog_features(training.images)
    X_valid = extract_hog_features(validation.images)

    feature_seconds = time.perf_counter() - feature_started

    if X_train.shape != (812, EXPECTED_HOG_FEATURES):
        raise RuntimeError("Invalid training HOG shape.")

    if X_valid.shape != (226, EXPECTED_HOG_FEATURES):
        raise RuntimeError("Invalid validation HOG shape.")

    if not (
        np.isfinite(X_train).all()
        and np.isfinite(X_valid).all()
    ):
        raise RuntimeError("Non-finite HOG features detected.")

    preprocessing = {
        "orientation": "EXIF transpose",
        "colour": "grayscale",
        "image_size": [128, 128],
        "resize_interpolation": "cv2.INTER_AREA",
    }

    hog_configuration = {
        "window_size": list(HOG_WIN_SIZE),
        "block_size": list(HOG_BLOCK_SIZE),
        "block_stride": list(HOG_BLOCK_STRIDE),
        "cell_size": list(HOG_CELL_SIZE),
        "bins": HOG_BINS,
        "feature_count": EXPECTED_HOG_FEATURES,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = []
    expected_files = []

    for candidate_name, c_value in CANDIDATES:
        print(f"\n=== {candidate_name} ===")

        parameters = candidate_parameters(c_value)
        model = create_rbf_model(c_value)

        # Fit using training features only.
        fit_started = time.perf_counter()
        model.fit(X_train, y_train)
        fit_seconds = time.perf_counter() - fit_started

        # Evaluate using validation features only.
        predictions = model.predict(X_valid)

        accuracy = float(
            accuracy_score(y_valid, predictions)
        )

        macro_f1 = float(
            f1_score(
                y_valid,
                predictions,
                labels=CLASS_ORDER,
                average="macro",
                zero_division=0,
            )
        )

        report = classification_report(
            y_valid,
            predictions,
            labels=CLASS_ORDER,
            target_names=CLASS_ORDER,
            output_dict=True,
            zero_division=0,
        )

        matrix = confusion_matrix(
            y_valid,
            predictions,
            labels=CLASS_ORDER,
        )

        prediction_ms = measure_prediction_time(
            model,
            X_valid,
            predictions,
        )

        # Match the project's baseline model-bundle structure.
        bundle = {
            "model": model,
            "class_names": CLASS_ORDER,
            "model_name": f"HOG + RBF SVM C={c_value}",
            "svm": parameters,
            "preprocessing": preprocessing,
            "hog": hog_configuration,
            "manifest_sha256": manifest_sha256,
        }

        model_size = measure_model_size(bundle)

        expected_files.extend(
            save_classification_report(candidate_name, report)
        )

        expected_files.extend(
            save_confusion_matrix(candidate_name, matrix)
        )

        result = {
            "candidate": candidate_name,
            "kernel": "rbf",
            "C": c_value,
            "gamma": "scale",
            "class_weight": None,
            "probability": False,
            "validation_accuracy": accuracy,
            "validation_macro_f1": macro_f1,
            "fit_seconds": float(fit_seconds),
            "prediction_median_ms_per_image": prediction_ms,
            "model_size_bytes": model_size,
            "support_vector_count": int(
                model.support_vectors_.shape[0]
            ),
            "validation_images": VALIDATION_COUNT,
            "training_images": TRAINING_COUNT,
            "test_images_used": 0,
        }

        if list(result) != SUMMARY_FIELDS:
            raise RuntimeError("Summary field specification mismatch.")

        summary.append(result)

        print(f"Accuracy: {accuracy * 100:.2f}%")
        print(f"Macro-F1: {macro_f1:.4f}")
        print(f"Fit time: {fit_seconds:.3f} seconds")
        print(f"Prediction: {prediction_ms:.4f} ms/image")
        print(f"Model size: {model_size} bytes")

    comparison_csv = OUTPUT_DIR / "comparison_summary.csv"
    comparison_json = OUTPUT_DIR / "comparison_summary.json"
    metadata_path = OUTPUT_DIR / "run_metadata.json"

    write_csv(comparison_csv, summary, SUMMARY_FIELDS)
    write_json(comparison_json, summary)

    metadata = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "implemented_by": "Member 2",
        "python_version": sys.version.split()[0],
        "scikit_learn_version": sklearn.__version__,
        "numpy_version": np.__version__,
        "opencv_version": cv2.__version__,
        "manifest_path": str(
            MANIFEST_PATH.relative_to(PROJECT_ROOT)
        ),
        "manifest_sha256": manifest_sha256,
        "training_images": TRAINING_COUNT,
        "validation_images": VALIDATION_COUNT,
        "test_images_used": 0,
        "class_order": CLASS_ORDER,
        "excluded_image": (
            "Pencil/"
            "00038_jpg.rf.7f94c208054cb0f13467f3967c7ed71c.jpg"
        ),
        "preprocessing": preprocessing,
        "hog_configuration": hog_configuration,
        "candidate_parameters": [
            {
                "candidate": name,
                **candidate_parameters(value),
            }
            for name, value in CANDIDATES
        ],
        "feature_extraction_seconds": feature_seconds,
        "prediction_timing_method": (
            "One warm-up followed by 10 timed predictions "
            "on the 226-image validation feature matrix; "
            "median milliseconds per image; "
            "HOG extraction excluded."
        ),
        "model_size_method": (
            "Uncompressed joblib model-bundle serialization "
            "using protocol 5; temporary files removed."
        ),
        "validation_selection_method": (
            "Three predefined RBF configurations compared "
            "using the approved validation split; "
            "grouped cross-validation not performed."
        ),
        "evaluation_limitation": (
            "Validation results are used for model selection, "
            "not as independent final test estimates."
        ),
    }

    write_json(metadata_path, metadata)

    expected_files.extend([
        comparison_csv,
        comparison_json,
        metadata_path,
    ])

    for path in expected_files:
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(
                f"Required evidence missing or empty: {path}"
            )

    if len(summary) != 3:
        raise RuntimeError("Expected exactly 3 RBF candidates.")

    print("\n=== RBF COMPARISON FINISHED ===")
    print("All three approved candidates evaluated.")
    print("Expected evidence files verified.")
    print("No held-out test images requested by this script.")
    print("Output:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
