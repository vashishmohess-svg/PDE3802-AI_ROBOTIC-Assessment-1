# PDE3802 Assessment 1 — Project Plan

## 1. Project Objective

Develop an Autonomous Office Item Organisation System. The project will include an image classification component that can recognise eight types of common office items and a system design describing how an autonomous robot could identify, locate and organise those items.

The implementation must follow the assessment requirements and the technical instructions provided by the lecturer.

The classification component will provide the predicted office-item class to the proposed robot system. The system design will explain how the robot could use this information as part of its wider item-finding and organisation workflow.

## 2. Team Responsibilities

### Member 1 — Project Lead and Dataset/Model Lead

- Coordinate the initial project setup and shared Git repository workflow.
- Lead dataset inspection, preparation and documentation.
- Develop and train the image classification models.
- Compare model performance using the validation dataset.
- Carry out the final evaluation using the held-out test dataset.
- Analyse classification errors and document the results.
- Coordinate project progress and maintain the overall development roadmap.

### Member 2 — Application and System Design Lead

- Verify the development environment and access to the shared repository.
- Independently check the shared software environment and dependencies.
- Develop the application that uses the trained classification model.
- Lead the autonomous robot system design.
- Support application testing and integration.
- Contribute to the project documentation and final deliverables.

### Shared Responsibilities

Both members will:

- Use the same agreed project repository.
- Follow the Git collaboration workflow.
- Review and test each other's contributions.
- Integrate the classification model and application.
- Check the final implementation and documentation.
- Prepare and review the final assessment submission.
- Maintain accurate records of their individual contributions.

## 3. Development Environment and Tools

The project uses:

- Visual Studio Code as the code editor.
- Python for the classification and application code.
- Git for version control.
- GitHub as the shared remote repository.
- Separate computers for both team members.
- The same project structure and dataset for both members.
- Python 3.13.17 (64-bit) as the agreed interpreter.
- Separate project-specific `.venv` virtual environments.
- Shared dependency files, including `requirements.txt` and `requirements-lock.txt`.

Both members have installed and verified the agreed Python version and dependencies.

Each member must use their own project virtual environment when working on the project. The shared dependency files should be used to maintain consistency between both computers.

Both members must keep their Git identity configured correctly before making commits to the shared repository.

ROS must not be used, in accordance with the lecturer's instruction. The proposed system design and classification application will therefore use a ROS-independent architecture.

## 4. Dataset and Classification Classes

### Dataset Source

- Dataset name: `office_home_dataset`
- Creator: `stefanpublic`
- Source: [Roboflow — office_home_dataset, version 1](https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1)
- Version: 1
- Licence: CC BY 4.0
- The project uses a selected subset containing eight office-item classes.

### Dataset Splits

**Original Physical Dataset Folders**

The original dataset folders contain the following image counts:

| Original split | Number of images |
|---|---:|
| Training (`train`) | 816 |
| Validation (`valid`) | 223 |
| Testing (`test`) | 103 |
| **Total** | **1,142** |

These counts describe the original physical dataset folders audited in Step 1.

**Approved Logical Dataset Splits — D014**

Following the group-aware dataset review, the approved manifest-based logical allocation is:

| Logical split | Number of images |
|---|---:|
| Training allocation | 813 |
| Validation | 226 |
| Testing | 103 |
| **Total** | **1,142** |

The classifier uses the approved manifest:

`docs/evidence/step3.5.5J/step3.5.5K3_full_split_manifest_proposal.csv`

The manifest maps images to their original physical locations and determines their logical assignments. The original dataset folders and image files remain unchanged.

One severely pixelated Pencil image is excluded from model fitting. Therefore, the effective training count is **812 images**.

### Classification Classes

1. Bottle
2. Calculator
3. Keyboard
4. Mouse
5. Mug
6. Notebook
7. Pencil
8. Scissors

Both members have confirmed the original dataset structure and image counts and participated in the dataset verification process.

The original physical dataset folders must remain unchanged. The approved manifest must be used for logical training and validation assignments.

The test dataset must remain separate from training and model selection. The 103 logical test images are reserved for final evaluation in Step 6 and must not be accessed during Steps 3 and 4.

The dataset source and CC BY 4.0 licence must be acknowledged in the project documentation and final dataset card.

