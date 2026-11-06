"""Manifest-driven dataset loading for the office-item classifier.

The original dataset folders are never rearranged. Logical split assignment
comes from the approved manifest.

Important: the proposed test split is deliberately blocked in this module.
It is reserved for the final held-out evaluation in Step 6.
"""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import cv2
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError


CLASS_NAMES = (
    "Bottle",
    "Calculator",
    "Keyboard",
    "Mouse",
    "Mug",
    "Notebook",
    "Pencil",
    "Scissors",
)

IMAGE_SIZE = (128, 128)  # width, height

MANIFEST_RELATIVE_PATH = Path(
    "docs/evidence/step3.5.5J/"
    "step3.5.5K3_full_split_manifest_proposal.csv"
)

EXPECTED_MANIFEST_SHA256 = (
    "40FAD2A63BF4BA3185731154D1F5908901F5D224FD3F2D098FAE84C9B234B7D5"
)

EXPECTED_ORIGINAL_COUNTS = {
    "train": 816,
    "valid": 223,
    "test": 103,
}

EXPECTED_PROPOSED_COUNTS = {
    "train": 813,
    "valid": 226,
    "test": 103,
}

EXPECTED_EFFECTIVE_TRAIN_COUNT = 812

EXPECTED_CLASS_COUNTS = {
    "Bottle": (95, 27, 10),
    "Calculator": (104, 31, 19),
    "Keyboard": (122, 37, 14),
    "Mouse": (108, 34, 14),
    "Mug": (72, 19, 7),
    "Notebook": (115, 28, 16),
    "Pencil": (72, 14, 10),
    "Scissors": (125, 36, 13),
}

EXPECTED_EXCLUDED_CLASS = "Pencil"
EXPECTED_EXCLUDED_FILENAME = (
    "00038_jpg.rf.7f94c208054cb0f13467f3967c7ed71c.jpg"
)


class DatasetManifestError(ValueError):
    """Raised when the approved dataset manifest is invalid."""


class DatasetImageError(RuntimeError):
    """Raised when a permitted dataset image cannot be loaded."""


@dataclass(frozen=True)
class ImageRecord:
    """Metadata and original physical location for one manifest image."""

    class_name: str
    filename: str
    original_split: str
    proposed_split: str
    group_id: str
    effective_training_eligible: str
    existing_training_exclusion: str
    source_path: Path


@dataclass(frozen=True)
class LoadedSplit:
    """Image data and labels for one permitted logical split."""

    images: np.ndarray
    labels: np.ndarray
    paths: tuple[Path, ...]


def _canonical_sha256(data: bytes) -> str:
    """Hash file bytes after normalising Windows CRLF to canonical LF."""
    if b"\r" in data.replace(b"\r\n", b""):
        raise DatasetManifestError(
            "Manifest contains unexpected bare carriage-return characters."
        )

    canonical_bytes = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(canonical_bytes).hexdigest().upper()


