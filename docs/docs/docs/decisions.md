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

## D007 — Git Collaboration Workflow

**Decision:** Both members will use separate branches when contributing changes.

**Workflow:**

1. Member 1 prepares and pushes the initial project structure to the shared repository.
2. Member 2 clones the repository.
3. Member 2 creates a separate contribution branch.
4. Member 2 makes and commits a genuine project contribution.
5. Member 2 pushes the branch to GitHub.
6. Member 1 reviews the changes before merging them into `main`.
7. Both members pull the updated `main` branch.

**Reason:** This workflow helps prevent conflicting changes and provides a reviewable record of each member's contributions.

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

## D011 — Evaluation Method

**Decision:** Use the validation dataset for model comparison and reserve the test dataset for final evaluation.

**Reason:** The final test results should provide an independent assessment of the selected model's performance.

The final evaluation must include:

- Test accuracy.
- Macro-F1 score.
- Confusion matrix.
- Error analysis.

The test dataset must not be used to select or tune models.

## D012 — Project Documentation

**Decision:** Maintain an updated README, project plan, decision log and contribution log.

**Reason:** The documentation should accurately describe the project, explain important decisions and provide evidence of each member's actual work.

Documentation must be updated when the project workflow or agreed decisions change.