## 5. Project Folder Structure

The project uses the following repository structure. The displayed root name represents the repository root; the local checkout folder name may differ between team members.

```text
repository-root/
│
├── dataset/
│   ├── train/
│   ├── valid/
│   └── test/
│
├── docs/
│   ├── contribution-log.md
│   ├── dataset-audit.md
│   ├── decisions.md
│   ├── member2-dataset-verification.md
│   ├── member2-setup-check.md
│   ├── project-plan.md
│   ├── step2-application-interface.md
│   ├── step2-classifier-requirements.md
│   ├── step2-environment-setup.md
│   ├── step2-system-design-outline.md
│   ├── step3-visual-label-review.md
│   ├── step3-baseline-results.md
│   └── evidence/
│       └── step3.5.5J/
│           └── approved dataset split and verification evidence
│
├── report/
│   └── .gitkeep
│
├── results/
│   ├── dataset_audit/
│   │   ├── audit_summary.json
│   │   ├── class_counts.csv
│   │   ├── duplicates.json
│   │   └── file_audit.csv
│   │
│   └── baseline/
│       ├── baseline_hog_linear_svm.joblib
│       ├── run_metadata.json
│       ├── validation_metrics.json
│       ├── validation_classification_report.json
│       ├── validation_classification_report.csv
│       ├── validation_confusion_matrix.csv
│       └── validation_confusion_matrix.png
│
├── scripts/
│   ├── audit_dataset.py
│   ├── train_baseline.py
│   └── verify_baseline.py
│
├── src/
│   └── office_item_classifier/
│       ├── __init__.py
│       ├── dataset.py
│       └── features.py
│
├── tests/
│   ├── test_dataset_loader.py
│   └── test_hog_features.py
│
├── .gitattributes
├── .gitignore
├── README.md
├── requirements-lock.txt
└── requirements.txt
```

The `dataset` directory contains the original training, validation and test image folders. The original physical dataset structure and image assignments remain unchanged. The approved manifest in `docs/evidence/step3.5.5J/` determines the logical training, validation and held-out test assignments used by the classifier.

The `docs` directory contains the project plan, decisions, requirements, system design, dataset audit, visual-review documentation, baseline results and supporting evidence.

The `scripts` directory contains the read-only dataset audit script, the baseline model training script and the saved-model verification script.

The `src/office_item_classifier` package contains the Python implementation. `dataset.py` handles manifest-driven dataset loading and image preprocessing. `features.py` implements HOG feature extraction.

The `tests` directory contains automated tests for the dataset loader and HOG feature extractor.

The `results/dataset_audit` directory stores the dataset audit outputs. The `results/baseline` directory stores the initial trained model and its validation evidence, including metrics, classification reports and confusion-matrix files.

The `.gitattributes` file configures Git LFS tracking for Joblib model files. The `.gitignore` file excludes unnecessary temporary and environment files.

The `requirements.txt` file records the six direct Python dependencies. The `requirements-lock.txt` file records the complete pinned dependency set.

The `report` directory is reserved for the final system design report.

The `.venv` directory is a local virtual environment and is not part of the shared project structure.

This structure may be extended as development progresses. Existing dataset files and established project files must not be moved or renamed without an agreed reason.

## 6. Development Stages

### Step 0 — Project Setup and Git Collaboration

Establish the initial project structure and shared repository workflow before beginning model development.

The workflow is:

1. Member 1 checks the local project folder, Python installation, Git installation and initial project files.
2. Member 1 establishes the agreed shared GitHub repository and connects the local project to it.
3. Member 1 prepares the README, `.gitignore` and minimum project folder structure.
4. Member 1 checks the files and Git changes before committing and pushing the initial project.
5. Member 2 verifies Python and Git, clones the shared repository and configures their Git identity.
6. Member 2 creates a separate test/contribution branch, makes a genuine project contribution, commits it and pushes the branch.
7. Member 1 reviews Member 2's contribution and merges it into the main branch after checking it.
8. Both members pull the latest main branch and verify that their local repositories are synchronised.

**Step 0 completion criteria:**

- Both members can access the same shared repository.
- The initial project files and folder structure are available remotely.
- Member 2 can clone the repository successfully.
- Both members can work using separate Git branches.
- A contribution from Member 2 can be reviewed and merged.
- Both members can update their local main branch successfully.
- No credentials, unnecessary temporary files or unintended large files are committed.

