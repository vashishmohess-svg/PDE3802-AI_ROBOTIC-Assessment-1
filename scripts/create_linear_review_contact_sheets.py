
from __future__ import annotations

import csv
import math
import textwrap
from collections import Counter
from pathlib import Path

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = (
    PROJECT_ROOT
    / "results"
    / "model_comparison"
    / "linear"
    / "linear_misclassification_review.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "model_comparison"
    / "linear"
    / "review_contact_sheets"
)

GROUPS = [
    ("Scissors", "Pencil", 9, "scissors_to_pencil"),
    ("Mug", "Bottle", 6, "mug_to_bottle"),
    ("Calculator", "Mouse", 5, "calculator_to_mouse"),
]

COLUMNS = 3
TILE_WIDTH = 380
TILE_HEIGHT = 330
IMAGE_WIDTH = 350
IMAGE_HEIGHT = 220


def load_review_rows() -> list[dict]:
    if not CSV_PATH.is_file():
        raise FileNotFoundError(CSV_PATH)

    with CSV_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 20:
        raise RuntimeError(
            f"Expected 20 review records, found {len(rows)}."
        )

    expected = Counter({
        ("Scissors", "Pencil"): 9,
        ("Mug", "Bottle"): 6,
        ("Calculator", "Mouse"): 5,
    })

    actual = Counter(
        (
            row["actual_class"],
            row["predicted_class"],
        )
        for row in rows
    )

    if actual != expected:
        raise RuntimeError(
            f"Unexpected confusion groups: {actual}"
        )

    return rows


def create_contact_sheet(
    rows: list[dict],
    actual_class: str,
    predicted_class: str,
    output_name: str,
) -> Path:

    selected = [
        row for row in rows
        if (
            row["actual_class"] == actual_class
            and row["predicted_class"] == predicted_class
        )
    ]

    selected.sort(
        key=lambda row: row["image_filename"].lower()
    )

    if not selected:
        raise RuntimeError(
            f"No images found for {actual_class} -> {predicted_class}."
        )

    sheet_rows = math.ceil(len(selected) / COLUMNS)

    sheet = np.full(
        (
            sheet_rows * TILE_HEIGHT,
            COLUMNS * TILE_WIDTH,
            3,
        ),
        255,
        dtype=np.uint8,
    )

    for index, row in enumerate(selected):

        image_path = (
            PROJECT_ROOT / row["relative_path"]
        ).resolve()

        try:
            image_path.relative_to(PROJECT_ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(
                f"Image is outside the project: {image_path}"
            ) from exc

        if not image_path.is_file():
            raise FileNotFoundError(image_path)

        image = cv2.imread(
            str(image_path),
            cv2.IMREAD_COLOR,
        )

        if image is None:
            raise RuntimeError(
                f"Could not read image: {image_path}"
            )

        tile_x = (index % COLUMNS) * TILE_WIDTH
        tile_y = (index // COLUMNS) * TILE_HEIGHT

        tile = sheet[
            tile_y:tile_y + TILE_HEIGHT,
            tile_x:tile_x + TILE_WIDTH,
        ]

        # Group heading.
        cv2.putText(
            tile,
            f"{actual_class} -> {predicted_class}  "
            f"({index + 1}/{len(selected)})",
            (12, 27),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

        # Resize while preserving original image proportions.
        height, width = image.shape[:2]

        scale = min(
            IMAGE_WIDTH / width,
            IMAGE_HEIGHT / height,
        )

        new_width = max(1, int(width * scale))
        new_height = max(1, int(height * scale))

        interpolation = (
            cv2.INTER_AREA if scale < 1
            else cv2.INTER_LINEAR
        )

        resized = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=interpolation,
        )

        # Centre the image in the tile.
        x = (TILE_WIDTH - new_width) // 2
        y = 40 + (IMAGE_HEIGHT - new_height) // 2

        tile[
            y:y + new_height,
            x:x + new_width,
        ] = resized

        cv2.rectangle(
            tile,
            (x, y),
            (x + new_width - 1, y + new_height - 1),
            (160, 160, 160),
            1,
        )

        # Show the filename for traceability.
        filename_lines = textwrap.wrap(
            row["image_filename"],
            width=55,
        )

        if len(filename_lines) > 2:
            filename_lines = [
                filename_lines[0],
                filename_lines[1][:50] + "...",
            ]

        line_y = 287

        for line in filename_lines:
            cv2.putText(
                tile,
                line,
                (10, line_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.34,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )
            line_y += 20

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = OUTPUT_DIR / output_name

    if not cv2.imwrite(str(output_path), sheet):
        raise RuntimeError(
            f"Failed to save contact sheet: {output_path}"
        )

    return output_path


def main() -> None:
    print("=== LINEAR SVM VISUAL REVIEW CONTACT SHEETS ===")

    rows = load_review_rows()

    print("[PASS] Loaded 20 verified review records.")

    for actual, predicted, expected, filename in GROUPS:

        selected_count = sum(
            1 for row in rows
            if (
                row["actual_class"] == actual
                and row["predicted_class"] == predicted
            )
        )

        if selected_count != expected:
            raise RuntimeError(
                f"Expected {expected} images for "
                f"{actual} -> {predicted}, "
                f"found {selected_count}."
            )

        output_path = create_contact_sheet(
            rows,
            actual,
            predicted,
            filename + ".png",
        )

        print(
            f"[PASS] {actual} -> {predicted}: "
            f"{selected_count} images"
        )
        print("       Saved:", output_path)

    print("\n[PASS] All three contact sheets created.")
    print("[PASS] Original dataset files were not modified.")
    print("[PASS] No held-out test images were accessed.")


if __name__ == "__main__":
    main()
