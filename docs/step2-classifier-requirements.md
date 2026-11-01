# PDE3802 Assessment 1 — Classifier Requirements

**Project:** Autonomous Office Item Organisation System

**Document owner:** Member 1 — Project Lead

**Document status:** Draft for team review

**Purpose:** Define the requirements and scope of the office-item classification component for Part B of the assessment.

---

## 1. Purpose

This document defines the requirements for the office-item classification component of the Autonomous Office Item Organisation System.

The classifier will receive an image or camera frame containing one office item and predict which of the eight selected office-item classes it belongs to. The application must present the predicted class and its associated confidence score.

The purpose of this document is to establish the agreed classification scope, input and output requirements, functional requirements, error-handling expectations and evaluation requirements before implementation begins.

This document describes what the classifier is expected to do. It does not specify the final model architecture, detailed preprocessing implementation, camera hardware or application interface design.

## 2. Project Context and Scope

The project aims to develop an office-item organisation system. The image classifier is one component of the wider system and is responsible for recognising the category of an office item.

For Part B, the classification component will focus on identifying one office item per input image or camera frame.

The classifier's responsibility is to predict the item's class and provide a confidence score. It is not responsible for physically locating, picking up, moving or organising the item. Those wider system responsibilities will be considered in the overall system design.

The project will use the eight selected classes from the `office_home_dataset` subset.

ROS will not be used in this project, in accordance with the lecturer's instruction and the existing project decision D001.

## 3. Classification Classes

The classifier must support the following eight office-item classes:

| No. | Class |
|---:|---|
| 1 | Bottle |
| 2 | Calculator |
| 3 | Keyboard |
| 4 | Mouse |
| 5 | Mug |
| 6 | Notebook |
| 7 | Pencil |
| 8 | Scissors |

These classes are fixed for the current project scope and must remain consistent across the dataset, classifier, application and project documentation.

## 4. Dataset Requirements

The classifier will use the selected subset of `office_home_dataset`, obtained from Roboflow Universe.

**Dataset information:**

- Dataset name: `office_home_dataset`
- Creator: `stefanpublic`
- Version: 1
- Source: https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1
- Licence: Creative Commons Attribution 4.0 International (CC BY 4.0)

The dataset contains 1,142 images across the eight selected classes.

### 4.1 Existing Dataset Distribution

| Class | Training | Validation | Testing | Total |
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

### 4.2 Dataset Handling Requirements

The existing training, validation and testing splits must be preserved.

- The training split will be used to train the classifier.
- The validation split will be used to monitor performance and support model comparison and selection.
- The testing split must remain held out until the final evaluation.

The test split must not be used for training, model selection or repeated model tuning.

The original dataset must not be modified by deleting, renaming, moving or reassigning images between the existing splits.

The dataset source and CC BY 4.0 licence must be acknowledged in the project documentation.

## 5. Input Requirements

The classification application must support an input image or a camera frame for classification.

The following requirements apply:

- One office item must be presented per input image or camera frame.
- The input is expected to contain an item belonging to one of the eight supported classes.
- The input must be a valid and readable image before classification can take place.
- Unsupported or invalid inputs must be handled appropriately rather than causing the application to fail unexpectedly.

The audited dataset images are JPEG files with `.jpg` extensions and dimensions of 416 × 416 pixels. However, the final input-format restrictions and any image resizing or preprocessing requirements for the application will depend on the selected model and the agreed application design.

The project has not yet established a specific camera model or camera hardware requirement.

## 6. Functional Requirements

The classifier and its application must satisfy the following functional requirements.

| ID | Requirement |
|---|---|
| FR-01 | The application must accept an image as an input for classification. |
| FR-02 | The application must support classification from a camera frame. |
| FR-03 | Each classification input must represent one office item at a time. |
| FR-04 | The classifier must predict one of the eight supported office-item classes. |
| FR-05 | The application must make the predicted class available to the user. |
| FR-06 | The classifier must provide a confidence score associated with its predicted class. |
| FR-07 | The application must display the predicted class and its confidence score. |
| FR-08 | The application must handle invalid or unsupported inputs and provide an appropriate indication to the user. |
| FR-09 | The project must evaluate the selected classifier using the agreed evaluation metrics and the held-out test split. |

The requirements do not prescribe a particular classification algorithm or neural network architecture. Model selection will be addressed during the development and comparison stages.

## 7. Output Requirements

