
from __future__ import annotations

import csv
import hashlib
import json
import platform
import statistics
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

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

from office_item_classifier.dataset import load_split_images
from office_item_classifier.features import (
    EXPECTED_HOG_FEATURES,
    HOG_WIN_SIZE,
    HOG_BLOCK_SIZE,
    HOG_BLOCK_STRIDE,
    HOG_CELL_SIZE,
    HOG_BINS,
    extract_hog_features,
)


# Fixed project configuration
CLASS_NAMES = [
    "Bottle",
    "Calculator",
    "Keyboard",
    "Mouse",
    "Mug",
    "Notebook",
    "Pencil",
    "Scissors",
]

TRAINING_COUNT = 812
VALIDATION_COUNT = 226
EXPECTED_BASELINE_ACCURACY = 155 / 226
EXPECTED_BASELINE_MACRO_F1 = 0.6497

MANIFEST_RELATIVE_PATH = (
    "docs/evidence/step3.5.5J/"
    "step3.5.5K3_full_split_manifest_proposal.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "results" / "model_comparison" / "linear"
REPORT_DIR = OUTPUT_DIR / "reports"
MATRIX_DIR = OUTPUT_DIR / "confusion_matrices"

CANDIDATES = [
    {
        "name": "linear_baseline",
        "display_name": "HOG + Linear SVM",
        "kernel": "linear",
        "C": 1.0,
        "gamma": "scale",
        "class_weight": None,
        "probability": False,
        "decision_function_shape": "ovr",
    },
    {
        "name": "linear_balanced",
        "display_name": "HOG + Balanced Linear SVM",
        "kernel": "linear",
        "C": 1.0,
        "gamma": "scale",
        "class_weight": "balanced",
        "probability": False,
        "decision_function_shape": "ovr",
    },
]

TIMING_REPEATS = 10


def write_json(path: Path, content: dict | list) -> None:
    path.write_text(
        json.dumps(content, indent=2, allow_nan=False),
        encoding="utf-8",
    )


def canonical_sha256(path: Path) -> str:
    content = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()


def measure_prediction_time(
    model: SVC,
    features: np.ndarray,
) -> float:
    """Return median classifier-only milliseconds per image."""

    # Warm-up prediction is excluded from the measurements.
    model.predict(features)

    timings = []

    for _ in range(TIMING_REPEATS):
        started = time.perf_counter()
        model.predict(features)
        elapsed = time.perf_counter() - started

        timings.append(elapsed)

    median_seconds = statistics.median(timings)

    return float(
        median_seconds * 1000.0 / len(features)
    )


def measure_serialized_size(bundle: dict) -> int:
    """Measure consistent uncompressed joblib serialization size."""

    with tempfile.TemporaryDirectory(
        prefix="office_item_model_size_"
    ) as temporary_directory:

        temporary_path = (
            Path(temporary_directory) / "candidate.joblib"
        )

        joblib.dump(
            bundle,
            temporary_path,
            compress=0,
            protocol=5,
        )

        if not temporary_path.is_file():
            raise RuntimeError("Temporary model serialization failed.")

        size = temporary_path.stat().st_size

        if size <= 0:
            raise RuntimeError("Serialized model size is invalid.")

        return int(size)


def save_report(
    name: str,
    report: dict,
) -> None:

    json_path = REPORT_DIR / f"{name}_report.json"
    csv_path = REPORT_DIR / f"{name}_report.csv"

    write_json(json_path, report)

    fields = [
        "class",
        "precision",
        "recall",
        "f1-score",
        "support",
    ]

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )
        writer.writeheader()

        for class_name in CLASS_NAMES:
            values = report[class_name]

            writer.writerow({
                "class": class_name,
                "precision": float(values["precision"]),
                "recall": float(values["recall"]),
                "f1-score": float(values["f1-score"]),
                "support": int(values["support"]),
            })


