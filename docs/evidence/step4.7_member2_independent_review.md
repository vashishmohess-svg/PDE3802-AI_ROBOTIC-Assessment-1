# PDE3802 Assessment 1 — Step 4.7 Member 2 Independent Review

**Review date:** 6 November 2026

**Review decision:** APPROVED — Implementation and verification evidence.

## 1. Review Snapshot

- Repository: `PDE3802-AI_ROBOTIC-Assessment-1`
- Branch: `feature/step4-model-comparison`
- Commit: `edb1664`
- Checkout: Detached HEAD, read-only review.
- Git status: Clean.
- Permanent model: `results/selected_model/rbf_c10_hog_svm.joblib`
- Verified model size: 51,676,393 bytes.

## 2. Model Implementation

Member 2 independently inspected the selected-model implementation and confirmed the jointly approved configuration:

- Kernel: RBF.
- C: 10.0.
- Gamma: scale.
- Class weight: None.
- Decision function: OVR.
- Probability estimates: Disabled.
- HOG features: 8,100 per image.

The approved D014 manifest SHA-256 was confirmed as:

`40FAD2A63BF4BA3185731154D1F5908901F5D224FD3F2D098FAE84C9B234B7D5`

Training uses 812 eligible images and validation uses 226 images.

## 3. Independent Verification Execution

Member 2 independently executed:

`python .\scripts\verify_selected_model.py`

The execution successfully:

- Reloaded the permanent Joblib model.
- Verified the model configuration and approved manifest.
- Recreated all 226 validation predictions exactly.
- Reproduced validation accuracy of 0.725664.
- Reproduced validation macro-F1 of 0.683149.
- Reproduced the saved confusion matrix exactly.
- Verified CSV and JSON classification reports.
- Confirmed 796 support vectors.
- Confirmed the model size of 51,676,393 bytes.

No errors occurred.

## 4. Candidate Comparison

Member 2 inspected the linear and RBF comparison summaries.

All five candidates were consistent with the saved evidence. RBF C=10 achieved the highest validation accuracy and macro-F1 and remained the justified selected candidate.

## 5. Held-Out Test Protection

The reviewed training and verification workflows request only their authorised training and validation splits.

The 103 held-out test images remain reserved for Step 6. No independent test evaluation or dataset modification was performed.

## 6. Documentation Review

Member 2 reviewed D011, D014, D015, the Step 4 technical report, validation metrics, and verification metadata.

The selected configuration, validation metrics, manifest identity, image counts, and stated limitations were consistent.

The documentation correctly identifies that grouped cross-validation was not performed and that validation results are not independent test results.

The following documentation closeout changes were requested:

1. Clarify that the 20 visually reviewed misclassifications were selected examples, not all incorrect validation predictions.
2. Record the completed independent review in Sections 9.2, 9.3, and 12.
3. Update Section 10 with the pushed review snapshot at commit `edb1664`.

These are documentation closeout actions, not model implementation defects.

## 7. Final Decision

**APPROVED — No required model-code corrections.**

Member 2 independently confirms that the selected-model implementation and verification evidence are technically consistent with the approved Step 4 protocol.

No project files, datasets, model artifacts, or Git branches were modified during the review.