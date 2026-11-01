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
- Member 1 completed the initial review of PR #6 and requested corrections. Member 2 pushed correction commit 46c18b0 to PR #6 for the second review. Member 1 reviewed it and requested final formatting and status corrections. Re-review, approval, merge, joint consistency review and final synchronisation remain pending.
- The subsequent formal approval of PR #5 and its merge at `3294c1e` supersede the earlier entries stating that PR #5 review and integration were pending. Those earlier entries are retained as historical records.
- No classifier implementation, model training or physical robot integration was performed during this documentation work.
- The original dataset, split assignments and audit outputs remain unchanged.
- The project plan's historical Current Project Status section was identified as outdated and should be considered during joint documentation closeout.
