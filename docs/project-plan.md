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

Both members must keep their Git identity configured correctly before making commits to the shared repository

ROS must not be used, in accordance with the lecturer's instruction. The proposed system design and classification application will therefore use a ROS-independent architecture.

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

The dataset source and licence must be acknowledged in the project documentation and final dataset card.

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
│   ├── step2-environment-setup.md
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
├── requirements.txt
├── requirements-lock.txt
├── .gitignore
└── README.md
```

The `dataset` directory contains the existing training, validation and testing splits. Their class-folder structure and image assignments must remain unchanged.

The `docs` directory contains the project documentation, requirements, interface planning, system design, decisions, environment setup and contribution records.

The `scripts` directory currently contains the read-only dataset audit script. The `results/dataset_audit` directory contains the generated audit outputs.

The `requirements.txt` file records the six direct Python dependencies. The `requirements-lock.txt` file records the complete pinned dependency set.

The `report`, `src` and `tests` directories are reserved for their respective project work.

The `.venv` directories are local virtual environments and are not part of the shared repository.

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
- Record the dataset size and relevant dataset information., with the dataset size recorded for the dataset card.
- No credentials, unnecessary temporary files or unintended large files are committed.

### Step 1 — Dataset Audit

- Verify the dataset folder structure.
- Confirm the eight classification classes.
- Check the image counts in each split.
- Check image formats and image readability.
- Identify missing, corrupted or incorrectly labelled images.
- Record the dataset findings.
- Generate the dataset audit outputs.
- Have Member 2 independently verify the dataset structure and class counts.

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

- Develop an initial image classification model.
- Begin with a suitable baseline approach, such as HOG feature extraction with an SVM classifier.
- Train the model using the training dataset.
- Evaluate its performance using the validation dataset.
- Record the initial results.
- Keep the test dataset held out.

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
- Record the dataset size and relevant dataset information.
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

**Current stage: Step 2 — Environment Setup. Technical stages 2.1–2.6 are complete. Step 2.7 — Documentation and Integration is in progress.**

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

### Merged pull requests and Git integration

- PR #2 — Member 1 Dataset Audit: merged at commit `4dd6336`.
- PR #3 — Member 2 Independent Dataset Verification: merged at commit `41746fb`.
- PR #5 — Classifier Requirements: reviewed and merged at commit `3294c1e`.
- PR #6 — Application Interface and System Design: reviewed and merged at commit `b25e047`.
- PR #7 — Documentation Closeout: merged at commit `fda9951`.
- PR #8 — Shared Python Dependencies: reviewed and merged at commit `9a985b2`.
- PR #9 — Resolved Python Dependency Lock File: reviewed and merged at commit `b2e0aaa`.

Both members independently installed and tested the agreed Python environment. The shared dependency files contain six direct dependencies and 48 pinned package entries in the lock file.

Both members reported successful package imports, TensorFlow CPU execution, SVM testing, image decoding, Matplotlib testing and dependency consistency checks.

Both members also reported matching `requirements-lock.txt` SHA-256 hashes:

`99641B5F28BDE103918F0AA1E457E6C1386B6056BA68BF8D85DAFDA5A0A3E11D`

### Current Step 2.7 — Documentation and Integration

- Member 1 prepared `docs/step2-environment-setup.md`, documenting the agreed Python environment, hardware information, dependencies, installation procedure, runtime checks, Git integration and member contributions.
- Member 2 independently reviewed the environment information and confirmed that the technical details were consistent with his recorded environment and verification work.
- Member 1 committed the environment documentation on branch `member1/step2-environment-documentation` at commit `e9cc509`.
- Member 1 updated `docs/project-plan.md` to reflect the completed environment work and current project status at commit `5cf78b1`.
- Both documentation commits were pushed successfully to the shared GitHub repository.
- PR #10 — Step 2.7: Document environment setup and update project plan — is open and contains both documentation files.
- Member 2's initial review identified outdated Step 2.7 progress statements in the project plan and environment setup document. The technical environment information was reported as consistent with the recorded verification results.
- Member 1 corrected the outdated Step 2.7 progress statements in both documentation files following Member 2's initial review.
- The corrections have been committed and pushed to the existing PR #10 branch for final review.
- PR #10 is awaiting Member 2's final independent re-review and approval.

**Outstanding Step 2.7 work:**

- Obtain Member 2's final independent re-review and approval.
- Merge PR #10 into `main`.
- Have both members synchronise their local repositories.
- Verify that both documentation files are present on `main` and both working trees are clean.
- Formally close Step 2 after successful integration and verification.


### Outstanding development stages

- Step 2 — Environment Setup: technical installation and verification are complete; formal closure is awaiting documentation review and integration.
- Step 3 — Baseline Classifier: not started.
- Step 4 — Model Comparison and Selection: not started.
- Step 5 — Prediction Application: not started.
- Step 6 — Final Held-Out Evaluation: not started.
- Step 7 — Robustness and Input-Handling Tests: not started.
- Step 8 — Dataset Card and README: final development documentation remains outstanding.
- Step 9 — System Design Report: final report remains outstanding.
- Step 10 — Videos: required assessment videos remain outstanding.
- Step 11 — Final Checks and Release: final integration and submission checks remain outstanding.
No final office-item classifier has been trained or evaluated at this stage. The prediction application has not yet been implemented or tested, and no physical robot has been constructed or integrated.

After the Step 2 documentation has been reviewed, approved and merged, the team can formally close Step 2 and proceed to **Step 3 — Baseline Classifier**.
