# PDE3802 Assessment 1 — Contribution Log

This document records the actual contributions made by each team member throughout the project.

Each contribution should describe the work completed and include evidence where available, such as a commit hash, pull request, file, test result or other relevant record.

| Date | Member | Work completed | Evidence / Status |
|---|---|---|---|
| 29/10/2026 | Member 2 | Selected and downloaded the office-item dataset from Roboflow Universe for the project. | Dataset source: https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1 |
| 29–30/10/2026 | Both members | Confirmed that both members have the same dataset structure, eight classification classes and image counts. | Dataset audit and split-count verification. |
| 30/10/2026 | Member 1 | Checked the local project folder, Python installation and Git installation. | Local environment checks. |
| 30/10/2026 | Member 1 | Inspected the dataset folders, image counts, file formats, dataset size, source and licence. | Dataset audit: 1,142 images across train, valid and test. |
| 30/10/2026 | Member 1 | Prepared and updated the project README with the project overview, dataset information, folder structure, development stages and dataset attribution. | `README.md` |
| 30/10/2026 | Member 1 | Prepared the `.gitignore` file to exclude Python temporary files, virtual environments, notebook checkpoints and other unnecessary files. | `.gitignore` |
| 30/10/2026 | Member 1 | Inspected the existing documentation and identified the need to update the project plan, decisions and contribution log to reflect the agreed Step 0 workflow. | `project-plan.md`, `decisions.md`, `contribution-log.md` |
| 30/10/2026 | Member 1 | Initialised the local Git repository, connected it to the shared GitHub repository, prepared the project files and created the initial commit. | Initial commit: `3274eba` |
| 30/10/2026 | Member 1 | Created and pushed the Step 0 contribution-log update after Member 2's pull request was merged. | Commit: `357d8bf` |
| 6/11/2026 | Member 1 | Implemented and trained the baseline HOG + Linear SVM classifier, generated validation evidence, verified the saved model and submitted the implementation through PR #12. | Commit `6fbae66`; 20 tests passed; validation accuracy 68.58%; macro-F1 0.6497; Git LFS model uploaded successfully. |
| 6/11/2026 | Member 2 | Independently verified the Step 3 baseline implementation, tests, saved model and validation results, and submitted formal approval on PR #12. | Review branch `review/step3-baseline-pr12`; 20/20 tests passed; model retrieved through Git LFS; validation metrics and confusion matrix reproduced; PR #12 approved. |


## Contribution Recording Rules

1. Record only work that has actually been completed.
2. Use the correct member name or role for each contribution.
3. Include the date on which the work was completed.
4. Add commit hashes when a contribution has been committed.
5. Do not invent commit hashes or evidence.
6. Update this log throughout the project rather than waiting until the final submission.
7. Record shared work as a joint contribution when both members genuinely participated.

## 30 October 2026 — Step 0 GitHub Collaboration and Integration

### Member 1 — Project Lead

- Created the initial shared project repository.
- Committed and pushed the initial project setup and dataset to GitHub.
- Initial commit: `3274eba` — Initial project setup and dataset.
- Reviewed Member 2's setup verification document.
- Independently compared all eight class counts across training, validation and testing against the original dataset audit.
- Confirmed that all 1,142 image counts matched.
- Corrected and committed documentation updates on the `member2-setup` branch.
- Reviewed and merged Member 2's Pull Request into `main`.

### Member 2 — Setup Verification

- Accepted access to the shared GitHub repository.
- Verified Python, Git and VS Code.
- Cloned the shared repository.
- Verified the project structure and dataset.
- Created `member2-setup` and added `docs/member2-setup-check.md`.
- Commit: `d35e66a` — docs: add member 2 setup verification.
- Successfully pushed the contribution to GitHub.

### Integration Status

- Member 2's contribution was reviewed by Member 1.
- Dataset counts were independently compared and confirmed.
- Documentation corrections were completed.
- Pull Request successfully merged into `main`.
- Both members synchronised their local repositories with the completed Step 0 changes.
- Step 0 was completed successfully by both members.

