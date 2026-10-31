# PDE3802 Assessment 1 — Member 2 Dataset Verification

**Project:** Autonomous Office Item Organisation System
**Verified by:** Member 2
**Verification date:** 31 October 2026
**Branch:** `docs/step1-member2-verification`
**Audit baseline:** PR #2, merged at commit `4dd6336`

## 1. Purpose and method

I independently checked the local dataset against Member 1's `docs/dataset-audit.md` after updating local `main` using `git pull --ff-only origin main`.

Git history showed local `main` and `origin/main` at merge commit `4dd6336`. I then created the verification branch.

The dataset checks used PowerShell and separate Python commands. They did not modify the dataset or regenerate Member 1's audit output files.

**Environment:** Python 3.13.14 and Pillow 12.3.0.

## 2. Dataset source

I opened the Roboflow Universe source page and confirmed the following displayed information:

- Dataset: `office_home_dataset`
- Creator: `stefanpublic`
- Version: 1
- Task: Classification
- Displayed licence: CC BY 4.0
- Source: https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1

The source page displayed 8,618 images. The local project selection checked below contains 1,142 images across eight classes. These are different dataset scopes.

## 3. Folder structure and image counts

I confirmed that the local `dataset` directory contains `train`, `valid` and `test`. Each split contains the same eight expected class folders.

I independently counted `.jpg` files in every class and split:

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

All 24 class/split counts match Member 1's report.

A recursive file-extension check found 1,142 files, all with the `.jpg` extension. A separate recursive path check found zero unexpected folders or misplaced files.

## 4. Image integrity and exact duplicates

I independently opened and fully decoded the local images using Pillow's `Image.open()` and `image.load()`.

| Check | Independently observed result |
|---|---|
| Fully decoded images | 1,142 |
| Unreadable files | 0 |
| Image format | JPEG for all 1,142 images |
| Image dimensions | 416 × 416 pixels for all 1,142 images |
| SHA-256 exact duplicate groups | 0 |
| Unexpected folders or misplaced files | 0 |

Exact duplicates were checked across the local dataset using PowerShell's `Get-FileHash -Algorithm SHA256`, grouping files by hash.

## 5. Split assessment and limitations

All eight classes are represented in every split. The split totals are approximately 71.5% training, 19.5% validation and 9.0% testing.

The classes are uneven in size: Scissors contains 174 images and Pencil contains 96. The test split contains only 7–19 images per class, so later evaluation should account for the small sample sizes.

These checks establish file readability, dimensions, format, counts, directory placement and the absence of identical file hashes. They do not establish that every image has the correct visual label, that visually similar images are absent, or that the dataset represents real-world conditions adequately.

Checking the source page's displayed licence does not independently establish the provenance of every local image.

## 6. Verification conclusion and integration status

The independently checked local structure, all class/split counts, image properties, decoding results and exact duplicate findings agree with Member 1's dataset audit report.

No dataset changes were required by these checks. The existing splits can be retained for subsequent work, with the limitations above documented. The test split should remain reserved for final evaluation.

PR #2 is merged at `4dd6336`. This Member 2 verification document still requires its own pull request, Member 1's review and merge, and final synchronization by both members. Step 1 is not yet fully complete.
