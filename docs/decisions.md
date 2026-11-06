# PDE3802 Assessment 1 — Project Decisions

This document records the technical and organisational decisions agreed by the project team. Decisions should be updated when the team agrees on a change.

## D001 — No ROS

**Decision:** ROS will not be used in this project.

**Reason:** The lecturer explicitly instructed the group not to use ROS.

## D002 — Classification Scope

**Decision:** Part B will classify one office item per input image or camera frame.

**Reason:** This matches the assessment requirements.

## D003 — Classification Classes

**Decision:** The project will use the following eight classes:

1. Bottle
2. Calculator
3. Keyboard
4. Mouse
5. Mug
6. Notebook
7. Pencil
8. Scissors

**Reason:** These are the eight classes available in the selected dataset subset.

## D004 — Dataset Source and Licence

**Decision:** Use the selected subset of `office_home_dataset`, created by `stefanpublic`, from Roboflow Universe, version 1.

**Source:** https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1

**Licence:** CC BY 4.0.

**Reason:** The dataset provides the eight office-item classes required for the project. The source and licence have been checked and must be acknowledged in the project documentation.

## D005 — Dataset Splits

**Decision:** Preserve the existing training, validation and test splits.

**Current dataset counts:**

- Training: 816 images.
- Validation: 223 images.
- Testing: 103 images.
- Total: 1,142 images.

**Reason:** Keeping the existing splits supports consistent model development and evaluation.

The validation split will be used for model comparison and selection. The test split will remain held out until the final evaluation.

## D006 — Shared Git Repository

**Decision:** Both members will work from one agreed private GitHub repository.

**Reason:** A single shared repository provides a central location for project files, version history and collaboration.

Member 1 will coordinate the initial repository setup and connection to the local project. Member 2 will clone the shared repository rather than independently initialising a second repository for the same project.

The team must use the same agreed remote repository. A separate competing repository must not be used for project development.

## D007 — Shared Repository and Branch-Based Collaboration

**Decision:** The project uses a shared private GitHub repository and a branch-based collaboration workflow to support individual contributions, code review, integration, and traceability.

The `main` branch is maintained as the stable project baseline. Members must use task-specific branches for development rather than committing directly to `main` or another member's working branch.

For Step 4, the following integration arrangement was adopted:

- Member 1 maintained `feature/step4-model-comparison` as the Step 4 integration branch.
- Member 2 developed the RBF SVM implementation on `feature/step4-rbf-svm`.
- Member 1 reviewed Member 2's submitted work before integration.
- Implementation changes and supporting experimental evidence were integrated into the Step 4 branch through pull requests #16 and #17.
- The integrated Step 4 work remains separate from `main` until its verification, documentation, and closeout have been completed and the final integration has been reviewed.

Both members must synchronise their local repositories with the appropriate remote branch after approved changes. Commits should be meaningful and descriptive, and pull requests should provide a reviewable record of changes.

This workflow preserves contribution traceability, reduces the risk of conflicting changes, and allows the project to maintain a stable baseline while individual assessment stages are developed and reviewed.

## D008 — Git Commit and File Management

**Decision:** Commit meaningful project files and changes, and exclude unnecessary temporary files and sensitive information.

**Reason:** The repository should contain the files needed to understand, develop and run the project without storing passwords, access tokens, unnecessary caches or temporary files.

The `.gitignore` file will be used to exclude appropriate temporary and environment-specific files.

Before committing, members must inspect the Git status and review the changes being staged.

## D009 — Dataset Handling

**Decision:** Check the dataset's source, licence, size and intended distribution before committing dataset files to the repository.

**Current findings:**

- The local dataset contains 1,142 images.
- The dataset is approximately 21.04 MB.
- The source is Roboflow Universe.
- The listed licence is CC BY 4.0.
- Both members have confirmed that they have the same dataset structure and image counts.

**Reason:** The team must ensure that the dataset can be redistributed appropriately and that the repository does not contain unnecessary large files.

The dataset source and licence must be acknowledged in the README. The final dataset storage and submission arrangement must remain consistent with the assessment requirements.

## D010 — Development Environment

**Decision:** Use Visual Studio Code, Python and Git for project development and version control.

**Reason:** These tools provide a consistent development and collaboration workflow for both members.

Each member must verify their own environment and configure their Git identity before making commits.

## D011 — Model Validation and Held-Out Test Policy

**Decision:** The validation dataset is used for model development, candidate comparison, error analysis, and model selection. The held-out test dataset is reserved exclusively for the authorised final evaluation stage in Step 6.