### Step 1 — Dataset Audit

- Verify the dataset folder structure.
- Confirm the eight classification classes.
- Check the image counts in each split.
- Check image formats and image readability.
- Identify file-level problems, including missing or unreadable images and misplaced files.
- Record duplicate-file findings.
- Record the dataset findings.
- Generate the dataset audit outputs.
- Have Member 2 independently verify the dataset structure and class counts.

The completed automated audit checked the dataset structure, class counts, image formats and readability, misplaced files and exact byte-identical duplicates. It did not constitute a full manual semantic review of every image label. A targeted visual review of representative images from all eight classes is therefore required as a separate pre-training quality check. This activity is included at the beginning of Step 3.

### Step 2 — Environment Setup

Prepare and verify a consistent Python development environment on both computers.

The work is divided into the following sub-stages:

**Step 2.1 — Repository Baseline**

- Confirm the shared repository and current Git branch.
- Check the project files and dependency documentation.
- Verify that both members are working from the shared repository.

**Step 2.2 — Independent Environment Inspection**

- Inspect both computers' Windows, Python, Git and development environments.
- Record CPU, RAM, graphics and available disk space.
- Check the previously installed Python packages and virtual environments.

**Step 2.3 — Shared Environment Agreement**

- Agree on the Python version.
- Review the dependency requirements.
- Consider compatibility and the hardware available on both computers.
- Agree on the shared environment configuration.

**Step 2.4A — Python 3.13.17 Installation and Verification**

- Install Python 3.13.17, 64-bit, on both computers.
- Verify the Python version and pip installation.
- Confirm that both members can access the selected interpreter.

**Step 2.4B — Clean Virtual Environments**

- Preserve and archive the previous virtual environments.
- Create a new project-specific `.venv` on each computer.
- Verify that each environment uses Python 3.13.17.
- Check the separate environment paths and package management.

**Step 2.5 — Shared Dependencies**

- Prepare the six direct dependencies in `requirements.txt`.
- Resolve and record the complete package set in `requirements-lock.txt`.
- Install the agreed packages on both computers.
- Confirm that the installed versions match the shared dependency files.

**Step 2.6 — Runtime and Cross-Computer Verification**

- Test the package imports.
- Test TensorFlow CPU execution.
- Test a basic scikit-learn SVM operation.
- Check image decoding using Pillow and OpenCV.
- Test basic Matplotlib plotting.
- Run `pip check`.
- Compare installed packages against the lock file.
- Verify the SHA-256 hash of the shared lock file.

**Step 2.7 — Documentation and Integration**

- Document the agreed Python environment and hardware information.
- Record the dependency versions and installation procedure.
- Document the runtime and cross-computer verification results.
- Record both members' contributions.
- Update the project plan to reflect the completed environment work.
- Review and merge the documentation changes through GitHub.

### Step 3 — Baseline Classifier

The purpose of this stage is to develop and evaluate an initial image-classification model that recognises the eight agreed office-item classes.

**Step 3.1 — Visual and Label Review (Complete)**

- Inspect representative training images from all eight classes.
- Have both members independently review the selected samples.
- Investigate suspected image-quality and label issues.
- Record the review findings.
- Exclude the severely pixelated Pencil image from model fitting while preserving the original image and dataset folders.

**Step 3.2 — Approved Dataset Allocation (Complete)**

- Use the group-aware, manifest-based logical split approved under decision D014.
- Preserve the original physical dataset folders and image files.
- Use 812 eligible training images after the approved Pencil-image exclusion.
- Use all 226 proposed validation images.
- Keep all 103 proposed test images held out for Step 6.

**Step 3.3 — Dataset Loader and Image Preprocessing (Complete)**

- Implement manifest-driven dataset loading.
- Apply EXIF orientation correction.
- Convert images to grayscale.
- Resize images to 128 × 128 pixels using OpenCV `INTER_AREA`.
- Verify that the approved training and validation images can be decoded successfully.
- Add automated dataset-loader tests.

**Step 3.4 — HOG Feature Extraction (Complete)**

