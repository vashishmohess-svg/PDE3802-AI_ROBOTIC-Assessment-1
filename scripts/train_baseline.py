from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Allow this script to import the package from the project's src layout.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

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
    HOG_BINS,
    HOG_BLOCK_SIZE,
    HOG_BLOCK_STRIDE,
    HOG_CELL_SIZE,
    HOG_WIN_SIZE,
    extract_hog_features,
)


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
SVM_C = 1.0


def canonical_file_sha256(path: Path) -> str:
    """Calculate SHA-256 after normalising Windows line endings to LF."""

    content = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()


def write_confusion_matrix_csv(path: Path, matrix: np.ndarray) -> None:
    """Write the confusion matrix with readable class labels."""

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Actual / Predicted", *CLASS_NAMES])

        for class_name, row in zip(CLASS_NAMES, matrix):
            writer.writerow([class_name, *[int(value) for value in row]])


def write_classification_report_csv(
    path: Path,
    report: dict,
) -> None:
    """Write per-class precision, recall, F1 and support."""

    fields = ["class", "precision", "recall", "f1-score", "support"]

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for class_name in CLASS_NAMES:
            values = report[class_name]
            writer.writerow({
                "class": class_name,
                "precision": values["precision"],
                "recall": values["recall"],
                "f1-score": values["f1-score"],
                "support": int(values["support"]),
            })