## 30–31 October 2026 — Step 1 Dataset Audit

### Member 1 — Project Lead

- Created the Step 1 audit branch `data/step1-dataset-audit`.
- Inspected the dataset structure and confirmed that all three splits contain the eight expected class folders.
- Prepared `scripts/audit_dataset.py` to perform a read-only dataset audit using Python and Pillow.
- Installed and verified Pillow in the project's Python virtual environment.
- Executed the initial audit and inspected all 1,142 dataset images.
- Confirmed the original image counts: 816 training, 223 validation and 103 testing images.
- Confirmed that all images use JPEG format, have `.jpg` extensions and have dimensions of 416 × 416 pixels.
- Performed SHA-256 exact duplicate detection and found zero exact duplicate groups.
- Generated the audit results in `results/dataset_audit/`.
- Prepared `docs/dataset-audit.md`, documenting the dataset source, licence, class distribution, split suitability and audit limitations.
- Committed and pushed the initial audit work to the shared GitHub repository.
- Addressed the requested improvements from Member 2's independent review by adding full image decoding using Pillow's `image.load()`, recursive directory checks and misplaced-file detection.
- Reran the revised audit and confirmed that all 1,142 images were successfully decoded, with zero invalid images, misplaced files, unexpected directories, exact duplicate groups or reported file issues.
- Updated the dataset audit report and audit results following the corrections.

**Evidence / Status:**

