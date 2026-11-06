from __future__ import annotations

import cv2
import numpy as np


# All input images must already be preprocessed by dataset.py.
IMAGE_SHAPE = (128, 128)

# HOG descriptor configuration.
HOG_WIN_SIZE = (128, 128)
HOG_BLOCK_SIZE = (16, 16)
HOG_BLOCK_STRIDE = (8, 8)
HOG_CELL_SIZE = (8, 8)
HOG_BINS = 9

# 15 x 15 blocks, with 2 x 2 cells per block and 9 bins per cell.
EXPECTED_HOG_FEATURES = 8100


def create_hog_descriptor() -> cv2.HOGDescriptor:
    """Create the project's fixed HOG descriptor."""

    descriptor = cv2.HOGDescriptor(
        HOG_WIN_SIZE,
        HOG_BLOCK_SIZE,
        HOG_BLOCK_STRIDE,
        HOG_CELL_SIZE,
        HOG_BINS,
    )

    actual_size = descriptor.getDescriptorSize()

    if actual_size != EXPECTED_HOG_FEATURES:
        raise RuntimeError(
            "Unexpected HOG descriptor length: "
            f"expected {EXPECTED_HOG_FEATURES}, got {actual_size}."
        )

    return descriptor


def extract_hog_features(images: np.ndarray) -> np.ndarray:
    """
    Extract one HOG feature vector per preprocessed grayscale image.

    Parameters
    ----------
    images:
        A non-empty uint8 NumPy array with shape
        (number_of_images, 128, 128).

    Returns
    -------
    np.ndarray
        A float32 feature matrix with shape
        (number_of_images, 8100).
    """

    if not isinstance(images, np.ndarray):
        raise TypeError("images must be a NumPy array.")

    if images.ndim != 3:
        raise ValueError(
            "Expected a three-dimensional image array "
            "with shape (N, 128, 128)."
        )

    if images.shape[0] == 0:
        raise ValueError("Cannot extract HOG features from an empty batch.")

    if images.shape[1:] != IMAGE_SHAPE:
        raise ValueError(
            f"Every image must have shape {IMAGE_SHAPE}; "
            f"received {images.shape[1:]}."
        )

    if images.dtype != np.uint8:
        raise TypeError(
            f"Expected uint8 image data; received {images.dtype}."
        )

    descriptor = create_hog_descriptor()

    features = np.empty(
        (images.shape[0], EXPECTED_HOG_FEATURES),
        dtype=np.float32,
    )

    for index, image in enumerate(images):
        image = np.ascontiguousarray(image)

        feature_vector = descriptor.compute(image)

        if feature_vector is None:
            raise RuntimeError(
                f"HOG extraction returned no features for image index {index}."
            )

        feature_vector = np.asarray(
            feature_vector,
            dtype=np.float32,
        ).reshape(-1)

        if feature_vector.size != EXPECTED_HOG_FEATURES:
            raise RuntimeError(
                f"Image index {index}: expected "
                f"{EXPECTED_HOG_FEATURES} features, "
                f"received {feature_vector.size}."
            )

        if not np.isfinite(feature_vector).all():
            raise ValueError(
                f"Non-finite HOG values found at image index {index}."
            )

        features[index] = feature_vector

    return features
