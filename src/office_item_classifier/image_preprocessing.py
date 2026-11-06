
"""Shared image preprocessing for training and prediction.

File images and OpenCV camera frames are converted into the same
128x128 grayscale uint8 representation before HOG extraction.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError


IMAGE_SIZE = (128, 128)  # width, height

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class ImagePreprocessingError(ValueError):
    """Raised when an image cannot be prepared for classification."""


def _validate_image_size(image_size: tuple[int, int]) -> tuple[int, int]:
    if (
        not isinstance(image_size, (tuple, list))
        or len(image_size) != 2
        or any(type(value) is not int or value <= 0 for value in image_size)
    ):
        raise ValueError("image_size must contain two positive integers.")

    return image_size[0], image_size[1]


def preprocess_pil_image(
    image: Image.Image,
    image_size: tuple[int, int] = IMAGE_SIZE,
) -> np.ndarray:
    """Apply the approved EXIF, grayscale and resize pipeline."""

    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL Image.")

    width, height = _validate_image_size(image_size)

    try:
        corrected = ImageOps.exif_transpose(image)
        grayscale = ImageOps.grayscale(corrected)

        pixels = np.asarray(grayscale, dtype=np.uint8)

        resized = cv2.resize(
            pixels,
            (width, height),
            interpolation=cv2.INTER_AREA,
        )

    except (OSError, ValueError, cv2.error) as exc:
        raise ImagePreprocessingError(
            f"Image preprocessing failed: {exc}"
        ) from exc

    expected_shape = (height, width)

    if resized.shape != expected_shape:
        raise ImagePreprocessingError(
            f"Expected image shape {expected_shape}, got {resized.shape}."
        )

    return np.ascontiguousarray(resized, dtype=np.uint8)


def preprocess_image_file(
    image_path: str | Path,
    image_size: tuple[int, int] = IMAGE_SIZE,
) -> np.ndarray:
    """Read and preprocess a supported image file."""

    path = Path(image_path).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    if not path.is_file():
        raise ImagePreprocessingError(
            f"Input path is not a file: {path}"
        )

    if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ImagePreprocessingError(
            f"Unsupported image extension '{path.suffix}'. "
            "Supported formats: JPG, JPEG and PNG."
        )

    try:
        with Image.open(path) as image:
            return preprocess_pil_image(image, image_size)

    except (OSError, UnidentifiedImageError) as exc:
        raise ImagePreprocessingError(
            f"Could not open or decode image: {path}"
        ) from exc


def preprocess_camera_frame(
    frame: np.ndarray,
    image_size: tuple[int, int] = IMAGE_SIZE,
) -> np.ndarray:
    """Convert an OpenCV BGR or grayscale camera frame into model input."""

    if not isinstance(frame, np.ndarray):
        raise TypeError("Camera frame must be a NumPy array.")

    if frame.size == 0:
        raise ImagePreprocessingError("Camera frame is empty.")

    if frame.dtype != np.uint8:
        raise TypeError(
            f"Camera frame must use uint8 data; got {frame.dtype}."
        )

    if frame.ndim == 2:
        image = Image.fromarray(frame)

    elif frame.ndim == 3 and frame.shape[2] == 3:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)

    elif frame.ndim == 3 and frame.shape[2] == 4:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        image = Image.fromarray(rgb)

    else:
        raise ImagePreprocessingError(
            f"Unsupported camera-frame shape: {frame.shape}"
        )

    return preprocess_pil_image(image, image_size)