For the Step 4 model comparison, all approved candidates must use the same fixed training and validation allocation established by D014. Training uses 812 eligible images, while validation uses 226 images. The 103 held-out test images must not be used for training, preprocessing, feature extraction, validation, hyperparameter selection, or model selection.

Model comparison considers:

- Validation accuracy.
- Macro-averaged F1-score.
- Per-class precision, recall, and F1-score.
- Confusion matrices and validation misclassification analysis.
- Model fitting time.
- Median prediction time per image, measured using the agreed timing procedure.
- Saved model size and relevant experiment metadata.

All candidates must use the same class order, preprocessing configuration, HOG feature-extraction configuration, and approved data allocation so that their results can be compared consistently.

Validation results are used to select the most suitable candidate for the project. They must not be described as independent test performance or as proof of generalisation to unseen data. Grouped cross-validation was not performed during Step 4 and must not be claimed.

The held-out test dataset remains untouched until Step 6, when the selected model may undergo the authorised final evaluation. Any reported results must clearly distinguish validation performance from final test performance.

## D012 — Project Documentation

**Decision:** Maintain an updated README, project plan, decision log and contribution log.

**Reason:** The documentation should accurately describe the project, explain important decisions and provide evidence of each member's actual work.

Documentation must be updated when the project workflow or agreed decisions change.

## D013 — Non-Time-Critical Organisation Task

**Decision:** The Part A organisation activity is not time-critical. There is no strict time limit per action once a turn or command has been established.

**Safety qualification:** The non-time-critical assumption does not remove the need for emergency-stop capability, appropriate fallback behaviour or timely responses to unsafe conditions.

**Timing:** No numerical task-completion-time target is established by this decision.

**Reason:** The Assessment 1 Part A brief explicitly states that the organisation activity is not time-critical. This decision records that requirement while preserving the need for safe operation and appropriate safety responses.

## D014 - Approved Group-Aware Manifest-Based Dataset Split

**Decision date:** 6 November 2026

**Decision status:** Approved by Member 1 (Project Lead), with Member 2's independent verification completed.

**Decision:** Use the approved group-aware full split manifest to determine the logical training, validation and test assignments used during classifier development and final evaluation.


### Relationship to earlier decision D005

This decision supersedes D005 only in relation to the logical split assignments used by classifier code.

The requirement to preserve the original dataset remains in force. The physical `dataset/train`, `dataset/valid` and `dataset/test` folders, their contents and their original assignments must not be moved, renamed, deleted or overwritten.

### Approved logical split

| Logical split | Images |
|---|---:|
| Training | 813 |
| Validation | 226 |
| Test | 103 |
| **Total** | **1,142** |

The manifest maps an image to its unchanged physical location using `Original_Split`, `Class` and `Filename`. The classifier uses `Proposed_Split` to determine its logical development assignment.

### Eligibility and evaluation boundaries

- Training: use only rows with `Proposed_Split=train` and `Effective_Training_Eligible=YES`. This gives 812 eligible training images.
- Validation: use all 226 rows with `Proposed_Split=valid`. The training-eligibility field is not a validation filter.
- Test: keep all 103 rows with `Proposed_Split=test` completely outside Step 3 and Step 4 image loading, preprocessing, feature extraction, training, validation and model selection. Reserve them for Step 6.

The existing severely pixelated Pencil image remains in the original dataset, but is excluded from effective training.

### Evidence and limitations

The approved manifest has 1,142 records and eight represented classes. The 47 supported and unresolved candidate relationships are contained within their proposed groups and splits. Candidate 007 remains separate because it was classified as related but distinct.

The 16 unresolved relationships remain unresolved; conservative grouping does not establish that they are confirmed duplicates. The allocation was manually configured and checked, not proven globally optimal. The review does not establish that every possible duplicate relationship in the dataset has been found.

### Authoritative manifest

`docs/evidence/step3.5.5J/step3.5.5K3_full_split_manifest_proposal.csv`

Canonical committed Git-file SHA256 (LF line endings):

`40FAD2A63BF4BA3185731154D1F5908901F5D224FD3F2D098FAE84C9B234B7D5`

### Independent verification

Member 2 independently verified the manifest contents, class counts, eligibility, group assignments and all 47 supported/unresolved relationships. The final canonical Git hash and documentation verification returned `OVERALL PASS` at shared commit `6b58e9fd25d4779a9ad8acff3909e40ca39d6e7b`.

