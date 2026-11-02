

# PDE3802 Assessment 1 — Project Plan

## 1. Project Objective

Develop an Autonomous Office Item Organisation System. The project will include an image classification component that can recognise eight types of common office items and a system design describing how an autonomous robot could identify, locate and organise those items.

The implementation must follow the assessment requirements and the technical instructions provided by the lecturer.

## 2. Team Responsibilities

### Member 1 — Project Lead and Dataset/Model Lead

- Coordinate the initial project setup and shared Git repository workflow.
- Lead dataset inspection, preparation and documentation.
- Develop and train the image classification models.
- Compare model performance using the validation dataset.
- Carry out the final evaluation using the held-out test dataset.
- Analyse classification errors and document the results.

### Member 2 — Application and System Design Lead

- Verify the development environment and access to the shared repository.
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

## 3. Development Environment and Tools

The project will use:

- Visual Studio Code as the code editor.
- Python for the classification and application code.
- Git for version control.
- GitHub as the shared remote repository.
- Separate computers for both team members.
- The same project structure and dataset for both members.

Each member must verify their own Python and Git installations and configure Git identity before contributing to the shared repository.

## 4. Dataset and Classification Classes

### Dataset Source

- Dataset name: `office_home_dataset`
- Creator: `stefanpublic`
- Source: https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1
- Version: 1
- Licence: CC BY 4.0
- The project uses a selected subset containing eight office-item classes.

### Dataset Splits

| Split | Number of images |
|---|---:|
| Training | 816 |
| Validation | 223 |
| Testing | 103 |
| **Total** | **1,142** |

### Classification Classes

1. Bottle
2. Calculator
3. Keyboard
4. Mouse
5. Mug
6. Notebook
7. Pencil
8. Scissors

Both members have confirmed that they have the same dataset structure and image counts.

The existing training, validation and test splits must be preserved. The completed dataset audit did not identify a reason to change the existing split assignments.

The test dataset must remain separate from training and model selection. It will only be used for the final evaluation.

## 5. Project Folder Structure

The project uses the following structure:

```text
1.office-item-classifier/
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
│   └── step2-system-design-outline.md
│
├── report/
│   └── .gitkeep
│
├── results/
│   ├── .gitkeep
│   └── dataset_audit/
│       ├── audit_summary.json
│       ├── class_counts.csv
│       ├── duplicates.json
│       └── file_audit.csv
│
├── scripts/
│   └── audit_dataset.py
│
├── src/
│   └── .gitkeep
│
├── tests/
│   └── .gitkeep
│
├── .gitignore
└── README.md
```

The `dataset` directory contains the existing training, validation and testing splits. Their class-folder structure and image assignments must remain unchanged.

The `docs` directory contains the project documentation, requirements, interface planning, system design, decisions and contribution records.

The `scripts` directory currently contains the read-only dataset audit script. The `results/dataset_audit` directory contains the generated audit outputs.

The `report`, `src` and `tests` directories are reserved for their respective project work.

The folder structure may be extended as development progresses, but existing project files and dataset folders must not be moved or renamed without an agreed reason.

## 6. Development Stages

### Step 0 — Project Setup and Git Collaboration

Establish a working development environment and a shared repository before beginning model development.

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
- The dataset source, licence, size and access arrangements are documented.
- No credentials, unnecessary temporary files or unintended large files are committed.

### Step 1 — Dataset Audit

- Verify the dataset folder structure.
- Confirm the eight classification classes.
- Check the image counts in each split.
- Check image formats and image readability.
- Identify missing, corrupted or incorrectly labelled images.
- Record the dataset findings.

### Step 2 — Environment Setup

- Prepare the Python environment.
- Install the required libraries.
- Verify that the classification libraries work correctly.
- Confirm that both members can run the project code.

### Step 3 — Baseline Classifier

- Develop an initial image classification model.
- Train it using the training dataset.
- Evaluate its performance using the validation dataset.
- Record the initial results.

### Step 4 — Model Comparison and Selection

