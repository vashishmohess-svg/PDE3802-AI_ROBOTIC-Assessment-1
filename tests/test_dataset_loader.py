"""Tests for the approved manifest-driven dataset loader."""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from office_item_classifier.dataset import (
    CLASS_NAMES,
    DatasetManifestError,
    load_image,
    load_manifest,
    load_split_images,
    load_split_records,
)


MANIFEST_PATH = (
    PROJECT_ROOT
    / "docs/evidence/step3.5.5J/"
    / "step3.5.5K3_full_split_manifest_proposal.csv"
)

DATASET_ROOT = PROJECT_ROOT / "dataset"


class TestDatasetManifest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.records = load_manifest(
            MANIFEST_PATH,
            DATASET_ROOT,
        )

    def test_manifest_has_1142_records(self):
        self.assertEqual(len(self.records), 1142)

    def test_all_eight_classes_are_present(self):
        actual = {record.class_name for record in self.records}
        self.assertEqual(actual, set(CLASS_NAMES))

    def test_training_selection_has_812_eligible_images(self):
        records = load_split_records(
            MANIFEST_PATH, DATASET_ROOT, "train"
        )

        self.assertEqual(len(records), 812)
        self.assertTrue(
            all(record.proposed_split == "train" for record in records)
        )
        self.assertTrue(
            all(
                record.effective_training_eligible == "YES"
                for record in records
            )
        )

    def test_validation_selection_has_226_images(self):
        records = load_split_records(
            MANIFEST_PATH, DATASET_ROOT, "valid"
        )

        self.assertEqual(len(records), 226)
        self.assertTrue(
            all(record.proposed_split == "valid" for record in records)
        )

    def test_pixelated_pencil_image_is_excluded_from_training(self):
        training = load_split_records(
            MANIFEST_PATH, DATASET_ROOT, "train"
        )

        excluded_filename = (
            "00038_jpg.rf.7f94c208054cb0f13467f3967c7ed71c.jpg"
        )

        self.assertNotIn(
            excluded_filename,
            {record.filename for record in training},
        )

        excluded_records = [
            record for record in self.records
            if record.filename == excluded_filename
        ]

        self.assertEqual(len(excluded_records), 1)
        self.assertEqual(
            excluded_records[0].effective_training_eligible, "NO"
        )

    def test_all_selected_training_and_validation_paths_exist(self):
        for split in ("train", "valid"):
            records = load_split_records(
                MANIFEST_PATH, DATASET_ROOT, split
            )
            self.assertTrue(
                all(record.source_path.is_file() for record in records)
            )

    def test_test_split_is_blocked(self):
        with self.assertRaisesRegex(
            DatasetManifestError, "intentionally blocked"
        ):
            load_split_records(
                MANIFEST_PATH, DATASET_ROOT, "test"
            )

    def test_test_image_is_rejected_before_file_access(self):
        test_record = next(
            record for record in self.records
            if record.proposed_split == "test"
        )

        with self.assertRaisesRegex(
            DatasetManifestError, "cannot be loaded"
        ):
            load_image(test_record)

    def test_training_and_validation_sample_preprocessing(self):
        for split in ("train", "valid"):
            record = load_split_records(
                MANIFEST_PATH, DATASET_ROOT, split
            )[0]

            image = load_image(record)

            self.assertEqual(image.shape, (128, 128))
            self.assertEqual(str(image.dtype), "uint8")


    def test_full_training_and_validation_images_decode(self):
        """Decode all approved training and validation images."""

        training = load_split_images(
            MANIFEST_PATH, DATASET_ROOT, "train"
        )

        validation = load_split_images(
            MANIFEST_PATH, DATASET_ROOT, "valid"
        )

        self.assertEqual(training.images.shape, (812, 128, 128))
        self.assertEqual(validation.images.shape, (226, 128, 128))

        self.assertEqual(str(training.images.dtype), "uint8")
        self.assertEqual(str(validation.images.dtype), "uint8")

        self.assertEqual(len(training.labels), 812)
        self.assertEqual(len(validation.labels), 226)

        self.assertEqual(len(training.paths), 812)
        self.assertEqual(len(validation.paths), 226)

        expected_counts = {
            "Bottle": (95, 27),
            "Calculator": (104, 31),
            "Keyboard": (122, 37),
            "Mouse": (108, 34),
            "Mug": (72, 19),
            "Notebook": (115, 28),
            "Pencil": (71, 14),
            "Scissors": (125, 36),
        }

        for class_name, (expected_train, expected_valid) in expected_counts.items():
            actual_train = sum(
                label == class_name for label in training.labels
            )
            actual_valid = sum(
                label == class_name for label in validation.labels
            )

            self.assertEqual(
                actual_train,
                expected_train,
                f"Training count mismatch for {class_name}",
            )
            self.assertEqual(
                actual_valid,
                expected_valid,
                f"Validation count mismatch for {class_name}",
            )

        self.assertTrue(all(p.is_file() for p in training.paths))
        self.assertTrue(all(p.is_file() for p in validation.paths))

        excluded_filename = (
            "00038_jpg.rf.7f94c208054cb0f13467f3967c7ed71c.jpg"
        )
        self.assertNotIn(
            excluded_filename,
            {p.name for p in training.paths},
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
