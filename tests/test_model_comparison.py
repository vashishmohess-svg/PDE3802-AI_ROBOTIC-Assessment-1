
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest
from sklearn.metrics import classification_report
from sklearn.svm import SVC


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "compare_models.py"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

spec = importlib.util.spec_from_file_location(
    "step4_compare_models",
    SCRIPT_PATH,
)

if spec is None or spec.loader is None:
    raise RuntimeError("Could not load comparison script.")

comparison = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = comparison
spec.loader.exec_module(comparison)


def test_candidate_configurations():
    assert len(comparison.CANDIDATES) == 2

    baseline, balanced = comparison.CANDIDATES

    assert baseline["kernel"] == "linear"
    assert baseline["C"] == 1.0
    assert baseline["class_weight"] is None

    assert balanced["kernel"] == "linear"
    assert balanced["C"] == 1.0
    assert balanced["class_weight"] == "balanced"

    assert all(
        candidate["probability"] is False
        for candidate in comparison.CANDIDATES
    )


def test_approved_class_order():
    assert comparison.CLASS_NAMES == [
        "Bottle",
        "Calculator",
        "Keyboard",
        "Mouse",
        "Mug",
        "Notebook",
        "Pencil",
        "Scissors",
    ]


def test_training_and_validation_constants():
    assert comparison.TRAINING_COUNT == 812
    assert comparison.VALIDATION_COUNT == 226
    assert comparison.EXPECTED_HOG_FEATURES == 8100


def test_timing_configuration():
    assert comparison.TIMING_REPEATS == 10


def test_prediction_timing_returns_positive_value():
    features = np.array(
        [
            [0.0, 0.0],
            [0.1, 0.1],
            [1.0, 1.0],
            [1.1, 1.1],
        ],
        dtype=np.float32,
    )

    labels = np.array(
        ["Bottle", "Bottle", "Mug", "Mug"]
    )

    model = SVC(
        kernel="linear",
        C=1.0,
        probability=False,
    )
    model.fit(features, labels)

    result = comparison.measure_prediction_time(
        model,
        features,
    )

    assert np.isfinite(result)
    assert result > 0


def test_serialized_model_size_is_positive():
    features = np.array(
        [[0.0, 0.0], [1.0, 1.0]],
        dtype=np.float32,
    )
    labels = np.array(["Bottle", "Mug"])

    model = SVC(kernel="linear", probability=False)
    model.fit(features, labels)

    size = comparison.measure_serialized_size(
        {"model": model}
    )

    assert isinstance(size, int)
    assert size > 0


def test_classification_report_saving(tmp_path, monkeypatch):
    monkeypatch.setattr(
        comparison,
        "REPORT_DIR",
        tmp_path,
    )

    classes = comparison.CLASS_NAMES

    report = classification_report(
        classes,
        classes,
        labels=classes,
        target_names=classes,
        output_dict=True,
        zero_division=0,
    )

    comparison.save_report("test_candidate", report)

    csv_path = tmp_path / "test_candidate_report.csv"
    json_path = tmp_path / "test_candidate_report.json"

    assert csv_path.is_file()
    assert json_path.is_file()
    assert csv_path.stat().st_size > 0
    assert json_path.stat().st_size > 0


def test_confusion_matrix_saving(tmp_path, monkeypatch):
    monkeypatch.setattr(
        comparison,
        "MATRIX_DIR",
        tmp_path,
    )

    matrix = np.eye(8, dtype=np.int64)

    comparison.save_confusion_matrix(
        "test_candidate",
        matrix,
    )

    csv_path = tmp_path / "test_candidate.csv"
    png_path = tmp_path / "test_candidate.png"

    assert csv_path.is_file()
    assert png_path.is_file()
    assert csv_path.stat().st_size > 0
    assert png_path.stat().st_size > 0