- Experiment with suitable classification models.
- Compare their performance using validation results.
- Consider accuracy and macro-F1.
- Select the most suitable model for the project.

### Step 5 — Prediction Application

- Develop the application that loads the selected trained model.
- Allow an office-item image to be provided as input.
- Display the predicted class and relevant confidence information.
- Handle invalid or unsupported inputs appropriately.

### Step 6 — Final Held-Out Evaluation

- Evaluate the selected model using the test dataset.
- Calculate test accuracy and macro-F1.
- Generate a confusion matrix.
- Record and analyse incorrect predictions.
- Do not use test results to select or tune the model.

### Step 7 — Robustness and Input-Handling Tests

- Test the application with different office-item images.
- Check how it handles invalid image files and unsupported inputs.
- Record any limitations and errors.
- Verify that the application behaves consistently.

### Step 8 — Dataset Card and README

- Document the dataset source and licence.
- Describe the eight classes and dataset splits.
- Explain the project setup and execution instructions.
- Document the model and evaluation results.
- Keep the README accurate and up to date.

### Step 9 — System Design Report

Prepare a system design report of fewer than four pages.

The report should explain the proposed autonomous office-item organisation system, including its main components, workflow and interaction with the image classification system.

### Step 10 — Videos

- Prepare the required assessment videos.
- Demonstrate the working classification application.
- Demonstrate the relevant system design or project functionality.
- Ensure that submitted video links are accessible.

### Step 11 — Final Checks and Release

- Review the source code and project structure.
- Check the README and dataset documentation.
- Verify the evaluation results.
- Check the report and videos.
- Confirm that both members' contributions are recorded.
- Create a meaningful final Git commit and tagged submission release.

## 7. Working Constraints

- ROS must not be used.
- Part B handles one office item per input image or camera frame.
- The project uses the eight agreed office-item classes.
- The existing training, validation and test splits must be preserved.
- The test dataset must remain held out during training and model selection.
- Git commits must represent meaningful project changes.
- Both members must use the agreed shared repository.
- Credentials, passwords and private access tokens must never be committed.

## 8. Assessment Deliverables

The final submission must include:

- Working office-item classification code.
- Dataset files or an accessible dataset download link.
- Dataset card and complete README.
- Model evaluation results, including test accuracy, macro-F1, confusion matrix and error analysis.
- System design report of fewer than four pages.
- Required videos and accessible links.
- Meaningful Git commit history and a tagged submission release.

## 9. Current Project Status

**Current stage: Documentation closeout; official Step 2 — Environment Setup has not started.**

### Completed stages and integration

- Step 0 — Project Setup and Git Collaboration: completed by both members.
- Step 1 — Dataset Audit and Independent Verification: completed by both members.
- PR #2 — Member 1 dataset audit: merged at commit `4dd6336`.
- PR #3 — Member 2 independent dataset verification: merged at commit `41746fb`.
- PR #5 — Classifier Requirements: approved and merged at commit `3294c1e`.
- PR #6 — Application Interface and System Design: approved and merged at commit `b25e047`.
- Both members synchronised their local `main` branches with `origin/main` at `b25e047` and confirmed clean working trees.

### Current documentation closeout

- The three planning documents have undergone a joint consistency review.
- The members agreed to clarify multiple-file result association while leaving the batch continue-or-stop policy unresolved.
- The documentation files have been consolidated into a single `docs/` directory on branch `docs/documentation-closeout`.
- The decisions document preserves D001–D012, records D013 and distinguishes open questions from approved decisions.
- Document statuses, contribution history, project references and the folder structure have been updated on branch `docs/documentation-closeout`.
- The documentation-closeout changes have not yet been submitted through a pull request or merged into `main`.

### Outstanding development stages

- Official Step 2 — Environment Setup is the next development stage and has not started.
- Classifier implementation and model training have not started.
- The prediction application has not been implemented or tested.
- No physical robot has been constructed or integrated.

Model development and implementation will proceed after the documentation closeout and the required environment checks.