def load_manifest(
    manifest_path: str | Path,
    dataset_root: str | Path,
) -> list[ImageRecord]:
    """Read and validate the approved manifest without opening any images.

    Reading manifest metadata does not load or process image pixels.
    """

    manifest_path = Path(manifest_path)
    dataset_root = Path(dataset_root).resolve()

    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"Dataset manifest not found: {manifest_path}"
        )

    raw_bytes = manifest_path.read_bytes()
    actual_hash = _canonical_sha256(raw_bytes)

    if actual_hash != EXPECTED_MANIFEST_SHA256:
        raise DatasetManifestError(
            "Approved manifest integrity check failed. "
            f"Expected {EXPECTED_MANIFEST_SHA256}, got {actual_hash}."
        )

    required_columns = {
        "Class",
        "Filename",
        "Original_Split",
        "Proposed_Split",
        "Group_ID",
        "Effective_Training_Eligible",
        "Existing_Training_Exclusion",
    }

    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise DatasetManifestError(
            "Manifest is not valid UTF-8."
        ) from exc

    with manifest_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])

        missing_columns = required_columns - columns
        if missing_columns:
            raise DatasetManifestError(
                f"Manifest is missing columns: {sorted(missing_columns)}"
            )

        rows = list(reader)

    if len(rows) != 1142:
        raise DatasetManifestError(
            f"Expected 1,142 manifest records, found {len(rows)}."
        )

    records: list[ImageRecord] = []
    seen_keys: set[tuple[str, str]] = set()

    for line_number, row in enumerate(rows, start=2):
        class_name = (row["Class"] or "").strip()
        filename = (row["Filename"] or "").strip()
        original_split = (row["Original_Split"] or "").strip()
        proposed_split = (row["Proposed_Split"] or "").strip()
        group_id = (row["Group_ID"] or "").strip()
        eligible = (
            row["Effective_Training_Eligible"] or ""
        ).strip()
        exclusion = (
            row["Existing_Training_Exclusion"] or ""
        ).strip()

        if class_name not in CLASS_NAMES:
            raise DatasetManifestError(
                f"Unknown class at manifest line {line_number}: {class_name!r}"
            )

        if original_split not in EXPECTED_ORIGINAL_COUNTS:
            raise DatasetManifestError(
                f"Invalid original split at line {line_number}."
            )

        if proposed_split not in EXPECTED_PROPOSED_COUNTS:
            raise DatasetManifestError(
                f"Invalid proposed split at line {line_number}."
            )

        # Prevent path traversal or nested paths from manifest filenames.
        if (
            not filename
            or Path(filename).name != filename
            or "/" in filename
            or "\\" in filename
        ):
            raise DatasetManifestError(
                f"Unsafe filename at manifest line {line_number}: {filename!r}"
            )

        key = (class_name, filename)
        if key in seen_keys:
            raise DatasetManifestError(
                f"Duplicate class/filename record: {key}"
            )
        seen_keys.add(key)

        if proposed_split == "train":
            if eligible not in {"YES", "NO"}:
                raise DatasetManifestError(
                    f"Invalid training eligibility at line {line_number}."
                )
        elif eligible != "NOT_APPLICABLE":
            raise DatasetManifestError(
                f"Non-training row has unexpected training eligibility "
                f"at line {line_number}."
            )

        if exclusion not in {"YES", "NO"}:
            raise DatasetManifestError(
                f"Invalid exclusion flag at line {line_number}."
            )

        source_path = (
            dataset_root
            / original_split
            / class_name
            / filename
        )

        records.append(
            ImageRecord(
                class_name=class_name,
                filename=filename,
                original_split=original_split,
                proposed_split=proposed_split,
                group_id=group_id,
                effective_training_eligible=eligible,
                existing_training_exclusion=exclusion,
                source_path=source_path,
            )
        )

    original_counts = Counter(r.original_split for r in records)
    proposed_counts = Counter(r.proposed_split for r in records)

    if dict(original_counts) != EXPECTED_ORIGINAL_COUNTS:
        raise DatasetManifestError(
            f"Original split counts do not match the audit: "
            f"{dict(original_counts)}"
        )

    if dict(proposed_counts) != EXPECTED_PROPOSED_COUNTS:
        raise DatasetManifestError(
            f"Proposed split counts do not match D014: "
            f"{dict(proposed_counts)}"
        )

    # Check all eight class distributions in the approved logical splits.
    for class_name, expected in EXPECTED_CLASS_COUNTS.items():
        class_records = [
            r for r in records if r.class_name == class_name
        ]
        actual = tuple(
            sum(
                1 for r in class_records
                if r.proposed_split == split
            )
            for split in ("train", "valid", "test")
        )

        if actual != expected:
            raise DatasetManifestError(
                f"Class distribution mismatch for {class_name}: "
                f"expected {expected}, got {actual}."
            )

    effective_train = [
        r for r in records
        if r.proposed_split == "train"
        and r.effective_training_eligible == "YES"
    ]

    if len(effective_train) != EXPECTED_EFFECTIVE_TRAIN_COUNT:
        raise DatasetManifestError(
            f"Expected 812 eligible training images, "
            f"found {len(effective_train)}."
        )

    exclusions = [
        r for r in records
        if r.existing_training_exclusion == "YES"
    ]

    if not (
        len(exclusions) == 1
        and exclusions[0].class_name == EXPECTED_EXCLUDED_CLASS
        and exclusions[0].filename == EXPECTED_EXCLUDED_FILENAME
        and exclusions[0].proposed_split == "train"
        and exclusions[0].effective_training_eligible == "NO"
    ):
        raise DatasetManifestError(
            "The existing severely pixelated Pencil exclusion "
            "does not match the approved record."
        )

    # Confirm that no recorded candidate group crosses logical splits.
    group_splits: dict[str, set[str]] = defaultdict(set)
    for record in records:
        if record.group_id:
            group_splits[record.group_id].add(record.proposed_split)

    if len(group_splits) != 13:
        raise DatasetManifestError(
            f"Expected 13 candidate groups, found {len(group_splits)}."
        )

    if any(len(splits) != 1 for splits in group_splits.values()):
        raise DatasetManifestError(
            "At least one candidate group crosses proposed splits."
        )

    grouped_records = [r for r in records if r.group_id]
    if len(grouped_records) != 44:
        raise DatasetManifestError(
            f"Expected 44 grouped images, found {len(grouped_records)}."
        )

    return records


