from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import compare_rbf_models as rbf

from office_item_classifier.dataset import (
    DatasetManifestError,
    load_split_images,
)


def test_approved_candidates():
    assert rbf.CANDIDATES == [
        ("rbf_c0_1", 0.1),
        ("rbf_c1", 1.0),
        ("rbf_c10", 10.0),
    ]


@pytest.mark.parametrize("c_value", [0.1, 1.0, 10.0])
def test_rbf_configuration(c_value):
    model = rbf.create_rbf_model(c_value)
    params = model.get_params()

    assert params["kernel"] == "rbf"
    assert params["C"] == c_value
    assert params["gamma"] == "scale"
    assert params["class_weight"] is None
    assert params["decision_function_shape"] == "ovr"
    assert params["probability"] is False


def test_unapproved_c_rejected():
    with pytest.raises(ValueError):
        rbf.create_rbf_model(5.0)


def test_summary_schema():
    expected = [
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

    assert rbf.SUMMARY_FIELDS == expected
    assert rbf.TRAINING_COUNT == 812
    assert rbf.VALIDATION_COUNT == 226
    assert len(rbf.CLASS_ORDER) == 8


def test_prediction_timing_uses_eleven_calls():
    class FakeModel:
        def __init__(self):
            self.calls = 0

        def predict(self, features):
            self.calls += 1
            return np.zeros(len(features), dtype=int)

    model = FakeModel()
    features = np.zeros((226, 2), dtype=np.float32)
    reference = np.zeros(226, dtype=int)

    milliseconds = rbf.measure_prediction_time(
        model, features, reference
    )

    # One warm-up plus ten timed predictions.
    assert model.calls == 11
    assert np.isfinite(milliseconds)
    assert milliseconds >= 0


def test_prediction_timing_rejects_wrong_count():
    class FakeModel:
        def predict(self, features):
            return np.zeros(len(features), dtype=int)

    with pytest.raises(ValueError):
        rbf.measure_prediction_time(
            FakeModel(),
            np.zeros((10, 2)),
            np.zeros(10),
        )


def test_model_size_protocol(monkeypatch):
    original_dump = rbf.joblib.dump
    observed = []

    def checked_dump(value, filename, **kwargs):
        observed.append(kwargs.copy())
        return original_dump(value, filename, **kwargs)

    monkeypatch.setattr(rbf.joblib, "dump", checked_dump)

    size = rbf.measure_model_size({
        "synthetic_data": np.arange(8)
    })

    assert size > 0
    assert len(observed) == 1
    assert observed[0]["compress"] == 0
    assert observed[0]["protocol"] == 5


def test_reports_and_confusion_matrix(monkeypatch, tmp_path):
    # All files are written to pytest's temporary directory.
    monkeypatch.setattr(rbf, "OUTPUT_DIR", tmp_path)

    class_counts = [27, 31, 37, 34, 19, 28, 14, 36]

    report = {
        name: {
            "precision": 1.0,
            "recall": 1.0,
            "f1-score": 1.0,
            "support": count,
        }
        for name, count in zip(rbf.CLASS_ORDER, class_counts)
    }

    report_files = rbf.save_classification_report(
        "rbf_c0_1", report
    )

    matrix = np.diag(class_counts)
    matrix_files = rbf.save_confusion_matrix(
        "rbf_c0_1", matrix
    )

    for file_path in report_files + matrix_files:
        assert file_path.is_file()
        assert file_path.stat().st_size > 0

    with report_files[0].open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert [row["class"] for row in rows] == rbf.CLASS_ORDER

    saved_report = json.loads(
        report_files[1].read_text(encoding="utf-8")
    )
    assert list(saved_report) == rbf.CLASS_ORDER

    with matrix_files[0].open(
        newline="", encoding="utf-8"
    ) as handle:
        matrix_rows = list(csv.reader(handle))

    assert matrix_rows[0][1:] == rbf.CLASS_ORDER
    assert len(matrix_rows) == 9
    assert matrix.sum() == 226


def test_existing_loader_blocks_test_split():
    # The existing loader rejects "test" before opening files.
    with pytest.raises(
        DatasetManifestError, match="intentionally blocked"
    ):
        load_split_images(
            PROJECT_ROOT / "unused_manifest.csv",
            PROJECT_ROOT / "dataset",
            "test",
        )

def test_rbf_summary_class_weight_consistency():
    """Check summary schema without running model experiments."""
    import ast

    source_path = PROJECT_ROOT / "scripts" / "compare_rbf_models.py"
    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    result_dicts = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "result"
            for target in node.targets
        )
        and isinstance(node.value, ast.Dict)
    ]

    assert len(result_dicts) == 1

    summary_fields = {
        key.value: value
        for key, value in zip(
            result_dicts[0].keys,
            result_dicts[0].values,
        )
        if isinstance(key, ast.Constant)
        and isinstance(key.value, str)
    }

    assert ast.literal_eval(summary_fields["class_weight"]) == "none"

    for c_value in (0.1, 1.0, 10.0):
        assert rbf.candidate_parameters(c_value)["class_weight"] is None