- Branch: `data/step1-dataset-audit`
- Initial audit commit: `0b5cb51` — data: add dataset audit and verification results.
- Pull Request: [PR #2](https://github.com/vashishmohess-svg/PDE3802-AI_ROBOTIC-Assessment-1/pull/2)
- Script: `scripts/audit_dataset.py`
- Report: `docs/dataset-audit.md`
- Results: `results/dataset_audit/audit_summary.json`, `class_counts.csv`, `file_audit.csv` and `duplicates.json`.
- Revised audit findings: 1,142 fully decoded images; zero invalid images, unsupported files, misplaced files, unexpected directories or exact duplicate groups.
- Status: Corrections prepared and revised audit completed; updated commit and Member 2's final review pending.

### Member 2 — Independent Dataset Verification

- Updated their local repository and checked out Member 1's Step 1 audit branch.
- Independently reran the dataset verification using their own local dataset.
- Confirmed the overall total of 1,142 images and all 24 class/split counts.
- Independently checked full image decoding using Pillow's `image.load()` and confirmed zero decoding failures.
- Confirmed that all images were JPEG files with dimensions of 416 × 416 pixels.
- Confirmed zero exact duplicate groups and no unexpected nested directories or misplaced files.
- Compared the independent audit results with Member 1's results and confirmed that they matched, apart from the audit timestamp.
- Reviewed Member 1's Pull Request #2 and submitted a Request changes review identifying improvements to full image decoding, recursive structure checks and contribution-log accuracy.

**Evidence / Status:**

- Independent verification: Completed.
- Pull Request review: Request changes submitted successfully.
- Final approval: Pending Member 2's verification of the final documentation corrections and approval of PR #2.

### Step 1 Integration Status

- Member 1's initial audit commit and pull request were completed.
- Member 2's independent dataset verification was completed.
- Member 1 has addressed Member 2's requested corrections, including full image decoding and recursive structure checks.
- The revised audit was executed successfully, and the audit report and results were updated. Member 1 committed and pushed the corrections in commit `77fe99e`; Member 2's final verification and approval are pending.
- Pull Request #2 remains open and must receive Member 2's final review and approval before merging.
- Member 2's verification document and final Step 1 integration remain pending.
## 31 October 2026 — Step 1.12 Member 2 Verification Update

This update supersedes the earlier pending statements about PR #2.

### Member 2 — Independent Verification

- Pulled main using git pull --ff-only origin main.
- Confirmed local main and origin/main at PR #2 merge commit 4dd6336.
- Created branch docs/step1-member2-verification.
- Independently confirmed all eight class folders in train, valid and test.
- Confirmed all 24 class/split counts against Member 1's report: 816 training, 223 validation and 103 testing images; 1,142 total.
- Confirmed all 1,142 files have .jpg extensions.
- Fully decoded all images using Python 3.13.14 and Pillow 12.3.0: all JPEG, all 416 x 416 pixels, zero unreadable files.
- Independently checked SHA-256 hashes: zero exact duplicate groups.
- Recursively checked directory placement: zero unexpected folders or misplaced files.
- Personally checked the Roboflow source page: office_home_dataset by stefanpublic, version 1, displayed licence CC BY 4.0.
- Prepared docs/member2-dataset-verification.md with verified findings and limitations.
- Performed these checks without modifying dataset images or regenerating Member 1's audit outputs.

### Current Integration Status

- PR #2 is merged at commit 4dd6336; the earlier statement that it remains open is outdated.
- Member 2's verification document is prepared locally.
- Commit, push and a separate verification-document PR remain pending.
- Member 1's review and merge of that PR remain pending.
- Final synchronization and verification by both members remain pending.
- Step 1 is not yet fully complete.

## 31 October 2026 — Step 1.13 Final Synchronization and Completion

This section records the final integration of the Member 2 dataset verification contribution and supersedes the earlier pending integration statements in the Step 1 records above.

### Member 1 — Project Lead

- Reviewed Member 2's independent dataset verification document and contribution-log update.
- Confirmed that the verification findings, class/split counts, image properties and limitations were consistent with the completed dataset audit.
- Approved and merged PR #3 into `main`.
- Pulled the merged changes using `git pull --ff-only origin main`.
- Confirmed that local `main` and `origin/main` were synchronized at commit `41746fb`.
- Confirmed that the working tree was clean.

### Member 2 — Independent Verification

- Submitted the independent dataset verification document through PR #3.
- Confirmed that PR #3 was successfully merged into `main`.
- Pulled the merged changes and confirmed that local `main` and `origin/main` were synchronized at commit `41746fb`.
- Confirmed that the working tree was clean.

### Final Integration Status

- PR #2 — Member 1 dataset audit: merged at commit `4dd6336`.
- PR #3 — Member 2 independent dataset verification: merged at commit `41746fb`.
- Both members confirmed that their local `main` branches match `origin/main`.
- Both members confirmed clean working trees.
- The dataset remains unchanged following the audit and independent verification.
- Step 1.13 — Final synchronization: completed.
- **Step 1 — Dataset audit and independent verification: completed by both members.**

## 1 November 2026 — Classifier Requirements Revision Following Member 2 Review

### Member 1 — Project Lead

- Received and reviewed Member 2's feedback on Pull Request #5.
- Revised `docs/step2-classifier-requirements.md` to clarify that confidence is returned and displayed when the selected model provides it.
- Defined the classifier result contract, including predicted class, confidence when available, input source, success/failure status and meaningful error information.
- Clarified that failed input acquisition, image opening, decoding or classification processing must not return a predicted class.
- Explicitly documented image-file input and standard-camera input requirements.
- Added requirements for independent processing of multiple image files, camera-opening and frame-acquisition failure handling, and safe camera-resource release.
- Added functional requirements FR-01 to FR-10, non-functional requirements NFR-01 to NFR-08, and acceptance criteria AC-01 to AC-16.
- Added requirement priorities and planned verification stages based on the official project-plan stages.
- Preserved the eight agreed classification classes, verified dataset counts, existing dataset splits, held-out test policy, CC BY 4.0 attribution and no-ROS decision.
- Reviewed the revised document structure, illustrative result examples, formatting and Git whitespace checks.

### Review and Integration Status

- Member 2 provided review feedback on PR #5 and requested corrections before approval.
- The revised requirements document is being prepared for Member 2's second review.
- PR #5 remains open and has not yet been merged.
- The requirements-document revision and contribution-log update must be committed and pushed before the second review.

**Status:** Requirements revision prepared; second review and integration pending.
## 1 November 2026 — Member 2 Requirements Review and Design Drafts

### Completed work

- Reviewed Member 1's classifier requirements in PR #5 and provided correction requests.
- Reviewed revision `d81e4a3` and submitted formal approval.
- Synchronised local `main` with PR #5 merge commit `3294c1e` and confirmed a clean working tree.
- Created branch `docs/step2-system-interface-design`.
- Inspected the existing decisions D001–D012 and official project plan.
- Confirmed that the requirements' verification-stage references match the official project stages. Official Step 2 remains Environment Setup; this requirements/interface planning activity does not replace it.
- Prepared `docs/step2-application-interface.md`, covering proposed interaction, file and camera workflows, result fields, conditional confidence, failure handling and safe camera shutdown.
- Prepared `docs/step2-system-design-outline.md`, covering the proposed mission, task sequence, skills, architecture, data flow, hardware alternatives, handling, safety and assistance.
- Kept unapproved design choices identified as proposals or open questions. No new approved decisions have been added.

### Current status

- Both design documents were committed as `a75d19c`, pushed on branch `docs/step2-system-interface-design` and submitted through PR #6.
- Member 1 completed the initial review of PR #6 and requested corrections. Member 2 pushed correction commit 46c18b0 to PR #6 for the second review. Member 1 reviewed it and requested final formatting and status corrections. Member 2 completed and pushed those final corrections in commit 6b96129. PR #6 is now awaiting Member 1 final review and approval. Re-review, approval, merge, joint consistency review and final synchronisation remain pending.
- The subsequent formal approval of PR #5 and its merge at `3294c1e` supersede the earlier entries stating that PR #5 review and integration were pending. Those earlier entries are retained as historical records.
- No classifier implementation, model training or physical robot integration was performed during this documentation work.
- The original dataset, split assignments and audit outputs remain unchanged.
- The project plan's historical Current Project Status section was identified as outdated and should be considered during joint documentation closeout.

## 2 November 2026 — Documentation Closeout Review and Consolidation

This section records the joint consistency review and completed documentation consolidation following the approval and merge of PR #6. It supersedes the earlier historical statements that PR #5 and PR #6 were still awaiting review, approval or merge.

### Joint Review and Agreed Clarifications

- Completed a joint consistency review of:
  - `docs/step2-classifier-requirements.md`
  - `docs/step2-application-interface.md`
  - `docs/step2-system-design-outline.md`
- Confirmed that the three documents consistently describe the eight agreed office-item classes and the one-item-per-image or camera-frame classification scope.
- Agreed to clarify multiple-file processing: each processed file must retain its own result or failure information, and an individual failure must not corrupt or be incorrectly attributed to another file.
- Left the batch continue-or-stop behaviour after an individual file failure as an open question. Files not processed must not be presented as successfully classified.
- Confirmed that the Part A organisation activity is not time-critical, while safety responses, emergency-stop capability and appropriate fallback behaviour remain necessary.
- Recorded D013 in `docs/decisions.md` to document the non-time-critical Part A requirement and its safety qualification.
- Added a separate `Open Questions — Not Yet Approved Decisions` section to distinguish unresolved matters from approved decisions. It contains 20 questions grouped by project topic.
- Preserved decisions D001–D012 and added D013 for the non-time-critical Part A requirement.

### Member 1 — Project Lead

- Created branch `docs/documentation-closeout` from the synchronised `main` branch at commit `b25e047`.
- Consolidated the documentation structure into a single `docs/` directory using Git file moves.
- Moved the contribution log, decisions document and project plan to the root of `docs/`, and removed the obsolete empty nested documentation directories after checking their contents.
- Updated affected document references to the consolidated paths.
- Updated `docs/step2-classifier-requirements.md` with the agreed multiple-file clarification and an accurate status distinguishing the merged requirements baseline from the pending closeout update.
- Updated `docs/step2-application-interface.md` and `docs/step2-system-design-outline.md` to reflect the PR #6 merge, joint review and current implementation status.
- Updated `docs/decisions.md` with D013 and the separate open-questions section.
- Updated `docs/project-plan.md` with the verified project folder structure, current documentation-closeout status and outstanding development stages.
- Checked the project documentation for obsolete `docs/docs/` references and ran Git whitespace validation.

### Integration Status

- PR #5 — Classifier Requirements: approved and merged at commit `3294c1e`.
- PR #6 — Application Interface and System Design: approved and merged at commit `b25e047`.
- Both members previously synchronised their local `main` branches with `origin/main` at `b25e047` and confirmed clean working trees.
- The documentation-closeout changes were committed as `f6a951f`, pushed to `origin/docs/documentation-closeout` and submitted through PR #7.
- Member 2 completed an initial review and identified three outdated current-status statements in this contribution log, the project plan and the README. The corrections have been incorporated into this PR #7 revision.
- Member 2's re-review and formal approval, Member 1's merge of PR #7, and final synchronisation by both members remain outstanding.
- Official Step 2 — Environment Setup has not started.
- Classifier implementation, model training, prediction-application implementation and physical robot construction or integration have not started.
- No dataset images, existing split assignments or dataset-audit outputs were changed during this documentation closeout work.

## 4 November 2026 — Step 2.7 Environment Setup Documentation and Integration

### Member 1 — Project Lead

- Prepared `docs/step2-environment-setup.md`, documenting the agreed Python environment, hardware information, dependencies, installation procedure, runtime checks, Git integration and member contributions.
- Updated the project documentation to reflect the agreed environment and completed verification activities.
- Submitted the documentation changes for review through PR #10.

### Member 2 — Independent Review

- Independently reviewed the environment documentation.
- Checked the agreed Python environment, dependency information and verification records.
- Completed the final documentation review and approval.

### Final Integration Status

- PR #10 — Step 2.7 Environment Setup Documentation and Project Plan: approved and merged at commit `54f7fda`.
- Member 1 and Member 2 synchronised their local `main` branches with `origin/main`.
- Both members confirmed the merged documentation was available and their working trees were clean.
- Both members completed the post-merge documentation verification.
- **Step 2.7 — Documentation and Integration: completed.**
- **Step 2 — Environment Setup: completed by both members.**

This update supersedes the earlier historical statements in the 2 November 2026 documentation closeout entry that Step 2 had not started or that the final integration remained pending.

## 6 November 2026 — Step 3 Baseline Classifier Implementation

### Member 1 — Project Lead

- Implemented the manifest-driven dataset loader in `src/office_item_classifier/dataset.py`.
- Implemented image preprocessing, including EXIF orientation correction, grayscale conversion and resizing to 128 × 128 pixels.
- Added 10 dataset-loader tests and successfully verified the complete decoding of 812 training images and 226 validation images.
- Implemented HOG feature extraction in `src/office_item_classifier/features.py`, producing 8,100 features per image.
- Added 10 HOG feature-extraction tests covering descriptor dimensions, numerical validity, deterministic extraction and invalid inputs.
- Successfully ran the complete automated test suite, with all 20 tests passing.
- Implemented `scripts/train_baseline.py` and trained the initial HOG + Linear SVM classifier using 812 training images.
- Evaluated the model using 226 validation images, achieving 68.58% accuracy and 0.6497 macro-F1.
- Generated the validation metrics, per-class classification reports, confusion matrix and saved model under `results/baseline/`.
- Implemented `scripts/verify_baseline.py` and successfully reloaded the saved model.
- Reproduced the validation accuracy, macro-F1 and confusion matrix from the reloaded model.
- Confirmed that probability estimates are not enabled and that the held-out test dataset was not accessed.
- Prepared `docs/step3-baseline-results.md` to document the baseline configuration, evaluation results and limitations.
- Updated the project plan and visual-review documentation to reflect the approved D014 logical split and completed baseline work.
- Configured Git LFS to track `.joblib` model files and verified that the baseline model matches the LFS tracking rule.

**Evidence / Status:**

- Branch: `feature/step3-baseline-classifier`.
- Dataset loader: `src/office_item_classifier/dataset.py`.
- HOG implementation: `src/office_item_classifier/features.py`.
- Training script: `scripts/train_baseline.py`.
- Verification script: `scripts/verify_baseline.py`.
- Automated tests: 20 passed.
- Validation accuracy: 68.58%.
- Validation macro-F1: 0.6497.
- Baseline outputs: `results/baseline/`.
- Detailed results: `docs/step3-baseline-results.md`.
- Git commit: `6fbae66` — baseline HOG + Linear SVM implementation and supporting files.
- Pull Request: [PR #12](https://github.com/vashishmohess-svg/PDE3802-AI_ROBOTIC-Assessment-1/pull/12).
- Git LFS: configured and successfully uploaded the 48,560,430-byte Joblib model.
- Member 2's independent baseline code and model verification: completed; formal approval submitted on PR #12.
- Final PR merge and repository synchronisation: pending.

### AI Assistance Record

ChatGPT provided code drafts, test scaffolding, debugging guidance and documentation suggestions. Member 1 executed the commands in the local project environment, inspected the outputs, applied corrections and verified the implementation. No percentage of AI contribution is claimed.

**### Member 2 — Independent Baseline Verification**

Member 2 completed the independent verification of the Step 3 baseline implementation on 6 November 2026 and submitted formal approval on PR #12.

- Checked out the separate review branch `review/step3-baseline-pr12`.
- Successfully retrieved the saved model through Git LFS and verified its size as 48,560,430 bytes.
- Independently ran the complete automated test suite: 20/20 tests passed.
- Reloaded the saved model and verified the Linear SVM configuration with `C = 1.0`.
- Confirmed the eight classification classes and D014-approved manifest.
- Confirmed 812 effective training images and 226 validation images.
- Regenerated validation predictions and reproduced 68.58% accuracy and 0.6497 macro-F1.
- Confirmed that the saved confusion matrix matched exactly.
- Confirmed that the 103 held-out test images were not accessed.
- Reviewed the dataset loader, HOG feature extraction, training and verification scripts, tests and supporting documentation.
- Submitted a formal approved GitHub review on PR #12.
- Identified one non-blocking documentation correction: the project plan still stated that the Git LFS model upload was pending.

**Evidence / Status:**

- Pull Request: https://github.com/vashishmohess-svg/PDE3802-AI_ROBOTIC-Assessment-1/pull/12
- Review branch: `review/step3-baseline-pr12`.
- Reviewed commit: `6fbae66`.
- Automated tests: 20/20 passed.
- Git LFS model retrieval: successful.
- Validation metrics and confusion matrix: independently reproduced.
- GitHub review: approved.
- Member 2 confirmed a clean working tree and made no source-code, dataset, manifest or repository-history changes.

Member 2's local verification evidence is retained in their temporary folder `PDE3802_PR12_Verification`.

### Step 3 Integration Status**

The initial baseline implementation, training, validation and saved-model verification have been completed by Member 1.

- The baseline source code, tests, training script, verification script, saved model and validation results were committed in `6fbae66`.
- Git LFS tracking was configured, and the 48,560,430-byte Joblib model was successfully uploaded.
- PR #12 was submitted for integration.
- Member 2 independently retrieved and verified the saved model, ran all 20 automated tests successfully, reproduced the validation metrics and confusion matrix, and submitted formal approval on PR #12.
- One non-blocking documentation correction was identified: the project plan still described the Git LFS upload as pending.

**Remaining integration work:**

- Correct the outdated Git LFS statement in the project plan and finalise the contribution-log update.
- Commit and push the documentation corrections to PR #12.
- Confirm whether Member 2's approval remains active after the additional commit.
- Merge PR #12.
- Both members synchronise their local `main` branches with `origin/main`.
- Both members verify the merged model, automated tests and saved-model validation results, and confirm clean working trees.

Step 3 remains in progress until the documentation correction, PR merge and final synchronisation are completed.
