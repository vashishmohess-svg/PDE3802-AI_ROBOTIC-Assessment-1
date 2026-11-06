
# Step 4 — Model Comparison, Selection and Verification

**Project:** PDE3802 Assessment 1 — Autonomous Office Item Organisation System and Office-Goods Classification

**Date:** 6 November 2026

**Status:** Model comparison, validation-based selection, visual error review, permanent model creation and selected-model verification completed. Independent review, documentation and final Git integration in progress.

## 1. Purpose and Scope

Step 4 compares suitable HOG + Support Vector Machine (SVM) classifiers for the eight office-item categories established during Step 3.

The objective is to select a suitable classifier using the approved training and validation data, considering predictive performance, computational requirements and model size.

The five candidates compared were:

1. HOG + Linear SVM, C = 1.0.
2. HOG + Balanced Linear SVM, C = 1.0.
3. HOG + RBF SVM, C = 0.1.
4. HOG + RBF SVM, C = 1.0.
5. HOG + RBF SVM, C = 10.0.

The selected model is HOG + RBF SVM with C = 10.0.

The evaluation in this stage uses validation data only. The 103-image held-out test split remains reserved for Step 6.

## 2. Approved Dataset and Feature Configuration

Step 4 uses the D014-approved logical dataset allocation:

| Data allocation | Images | Purpose |
|---|---:|---|
| Effective training | 812 | Model fitting |
| Validation | 226 | Candidate comparison and model selection |
| Held-out test | 103 | Reserved for Step 6 |

The approved manifest is:

`docs/evidence/step3.5.5J/step3.5.5K3_full_split_manifest_proposal.csv`

Canonical manifest SHA-256:

`40FAD2A63BF4BA3185731154D1F5908901F5D224FD3F2D098FAE84C9B234B7D5`

The original physical dataset folders and files remain unchanged. The manifest determines the logical assignments used by the classifier.

The severely pixelated Pencil image remains physically present in the original dataset but is excluded from effective model training in accordance with the approved dataset decision.

### 2.1 Class order

All candidates use the following eight classes in the same order:

1. Bottle
2. Calculator
3. Keyboard
4. Mouse
5. Mug
6. Notebook
7. Pencil
8. Scissors

### 2.2 Image preprocessing

The approved preprocessing pipeline is:

1. Apply EXIF orientation correction.
2. Convert the image to grayscale.
3. Resize to 128 × 128 pixels.
4. Use OpenCV `INTER_AREA` interpolation.
5. Convert the processed image into the required numerical representation for feature extraction.

Original dataset image files are not modified.

### 2.3 HOG feature extraction

Histogram of Oriented Gradients (HOG) is used to represent image structure.

| Parameter | Configuration |
|---|---|
| Window size | 128 × 128 |
| Block size | 16 × 16 |
| Block stride | 8 × 8 |
| Cell size | 8 × 8 |
| Orientation bins | 9 |
| Features per image | 8,100 |

The feature matrices used in the experiments were:

- Training: `(812, 8100)`
- Validation: `(226, 8100)`

The same preprocessing, HOG configuration, class order and approved manifest were used for the five candidates.

## 3. Experimental Protocol

### 3.1 Candidate configurations

| Candidate | Kernel | C | Gamma | Class weight | Probability |
|---|---|---:|---|---|---|
| linear_baseline | Linear | 1.0 | scale | None | Disabled |
| linear_balanced | Linear | 1.0 | scale | Balanced | Disabled |
| rbf_c0_1 | RBF | 0.1 | scale | None | Disabled |
| rbf_c1 | RBF | 1.0 | scale | None | Disabled |
| rbf_c10 | RBF | 10.0 | scale | None | Disabled |

The RBF candidates use the same gamma setting. The balanced linear candidate differs from the baseline through its class-weight configuration.

Probability estimates were disabled for all candidates.

### 3.2 Evaluation measures

The comparison recorded:

- Validation accuracy.
- Validation macro-F1.
- Per-class precision, recall and F1-score.
- Confusion matrices.
- Model-fitting time.
- Prediction time per validation image.
- Serialized model size.
- Number of support vectors.
- Training, validation and test-image counts.

