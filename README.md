# PDE3802 – AI Robotic Assessment 1
## Autonomous Office Item Organisation System

## 1. Project Overview

This project is being developed as part of the PDE3802 assessment. It focuses on an Autonomous Office Item Organisation System, incorporating an image classification component to recognise different types of office items.

The aim is to develop a system that can identify office-related objects from images and use the classification results as part of an office item organisation process.

The project involves dataset preparation, image processing, machine learning or deep learning model development, model evaluation and testing.

Development is carried out collaboratively by two team members, with Git and GitHub used for version control and project coordination.

## 2. Project Objectives

The main objectives of this project are to:

- Examine and understand the provided office-item image dataset.
- Prepare and organise the dataset for classification.
- Apply suitable image processing and preprocessing techniques.
- Develop an image classification model capable of recognising the office-item categories.
- Train and validate the classification model.
- Evaluate the model using appropriate performance measures.
- Test the developed system using unseen images.
- Investigate how the classification component can support an autonomous office item organisation system.
- Document the development process, experiments, results and limitations.

## 3. Dataset Description

The project uses an image dataset containing eight categories of office items.

The dataset is organised into three separate subsets:

- `train/` – images used to train the classification model.
- `valid/` – images used to validate the model during development.
- `test/` – images reserved for testing the model's performance on unseen data.

### 3.1 Object Categories

The eight object categories are:

1. Bottle
2. Calculator
3. Keyboard
4. Mouse
5. Mug
6. Notebook
7. Pencil
8. Scissors

### 3.2 Dataset Distribution

The completed dataset audit confirmed the following image counts:

| Category | Training | Validation | Testing | Total |
|---|---:|---:|---:|---:|
| Bottle | 95 | 27 | 10 | 132 |
| Calculator | 104 | 31 | 19 | 154 |
| Keyboard | 122 | 37 | 14 | 173 |
| Mouse | 108 | 34 | 14 | 156 |
| Mug | 72 | 19 | 7 | 98 |
| Notebook | 117 | 27 | 15 | 159 |
| Pencil | 72 | 14 | 10 | 96 |
| Scissors | 126 | 34 | 14 | 174 |
| **Total** | **816** | **223** | **103** | **1,142** |

The completed dataset audit verified 1,142 image files, all using the `.jpg` extension. All 1,142 images decoded successfully and measured 416 × 416 pixels.

The audit identified no exact duplicate image groups, unexpected folders or misplaced files. The existing training, validation and test split assignments have been preserved.

The test subset remains held out from training and model selection and is reserved for the final model evaluation.

### 3.3 Dataset Folder Structure

```text
dataset/
│
├── train/
│   ├── Bottle/
│   ├── Calculator/
│   ├── Keyboard/
│   ├── Mouse/
│   ├── Mug/
│   ├── Notebook/
│   ├── Pencil/
│   └── Scissors/
│
├── valid/
│   ├── Bottle/
│   ├── Calculator/
│   ├── Keyboard/
│   ├── Mouse/
│   ├── Mug/
│   ├── Notebook/
│   ├── Pencil/
│   └── Scissors/
│
└── test/
    ├── Bottle/
    ├── Calculator/
    ├── Keyboard/
    ├── Mouse/
    ├── Mug/
    ├── Notebook/
    ├── Pencil/
    └── Scissors/
```
### 3.4 Dataset Source and Attribution

The dataset used in this project was downloaded from Roboflow Universe:

- **Dataset name:** office_home_dataset
- **Creator:** stefanpublic
- **Source:** https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1
- **Dataset version:** 1
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)

This project uses a selected subset of eight office-item categories from the downloaded dataset.

The selected categories are Bottle, Calculator, Keyboard, Mouse, Mug, Notebook, Pencil and Scissors.

The dataset was organised into training, validation and testing subsets. Both project members use the same dataset structure and image counts.

The original dataset creator and source are acknowledged in accordance with the CC BY 4.0 licence.

## 4. Project Folder Structure

The project repository is organised as follows:

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

