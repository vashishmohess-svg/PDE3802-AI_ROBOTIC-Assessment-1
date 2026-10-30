
from pathlib import Path
from collections import Counter, defaultdict
from hashlib import sha256
from datetime import datetime
import csv
import json

from PIL import Image, UnidentifiedImageError


# --------------------------------------------------
# 1. Project settings
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
OUTPUT_DIR = PROJECT_ROOT / "results" / "dataset_audit"

SPLITS = ["train", "valid", "test"]

EXPECTED_CLASSES = [
    "Bottle",
    "Calculator",
    "Keyboard",
    "Mouse",
    "Mug",
    "Notebook",
    "Pencil",
    "Scissors",
]

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg"}

# Set the expected image format based on the dataset inspection.
EXPECTED_FORMATS = {"JPEG"}


# --------------------------------------------------
# 2. Prepare audit output folder
# --------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

audit_time = datetime.now().isoformat(timespec="seconds")

print("=" * 65)
print("PDE3802 ASSESSMENT 1 - DATASET AUDIT")
print("=" * 65)
print(f"Dataset location: {DATASET_DIR}")
print(f"Audit output:     {OUTPUT_DIR}")
print(f"Audit started:    {audit_time}")
print()


# --------------------------------------------------
# 3. Check the dataset directory structure
# --------------------------------------------------

structure_issues = []

if not DATASET_DIR.exists():
    raise FileNotFoundError(
        f"Dataset directory not found: {DATASET_DIR}"
    )

actual_splits = {
    item.name
    for item in DATASET_DIR.iterdir()
    if item.is_dir()
}

for split in SPLITS:
    if split not in actual_splits:
        structure_issues.append(
            f"Missing split directory: {split}"
        )

unexpected_splits = actual_splits - set(SPLITS)

for split in sorted(unexpected_splits):
    structure_issues.append(
        f"Unexpected split directory: {split}"
    )

print("DATASET STRUCTURE")
print("-" * 65)

for split in SPLITS:
    split_path = DATASET_DIR / split

    if not split_path.is_dir():
        print(f"{split}: MISSING")
        continue

    actual_classes = {
        item.name
        for item in split_path.iterdir()
        if item.is_dir()
    }

    missing_classes = set(EXPECTED_CLASSES) - actual_classes
    unexpected_classes = actual_classes - set(EXPECTED_CLASSES)

    print(f"\n{split}:")

    for class_name in EXPECTED_CLASSES:
        class_path = split_path / class_name

        if class_path.is_dir():
            print(f"  {class_name}: folder exists")
        else:
            print(f"  {class_name}: MISSING")
            structure_issues.append(
                f"Missing class folder: {split}/{class_name}"
            )

    for class_name in sorted(unexpected_classes):
        print(f"  Unexpected class folder: {class_name}")
        structure_issues.append(
            f"Unexpected class folder: {split}/{class_name}"
        )


# --------------------------------------------------
# 4. Inspect files and count images
# --------------------------------------------------

class_counts = defaultdict(int)
split_totals = Counter()
extension_counts = Counter()
format_counts = Counter()
dimension_counts = Counter()

file_records = []
file_issues = []
hash_locations = defaultdict(list)

total_files = 0
total_images = 0
valid_images = 0
invalid_images = 0
unsupported_files = 0

print("\n\nFILE AND IMAGE INSPECTION")
print("-" * 65)

for split in SPLITS:
    split_path = DATASET_DIR / split

    if not split_path.is_dir():
        continue

    for class_name in EXPECTED_CLASSES:
        class_path = split_path / class_name

        if not class_path.is_dir():
            continue

        files = sorted(
            item for item in class_path.iterdir()
            if item.is_file()
        )

        for file_path in files:
            total_files += 1
            relative_path = file_path.relative_to(
                PROJECT_ROOT
            ).as_posix()

            extension = file_path.suffix.lower()
            extension_counts[extension] += 1

            record = {
                "split": split,
                "class": class_name,
                "file": relative_path,
                "extension": extension,
                "size_bytes": file_path.stat().st_size,
                "sha256": "",
                "image_format": "",
                "width": "",
                "height": "",
                "mode": "",
                "status": "",
                "issue": "",
            }

            if extension not in SUPPORTED_EXTENSIONS:
                unsupported_files += 1
                record["status"] = "unsupported_extension"
                record["issue"] = "Unsupported file extension"

                file_issues.append({
                    "file": relative_path,
                    "issue": "Unsupported file extension",
                })

                file_records.append(record)
                continue

            total_images += 1

            try:
                # Calculate SHA-256 hash for exact duplicate detection.
                file_hash = sha256(
                    file_path.read_bytes()
                ).hexdigest()

                record["sha256"] = file_hash
                hash_locations[file_hash].append(
                    relative_path
                )

                # Verify that Pillow can decode the image.
                with Image.open(file_path) as image:
                    image.verify()

                # Reopen the image to inspect its properties.
                with Image.open(file_path) as image:
                    image_format = image.format
                    width, height = image.size
                    mode = image.mode

                valid_images += 1
                class_counts[(split, class_name)] += 1
                split_totals[split] += 1
                format_counts[image_format] += 1
                dimension_counts[(width, height)] += 1

                record["image_format"] = image_format
                record["width"] = width
                record["height"] = height
                record["mode"] = mode
                record["status"] = "valid"

                if image_format not in EXPECTED_FORMATS:
                    record["issue"] = "Unexpected image format"

                    file_issues.append({
                        "file": relative_path,
                        "issue": "Unexpected image format",
                    })

            except (
                UnidentifiedImageError,
                OSError,
                ValueError,
            ) as error:
                invalid_images += 1
                record["status"] = "invalid"
                record["issue"] = str(error)

                file_issues.append({
                    "file": relative_path,
                    "issue": str(error),
                })

            file_records.append(record)