Macro-F1 gives equal importance to each of the eight classes when calculating the average F1-score.

### 3.3 Prediction timing method

Prediction timing used:

1. One warm-up prediction.
2. Ten timed predictions over the complete batch of 226 validation feature vectors.
3. The median elapsed prediction time divided by 226 to obtain milliseconds per image.

HOG feature extraction was excluded from this prediction-time measurement.

### 3.4 Model size method

Model sizes were measured using uncompressed Joblib serialization with protocol 5.

The reported sizes are measured in bytes.

### 3.5 Evaluation restrictions

- Training used only the 812 eligible training images.
- Model evaluation and selection used the 226 validation images.
- The 103 test images were not used.
- No independent held-out test evaluation was performed.
- Grouped cross-validation was not performed.
- No claim of independent test performance is made.

## 4. Candidate Comparison Results

The following values are taken from the saved candidate comparison summaries.

| Candidate | Validation accuracy | Macro-F1 | Fit time (s) | Prediction (ms/image) | Model size (bytes) | Support vectors |
|---|---:|---:|---:|---:|---:|---:|
| Linear baseline | 0.685841 | 0.649654 | 6.0024 | 4.6995 | 48,560,421 | 748 |
| Balanced linear | 0.685841 | 0.649654 | 6.1708 | 5.7551 | 48,560,447 | 748 |
| RBF C=0.1 | 0.296460 | 0.170811 | 9.9661 | 9.7526 | 52,715,048 | 812 |
| RBF C=1 | 0.703540 | 0.618320 | 14.0173 | 6.0020 | 51,676,392 | 796 |
| RBF C=10 | **0.725664** | **0.683149** | 5.3498 | 6.5092 | 51,676,393 | 796 |

All five candidates used 812 training images and 226 validation images. Their comparison summaries recorded zero test images used.

### 4.1 Interpretation

The balanced linear candidate achieved the same validation accuracy and macro-F1 as the original linear baseline. It therefore did not improve the recorded overall validation metrics.

The RBF C=0.1 candidate performed poorly, achieving approximately 29.65% validation accuracy and 0.1708 macro-F1.

Increasing C to 1.0 improved RBF validation accuracy to approximately 70.35%, although its macro-F1 was lower than the linear baseline.

RBF C=10.0 achieved the strongest overall validation results among the five candidates:

- Accuracy: 72.57%.
- Macro-F1: 0.6831.

The selected RBF model's median prediction time was higher than the two linear candidates and RBF C=1.0. The selection therefore prioritises the strongest validation accuracy and macro-F1 while acknowledging the prediction-time trade-off.

The comparison fitting times are individual experimental measurements and may vary between separate executions.

## 5. Joint Model Selection

Following comparison of all five candidates, Member 1 and Member 2 jointly selected:

**HOG + RBF SVM, C = 10.0, gamma = scale.**

The agreed configuration is:

| Parameter | Selected value |
|---|---|
| Model | HOG + RBF SVM |
| Kernel | `rbf` |
| C | `10.0` |
| Gamma | `scale` |
| Class weight | `None` |
| Decision function shape | `ovr` |
| Probability estimates | Disabled |

### 5.1 Selection rationale

The selected candidate achieved the highest validation accuracy and macro-F1 among the five evaluated configurations.

Compared with the original linear baseline:

- Validation accuracy increased from approximately 68.58% to 72.57%, an improvement of approximately 3.98 percentage points.
- Macro-F1 increased from approximately 0.6497 to 0.6831.

The selection was made using validation results only. No held-out test results contributed to the decision.

Both members explicitly agreed to the selected configuration and its limitations.

## 6. Validation Error Analysis and Visual Review

The linear baseline misclassification review identified 20 incorrect predictions in the 226-image validation set.

The three largest error groups were:

| Actual class | Predicted class | Errors |
|---|---|---:|
| Scissors | Pencil | 9 |
| Mug | Bottle | 6 |
| Calculator | Mouse | 5 |
| **Total** | | **20** |

Member 2 led the visual review of all 20 misclassified validation images.

### 6.1 Scissors predicted as Pencil

All nine reviewed images were visually consistent with the Scissors label.

