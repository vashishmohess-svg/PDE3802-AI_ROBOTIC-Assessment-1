"""Office-item prediction module for the selected RBF SVM model.

This module loads the trained HOG + RBF SVM model and provides
prediction capabilities for image files and camera frames.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import cv2
import joblib
import numpy as np

from .dataset import CLASS_NAMES
from .features import EXPECTED_HOG_FEATURES, extract_hog_features
from .image_preprocessing import (
    ImagePreprocessingError,
    preprocess_camera_frame,
    preprocess_image_file,
)


@dataclass(frozen=True)
class PredictionResult:
    """Result of a classification operation."""

    predicted_class: str | None
    confidence: float | None
    input_source: Literal["image_file", "camera_frame"]
    status: Literal["success", "failure"]
    error_message: str | None


class ModelLoadError(RuntimeError):
    """Raised when the trained model cannot be loaded."""


class PredictionError(RuntimeError):
    """Raised when prediction processing fails."""


class OfficeItemPredictor:
    """Predictor for office-item classification using the selected RBF SVM model."""

    def __init__(self, model_path: str | Path):
        """Load the trained model and verify its configuration."""
        self.model_path = Path(model_path)
        self._model = None
        self._load_model()

    def _load_model(self) -> None:
        """Load and validate the trained Joblib model."""
        if not self.model_path.is_file():
            raise ModelLoadError(
                f"Model file not found: {self.model_path}"
            )

        try:
            loaded = joblib.load(self.model_path)
        except Exception as exc:
            raise ModelLoadError(
                f"Failed to load model from {self.model_path}: {exc}"
            ) from exc

        # Handle dictionary structure from selected model
        if isinstance(loaded, dict):
            if "svm" not in loaded:
                raise ModelLoadError("Model dict missing 'svm' key.")
            if "class_names" not in loaded:
                raise ModelLoadError("Model dict missing 'class_names' key.")
            
            self._model = loaded
            svm_config = loaded["svm"]
            self._class_names = loaded["class_names"]
        else:
            raise ModelLoadError(
                f"Unexpected model type: {type(loaded)}"
            )

        # Verify SVM configuration
        if not isinstance(svm_config, dict):
            raise ModelLoadError("SVM configuration is not a dictionary.")

        if svm_config.get("kernel") != "rbf":
            raise ModelLoadError(
                f"Expected RBF kernel, got {svm_config.get('kernel')}."
            )

        if svm_config.get("C") != 10.0:
            raise ModelLoadError(
                f"Expected C=10.0, got C={svm_config.get('C')}."
            )

        if svm_config.get("probability"):
            raise ModelLoadError(
                "Probability estimates should be disabled for the selected model."
            )

        # Verify class names
        if len(self._class_names) != 8:
            raise ModelLoadError(
                f"Expected 8 classes, got {len(self._class_names)}."
            )

        if not np.array_equal(self._class_names, CLASS_NAMES):
            raise ModelLoadError(
                "Model class order does not match expected class names."
            )

    def predict_image_file(
        self,
        image_path: str | Path,
    ) -> PredictionResult:
        """Predict the class of an image file."""
        try:
            preprocessed = preprocess_image_file(image_path)
            return self._predict_preprocessed(
                preprocessed,
                input_source="image_file",
            )
        except (FileNotFoundError, ImagePreprocessingError) as exc:
            return PredictionResult(
                predicted_class=None,
                confidence=None,
                input_source="image_file",
                status="failure",
                error_message=str(exc),
            )
        except Exception as exc:
            return PredictionResult(
                predicted_class=None,
                confidence=None,
                input_source="image_file",
                status="failure",
                error_message=f"Unexpected error: {exc}",
            )

    def predict_camera_frame(
        self,
        frame: np.ndarray,
    ) -> PredictionResult:
        """Predict the class of a camera frame."""
        try:
            preprocessed = preprocess_camera_frame(frame)
            return self._predict_preprocessed(
                preprocessed,
                input_source="camera_frame",
            )
        except (ImagePreprocessingError, TypeError) as exc:
            return PredictionResult(
                predicted_class=None,
                confidence=None,
                input_source="camera_frame",
                status="failure",
                error_message=str(exc),
            )
        except Exception as exc:
            return PredictionResult(
                predicted_class=None,
                confidence=None,
                input_source="camera_frame",
                status="failure",
                error_message=f"Unexpected error: {exc}",
            )

    def _predict_preprocessed(
        self,
        preprocessed: np.ndarray,
        input_source: Literal["image_file", "camera_frame"],
    ) -> PredictionResult:
        """Predict from a preprocessed image array."""
        try:
            # Ensure shape is (1, 128, 128) for batch processing
            if preprocessed.ndim == 2:
                preprocessed = preprocessed[np.newaxis, ...]

            # Extract HOG features
            features = extract_hog_features(preprocessed)

            if features.shape[1] != EXPECTED_HOG_FEATURES:
                raise PredictionError(
                    f"Expected {EXPECTED_HOG_FEATURES} HOG features, "
                    f"got {features.shape[1]}."
                )

            # The model is stored as a dict with SVM parameters
            # We need to reconstruct the SVC and use it for prediction
            from sklearn.svm import SVC
            
            svm_config = self._model["svm"]
            svc = SVC(
                kernel=svm_config["kernel"],
                C=svm_config["C"],
                gamma=svm_config["gamma"],
                class_weight=svm_config["class_weight"],
                decision_function_shape=svm_config["decision_function_shape"],
                probability=svm_config["probability"],
            )
            
            # The model dict should contain the fitted SVC
            if "model" in self._model:
                svc = self._model["model"]
            else:
                raise ModelLoadError("Model dict missing fitted 'model' key.")

            # Make prediction
            prediction = svc.predict(features)[0]
            predicted_class = str(prediction)

            # The selected SVM model does not have probability estimates enabled
            confidence = None

            return PredictionResult(
                predicted_class=predicted_class,
                confidence=confidence,
                input_source=input_source,
                status="success",
                error_message=None,
            )

        except Exception as exc:
            raise PredictionError(f"Prediction failed: {exc}") from exc

    @property
    def class_names(self) -> tuple[str, ...]:
        """Return the supported class names."""
        return tuple(self._class_names)

    @property
    def model_info(self) -> dict:
        """Return information about the loaded model."""
        svm_config = self._model["svm"]
        svc = self._model["model"]
        return {
            "kernel": svm_config["kernel"],
            "C": svm_config["C"],
            "gamma": svm_config["gamma"],
            "probability": svm_config["probability"],
            "n_classes": len(self._class_names),
            "classes": list(self._class_names),
            "n_support": svc.n_support_.sum() if hasattr(svc, "n_support_") else None,
        }
