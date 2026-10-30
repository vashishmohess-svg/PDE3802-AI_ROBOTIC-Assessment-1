# PDE3802 Assessment 1 — Dataset Audit Report

**Project:** Autonomous Office Item Organisation System

**Dataset:** office_home_dataset

**Audit owner:** Member 1 — Project Lead

**Audit date:** 31 October 2026

**Audit branch:** `data/step1-dataset-audit`



## 1. Purpose of the Audit

The purpose of this audit was to inspect the selected office-item image dataset before developing the classification model.

The audit checked the dataset structure, class distribution, image file formats, image readability, image dimensions and exact duplicate files.

The original dataset was preserved throughout the audit. No images were deleted, renamed, moved, modified or reassigned between the training, validation and testing splits.

## 2. Dataset Source and Licence

The dataset was obtained from Roboflow Universe.

- **Dataset name:** office_home_dataset
- **Creator:** stefanpublic
- **Version:** 1
- **Source:** https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)

A selected subset of eight office-item categories was used for this project.

## 3. Dataset Structure

The dataset contains three splits:

- `train`
- `valid`
- `test`

Each split contains the following eight class folders:

1. Bottle
2. Calculator
3. Keyboard
4. Mouse
5. Mug
6. Notebook
7. Pencil
8. Scissors

All eight expected class folders were present in all three splits.

The revised audit script also performs a recursive check of the dataset directory. It checks for unexpected split folders, unexpected class folders, nested directories and files located outside the expected class folders.

No unexpected directories or misplaced files were identified.

## 4. Class Distribution

The audit identified the following image counts:

| Class | Train | Valid | Test | Total |
|---|---:|---:|---:|---:|
| Bottle | 95 | 27 | 10 | 132 |
| Calculator | 104 | 31 | 19 | 154 |
| Keyboard | 122 | 37 | 14 | 173 |
| Mouse | 108 | 34 | 14 | 156 |
| Mug | 72 | 19 | 7 | 98 |
| Notebook | 117 | 27 | 15 | 159 |
| Pencil | 72 | 14 | 10 | 96 |
| Scissors | 126 | 34 | 14 | 174 |
| **Total** | **816** | **223** | **103** | **1,142** |

The dataset contains 1,142 images in total:

- Training: 816 images (approximately 71.5%).
- Validation: 223 images (approximately 19.5%).
- Testing: 103 images (approximately 9.0%).

## 5. Image Integrity and Properties

The revised audit script used Python and Pillow to inspect and fully decode the image files.

The results were:

| Check | Result |
|---|---:|
| Total files inspected | 1,142 |
| Supported image files | 1,142 |
| Successfully decoded images | 1,142 |
| Invalid or unreadable images | 0 |
| Unsupported files | 0 |
| JPEG images | 1,142 |
| Images with `.jpg` extension | 1,142 |
| Image dimensions | 416 × 416 pixels |
| Exact duplicate groups | 0 |
| Misplaced files | 0 |
| Reported structure issues | 0 |
| Reported file issues | 0 |

All 1,142 inspected images were successfully opened and fully decoded using Pillow's `image.load()` method. Every image was in JPEG format and had dimensions of 416 × 416 pixels.

The revised audit also checked for files outside the expected class folders. No misplaced files, unexpected directories or file-integrity issues were identified.


## 6. Duplicate Detection

Exact duplicate detection was performed using SHA-256 file hashes.

The audit identified zero exact duplicate groups among the inspected images.

This means no files with identical contents were detected by the hash comparison.

The check does not rule out visually similar images with different file contents.

## 7. Dataset Suitability

The existing dataset splits were assessed for their suitability for developing and evaluating the office-item classifier.

The training split contains 816 images across all eight classes and will be used to train the classification model.

The validation split contains 223 images and will be used to monitor model performance and support model selection.

The testing split contains 103 images and will be kept separate for final model evaluation.

All eight classes are represented in all three splits.

However, the dataset is not perfectly balanced. For example, Scissors has 174 images, whereas Pencil has 96 images. The test split is also relatively small, with between 7 and 19 images per class.

These limitations should be considered when interpreting the final classification results.

The test split must not be used for training or repeated model tuning. It will be reserved for final evaluation.

Based on the audit findings, the existing dataset structure and splits are acceptable for proceeding with the project. No changes to the original dataset were considered necessary.

## 8. Audit Limitations

The audit checked file integrity through full image decoding, image properties, folder structure, misplaced files and exact duplicates. The revised script also performs recursive directory checks to identify unexpected nested directories and files outside the expected class folders.

However, it did not establish that every image has the correct class label or that every image visually represents its assigned category.

SHA-256 duplicate detection identifies identical files but does not identify visually similar images with different file contents.

The audit also does not assess whether the dataset contains sufficient visual variation for reliable real-world classification.

These aspects should be considered during model development and evaluation.

## 9. Audit Output Files

The audit generated the following files in `results/dataset_audit/`:

| File | Description |
|---|---|
| `audit_summary.json` | Overall audit statistics and findings |
| `class_counts.csv` | Image counts for each class and split |
| `file_audit.csv` | Individual file information, image properties and SHA-256 hashes |
| `duplicates.json` | Exact duplicate detection results |

The audit program is stored at:

`scripts/audit_dataset.py`

## 10. Conclusion

The revised dataset audit confirmed that the selected dataset contains 1,142 JPEG images across eight office-item classes and three splits.

All 1,142 inspected images were successfully fully decoded, and all images had dimensions of 416 × 416 pixels. No unsupported files, invalid images, exact duplicate groups, misplaced files or unexpected directories were identified. No reported structure or file issues remained.

The training, validation and testing splits contain 816, 223 and 103 images respectively.

The existing dataset is acceptable for proceeding with the development of the office-item classification model. The original images and split assignments have been preserved.

The dataset's class imbalance, relatively small test set and the limitations of automated integrity checks will be considered during subsequent model development and evaluation.



**Audit prepared by:** Member 1 — Project Lead

**Date:** 31 October 2026