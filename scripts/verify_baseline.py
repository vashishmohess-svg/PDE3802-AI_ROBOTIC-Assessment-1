from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import joblib
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.svm import SVC

from office_item_classifier.dataset import load_split_images
from office_item_classifier.features import extract_hog_features


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


def canonical_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    manifest = (
        PROJECT_ROOT
        / "docs"
        / "evidence"
        / "step3.5.5J"
        / "step3.5.5K3_full_split_manifest_proposal.csv"
    )
    dataset_root = PROJECT_ROOT / "dataset"
    output_dir = PROJECT_ROOT / "results" / "baseline"

    model_path = output_dir / "baseline_hog_linear_svm.joblib"
    metrics_path = output_dir / "validation_metrics.json"
    matrix_path = output_dir / "validation_confusion_matrix.csv"
    report_path = output_dir / "validation_classification_report.json"
    metadata_path = output_dir / "run_metadata.json"

    required_files = [
        model_path,
        metrics_path,
        matrix_path,
        report_path,
        metadata_path,
        output_dir / "validation_classification_report.csv",
        output_dir / "validation_confusion_matrix.png",
    ]

    print("=== CHECK BASELINE ARTIFACTS ===")
    for path in required_files:
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Missing or empty artifact: {path.name}")
        print(f"[PASS] {path.name}: {path.stat().st_size:,} bytes")

    print("\n=== RELOAD SAVED MODEL ===")
    bundle = joblib.load(model_path)

    if not isinstance(bundle, dict):
        raise TypeError("Saved model bundle is not a dictionary.")

    model = bundle.get("model")

    if not isinstance(model, SVC):
        raise TypeError("Saved estimator is not an sklearn SVC.")

    if bundle.get("class_names") != CLASS_NAMES:
        raise RuntimeError("Saved class order does not match the approved class order.")

    if model.kernel != "linear":
        raise RuntimeError("Saved SVC does not use a linear kernel.")

    if model.C != 1.0:
        raise RuntimeError("Saved SVC has an unexpected C value.")

    probability_setting = model.get_params(deep=False)["probability"]

    # scikit-learn 1.9 uses the string "deprecated" as the default
    # sentinel. This default does not enable probability estimates.
    if probability_setting is True:
        raise RuntimeError("Probability estimates were unexpectedly enabled.")

    if probability_setting not in (False, "deprecated"):
        raise RuntimeError(
            f"Unexpected probability setting: {probability_setting!r}"
        )

    # Confirm through the public API that this fitted model cannot
    # produce probabilities.
    try:
        model.predict_proba(
            np.zeros((1, model.n_features_in_), dtype=np.float32)
        )
    except AttributeError:
        print("[PASS] predict_proba is unavailable; no probabilities were fitted.")
    else:
        raise RuntimeError(
            "predict_proba unexpectedly returned values for this model."
        )

    print("[PASS] Model reloaded as sklearn SVC.")
    print("[PASS] Linear kernel and C=1.0 verified.")
    print(f"[PASS] Probability setting is {probability_setting!r}.")
    print("[PASS] Probability estimates are not enabled.")
    print("[PASS] Eight-class order verified.")

    print("\n=== VERIFY MANIFEST IDENTITY ===")
    expected_hash = bundle.get("manifest_sha256")
    actual_hash = canonical_sha256(manifest)

    if expected_hash != actual_hash:
        raise RuntimeError("Saved model manifest hash does not match the current manifest.")

    print("[PASS] Saved model references the current approved manifest.")

    print("\n=== RECREATE VALIDATION PREDICTIONS ===")
    validation = load_split_images(
        manifest,
        dataset_root,
        "valid",
    )

    if len(validation.labels) != 226:
        raise RuntimeError("Unexpected validation image count.")

    X_valid = extract_hog_features(validation.images)
    y_valid = np.asarray(validation.labels)

    predictions = model.predict(X_valid)

    if len(predictions) != 226:
        raise RuntimeError("Unexpected prediction count.")

    accuracy = accuracy_score(y_valid, predictions)
    macro_f1 = f1_score(
        y_valid,
        predictions,
        labels=CLASS_NAMES,
        average="macro",
        zero_division=0,
    )

    print("[PASS] Reloaded model generated 226 validation predictions.")

    print("\n=== COMPARE WITH RECORDED METRICS ===")
    saved_metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    if not np.isclose(
        accuracy,
        saved_metrics["validation_accuracy"],
        rtol=0,
        atol=1e-12,
    ):
        raise RuntimeError("Reproduced accuracy does not match saved metrics.")

    if not np.isclose(
        macro_f1,
        saved_metrics["validation_macro_f1"],
        rtol=0,
        atol=1e-12,
    ):
        raise RuntimeError("Reproduced macro-F1 does not match saved metrics.")

    print(f"[PASS] Accuracy reproduced: {accuracy * 100:.2f}%")
    print(f"[PASS] Macro-F1 reproduced: {macro_f1:.4f}")

    print("\n=== VERIFY CONFUSION MATRIX ===")
    matrix = confusion_matrix(
        y_valid,
        predictions,
        labels=CLASS_NAMES,
    )

    with matrix_path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    saved_class_order = rows[0][1:]
    saved_matrix = np.asarray(
        [[int(value) for value in row[1:]] for row in rows[1:]],
        dtype=np.int64,
    )

    if saved_class_order != CLASS_NAMES:
        raise RuntimeError("Saved confusion-matrix class order is incorrect.")

    if not np.array_equal(matrix, saved_matrix):
        raise RuntimeError("Reproduced confusion matrix differs from the saved CSV.")

    print("[PASS] Saved confusion matrix exactly matches reloaded predictions.")

    print("\nConfusion matrix (rows = actual, columns = predicted):")
    print(" " * 13 + " ".join(f"{name[:5]:>6s}" for name in CLASS_NAMES))

    for name, row in zip(CLASS_NAMES, matrix):
        print(f"{name:12s}" + " ".join(f"{int(value):6d}" for value in row))

    print("\n=== LARGEST CLASSIFICATION CONFUSIONS ===")
    errors = []

    for actual_index, actual_name in enumerate(CLASS_NAMES):
        for predicted_index, predicted_name in enumerate(CLASS_NAMES):
            if actual_index != predicted_index:
                count = int(matrix[actual_index, predicted_index])
                if count:
                    errors.append((count, actual_name, predicted_name))

    for count, actual_name, predicted_name in sorted(errors, reverse=True)[:10]:
        print(f"{actual_name} predicted as {predicted_name}: {count}")

    print("\n=== CHECK TEST-SET SEPARATION ===")
    saved_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    if saved_metrics.get("held_out_test_accessed") is not False:
        raise RuntimeError("Metrics do not confirm test-set separation.")

    if saved_metadata.get("test_images_used") != 0:
        raise RuntimeError("Metadata does not confirm zero test images used.")

    print("[PASS] Recorded metrics state that held-out test data was not accessed.")
    print("[PASS] Run metadata records zero test images used.")

    print("\n=== BASELINE RELOAD VERIFICATION COMPLETE ===")
    print("[PASS] Saved model, metrics and confusion matrix are consistent.")
    print("[INFO] Only the validation split was loaded by this verification.")
    print("[INFO] The held-out test split remains reserved.")


if __name__ == "__main__":
    main()
