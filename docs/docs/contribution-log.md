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

## 30 October 2026 — Step 1 Dataset Audit

### Member 1 — Project Lead

- Created the Step 1 audit branch `data/step1-dataset-audit`.
- Inspected the dataset structure and confirmed that all three splits contain the eight expected class folders.
- Prepared `scripts/audit_dataset.py` to perform a read-only dataset audit using Python and Pillow.
- Installed and verified Pillow in the project's Python virtual environment.
- Executed the audit and inspected all 1,142 dataset images.
- Confirmed that all 1,142 images were successfully decoded, with zero invalid or unreadable images and zero unsupported files.
- Confirmed that all images use JPEG format, have `.jpg` extensions and have dimensions of 416 × 416 pixels.
- Performed SHA-256 exact duplicate detection and found zero exact duplicate groups.
- Confirmed zero reported structure issues and zero reported file issues.
- Generated the audit results in `results/dataset_audit/`.
- Prepared the dataset audit report, including dataset source, licence, class distribution, split suitability and audit limitations.

**Evidence / Status:**

- Branch: `data/step1-dataset-audit`
- Script: `scripts/audit_dataset.py`
- Report: `docs/dataset-audit.md`
- Results: `results/dataset_audit/audit_summary.json`, `class_counts.csv`, `file_audit.csv` and `duplicates.json`
- Audit findings: 1,142 images inspected; zero invalid images, unsupported files, exact duplicate groups or reported issues.
- Status: Audit and report prepared; commit, push and Member 2 independent verification pending.