def save_confusion_matrix(
    name: str,
    matrix: np.ndarray,
) -> None:

    csv_path = MATRIX_DIR / f"{name}.csv"
    png_path = MATRIX_DIR / f"{name}.png"

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.writer(handle)
        writer.writerow(["Actual / Predicted", *CLASS_NAMES])

        for class_name, row in zip(CLASS_NAMES, matrix):
            writer.writerow([
                class_name,
                *[int(value) for value in row],
            ])

    figure, axis = plt.subplots(figsize=(10, 8))

    image = axis.imshow(matrix, interpolation="nearest")
    figure.colorbar(image, ax=axis)

    axis.set(
        xticks=np.arange(len(CLASS_NAMES)),
        yticks=np.arange(len(CLASS_NAMES)),
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        xlabel="Predicted class",
        ylabel="Actual class",
        title=f"{name} — Validation Confusion Matrix",
    )

    plt.setp(
        axis.get_xticklabels(),
        rotation=40,
        ha="right",
        rotation_mode="anchor",
    )

    threshold = matrix.max() / 2.0

    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            axis.text(
                column_index,
                row_index,
                str(int(matrix[row_index, column_index])),
                ha="center",
                va="center",
                color=(
                    "white"
                    if matrix[row_index, column_index] > threshold
                    else "black"
                ),
            )

    figure.tight_layout()
    figure.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(figure)


def verify_required_outputs(
    required_files: list[Path],
) -> None:

    for path in required_files:

        if not path.is_file():
            raise RuntimeError(
                f"Required output is missing: {path}"
            )

        if path.stat().st_size <= 0:
            raise RuntimeError(
                f"Required output is empty: {path}"
            )


