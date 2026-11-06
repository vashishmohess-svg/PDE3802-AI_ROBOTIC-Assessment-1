# Step 3 — Baseline HOG + Linear SVM Results

**Project:** PDE3802 Assessment 1 — Autonomous Office Item Organisation System and Office-Goods Classification

**Date:** 6 November 2026

**Status:** Step 3 baseline implementation, training, validation, independent review and Git integration completed. PR #12 was merged at commit `a72d482`. Both members successfully synchronised their repositories and reproduced the saved-model validation results after the merge. The held-out test dataset remains unused and reserved for Step 6.

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

## 7. Automated Testing and Verification

A total of 20 automated tests were implemented and successfully passed during baseline development and independent pre-merge review:

- 10 dataset-loader tests.
- 10 HOG feature-extraction tests.

All 812 effective training images and 226 validation images were successfully decoded during the baseline implementation.

### 7.1 Historical post-PR #12 test-runner limitation

After PR #12 was merged, both members independently attempted to execute:

`python -m pytest -q`

The command could not execute because `pytest` was not installed in either project virtual environment and was not included in the existing `requirements.txt` or `requirements-lock.txt`.

This was an unavailable test-runner dependency, not a failure of the 20 automated tests. The earlier successful 20/20 test results from implementation and independent pre-merge review remained valid.

Both members successfully completed the post-PR #12 saved-model verification using `scripts/verify_baseline.py`.

This limitation was subsequently resolved through PR #14.

### 7.2 Development dependency integration - PR #14

A separate development dependency setup was introduced to make the automated tests reproducible on both computers without changing the existing runtime dependency definitions.

The following files were added:

- `requirements-dev.txt` - inherits the existing pinned runtime dependencies from `requirements-lock.txt` and adds `pytest==9.2.0`.
- `requirements-dev-lock.txt` - records the complete 52-package development environment, including pytest and its supporting packages.

The existing `requirements.txt` and `requirements-lock.txt` were left unchanged. The existing `.gitignore` already excluded `.pytest_cache/`, so no modification was necessary.

Member 1 implemented the dependency setup, installed pytest and generated the development lock file. Member 2 independently installed the locked environment, checked the installed package versions against the lock file, ran the tests and reviewed the dependency changes.

PR #14 - Add locked pytest development dependencies - was formally approved by Member 2 and merged into `main`.

- Development dependency commit: `b3bcf52`.
- Pull Request: [PR #14](https://github.com/vashishmohess-svg/PDE3802-AI_ROBOTIC-Assessment-1/pull/14).
- Merge commit: `b98cb3a`.

### 7.3 Post-PR #14 verification by both members

Following the merge of PR #14, both members independently synchronised their local `main` branches with `origin/main` and performed the dependency, automated test and saved-model verification checks.

The agreed environment was Python 3.13.17 with pytest 9.2.0.

| Verification | Member 1 | Member 2 |
|---|---:|---:|
| `python -m pip check` | Passed | Passed |
| pytest version | 9.2.0 | 9.2.0 |
| Automated tests | 20 passed | 20 passed |
| Test execution time | 20.15 seconds | 5.79 seconds |
| Baseline verification | Passed | Passed |
| Validation accuracy | 68.58% | 68.58% |
| Validation macro-F1 | 0.6497 | 0.6497 |
| Confusion matrix | Exact match | Exact match |
| Held-out test images accessed | 0 | 0 |

Both members independently confirmed the following:

- The saved Joblib model was successfully reloaded.
- The Linear SVM configuration and `C = 1.0` were verified.
- Probability estimates remained disabled.
- The approved manifest identity was verified.
- The reloaded model generated 226 validation predictions.
- Validation accuracy of 68.58% and macro-F1 of 0.6497 were reproduced.
- The saved confusion matrix matched the reproduced predictions exactly.
- The held-out test split remained untouched.
- `python -m pip check` reported no broken requirements.

### 7.4 Final repository integration

PR #14 was merged into `main` at commit:

`b98cb3a946678eff3a55201d4a27f0e460a26d48`

Both members independently confirmed:

- Their current branch was `main`.
- Their local `HEAD` matched `origin/main` at the PR #14 merge commit.
- Their working trees were clean.
- The development dependency files were present on `main`.
- All 20 automated tests passed after the merge.
- Saved-model verification completed successfully.

The earlier post-PR #12 test-runner limitation is therefore resolved. The automated tests are now available through the shared development dependency setup.

The held-out test dataset remains unused and reserved for Step 6.

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

## 10. Current Completion Status

Member 1 implemented, trained and evaluated the baseline HOG + Linear SVM classifier. Member 2 independently reviewed the implementation and verified the saved model and validation results.

### 10.1 Baseline implementation

- Member 1 implemented the manifest-driven dataset loader and image preprocessing.
- HOG feature extraction was implemented and verified, producing 8,100 features per image.
- The baseline Linear SVM was trained using the 812 effective training images.
- Validation used all 226 approved validation images.
- The resulting baseline achieved 68.58% validation accuracy and 0.6497 macro-F1.
- The saved model, validation reports and confusion matrix were generated and committed.
- The saved model was configured for Git LFS and successfully retrieved by both members.

### 10.2 Pull requests and integration

The following Step 3 pull requests have been merged:

| Pull Request | Purpose | Merge commit |
|---|---|---|
| PR #12 | Baseline HOG + Linear SVM implementation | `a72d482` |
| PR #13 | Final post-merge Step 3 documentation corrections | `edf3819` |
| PR #14 | Locked pytest development dependencies | `b98cb3a` |

PR #12 received Member 2's independent review of the baseline implementation, automated tests, saved model and validation results.

PR #13 corrected the Step 3 documentation following the baseline merge.

PR #14 resolved the missing pytest development dependency and was independently reviewed and approved by Member 2.

### 10.3 Final post-merge verification

Both members synchronised their local repositories with `origin/main` after PR #14.

The final shared main commit is:

`b98cb3a946678eff3a55201d4a27f0e460a26d48`

Both members independently:

- Confirmed that local `main` matched `origin/main`.
- Confirmed clean working trees.
- Confirmed Python 3.13.17 and pytest 9.2.0.
- Ran `python -m pip check` successfully.
- Ran the complete automated test suite, with 20/20 tests passing.
- Ran `scripts/verify_baseline.py` successfully.
- Reproduced 68.58% validation accuracy and 0.6497 macro-F1.
- Confirmed an exact match between the saved and reproduced confusion matrices.
- Confirmed that the saved model referenced the approved manifest.
- Confirmed that no held-out test images were accessed.

### 10.4 Remaining limitations

1. The baseline is an initial classifier, not necessarily the final selected model.
2. It classifies one whole image into one class; it is not an object detector.
3. It does not provide calibrated confidence probabilities.
4. Pencil and Mug remain the weakest-performing classes and require attention during model comparison.
5. The held-out test dataset has not been accessed and remains reserved for Step 6.
6. The prediction application and camera-input workflow remain for Step 5.
7. Physical robot construction and integration remain outside the completed baseline implementation.

### 10.5 Final Step 3 status

The baseline implementation, validation, independent review, dependency integration, automated testing, saved-model verification and Git integration have been completed.

Both members independently reproduced the baseline results after the final dependency integration.

The final documentation closeout is being prepared on the `docs/step3-final-closeout` branch for independent review and integration.

**Step 3 - Baseline Classifier: COMPLETE.**

**Step 4 - Model Comparison and Selection: NOT STARTED.**

The held-out test dataset remains reserved for Step 6.
