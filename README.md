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

### Installation

1. Clone the repository:
```bash
git clone https://github.com/vashishmohess-svg/PDE3802-AI_ROBOTIC-Assessment-1.git
cd PDE3802-AI_ROBOTIC-Assessment-1
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Prediction Application

The prediction application supports both image file and camera input.

#### Classify an Image File

```bash
python scripts/predict_app.py --image path/to/image.jpg
```

Example:
```bash
python scripts/predict_app.py --image dataset/train/Bottle/00001_jpg.rf.7d50e7e57d941fdcb0df860c2245e619.jpg
```

#### Use Camera for Live Classification

```bash
python scripts/predict_app.py --camera
```

To use a specific camera index:
```bash
python scripts/predict_app.py --camera --camera-index 1
```

**Camera Controls:**
- Press `c` to capture and classify the current frame
- Press `q` to quit and release the camera

### Running Tests

Run the robustness tests:
```bash
python scripts/test_robustness.py
```

### Model Evaluation

To run the final held-out test evaluation:
```bash
python scripts/evaluate_test_set.py
```

### Supported Image Formats

The application supports the following image formats:
- JPG/JPEG
- PNG

## 9. Project Status

**Current status: Steps 0-7 completed. Step 8 (Dataset Card and README) in progress.**

### Completed stages

- **Step 0 — Project Setup and Git Collaboration:** completed by both members.
- **Step 1 — Dataset Audit and Independent Verification:** completed by both members.
- **Step 2 — Environment Setup:** completed by both members.
- **Step 3 — Baseline Classifier:** completed. HOG + Linear SVM baseline achieved 68.58% validation accuracy.
- **Step 4 — Model Comparison and Selection:** completed. Selected HOG + RBF SVM (C=10.0) with 72.57% validation accuracy.
- **Step 5 — Prediction Application:** completed. Supports image file and camera input.
- **Step 6 — Final Held-Out Evaluation:** completed. Test accuracy: 66.99%, Test macro-F1: 0.6288.
- **Step 7 — Robustness and Input-Handling Tests:** completed. All 11 tests passed.

### In progress

- **Step 8 — Dataset Card and README:** Dataset card created, README updated with installation and usage instructions.

### Remaining work

- **Step 9 — System Design Report:** To be completed.
- **Step 10 — Videos:** To be prepared.
- **Step 11 — Final Checks and Release:** To be completed.

### Model Performance Summary

**Selected Model:** HOG + RBF SVM (C=10.0, gamma=scale)

- **Validation accuracy:** 72.57%
- **Validation macro-F1:** 0.6831
- **Test accuracy:** 66.99%
- **Test macro-F1:** 0.6288
- **Support vectors:** 796
- **Model size:** 51.7 MB

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