# --------------------------------------------------
# 5. Identify files outside expected class folders
# --------------------------------------------------

unexpected_files = []

for split in SPLITS:
    split_path = DATASET_DIR / split

    if not split_path.is_dir():
        continue

    for item in split_path.iterdir():
        if item.is_file():
            unexpected_files.append(
                item.relative_to(PROJECT_ROOT).as_posix()
            )

for file_path in sorted(unexpected_files):
    file_issues.append({
        "file": file_path,
        "issue": "File directly inside split directory",
    })


# --------------------------------------------------
# 6. Detect exact duplicate images
# --------------------------------------------------

duplicates = []

for file_hash, locations in sorted(hash_locations.items()):
    if len(locations) > 1:
        duplicates.append({
            "sha256": file_hash,
            "files": locations,
            "number_of_copies": len(locations),
        })


# --------------------------------------------------
# 7. Print class and split counts
# --------------------------------------------------

print("\nCLASS COUNTS")
print("-" * 65)

for split in SPLITS:
    print(f"\n{split.upper()}")

    for class_name in EXPECTED_CLASSES:
        count = class_counts[(split, class_name)]
        print(f"  {class_name:<15} {count:>5}")

    print(f"  {'TOTAL':<15} {split_totals[split]:>5}")


# --------------------------------------------------
# 8. Print image inspection summary
# --------------------------------------------------

print("\n\nIMAGE INSPECTION SUMMARY")
print("-" * 65)
print(f"Total files inspected:       {total_files}")
print(f"Image files with supported extensions: {total_images}")
print(f"Successfully decoded images: {valid_images}")
print(f"Invalid or unreadable images: {invalid_images}")
print(f"Unsupported files:           {unsupported_files}")

print("\nFile extensions:")
for extension, count in sorted(extension_counts.items()):
    print(f"  {extension or '[no extension]'}: {count}")

print("\nImage formats:")
for image_format, count in sorted(format_counts.items()):
    print(f"  {image_format}: {count}")

print("\nImage dimensions:")
for dimensions, count in sorted(dimension_counts.items()):
    print(f"  {dimensions[0]} x {dimensions[1]}: {count}")


# --------------------------------------------------
# 9. Print duplicate and issue summary
# --------------------------------------------------

print("\n\nDUPLICATE CHECK")
print("-" * 65)
print(f"Exact duplicate groups: {len(duplicates)}")

for duplicate in duplicates:
    print(f"\nSHA-256: {duplicate['sha256']}")
    for location in duplicate["files"]:
        print(f"  {location}")

print("\n\nISSUES")
print("-" * 65)
print(f"Structure issues: {len(structure_issues)}")
print(f"File issues:      {len(file_issues)}")

for issue in structure_issues:
    print(f"STRUCTURE: {issue}")

for issue in file_issues:
    print(f"FILE: {issue['file']} - {issue['issue']}")


# --------------------------------------------------
# 10. Save detailed file audit as CSV
# --------------------------------------------------

csv_path = OUTPUT_DIR / "file_audit.csv"

fieldnames = [
    "split",
    "class",
    "file",
    "extension",
    "size_bytes",
    "sha256",
    "image_format",
    "width",
    "height",
    "mode",
    "status",
    "issue",
]

with csv_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:
    writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames
    )
    writer.writeheader()
    writer.writerows(file_records)


# --------------------------------------------------
# 11. Save class counts as CSV
# --------------------------------------------------

counts_path = OUTPUT_DIR / "class_counts.csv"

with counts_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow([
        "split",
        "class",
        "image_count",
    ])

    for split in SPLITS:
        for class_name in EXPECTED_CLASSES:
            writer.writerow([
                split,
                class_name,
                class_counts[(split, class_name)],
            ])


# --------------------------------------------------
# 12. Save duplicate report as JSON
# --------------------------------------------------

duplicates_path = OUTPUT_DIR / "duplicates.json"

with duplicates_path.open(
    "w",
    encoding="utf-8"
) as json_file:
    json.dump(
        duplicates,
        json_file,
        indent=4
    )


# --------------------------------------------------
# 13. Save overall audit summary as JSON
# --------------------------------------------------

summary = {
    "audit_time": audit_time,
    "dataset_location": "dataset",
    "expected_classes": EXPECTED_CLASSES,
    "splits": SPLITS,
    "total_files": total_files,
    "total_supported_image_files": total_images,
    "valid_images": valid_images,
    "invalid_images": invalid_images,
    "unsupported_files": unsupported_files,
    "split_totals": dict(split_totals),
    "extension_counts": dict(extension_counts),
    "format_counts": dict(format_counts),
    "dimension_counts": {
        f"{width}x{height}": count
        for (width, height), count in dimension_counts.items()
    },
    "duplicate_groups": len(duplicates),
    "structure_issues": structure_issues,
    "file_issue_count": len(file_issues),
}

summary_path = OUTPUT_DIR / "audit_summary.json"

with summary_path.open(
    "w",
    encoding="utf-8"
) as json_file:
    json.dump(
        summary,
        json_file,
        indent=4
    )


# --------------------------------------------------
# 14. Final result
# --------------------------------------------------

print("\n\nAUDIT OUTPUT FILES")
print("-" * 65)
print(csv_path)
print(counts_path)
print(duplicates_path)
print(summary_path)

print("\n" + "=" * 65)
print("DATASET AUDIT FINISHED")
print("=" * 65)
