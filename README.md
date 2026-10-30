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

The initial dataset inspection identified the following image counts:

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

The inspected dataset contains 1,142 image files, all in JPG format, with a combined size of approximately 21.04 MB.

These figures describe the initial dataset inspection. Further checks may be required to verify image integrity and suitability before model training.

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
├── dataset/          # Office-item image dataset
│
├── docs/             # Project documentation
│
├── report/           # Assessment report and written work
│
├── results/          # Model outputs, evaluation results and figures
│
├── src/              # Main project source code
│
├── tests/             # Testing scripts and test cases
│
├── .gitignore        # Files and folders excluded from Git
│
└── README.md         # Project overview and documentation
```

Additional files and subfolders may be introduced as development progresses.

## 5. Development Tools and Technologies

The project uses the following development tools:

- **Python:** Main programming language.
- **Visual Studio Code:** Code editor and development environment.
- **Git:** Version control system for tracking project changes.
- **GitHub:** Remote repository for storing and sharing project files.

The Python libraries and frameworks required for image processing, model development and evaluation will be documented once the final development environment has been established.

## 6. Development Approach

The project will be developed through the following stages:

1. **Project setup:** Prepare the development environment, project folders and GitHub repository.
2. **Dataset inspection:** Examine the dataset structure, class distribution and image quality.
3. **Data preprocessing:** Prepare images for use in the classification model.
4. **Model development:** Select and implement a suitable classification approach.
5. **Model training:** Train the model using the training dataset.
6. **Model validation:** Monitor model performance using the validation dataset.
7. **Model evaluation:** Evaluate the final model using the test dataset and suitable performance measures.
8. **System testing:** Test the classification component using appropriate input images.
9. **Documentation:** Record the implementation, experiments, results and conclusions.

These stages will be updated as the project progresses.

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

**Current status:** Initial project setup.

The project repository and basic folder structure have been created. The initial dataset inspection has also been completed.

The classification implementation, model training, evaluation and system testing are still to be completed and will be documented in this repository as development progresses.

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