The original dataset remains unchanged.

## D015 — Selected HOG and RBF SVM Classifier

**Decision date:** 6 November 2026
**Status:** Jointly selected by Member 1 and Member 2; selected-model verification passed on 6 November 2026.

**Decision:** The project selects the Histogram of Oriented Gradients (HOG) feature representation combined with a Radial Basis Function (RBF) Support Vector Machine (SVM) using `C=10` as the preferred classifier candidate for the subsequent project stage.

The selected configuration is:

- **Feature extraction:** HOG, producing 8,100 features per image.
- **Classifier:** SVM with an RBF kernel.
- **Regularisation parameter:** `C=10`.
- **Gamma:** `scale`.
- **Class weighting:** `None`.
- **Decision function:** One-versus-rest (`ovr`).
- **Probability estimation:** Disabled.
- **Input preprocessing:** EXIF orientation correction, grayscale conversion, and resizing to 128 × 128 pixels using `INTER_AREA`.

The comparison evaluated five candidates using the same approved training and validation allocation:

| Candidate | Validation accuracy | Macro-F1 |
|---|---:|---:|
| Linear baseline | 0.6858 | 0.6497 |
| Balanced linear | 0.6858 | 0.6497 |
| RBF, C=0.1 | 0.2965 | 0.1708 |
| RBF, C=1 | 0.7035 | 0.6183 |
| RBF, C=10 | 0.7257 | 0.6831 |

RBF SVM with `C=10` achieved the highest validation accuracy and macro-F1 among the five evaluated candidates. It was therefore preferred based on the agreed validation-based selection criteria. The selection was jointly accepted by both project members.

The selected model was retrained and saved at:

`results/selected_model/rbf_c10_hog_svm.joblib`

Its recorded validation results are:

- Validation accuracy: 72.57%.
- Validation macro-F1: 0.6831.
- Support vectors: 796.
- Saved model size: 51,676,393 bytes.

The recorded validation results reproduce the previous RBF C=10 candidate's accuracy, macro-F1, and confusion matrix.

**Dataset restriction:** Training used 812 eligible images and validation used 226 images, following the approved manifest in D014. The 103 held-out test images were not used. The selected model's reported performance is therefore validation performance, not independent test performance.

**Limitations:** Grouped cross-validation was not performed. The validation results alone cannot establish independent generalisation performance. The selected classifier must undergo the authorised final evaluation using the held-out test dataset in Step 6 before any independent test-performance claims are made.

**Supporting evidence:** The candidate comparison results are stored under `results/model_comparison/`. The selected model, validation metrics, predictions, classification report, confusion matrix, and verification metadata are stored under `results/selected_model/`.

## Open Questions — Not Yet Approved Decisions

The following matters require further team agreement, technical evidence or validation. Listing them here does not constitute approval of a particular solution.

### Application and Input Handling

1. Will the application use a command-line interface, graphical interface or another interaction method?
2. Which external image formats will be officially supported?
3. What camera hardware, camera selection method and acquisition method will be used?
4. What camera-preview and stop controls will be provided?
5. Will camera operation use manual or continuous frame classification?
6. What camera retry or recovery behaviour will be implemented?
7. If multiple-file input is provided, will the application continue processing remaining files or stop the batch after an individual failure?

### Classification and Image Processing

8. How will confidence values be displayed when available?
9. Will a confidence threshold or uncertain-prediction response be required?
10. How will images containing no supported item, unsupported objects or multiple items be handled?
11. What final image dimensions, colour representation, resizing, normalisation and preprocessing will the selected model require?

### Wider Autonomous System

12. What method will be used to find candidate office items?
13. Which mapping, robot-localisation and item-localisation methods will be selected?
14. What hardware will be selected for computing, cameras, sensors and the mobile platform?
15. Will autonomous manipulation be implemented, or will human assistance be required for some items?
16. How will classification categories be associated with approved storage destinations?
17. What retry, recovery and mission-completion rules will be used?

### Safety and Performance

18. What safety measures and operating limits will be required for the selected hardware?
19. How will emergency-stop, obstacle response, handling suitability and fallback behaviour be validated?
20. Are any additional response-time or frame-rate targets justified by the assessment requirements or technical evidence?

No numerical task-completion-time target is established for the Part A organisation activity. Any proposed classifier response-time or frame-rate target must be considered separately against the Part B requirements and supporting technical evidence, and must be agreed before being treated as a project decision.