The review identified visual challenges including uncommon object orientations, multiple objects, packaging, and slender or closed scissor shapes.

### 6.2 Mug predicted as Bottle

All six reviewed images were visually consistent with the Mug label.

The review included stacked or multiple mugs, a dessert mug and tall cylindrical mug shapes. Two images appeared visually similar, but no confirmed duplicate or incorrect label was established.

### 6.3 Calculator predicted as Mouse

All five reviewed images were visually consistent with the Calculator label.

The reviewed examples included variations in rotation, contrast, cropping and background appearance.

### 6.4 Review conclusion

Member 2 found no confirmed incorrect labels among the 20 reviewed validation errors.

No dataset image was renamed, moved, deleted, edited, relabelled or reassigned as a result of this review.

The visual findings are used to understand possible classification difficulties. They do not establish that all dataset images have been manually inspected or that every possible label issue has been identified.

Supporting files include:

- `results/model_comparison/linear/linear_misclassification_review.csv`
- `results/model_comparison/linear/review_contact_sheets/scissors_to_pencil.png`
- `results/model_comparison/linear/review_contact_sheets/mug_to_bottle.png`
- `results/model_comparison/linear/review_contact_sheets/calculator_to_mouse.png`

## 7. Permanent Selected Model

The selected model was trained again using the approved RBF C=10 configuration to create a permanent, reproducible model artifact.

Model path:

`results/selected_model/rbf_c10_hog_svm.joblib`

The permanent training process used:

- 812 eligible training images.
- 226 validation images.
- The approved manifest and manifest hash.
- The approved grayscale preprocessing and HOG configuration.
- RBF SVM with C=10.0 and gamma=`scale`.
- Probability estimates disabled.

The permanent model's recorded validation results are:

| Metric | Result |
|---|---:|
| Validation accuracy | 0.725664 |
| Validation macro-F1 | 0.683149 |
| Support vectors | 796 |
| Model size | 51,676,393 bytes |
| Test images used | 0 |

The permanent model's recorded fitting time was approximately 14.49 seconds. This is from the separate permanent-model training execution, whereas the candidate comparison table records approximately 5.35 seconds for the original RBF C=10 experiment. These are separate runs; the comparison-table fitting time is retained for the five-candidate comparison.

### 7.1 Per-class F1-score

The selected model achieved the following validation F1-scores:

| Class | Selected RBF C=10 F1 |
|---|---:|
| Bottle | 0.6667 |
| Calculator | 0.7143 |
| Keyboard | 0.8378 |
| Mouse | 0.7606 |
| Mug | 0.5806 |
| Notebook | 0.7000 |
| Pencil | 0.4000 |
| Scissors | 0.8052 |

Pencil remains the weakest class by F1-score, although its result improved compared with the linear baseline. Mug also remains a class requiring attention.

## 8. Permanent Model Verification

The permanent model was reloaded from its saved Joblib file using:

`scripts/verify_selected_model.py`

The verification successfully checked:

- Existence of all seven selected-model artifacts.
- Successful reloading of the permanent Joblib model.
- The actual SVC configuration.
- All eight class identities and their order.
- Disabled probability estimates.
- The approved manifest SHA-256 identity.
- Image preprocessing and HOG parameters.
- The expected 8,100 input features.
- Training and validation metadata.
- Held-out test safeguards.
- All 226 saved validation predictions.
- Validation accuracy and macro-F1.
- The saved confusion matrix.
- CSV and JSON classification reports.
- Support-vector count and serialized model size.

The verification recreated all 226 validation predictions exactly and reproduced:

- Validation accuracy: 0.725664.
- Validation macro-F1: 0.683149.
- The saved confusion matrix: exact match.
- Support vectors: 796.
- Saved model size: 51,676,393 bytes.

The verification completed successfully with all reported checks passing.

No held-out test images were requested by the training or verification workflows.

### 8.1 Selected-model artifacts

The permanent selected-model directory contains:

1. `rbf_c10_hog_svm.joblib`
2. `validation_classification_report.csv`
3. `validation_classification_report.json`
4. `validation_confusion_matrix.csv`
5. `validation_metrics.json`
6. `validation_predictions.csv`
7. `verification_metadata.json`

