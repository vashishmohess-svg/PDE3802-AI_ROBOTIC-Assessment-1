import unittest

import numpy as np

from office_item_classifier.features import (
    EXPECTED_HOG_FEATURES,
    extract_hog_features,
    create_hog_descriptor,
)


class TestHOGFeatures(unittest.TestCase):

    def setUp(self):
        self.blank = np.zeros((128, 128), dtype=np.uint8)

        self.pattern = np.zeros((128, 128), dtype=np.uint8)
        self.pattern[32:96, 32:96] = 255

    def test_descriptor_has_8100_features(self):
        descriptor = create_hog_descriptor()

        self.assertEqual(
            descriptor.getDescriptorSize(),
            EXPECTED_HOG_FEATURES,
        )

    def test_batch_returns_expected_shape(self):
        images = np.stack([self.blank, self.pattern])

        features = extract_hog_features(images)

        self.assertEqual(features.shape, (2, 8100))

    def test_output_uses_float32(self):
        images = np.stack([self.blank, self.pattern])

        features = extract_hog_features(images)

        self.assertEqual(features.dtype, np.float32)

    def test_all_features_are_finite(self):
        images = np.stack([self.blank, self.pattern])

        features = extract_hog_features(images)

        self.assertTrue(np.isfinite(features).all())

    def test_pattern_produces_nonzero_features(self):
        features = extract_hog_features(
            self.pattern[np.newaxis, :, :]
        )

        self.assertGreater(
            float(np.linalg.norm(features[0])),
            0.0,
        )

    def test_repeated_extraction_is_deterministic(self):
        images = self.pattern[np.newaxis, :, :]

        first = extract_hog_features(images)
        second = extract_hog_features(images)

        np.testing.assert_array_equal(first, second)

    def test_wrong_image_dimensions_are_rejected(self):
        images = np.zeros((1, 64, 64), dtype=np.uint8)

        with self.assertRaises(ValueError):
            extract_hog_features(images)

    def test_wrong_image_dtype_is_rejected(self):
        images = np.zeros((1, 128, 128), dtype=np.float32)

        with self.assertRaises(TypeError):
            extract_hog_features(images)

    def test_empty_batch_is_rejected(self):
        images = np.empty((0, 128, 128), dtype=np.uint8)

        with self.assertRaises(ValueError):
            extract_hog_features(images)

    def test_two_dimensional_input_is_rejected(self):
        image = np.zeros((128, 128), dtype=np.uint8)

        with self.assertRaises(ValueError):
            extract_hog_features(image)


if __name__ == "__main__":
    unittest.main()