- Implement Histogram of Oriented Gradients (HOG) feature extraction.
- Use a 128 × 128 window, 16 × 16 block size, 8 × 8 block stride, 8 × 8 cell size and 9 orientation bins.
- Verify the 8,100-feature descriptor for each image.
- Check feature dimensions, numerical validity and deterministic extraction.
- Add automated HOG feature-extraction tests.

**Step 3.5 — Baseline HOG + Linear SVM (Complete)**

- Implement an initial Support Vector Machine (SVM) classifier.
- Use a linear kernel with `C = 1.0`.
- Fit the classifier using the approved training set only.
- Keep probability estimates disabled.
- Save the fitted model and configuration.

**Step 3.6 — Baseline Validation and Evaluation (Complete)**

- Evaluate the baseline using the 226-image validation set.
- Calculate accuracy and macro-F1.
- Generate per-class precision, recall and F1 results.
- Generate a confusion matrix.
- Identify the largest classification errors and weaker-performing classes.
- Record the results and limitations.

The initial baseline achieved:

- Validation accuracy: **68.58%**.
- Validation macro-F1: **0.6497**.
- Automated tests: **20 passed**.

The strongest class by F1-score was Keyboard (0.8052). Pencil had the lowest F1-score (0.2857), followed by Mug (0.5333). These results will inform Step 4 model comparison.

**Step 3.7 — Saved Model Verification (Complete)**

- Reload the saved Joblib model.
- Verify its classifier type, linear kernel and `C = 1.0` configuration.
- Verify that probability estimates are not enabled.
- Confirm that the saved model references the approved manifest.
- Recreate validation predictions using the reloaded model.
- Confirm that the reproduced accuracy, macro-F1 and confusion matrix match the saved results.
- Confirm that the held-out test split has not been accessed.

**Step 3.8 — Documentation and Git Integration (In Progress)**

- Document the baseline configuration, validation results, confusion matrix and limitations in `docs/step3-baseline-results.md`.
- Update the project plan, dataset visual-review record and contribution log.
- Track the saved Joblib model using Git LFS.
- Commit and push the completed baseline implementation and documentation.
- Have Member 2 independently review the implementation, tests, saved model and validation results.
- Review and merge the contribution through GitHub.
- Confirm that both members can retrieve the model and run the verification successfully.
- Synchronise both members' repositories after integration.

**Step 3 completion criteria:**

- The baseline classifier is implemented and successfully trained.
- All approved training and validation images are processed successfully.
- Automated tests pass.
- Validation metrics and classification reports are saved.
- The saved model can be reloaded and its validation results reproduced.
- The held-out test split remains unused.
- Documentation and contribution records are updated.
- Member 2's independent verification and Git integration are completed.

The detailed baseline results are recorded in `docs/step3-baseline-results.md`.

**Important:** Completing the baseline does not mean that the final classifier has been selected. Model comparison and selection will take place separately in Step 4.


### Step 4 — Model Comparison and Selection

- Experiment with suitable classification models.
- Compare their performance using validation results.
- Consider accuracy, macro-F1 and computational requirements.
- Consider the hardware limits of both computers.
- Select the most suitable model for the project.
- Record the reasons for the selected model.

### Step 5 — Prediction Application

- Develop the application that loads the selected trained model.
- Allow an office-item image file or standard camera frame to be provided as input.
- Support the required image or file input workflow.
- Process one office item per image or camera frame.
- Display the predicted class and relevant confidence information.
- Handle invalid or unsupported inputs appropriately.
- Keep the application modular so that it can be integrated into the proposed robot system design.

### Step 6 — Final Held-Out Evaluation

- Evaluate the selected model using the test dataset.
- Calculate test accuracy and macro-F1.
- Generate a confusion matrix.
- Record and analyse incorrect predictions.
- Provide relevant examples of classification errors.
- Do not use test results to select or tune the model.

### Step 7 — Robustness and Input-Handling Tests

- Test the application with different office-item images.
- Test supported camera input.
- Check how it handles invalid image files and unsupported inputs.
- Test failure cases and image-loading problems.
- Record any limitations and errors.
- Verify that the application behaves consistently.

### Step 8 — Dataset Card and README