## 9. Automated Testing and Independent Review

### 9.1 Implementation and evidence

Member 1 implemented the comparison and selected-model training and verification workflows, generated the relevant evidence and performed the verification execution.

The existing project tests include:

- `tests/test_dataset_loader.py`
- `tests/test_hog_features.py`
- `tests/test_model_comparison.py`
- `tests/test_rbf_comparison.py`

The model comparison scripts and evidence were integrated into the Step 4 integration branch.

### 9.2 Member 2 Independent Review

**Status: Pending.**

Member 1 successfully executed the selected-model verification workflow using `scripts/verify_selected_model.py`.

The verification completed successfully, confirming that the permanent model could be reloaded, its configuration and manifest identity were correct, and all 226 validation predictions and reported metrics were reproduced.

An independent review by Member 2 of the selected-model implementation and supporting verification evidence remains outstanding.

The review will be conducted after the selected-model scripts and supporting evidence are made available on the shared Step 4 integration branch.

The review will cover the model configuration, approved dataset allocation, preprocessing and HOG configuration, held-out test safeguards, reproducibility of validation results, and consistency of the saved evidence.

Member 2's review decision and any required corrections will be recorded here after the review has been completed. No independent approval is claimed at this stage.

### 9.3 Review Findings and Follow-up

No independent Member 2 review findings have been recorded yet.

Any observations, required corrections, and agreed follow-up actions will be documented after the independent review.

The selected-model verification has already passed the checks reported in Section 8. The independent review is intended to provide an additional source-code and evidence consistency check, rather than to claim that Member 2 independently executed the verification scripts.

## 10. Git Integration Evidence

The Step 4 work was developed and integrated on:

`feature/step4-model-comparison`

The linear and RBF source-code integration was completed through PR #16, with merge commit:

`4a6783f`

The RBF comparison evidence was integrated through PR #17, with merge commit:

`b49ddb6`

The recorded integration branch head after PR #17 was:

`b49ddb6`

The selected permanent model and its seven supporting artifacts were created after these comparison-evidence integrations and are included in the Step 4 documentation and integration closeout work.

Git LFS is configured through `.gitattributes` to track:

`*.joblib filter=lfs diff=lfs merge=lfs -text`

The selected model was confirmed to match the Git LFS tracking rule before integration.

The selected model and the remaining local Step 4 artifacts must be reviewed and committed through the controlled Step 4.8 integration process.

## 11. Limitations

The following limitations apply to the Step 4 results:

1. Model selection was based on the approved validation dataset. The validation results are not independent test results.
2. Grouped cross-validation was not performed.
3. The held-out test split of 103 images remains unused and reserved for Step 6.
4. The classifier processes one whole image at a time and is not an object detector.
5. The model does not provide calibrated probability estimates.
6. Prediction timing is based on the documented local experimental protocol and is not a universal hardware-performance guarantee.
7. The visual error review covered the 20 baseline validation misclassifications, not every dataset image.
8. Pencil remains the weakest-performing class by validation F1-score.
9. The classifier has not yet been integrated into the Step 5 prediction application or a physical robot.

## 12. Step 4 Completion Record

The following Step 4 activities have been completed:

| Checkpoint | Activity | Status |
|---|---|---|
| 4.0 | Git synchronisation | Complete |
| 4.1 | Source inspection | Complete |
| 4.2 | Experiment protocol agreement | Complete |
| 4.3 | Implementation, review and integration | Complete |
| 4.4 | Experiments and visual review | Complete |
| 4.5 | Joint model selection | Complete |
| 4.6 | Permanent selected-model verification | Complete |
| 4.7 | Independent source-code review | Pending |
| 4.8 | Documentation and Git integration | In progress |
| 4.9 | Final Step 4 closeout | Pending |

The selected HOG + RBF SVM with C=10.0 has been jointly approved, trained, saved and successfully verified.

The held-out test dataset remains untouched and reserved for Step 6.

**Step 4 — Model Comparison and Selection: Experimental work, model selection and permanent-model verification complete; independent review, documentation and final Git integration in progress.**