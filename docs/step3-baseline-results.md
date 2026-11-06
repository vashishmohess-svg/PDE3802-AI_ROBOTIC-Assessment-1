# Step 3 — Baseline HOG + Linear SVM Results

**Project:** PDE3802 Assessment 1 — Autonomous Office Item Organisation System and Office-Goods Classification

**Date:** 6 November 2026

**Status:** Baseline trained and validation results reproduced. Member 2 independently verified the implementation and saved model on a second computer, reproduced the validation metrics and confusion matrix, and submitted formal approval on PR #12. Final documentation correction, PR integration and repository synchronisation remain pending.

## 1. Purpose

This document records the initial image-classification baseline. It will provide a reference for the model comparisons in Step 4.

The classifier predicts one of eight office-item classes from one image. It is an image classifier, not an object detector.

## 2. Dataset and approved split

- **Dataset:** `office_home_dataset`
- **Creator:** `stefanpublic`
- **Version:** 1
- **Licence:** CC BY 4.0

Source: https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1

The classifier uses the D014-approved manifest:

`docs/evidence/step3.5.5J/step3.5.5K3_full_split_manifest_proposal.csv`

| Data allocation | Images | Purpose |
|---|---:|---|
| Training allocation | 813 | Model fitting |
| Effective training | 812 | Actual model fitting |
| Validation | 226 | Model evaluation |
| Held-out test | 103 | Reserved for Step 6 |

One severely pixelated Pencil image was excluded from model fitting:

`Pencil/00038_jpg.rf.7f94c208054cb0f13467f3967c7ed71c.jpg`

The original image remains in the dataset. No original dataset image or folder was modified.

### Effective class distribution

| Class | Training | Validation |
|---|---:|---:|
| Bottle | 95 | 27 |
| Calculator | 104 | 31 |
| Keyboard | 122 | 37 |
| Mouse | 108 | 34 |
| Mug | 72 | 19 |
| Notebook | 115 | 28 |
| Pencil | 71 | 14 |
| Scissors | 125 | 36 |
| **Total** | **812** | **226** |

## 3. Image preprocessing

Each image is processed as follows:

1. EXIF orientation correction.
2. Conversion to grayscale.
3. Resizing to 128 × 128 pixels using OpenCV `INTER_AREA`.
4. Conversion to a `uint8` NumPy array.

The original image files are not changed.

## 4. HOG feature extraction

Histogram of Oriented Gradients (HOG) is used to extract image features.

| Parameter | Configuration |
|---|---|
| Window size | 128 × 128 |
| Block size | 16 × 16 |
| Block stride | 8 × 8 |
| Cell size | 8 × 8 |
| Orientation bins | 9 |
| Features per image | 8,100 |

Verified feature matrix sizes:

- Training: `(812, 8100)`
- Validation: `(226, 8100)`

Both matrices contain finite `float32` values.

## 5. Baseline classifier

The classifier is `sklearn.svm.SVC`.

| Parameter | Value |
|---|---|
| Kernel | Linear |
| C | 1.0 |
| Decision function | One-vs-rest |
| Probability estimates | Disabled |
| Support vectors | 748 |

The model does not provide calibrated probabilities. Its decision scores must not be presented as confidence percentages.

## 6. Validation results

The model was evaluated using all 226 validation images.

| Metric | Result |
|---|---:|
| Correct predictions | 155 out of 226 |
| Accuracy | **68.58%** |
| Macro-F1 | **0.6497** |

### Per-class results

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Bottle | 0.5882 | 0.7407 | 0.6557 |
| Calculator | 0.7241 | 0.6774 | 0.7000 |
| Keyboard | 0.7750 | 0.8378 | 0.8052 |
| Mouse | 0.8065 | 0.7353 | 0.7692 |
| Mug | 0.7273 | 0.4211 | 0.5333 |
| Notebook | 0.6897 | 0.7143 | 0.7018 |
| Pencil | 0.2381 | 0.3571 | 0.2857 |
| Scissors | 0.8065 | 0.6944 | 0.7463 |

### Main observed classification errors

| Actual class | Predicted class | Errors |
|---|---|---:|
| Scissors | Pencil | 9 |
| Mug | Bottle | 6 |
| Calculator | Mouse | 5 |
| Pencil | Bottle | 3 |
| Notebook | Calculator | 3 |
| Bottle | Notebook | 3 |

Keyboard achieved the highest F1-score. Pencil achieved the lowest F1-score, followed by Mug.

These results identify areas for investigation in Step 4. They do not establish the exact visual cause of the errors.

## 7. Automated testing

A total of 20 unit tests passed:

- 10 dataset-loader tests.
- 10 HOG feature-extraction tests.

All 812 approved training images and 226 validation images were successfully decoded.

The saved model was reloaded. Its reproduced accuracy, macro-F1 and confusion matrix matched the saved validation results.

## 8. Generated baseline files

The following files are saved under `results/baseline/`:

- `baseline_hog_linear_svm.joblib`
- `validation_metrics.json`
- `validation_classification_report.json`
- `validation_classification_report.csv`
- `validation_confusion_matrix.csv`
- `validation_confusion_matrix.png`
- `run_metadata.json`

The model file is configured for Git LFS tracking and was successfully committed and uploaded through PR #12 in commit `6fbae66`. The verified model file size is 48,560,430 bytes. Member 2 independently retrieved the model through Git LFS and verified that it could be loaded and used to reproduce the validation results.

The baseline implementation and supporting files are available on branch `feature/step3-baseline-classifier`.

Pull Request: https://github.com/vashishmohess-svg/PDE3802-AI_ROBOTIC-Assessment-1/pull/12

## 9. Limitations and next steps

1. This is an initial baseline, not the final selected classifier.
2. It classifies one whole image into one class; it does not detect multiple objects.
3. It does not provide calibrated confidence probabilities.
4. Pencil and Mug need particular attention during model comparison.
5. The held-out test split has not been accessed.
6. The prediction application and camera input remain for Step 5.
7. Model comparison and selection remain for Step 4.
8. Final held-out evaluation remains for Step 6.

## 10. Current completion status

The baseline implementation, training, validation and saved-model verification have been completed by Member 1.

Member 2 has independently reviewed the baseline implementation, automated tests, saved model and validation results. Member 2 successfully retrieved the model through Git LFS, ran all 20 automated tests, reproduced the validation accuracy of 68.58%, macro-F1 of 0.6497 and the saved confusion matrix, and submitted formal approval on PR #12.

The remaining work is the correction of the outdated Git LFS statement in the project plan, the contribution-log update, the documentation commit and push, PR #12 merge, and final repository synchronisation by both members.

The baseline implementation and independent verification are complete. Step 3 remains in progress until the documentation correction, Git integration and final synchronisation are completed.