- Document the dataset source and licence.
- Describe the eight classes and dataset splits.
- Record the total dataset size on disk, image dimensions, image counts for each split, and image counts for each class within each split.
- Explain the project setup and execution instructions.
- Document how to provide image files and camera input.
- Explain the prediction output.
- Document the model and evaluation results.
- Include relevant troubleshooting guidance.
- Keep the README accurate and up to date.

### Step 9 — System Design Report

Prepare a system design report of fewer than four pages, using the required 11-point Microsoft Word format.

The report should explain the proposed autonomous office-item organisation system, including:

- The mission and tasks of the robot.
- Required skills and their inputs, outputs and success criteria.
- Hardware components and possible alternatives.
- Sensors, processing and system architecture.
- The interaction between the classification component and the proposed robot workflow.
- Safety considerations and relevant risks.
- Bill of materials and estimated budget.
- Dataset and model approach.
- References and team contributions.

The report must follow the lecturer's instructions, including the requirement not to use ROS.

### Step 10 — Videos

Prepare the required assessment videos:

- **Part A:** System concept video of less than three minutes.
- **Part B:** Two-minute code walkthrough.

The videos should clearly demonstrate the relevant system design and classification application. Both members should be prepared to explain their contributions.

Ensure that the submitted video links are accessible.

### Step 11 — Final Checks and Release

- Review the source code and project structure.
- Check the README and dataset documentation.
- Verify the evaluation results.
- Check the report and videos.
- Confirm that both members' contributions are recorded.
- Check that all required submission files are present.
- Confirm that both members can access and run the final project.
- Create a meaningful final Git commit and tagged submission release.

## 7. Working Constraints

- ROS must not be used.
- Part B handles one office item per input image or camera frame.
- The project uses the eight agreed office-item classes.
- The existing training, validation and test splits must be preserved.
- The test dataset must remain held out during training and model selection.
- Git commits must represent meaningful project changes.
- Both members must use the agreed shared repository.
- Both members must use the shared dependency files and their own project virtual environments.
- The classifier must support the required image-file and standard camera input workflows.
- Credentials, passwords and private access tokens must never be committed.

## 8. Assessment Deliverables

The final submission must include:

- Working office-item classification code.
- Support for image-file and standard camera input.
- Dataset files or an accessible dataset download link.
- Dataset card and complete README.
- Model evaluation results, including test accuracy, macro-F1, confusion matrix and error analysis.
- System design report of fewer than four pages in the required 11-point Word format.
- Part A system concept video of less than three minutes.
- Part B two-minute code walkthrough.
- Accessible video links.
- Meaningful Git commit history and a tagged submission release.

## 9. Current Project Status

**Current stage: Step 3 — Baseline Classifier is in progress.** The initial HOG + Linear SVM baseline has been implemented, trained and evaluated using the approved training and validation data. The saved model and its validation results have also been successfully verified. Documentation, repository integration and Member 2's independent baseline verification remain outstanding.

### Completed stages and integration

- Step 0 — Project Setup and Git Collaboration: completed by both members.
- Step 1 — Dataset Audit and Independent Verification: completed by both members.
- Step 2.1 — Repository Baseline: completed.
- Step 2.2 — Independent Environment Inspection: completed.
- Step 2.3 — Shared Environment Agreement: completed.
- Step 2.4A — Python 3.13.17 Installation and Verification: completed by both members.
- Step 2.4B — Clean Virtual Environments: completed by both members.
- Step 2.5A — Shared Dependency Preparation and Dry-Run Resolution: completed.
- Step 2.5B — Dependency Installation: completed by both members.
- Step 2.6 — Runtime and Cross-Computer Verification: completed by both members.
- Step 2.7 — Documentation and Integration: completed by both members.
- Step 3.1 — Representative Visual and Label Review: completed by both members.
- Step 3.2 — Approved Manifest-Based Dataset Allocation: completed.
- Step 3.3 — Dataset Loader and Image Preprocessing: implemented and tested by Member 1.
- Step 3.4 — HOG Feature Extraction: implemented and tested by Member 1.
- Step 3.5 — Initial HOG + Linear SVM Baseline: trained by Member 1.
- Step 3.6 — Baseline Validation and Evaluation: completed by Member 1.
- Step 3.7 — Saved Model Verification: completed by Member 1.

### Merged pull requests and Git integration