def save_confusion_matrix_plot(
    path: Path,
    matrix: np.ndarray,
) -> None:
    """Save a labelled validation confusion-matrix figure."""

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
        title="Baseline HOG + Linear SVM — Validation Confusion Matrix",
    )

    plt.setp(
        axis.get_xticklabels(),
        rotation=40,
        ha="right",
        rotation_mode="anchor",
    )

    threshold = matrix.max() / 2.0 if matrix.size else 0

    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            axis.text(
                column_index,
                row_index,
                str(int(matrix[row_index, column_index])),
                ha="center",
                va="center",
                color="white" if matrix[row_index, column_index] > threshold else "black",
            )

    figure.tight_layout()
    figure.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    started = time.perf_counter()

    manifest_path = (
        PROJECT_ROOT
        / "docs"
        / "evidence"
        / "step3.5.5J"
        / "step3.5.5K3_full_split_manifest_proposal.csv"
    )

    dataset_root = PROJECT_ROOT / "dataset"
    output_dir = PROJECT_ROOT / "results" / "baseline"

    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    if not dataset_root.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_root}")

    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== BASELINE HOG + LINEAR SVM ===")
    print("Project:", PROJECT_ROOT)
    print("Manifest:", manifest_path)
    print("Output:", output_dir)

    print("\n=== LOAD TRAINING DATA ===")
    training = load_split_images(
        manifest_path,
        dataset_root,
        "train",
    )

    if len(training.labels) != TRAINING_COUNT:
        raise RuntimeError(
            f"Expected {TRAINING_COUNT} training images; "
            f"received {len(training.labels)}."
        )

    print("Training images:", training.images.shape)

    print("\n=== LOAD VALIDATION DATA ===")
    validation = load_split_images(
        manifest_path,
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
        raise RuntimeError("Training labels do not match the expected eight classes.")

    if set(y_valid) != set(CLASS_NAMES):
        raise RuntimeError("Validation labels do not match the expected eight classes.")

    train_paths = {path.resolve() for path in training.paths}
    valid_paths = {path.resolve() for path in validation.paths}

    if not train_paths.isdisjoint(valid_paths):
        raise RuntimeError("Training and validation contain a shared image path.")

    print("\n=== EXTRACT TRAINING HOG FEATURES ===")
    feature_started = time.perf_counter()
    X_train = extract_hog_features(training.images)
    train_feature_seconds = time.perf_counter() - feature_started

    print("Training features:", X_train.shape)

    print("\n=== EXTRACT VALIDATION HOG FEATURES ===")
    feature_started = time.perf_counter()
    X_valid = extract_hog_features(validation.images)
    validation_feature_seconds = time.perf_counter() - feature_started

    print("Validation features:", X_valid.shape)

    if X_train.shape != (TRAINING_COUNT, EXPECTED_HOG_FEATURES):
        raise RuntimeError("Unexpected training feature-matrix shape.")

    if X_valid.shape != (VALIDATION_COUNT, EXPECTED_HOG_FEATURES):
        raise RuntimeError("Unexpected validation feature-matrix shape.")

    if not np.isfinite(X_train).all() or not np.isfinite(X_valid).all():
        raise RuntimeError("Non-finite feature values found.")

    print("\n=== FIT BASELINE CLASSIFIER ===")
    model = SVC(
        kernel="linear",
        C=SVM_C,
        decision_function_shape="ovr",
    )

    fit_started = time.perf_counter()
    model.fit(X_train, y_train)
    fit_seconds = time.perf_counter() - fit_started

    print("Classifier:", type(model).__name__)
    print("Kernel:", model.kernel)
    print("C:", model.C)
    print("Probability estimates enabled:", model.get_params(deep=False)["probability"] is True)
    print("Support vectors:", int(model.support_vectors_.shape[0]))

    print("\n=== VALIDATION PREDICTIONS ===")
    predictions = model.predict(X_valid)

    accuracy = accuracy_score(y_valid, predictions)
    macro_f1 = f1_score(
        y_valid,
        predictions,
        labels=CLASS_NAMES,
        average="macro",
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_valid,
        predictions,
        labels=CLASS_NAMES,
    )

    report = classification_report(
        y_valid,
        predictions,
        labels=CLASS_NAMES,
        target_names=CLASS_NAMES,
        output_dict=True,
        zero_division=0,
    )

    print(f"Validation accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Validation macro-F1: {macro_f1:.4f}")

    print("\n=== PER-CLASS VALIDATION RESULTS ===")
    for class_name in CLASS_NAMES:
        values = report[class_name]
        print(
            f"{class_name:12s} "
            f"Precision={values['precision']:.4f}  "
            f"Recall={values['recall']:.4f}  "
            f"F1={values['f1-score']:.4f}  "
            f"Support={int(values['support'])}"
        )

    print("\n=== SAVE BASELINE ARTIFACTS ===")

    bundle = {
        "model": model,
        "class_names": CLASS_NAMES,
        "model_name": "HOG + Linear SVM",
        "svm": {
            "kernel": "linear",
            "C": SVM_C,
            "probability": False,
            "decision_function_shape": "ovr",
        },
        "preprocessing": {
            "orientation": "EXIF transpose",
            "colour": "grayscale",
            "image_size": [128, 128],
            "resize_interpolation": "cv2.INTER_AREA",
        },
        "hog": {
            "window_size": list(HOG_WIN_SIZE),
            "block_size": list(HOG_BLOCK_SIZE),
            "block_stride": list(HOG_BLOCK_STRIDE),
            "cell_size": list(HOG_CELL_SIZE),
            "bins": HOG_BINS,
            "feature_count": EXPECTED_HOG_FEATURES,
        },
        "manifest_sha256": canonical_file_sha256(manifest_path),
    }

    model_path = output_dir / "baseline_hog_linear_svm.joblib"
    joblib.dump(bundle, model_path)

    metrics = {
        "model": "HOG + Linear SVM",
        "validation_images": VALIDATION_COUNT,
        "training_images": TRAINING_COUNT,
        "class_count": len(CLASS_NAMES),
        "validation_accuracy": float(accuracy),
        "validation_accuracy_percent": float(accuracy * 100),
        "validation_macro_f1": float(macro_f1),
        "training_feature_shape": list(X_train.shape),
        "validation_feature_shape": list(X_valid.shape),
        "fit_seconds": fit_seconds,
        "training_feature_extraction_seconds": train_feature_seconds,
        "validation_feature_extraction_seconds": validation_feature_seconds,
        "held_out_test_accessed": False,
    }

    metrics_path = output_dir / "validation_metrics.json"
    metrics_path.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    report_path = output_dir / "validation_classification_report.json"
    report_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    report_csv_path = output_dir / "validation_classification_report.csv"
    write_classification_report_csv(report_csv_path, report)

    matrix_csv_path = output_dir / "validation_confusion_matrix.csv"
    write_confusion_matrix_csv(matrix_csv_path, matrix)

    matrix_plot_path = output_dir / "validation_confusion_matrix.png"
    save_confusion_matrix_plot(matrix_plot_path, matrix)

    metadata = {
        "created_at": datetime.now().astimezone().isoformat(),
        "python_version": sys.version.split()[0],
        "scikit_learn_version": sklearn.__version__,
        "manifest_sha256": bundle["manifest_sha256"],
        "classes": CLASS_NAMES,
        "training_images": TRAINING_COUNT,
        "validation_images": VALIDATION_COUNT,
        "test_images_used": 0,
        "model_configuration": bundle["svm"],
        "preprocessing": bundle["preprocessing"],
        "hog_configuration": bundle["hog"],
        "fit_seconds": fit_seconds,
        "total_pipeline_seconds": time.perf_counter() - started,
    }

    metadata_path = output_dir / "run_metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print("\n=== SAVED FILES ===")
    for path in [
        model_path,
        metrics_path,
        report_path,
        report_csv_path,
        matrix_csv_path,
        matrix_plot_path,
        metadata_path,
    ]:
        print(path.relative_to(PROJECT_ROOT))

    print("\n=== BASELINE TRAINING COMPLETE ===")
    print(f"Validation accuracy: {accuracy * 100:.2f}%")
    print(f"Validation macro-F1: {macro_f1:.4f}")
    print(f"Model fit time: {fit_seconds:.2f} seconds")
    print("[PASS] Model fitted using training data only.")
    print("[PASS] Validation data used for evaluation only.")
    print("[PASS] Held-out test split was not accessed.")


if __name__ == "__main__":
    main()
