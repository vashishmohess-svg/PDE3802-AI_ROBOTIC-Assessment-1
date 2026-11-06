
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

import joblib
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from office_item_classifier.dataset import (
    CLASS_NAMES,
    load_split_images,
)
from office_item_classifier.features import (
    EXPECTED_HOG_FEATURES,
    extract_hog_features,
)


# Approved project paths
MANIFEST_PATH = (
    PROJECT_ROOT
    / "docs"
    / "evidence"
    / "step3.5.5J"
    / "step3.5.5K3_full_split_manifest_proposal.csv"
)

DATASET_ROOT = PROJECT_ROOT / "dataset"

MODEL_PATH = (
    PROJECT_ROOT
    / "results"
    / "baseline"
    / "baseline_hog_linear_svm.joblib"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "results"
    / "model_comparison"
    / "linear"
    / "linear_misclassification_review.csv"
)

VALIDATION_COUNT = 226


# Only these three actual-to-predicted errors are being reviewed.
TARGET_PAIRS = {
    ("Scissors", "Pencil"): 9,
    ("Mug", "Bottle"): 6,
    ("Calculator", "Mouse"): 5,
}


def main() -> None:
    print("=== LINEAR SVM MISCLASSIFICATION REVIEW ===")

    # Check and reload the saved baseline model.
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(MODEL_PATH)

    bundle = joblib.load(MODEL_PATH)

    if not isinstance(bundle, dict) or "model" not in bundle:
        raise RuntimeError("Invalid saved baseline model bundle.")

    model = bundle["model"]

    parameters = model.get_params(deep=False)
    saved_svm = bundle.get("svm")

    if not isinstance(saved_svm, dict):
        raise RuntimeError(
            "Saved SVM configuration metadata is missing."
        )

    # Verify the actual model configuration.
    if (
        parameters.get("kernel") != "linear"
        or parameters.get("C") != 1.0
    ):
        raise RuntimeError(
            "Unexpected baseline SVM configuration."
        )

    # Verify the original saved training configuration.
    if (
        saved_svm.get("kernel") != "linear"
        or saved_svm.get("C") != 1.0
        or saved_svm.get("probability") is not False
    ):
        raise RuntimeError(
            "Saved baseline SVM metadata is incorrect."
        )

    # Scikit-learn 1.9+ may report "deprecated" through
    # get_params() for the deprecated probability parameter.
    # In this state, probability estimates remain disabled.
    if parameters.get("probability") not in (
        False,
        "deprecated",
    ):
        raise RuntimeError(
            "Probability estimates may be enabled."
        )

    print("[PASS] Approved baseline Linear SVM reloaded.")
    print("[PASS] Kernel: linear; C: 1.0.")
    print("[PASS] Probability estimates are disabled.")

    # Load validation images only.
    print("\nLoading approved validation split...")

    validation = load_split_images(
        MANIFEST_PATH,
        DATASET_ROOT,
        "valid",
    )

    if (
        len(validation.labels) != VALIDATION_COUNT
        or len(validation.paths) != VALIDATION_COUNT
        or len(validation.images) != VALIDATION_COUNT
    ):
        raise RuntimeError(
            "Unexpected validation split size."
        )

    print("[PASS] Exactly 226 validation images loaded.")
    print("[PASS] No training or test split requested.")

    # Reproduce the approved HOG feature pipeline.
    print("\nExtracting HOG features...")

    X_valid = extract_hog_features(validation.images)

    if X_valid.shape != (
        VALIDATION_COUNT,
        EXPECTED_HOG_FEATURES,
    ):
        raise RuntimeError(
            "Unexpected validation HOG feature shape."
        )

    print("[PASS] Validation HOG features:", X_valid.shape)

    # Reproduce baseline predictions.
    print("\nGenerating baseline predictions...")

    y_actual = np.asarray(validation.labels).astype(str)
    y_predicted = model.predict(X_valid).astype(str)

    if len(y_predicted) != VALIDATION_COUNT:
        raise RuntimeError(
            "Unexpected prediction count."
        )

    if not set(y_actual).issubset(set(CLASS_NAMES)):
        raise RuntimeError(
            "Unexpected actual class label."
        )

    if not set(y_predicted).issubset(set(CLASS_NAMES)):
        raise RuntimeError(
            "Unexpected predicted class label."
        )

    print("[PASS] Reproduced 226 baseline predictions.")

    # Collect only the three approved error groups.
    rows = []
    observed_counts = Counter()

    for index, (actual, predicted) in enumerate(
        zip(y_actual, y_predicted)
    ):
        pair = (str(actual), str(predicted))

        if pair not in TARGET_PAIRS:
            continue

        observed_counts[pair] += 1

        image_path = Path(
            validation.paths[index]
        ).resolve()

        try:
            relative_path = image_path.relative_to(
                PROJECT_ROOT
            ).as_posix()
        except ValueError as exc:
            raise RuntimeError(
                f"Image path is outside the project: {image_path}"
            ) from exc

        rows.append({
            "validation_index": index + 1,
            "actual_class": str(actual),
            "predicted_class": str(predicted),
            "confusion_group": (
                f"{actual} -> {predicted}"
            ),
            "image_filename": image_path.name,
            "relative_path": relative_path,
            "absolute_path": str(image_path),
        })

    # Confirm that predictions reproduce the expected counts.
    for pair, expected_count in TARGET_PAIRS.items():
        actual_count = observed_counts[pair]

        if actual_count != expected_count:
            raise RuntimeError(
                f"Unexpected count for {pair}: "
                f"expected {expected_count}, got {actual_count}"
            )

    if len(rows) != sum(TARGET_PAIRS.values()):
        raise RuntimeError(
            "Unexpected total review image count."
        )

    # Keep the three error groups together in the CSV.
    pair_order = {
        pair: index
        for index, pair in enumerate(TARGET_PAIRS)
    }

    rows.sort(
        key=lambda row: (
            pair_order[
                (
                    row["actual_class"],
                    row["predicted_class"],
                )
            ],
            row["image_filename"].lower(),
        )
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "validation_index",
        "actual_class",
        "predicted_class",
        "confusion_group",
        "image_filename",
        "relative_path",
        "absolute_path",
    ]

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    print("\n=== REVIEW GROUP COUNTS ===")

    for pair, expected_count in TARGET_PAIRS.items():
        print(
            f"{pair[0]} -> {pair[1]}: "
            f"{observed_counts[pair]} images"
        )

    print("\nTotal images selected:", len(rows))
    print("[PASS] All expected confusion counts reproduced.")
    print("[PASS] Original dataset files were not modified.")
    print("[PASS] Held-out test images were not accessed.")
    print("\nReview CSV:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