- PR #2 — Member 1 Dataset Audit: merged at commit `4dd6336`.
- PR #3 — Member 2 Independent Dataset Verification: merged at commit `41746fb`.
- PR #5 — Classifier Requirements: reviewed and merged at commit `3294c1e`.
- PR #6 — Application Interface and System Design: reviewed and merged at commit `b25e047`.
- PR #7 — Documentation Closeout: merged at commit `fda9951`.
- PR #8 — Shared Python Dependencies: reviewed and merged at commit `9a985b2`.
- PR #9 — Resolved Python Dependency Lock File: reviewed and merged at commit `b2e0aaa`.
- PR #10 — Step 2.7 Environment Setup Documentation and Project Plan: approved and merged at commit `54f7fda`.

Both members independently installed and tested the agreed Python environment. The shared dependency files contain six direct dependencies and 48 pinned package entries in the lock file.

Both members reported successful package imports, TensorFlow CPU execution, SVM testing, image decoding, Matplotlib testing and dependency consistency checks.

Both members also reported matching `requirements-lock.txt` SHA-256 hashes:

```text
99641B5F28BDE103918F0AA1E457E6C1386B6056BA68BF8D85DAFDA5A0A3E11D
```

### Step 2.7 — Documentation and Integration (Complete)

- Member 1 prepared `docs/step2-environment-setup.md`, documenting the agreed Python environment, hardware information, dependencies, installation procedure, runtime checks, Git integration and member contributions.
- Member 2 independently reviewed the environment information and completed the final documentation review.
- Both members synchronised their local `main` branches with `origin/main` after PR #10 was merged.
- Both members confirmed the merge commit, clean working trees and presence of the required documentation.
- Both members completed the post-merge documentation verification.

**Step 2 is complete. Steps 2.1–2.7 have been completed and verified by both members.**

### Step 3 — Baseline Classifier Progress

The following work has been completed by Member 1:

- The 48-image representative visual review was completed by both members.
- One severely pixelated Pencil image was excluded from model fitting while preserving the original dataset image.
- The D014-approved logical dataset allocation was implemented using the full split manifest.
- The dataset loader successfully processed 812 training images and 226 validation images.
- HOG feature extraction was implemented using 8,100 features per image.
- The automated test suite passed all 20 tests: 10 dataset-loader tests and 10 HOG feature tests.
- The linear SVM baseline was trained using 812 training images with `C = 1.0`.
- Validation produced 68.58% accuracy and a macro-F1 score of 0.6497.
- Validation metrics, per-class classification reports and confusion-matrix files were generated.
- The saved Joblib model was reloaded and the validation metrics and confusion matrix were reproduced successfully.
- The held-out test dataset was not accessed.

The baseline configuration and detailed results are recorded in `docs/step3-baseline-results.md`.

The `.joblib` model-file pattern has been configured for Git LFS, and the local tracking rule has been verified. The model has not yet been committed or uploaded through Git LFS.

**Remaining Step 3 work:**

- Complete the contribution-log update.
- Complete the visual-review documentation addendum for D014.
- Review all documentation changes.
- Confirm the Git LFS configuration and repository handling.
- Commit and push the baseline implementation, results and documentation.
- Have Member 2 independently verify the source code, tests, saved model and validation results.
- Review and merge the contribution through GitHub.
- Confirm that both members can retrieve the model and reproduce the verification results.
- Synchronise both members' repositories.

Step 3 remains in progress until these activities are completed.

### Outstanding development stages

- Step 4 — Model Comparison and Selection: not started.
- Step 5 — Prediction Application: not started.
- Step 6 — Final Held-Out Evaluation: not started.
- Step 7 — Robustness and Input-Handling Tests: not started.
- Step 8 — Dataset Card and README: final development documentation remains outstanding.
- Step 9 — System Design Report: final report remains outstanding.
- Step 10 — Videos: required assessment videos remain outstanding.
- Step 11 — Final Checks and Release: final integration and submission checks remain outstanding.

The initial baseline is not yet the final selected classifier. Model comparison must take place in Step 4 using training and validation data only. The 103-image held-out test set remains reserved for Step 6.

The prediction application, camera input workflow and physical robot have not yet been implemented or integrated.

The team must complete the outstanding Step 3 documentation, Git integration and Member 2 verification before proceeding to **Step 4 — Model Comparison and Selection**.