The `dataset` directory contains the existing training, validation and testing splits. The `docs` directory contains project planning, requirements, decisions, audit records and contribution history.

The `scripts` directory currently contains the read-only dataset audit script. The `results/dataset_audit` directory contains the generated dataset audit outputs. The `report`, `src` and `tests` directories are reserved for their respective project work.

Additional files and subfolders may be introduced as development progresses, provided changes are consistent with the agreed project structure and collaboration workflow.

## 5. Development Tools and Technologies

The project uses the following development tools:

- **Python:** Main programming language.
- **Visual Studio Code:** Code editor and development environment.
- **Git:** Version control system for tracking project changes.
- **GitHub:** Remote repository for storing and sharing project files.

The Python libraries and frameworks required for image processing, model development and evaluation will be documented once the final development environment has been established.

## 6. Development Approach

The project will be developed through the following stages:

0. **Step 0 — Project Setup and Git Collaboration:** Establish the project structure, shared repository and collaboration workflow.
1. **Step 1 — Dataset Audit:** Inspect and independently verify the dataset structure, image counts, image integrity and dataset properties.
2. **Step 2 — Environment Setup:** Establish and verify the Python development environment and required dependencies.
3. **Step 3 — Baseline Classifier:** Implement an initial office-item classification model.
4. **Step 4 — Model Comparison and Selection:** Compare suitable classification approaches and select the final model using validation results.
5. **Step 5 — Prediction Application:** Develop the application for image-file and standard-camera input.
6. **Step 6 — Final Held-Out Evaluation:** Evaluate the selected model using the reserved test dataset.
7. **Step 7 — Robustness and Input-Handling Tests:** Test application behaviour, invalid inputs, processing failures and other relevant conditions.
8. **Step 8 — Dataset Card and README:** Complete the dataset documentation and update the project README.
9. **Step 9 — System Design Report:** Complete the report describing the autonomous office-item organisation system.
10. **Step 10 — Videos:** Prepare the required assessment demonstration videos.
11. **Step 11 — Final Checks and Release:** Perform final project checks and prepare the submission.

Each stage will be completed and verified before proceeding to the next stage. The project plan and contribution log will be updated as work progresses.

## 7. Version Control and Team Collaboration

Git and GitHub are used to support collaborative development.

The GitHub repository is:

https://github.com/vashishmohess-svg/PDE3802-AI_ROBOTIC-Assessment-1

The repository is private and intended for the project team's development work.

Version control will be used to:

- Track changes to source code and documentation.
- Maintain a record of development progress.
- Share work between the two team members.
- Support collaboration through commits and branches.
- Integrate and review changes before merging them into the main project.

Team members should commit meaningful changes regularly and avoid overwriting each other's work.

## 8. Running the Project

Detailed installation instructions, dependency requirements and execution commands will be added after the development environment and project implementation have been finalised.

## 9. Project Status

**Current status: Documentation closeout in progress on branch `docs/documentation-closeout`.**

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
- The agreed multiple-file processing clarification has been incorporated into the classifier requirements and application-interface documents.
- The documentation structure has been consolidated into a single `docs/` directory.
- The project plan and contribution log have been updated to reflect the verified project status.
- The closeout changes have not yet been committed, pushed or submitted through a pull request.
- Member 2's independent review, approval and merge of the documentation-closeout pull request remain outstanding.

### Outstanding development work

- Official Step 2 — Environment Setup has not started.
- Classifier implementation and model training have not started.
- The prediction application has not been implemented or tested.
- Final held-out model evaluation has not been performed.
- No physical robot has been constructed or integrated.

The project will proceed to official Step 2 — Environment Setup after the documentation closeout has been reviewed, approved and merged.

## 10. Assessment Deliverables

The repository will be used to organise and maintain the project materials, including:

- Source code.
- Dataset-related documentation.
- Testing scripts.
- Experimental results.
- Model evaluation outputs.
- Assessment report.
- Relevant project documentation.

All final deliverables will be prepared in accordance with the PDE3802 assessment requirements.