For a valid classification input, the classifier must provide:

1. The predicted office-item class.
2. The confidence score associated with that prediction.

The predicted class must use one of the following labels:

- Bottle
- Calculator
- Keyboard
- Mouse
- Mug
- Notebook
- Pencil
- Scissors

The application must present the predicted class and confidence score clearly to the user.

The confidence score should be presented in a readable format. Its final display format and any threshold for treating a prediction as uncertain have not yet been agreed.

The confidence score must not automatically be interpreted as a guarantee that the prediction is correct.

## 8. Error Handling and Input Limitations

The application must handle invalid or unsupported inputs appropriately.

Examples include:

- An image file that cannot be opened or read.
- An unsupported image format.
- An unavailable or unsuccessful camera input.
- An input that cannot be processed by the application.

The application should provide a clear indication when classification cannot be performed. It should not silently display an incorrect classification as though processing had succeeded.

The current classification scope assumes one supported office item per image or camera frame. Detecting and separating multiple items is not part of the agreed classification scope.

The exact behaviour for inputs containing no supported item, multiple items or an uncertain prediction will require further agreement during application and interface design.

## 9. Evaluation Requirements

The classifier must be evaluated using the existing dataset splits.

The validation split will be used during model development, comparison and selection.

The testing split must remain separate from the training and model-selection process and will be used for the final evaluation of the selected model.

The final test evaluation must report:

- Classification accuracy.
- Macro-averaged F1-score.
- Confusion matrix.
- Error analysis of incorrect predictions.

The evaluation must consider the performance across all eight classes rather than relying only on overall accuracy.

No fixed minimum accuracy or macro-F1 target has been established in the current project decisions. The actual results must be reported honestly and interpreted in the context of the dataset's limitations.

## 10. Dataset Limitations and Project Constraints

The completed dataset audit confirmed that:

- All 1,142 images were successfully fully decoded.
- All inspected images were JPEG files with `.jpg` extensions.
- All inspected images had dimensions of 416 × 416 pixels.
- No invalid or unreadable images were identified.
- No unsupported files, misplaced files or unexpected directories were identified.
- No exact duplicate groups were detected using SHA-256 hashes.

However, the dataset has limitations that must be considered during development and evaluation.

### 10.1 Class Imbalance

The dataset is not perfectly balanced. For example, Scissors has 174 images, while Pencil has 96 images.

### 10.2 Small Test Split

The test split contains 103 images in total, with only 7 to 19 images per class. This relatively small test set may limit how confidently the final results can represent performance on a wider range of images.

### 10.3 Audit Limitations

The dataset audit checked file integrity, image properties, folder structure and exact duplicates. It did not visually verify that every image has the correct class label.

The duplicate check does not identify visually similar images that have different file contents.

The audit also did not establish whether the dataset contains sufficient visual variation for reliable real-world classification.

### 10.4 Project Constraints

The following constraints apply:

- The project will use the agreed eight classification classes.
- The classifier will process one office item per image or camera frame.
- The existing dataset splits must be preserved.
- The testing split must remain held out until final evaluation.
- ROS will not be used.
- The dataset source and licence must be acknowledged.
- Implementation choices must remain consistent with the assessment requirements and the agreed project scope.

## 11. Requirements Summary

The office-item classifier must accept an image or camera frame containing one supported office item and predict its class from the eight agreed categories.

The application must present the predicted class and its associated confidence score. Invalid or unsupported inputs must be handled appropriately.

The existing dataset and its training, validation and testing splits must be preserved. Model development and selection must use the training and validation splits, while the test split must be reserved for final evaluation.

The final evaluation must include accuracy, macro-F1 score, a confusion matrix and error analysis.

This requirements document establishes the expected behaviour and boundaries of the classification component before classifier implementation and application integration begin.

## 12. Items Requiring Further Team Agreement

The following details have not yet been established as agreed project decisions:

1. The exact image file formats that the application will accept.
2. The camera hardware and method of obtaining camera frames.
3. The final display format for the confidence score.
4. Whether a confidence threshold or an uncertain-prediction response will be required.
5. The expected behaviour when an input contains no supported item or more than one item.
6. Any specific response-time or real-time performance target.

These items should be reviewed with Member 2 during the application interface and system design activity. They must not be treated as approved decisions until both members agree.

---

**Document prepared by:** Member 1 — Project Lead

**Status:** Draft for team review