def main() -> None:

    started = time.perf_counter()

    manifest = PROJECT_ROOT / MANIFEST_RELATIVE_PATH
    dataset_root = PROJECT_ROOT / "dataset"

    if not manifest.is_file():
        raise FileNotFoundError(manifest)

    if not dataset_root.is_dir():
        raise FileNotFoundError(dataset_root)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MATRIX_DIR.mkdir(parents=True, exist_ok=True)

    manifest_hash = canonical_sha256(manifest)

    print("=== LINEAR SVM MODEL COMPARISON ===")

    print("\n=== LOAD APPROVED TRAINING DATA ===")

    training = load_split_images(
        manifest,
        dataset_root,
        "train",
    )

    if len(training.labels) != TRAINING_COUNT:
        raise RuntimeError(
            f"Expected {TRAINING_COUNT} training images; "
            f"received {len(training.labels)}."
        )

    print("Training images:", training.images.shape)

    print("\n=== LOAD APPROVED VALIDATION DATA ===")

    validation = load_split_images(
        manifest,
        dataset_root,
        "valid",
    )

    if len(validation.labels) != VALIDATION_COUNT:
        raise RuntimeError(
            f"Expected {VALIDATION_COUNT} validation images; "
            f"received {len(validation.labels)}."
        )

    print("Validation images:", validation.images.shape)

    y_train = np.asarray(training.labels)
    y_valid = np.asarray(validation.labels)

    if set(y_train) != set(CLASS_NAMES):
        raise RuntimeError("Training classes do not match.")

    if set(y_valid) != set(CLASS_NAMES):
        raise RuntimeError("Validation classes do not match.")

    train_paths = {
        path.resolve() for path in training.paths
    }
    valid_paths = {
        path.resolve() for path in validation.paths
    }

    if not train_paths.isdisjoint(valid_paths):
        raise RuntimeError(
            "Training and validation contain shared image paths."
        )

    print("\n=== EXTRACT SHARED HOG FEATURES ===")

    feature_started = time.perf_counter()
    X_train = extract_hog_features(training.images)
    train_feature_seconds = time.perf_counter() - feature_started

    feature_started = time.perf_counter()
    X_valid = extract_hog_features(validation.images)
    validation_feature_seconds = time.perf_counter() - feature_started

    if X_train.shape != (TRAINING_COUNT, EXPECTED_HOG_FEATURES):
        raise RuntimeError("Unexpected training feature shape.")

    if X_valid.shape != (VALIDATION_COUNT, EXPECTED_HOG_FEATURES):
        raise RuntimeError("Unexpected validation feature shape.")

    if not np.isfinite(X_train).all():
        raise RuntimeError("Invalid training feature values.")

    if not np.isfinite(X_valid).all():
        raise RuntimeError("Invalid validation feature values.")

    print("Training features:", X_train.shape)
    print("Validation features:", X_valid.shape)

    # These settings describe the common feature pipeline.
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

    summary_rows = []
    required_files = []

    for configuration in CANDIDATES:

        name = configuration["name"]

        print(f"\n=== FIT {configuration['display_name']} ===")

        model = SVC(
            kernel=configuration["kernel"],
            C=configuration["C"],
            class_weight=configuration["class_weight"],
            decision_function_shape="ovr",
            probability=False,
        )

        fit_started = time.perf_counter()
        model.fit(X_train, y_train)
        fit_seconds = time.perf_counter() - fit_started

        if model.get_params(deep=False)["probability"] is not False:
            raise RuntimeError(
                f"{name}: probability fitting is unexpectedly enabled."
            )

        predictions = model.predict(X_valid)

        accuracy = float(
            accuracy_score(y_valid, predictions)
        )

        macro_f1 = float(
            f1_score(
                y_valid,
                predictions,
                labels=CLASS_NAMES,
                average="macro",
                zero_division=0,
            )
        )

        report = classification_report(
            y_valid,
            predictions,
            labels=CLASS_NAMES,
            target_names=CLASS_NAMES,
            output_dict=True,
            zero_division=0,
        )

        matrix = confusion_matrix(
            y_valid,
            predictions,
            labels=CLASS_NAMES,
        )

        prediction_ms_per_image = measure_prediction_time(
            model,
            X_valid,
        )

        bundle = {
            "model": model,
            "class_names": CLASS_NAMES,
            "model_name": configuration["display_name"],
            "svm": {
                "kernel": configuration["kernel"],
                "C": configuration["C"],
                "gamma": configuration["gamma"],
                "class_weight": configuration["class_weight"],
                "probability": False,
                "decision_function_shape": "ovr",
            },
            "preprocessing": preprocessing,
            "hog": hog_configuration,
            "manifest_sha256": manifest_hash,
        }

        model_size_bytes = measure_serialized_size(bundle)

        # Save per-candidate reports and confusion matrices.
        save_report(name, report)
        save_confusion_matrix(name, matrix)

        report_json = REPORT_DIR / f"{name}_report.json"
        report_csv = REPORT_DIR / f"{name}_report.csv"
        matrix_csv = MATRIX_DIR / f"{name}.csv"
        matrix_png = MATRIX_DIR / f"{name}.png"

        required_files.extend([
            report_json,
            report_csv,
            matrix_csv,
            matrix_png,
        ])

        row = {
            "candidate": name,
            "kernel": configuration["kernel"],
            "C": configuration["C"],
            "gamma": configuration["gamma"],
            "class_weight": (
                configuration["class_weight"] or "none"
            ),
            "probability": False,
            "validation_accuracy": accuracy,
            "validation_macro_f1": macro_f1,
            "fit_seconds": float(fit_seconds),
            "prediction_median_ms_per_image": (
                prediction_ms_per_image
            ),
            "model_size_bytes": model_size_bytes,
            "support_vector_count": int(
                model.support_vectors_.shape[0]
            ),
            "validation_images": VALIDATION_COUNT,
            "training_images": TRAINING_COUNT,
            "test_images_used": 0,
        }

        summary_rows.append(row)

        print(f"Accuracy: {accuracy * 100:.2f}%")
        print(f"Macro-F1: {macro_f1:.4f}")
        print(f"Fit time: {fit_seconds:.3f} seconds")
        print(
            "Prediction median: "
            f"{prediction_ms_per_image:.6f} ms/image"
        )
        print(f"Model size: {model_size_bytes:,} bytes")

        del model

    # Candidate A must reproduce the verified Step 3 baseline.
    baseline_metrics_path = (
        PROJECT_ROOT
        / "results"
        / "baseline"
        / "validation_metrics.json"
    )

    if not baseline_metrics_path.is_file():
        raise FileNotFoundError(
            "Original Step 3 baseline metrics are missing."
        )

    baseline_metrics = json.loads(
        baseline_metrics_path.read_text(encoding="utf-8")
    )

    baseline_row = next(
        row for row in summary_rows
        if row["candidate"] == "linear_baseline"
    )

    if not np.isclose(
        baseline_row["validation_accuracy"],
        baseline_metrics["validation_accuracy"],
        rtol=0,
        atol=1e-12,
    ):
        raise RuntimeError(
            "Retrained Linear baseline accuracy does not "
            "match the original Step 3 result."
        )

    if not np.isclose(
        baseline_row["validation_macro_f1"],
        baseline_metrics["validation_macro_f1"],
        rtol=0,
        atol=1e-12,
    ):
        raise RuntimeError(
            "Retrained Linear baseline macro-F1 does not "
            "match the original Step 3 result."
        )

    print("\n[PASS] Candidate A reproduces the original baseline.")

    # Save common comparison evidence.
    summary_csv = OUTPUT_DIR / "comparison_summary.csv"
    summary_json = OUTPUT_DIR / "comparison_summary.json"
    metadata_json = OUTPUT_DIR / "run_metadata.json"

    fields = list(summary_rows[0].keys())

    with summary_csv.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    write_json(summary_json, summary_rows)

    run_metadata = {
        "created_at": datetime.now().astimezone().isoformat(),
        "python_version": platform.python_version(),
        "scikit_learn_version": sklearn.__version__,
        "numpy_version": np.__version__,
        "opencv_version": cv2.__version__,
        "joblib_version": joblib.__version__,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "manifest_sha256": manifest_hash,
        "classes": CLASS_NAMES,
        "training_images": TRAINING_COUNT,
        "validation_images": VALIDATION_COUNT,
        "test_images_used": 0,
        "held_out_test_accessed": False,
        "preprocessing": preprocessing,
        "hog_configuration": hog_configuration,
        "training_feature_extraction_seconds": (
            train_feature_seconds
        ),
        "validation_feature_extraction_seconds": (
            validation_feature_seconds
        ),
        "prediction_timing_method": (
            "One warm-up prediction followed by 10 timed "
            "predictions over all 226 validation feature vectors; "
            "median elapsed time divided by image count."
        ),
        "model_size_method": (
            "Uncompressed joblib serialization, protocol 5, "
            "measured in a temporary directory."
        ),
        "candidates": CANDIDATES,
        "validation_used_for_model_selection": True,
        "independent_test_evaluation_performed": False,
        "total_script_seconds": (
            time.perf_counter() - started
        ),
    }

    write_json(metadata_json, run_metadata)

    required_files.extend([
        summary_csv,
        summary_json,
        metadata_json,
    ])

    verify_required_outputs(required_files)

    # Verify the saved result files contain the expected candidates.
    saved_summary = json.loads(
        summary_json.read_text(encoding="utf-8")
    )

    if len(saved_summary) != 2:
        raise RuntimeError(
            "Expected exactly two Linear SVM candidates."
        )

    saved_names = {
        row["candidate"] for row in saved_summary
    }

    if saved_names != {
        "linear_baseline",
        "linear_balanced",
    }:
        raise RuntimeError(
            "Saved candidate names do not match the protocol."
        )

    print("\n=== LINEAR COMPARISON OUTPUTS VERIFIED ===")

    for path in required_files:
        print(
            f"[PASS] {path.relative_to(PROJECT_ROOT)} "
            f"({path.stat().st_size:,} bytes)"
        )

    print("\n=== LINEAR SVM IMPLEMENTATION RUN COMPLETE ===")
    print("[PASS] Both predefined candidates were evaluated.")
    print("[PASS] Candidate A reproduced the Step 3 baseline.")
    print("[PASS] All required comparison evidence was saved.")
    print("[PASS] Only training and validation splits were loaded.")
    print("[PASS] No held-out test images were accessed.")


if __name__ == "__main__":
    main()