def load_split_records(
    manifest_path: str | Path,
    dataset_root: str | Path,
    split: Literal["train", "valid"],
) -> list[ImageRecord]:
    """Select records for training or validation.

    The test split is deliberately not supported in Step 3 or Step 4.
    Test records are not checked for file existence or opened here.
    """

    if split not in {"train", "valid"}:
        raise DatasetManifestError(
            "Only 'train' and 'valid' can be loaded before Step 6. "
            "The test split is intentionally blocked."
        )

    records = load_manifest(manifest_path, dataset_root)

    selected = [
        record for record in records
        if record.proposed_split == split
        and (
            split == "valid"
            or record.effective_training_eligible == "YES"
        )
    ]

    expected_count = (
        EXPECTED_EFFECTIVE_TRAIN_COUNT
        if split == "train"
        else EXPECTED_PROPOSED_COUNTS["valid"]
    )

    if len(selected) != expected_count:
        raise DatasetManifestError(
            f"Expected {expected_count} {split} records, "
            f"found {len(selected)}."
        )

    # Only selected training or validation records are checked.
    # Proposed test image paths are never accessed here.
    missing = [
        record.source_path
        for record in selected
        if not record.source_path.is_file()
    ]

    if missing:
        preview = "\n".join(str(path) for path in missing[:10])
        raise FileNotFoundError(
            f"{len(missing)} {split} image files are missing. "
            f"First missing paths:\n{preview}"
        )

    return selected


def load_image(
    record: ImageRecord,
    image_size: tuple[int, int] = IMAGE_SIZE,
) -> np.ndarray:
    """Load one permitted image as a grayscale uint8 array.

    EXIF orientation is corrected before grayscale conversion and resizing.
    Test-split records are rejected before any file access.
    """

    if record.proposed_split not in {"train", "valid"}:
        raise DatasetManifestError(
            "Test images cannot be loaded before the final evaluation in Step 6."
        )

    if len(image_size) != 2 or min(image_size) <= 0:
        raise ValueError("image_size must contain two positive dimensions.")

    try:
        with Image.open(record.source_path) as image:
            corrected = ImageOps.exif_transpose(image)
            grayscale = ImageOps.grayscale(corrected)
            pixels = np.asarray(grayscale, dtype=np.uint8)

        resized = cv2.resize(
            pixels,
            image_size,
            interpolation=cv2.INTER_AREA,
        )

    except (OSError, UnidentifiedImageError, cv2.error) as exc:
        raise DatasetImageError(
            f"Could not load image for class {record.class_name}: "
            f"{record.source_path}"
        ) from exc

    if resized.shape != (image_size[1], image_size[0]):
        raise DatasetImageError(
            f"Unexpected resized image shape {resized.shape} "
            f"for {record.source_path}."
        )

    return resized


def load_split_images(
    manifest_path: str | Path,
    dataset_root: str | Path,
    split: Literal["train", "valid"],
) -> LoadedSplit:
    """Load all eligible images for a permitted logical split."""

    records = load_split_records(
        manifest_path=manifest_path,
        dataset_root=dataset_root,
        split=split,
    )

    images = np.stack(
        [load_image(record) for record in records],
        axis=0,
    )

    labels = np.asarray(
        [record.class_name for record in records],
        dtype=str,
    )

    paths = tuple(record.source_path for record in records)

    return LoadedSplit(
        images=images,
        labels=labels,
        paths=paths,
    )
