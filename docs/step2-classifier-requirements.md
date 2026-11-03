# PDE3802 Assessment 1 — Classifier Requirements

**Project:** Autonomous Office Item Organisation System

**Document owner:** Member 1 — Project Lead

**Document status:** Approved requirements baseline; joint documentation closeout update in progress

**Purpose:** Define the scope, functional and non-functional requirements, input/output contract, priorities, acceptance criteria and future verification stages for the office-item classification component of Part B.

---

## 1. Purpose

This document defines the requirements for the office-item classification component of the Autonomous Office Item Organisation System.

The classifier receives an image file or a frame from a standard camera containing one office item. It processes the input and predicts which of the eight selected office-item classes the item belongs to. It returns the predicted class and a confidence score when the selected model provides one.

The application must communicate whether processing succeeded or failed. It must identify the input source and provide meaningful error information when an operation cannot be completed. A failed operation must not return a predicted class.

The purpose of this document is to establish the classification scope, input and output contract, functional requirements, non-functional requirements, priorities, acceptance criteria and future verification stages before implementation begins.

This document describes what the classifier and its application are expected to do. It does not specify the final model architecture, detailed preprocessing implementation, camera hardware or final application interface design.

## 2. Project Context and Scope

The project aims to develop an office-item organisation system. The image classifier is one component of the wider system and is responsible for recognising the category of an office item.

For Part B, the classification component will focus on identifying one office item per input image or camera frame.

The classifier is responsible for predicting the item's class and returning a confidence score when available from the selected model. It does not itself determine the item's physical location, produce object bounding boxes, plan robot movement or physically pick up, move or organise the item.

Those wider system responsibilities will be considered in the overall system design.

The project will use the eight selected classes from the `office_home_dataset` subset.

ROS will not be used in this project, in accordance with the lecturer's instruction and existing project decision D001.

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

The selected dataset subset contains 1,142 images across the eight selected classes.

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

The classification application must provide for both image-file input and input from a standard camera.

### 5.1 Image-File Input

The application must accept an image file for classification.

- Each image file must be processed as an independent classification input.
- Each input image is expected to contain one office item.
- The application must check that the file can be accessed, opened and decoded before classification.
- Missing, unreadable, unsupported or invalid image files must be handled appropriately.
- If multiple image files are supplied, each processed file must have its result or failure information associated with the correct file. A failure for one file must not corrupt, replace or be incorrectly attributed to another file's result. The batch continue-or-stop policy after an individual failure remains open for team agreement. Any files not processed must not be presented as successfully classified.

The exact external image formats that the application will accept have not yet been agreed. JPG/JPEG and PNG are possible formats for consideration, but they must not be described as confirmed supported formats until agreed and verified during implementation.

### 5.2 Standard-Camera Input

The completed application must provide for input from a standard camera.

The camera input must provide usable image frames for classification, with one office item per frame.

The application must handle situations where:

- The camera cannot be opened.
- The camera is unavailable or cannot be accessed.
- A frame cannot be obtained.
- Camera-frame acquisition fails during operation.

The application must communicate camera-related failures appropriately. When camera operation is stopped or terminated, the camera resource must be released safely.

Camera resources must also be released when camera operation ends because of an unexpected error.

The specific camera model, camera index and hardware arrangement have not yet been agreed.

### 5.3 Image Preparation

File images and camera frames must be prepared in a suitable form before classification.

The final image dimensions, colour representation, resizing, normalisation and other model-specific preprocessing requirements will depend on the selected model and its implementation.

These details must be established during the later development stages rather than assumed at this requirements stage.

## 6. Classifier Input and Output Contract

The classifier and application must use a consistent result structure so that successful predictions and failed operations can be distinguished clearly.

### 6.1 Input Information

The classification process must receive the following information:

| Input information | Meaning |
|---|---|
| Input source | Identifies whether the input is an image file or a standard-camera frame. |
| Image data | The image or frame supplied for classification. |
| Image dimensions | Width and height of the supplied image or frame. |
| Image representation | The image format and colour representation required by the selected preprocessing method. |
| Input status | Indicates whether the input was successfully obtained, opened and decoded. |

The final image representation and preprocessing method will be confirmed during model development.

### 6.2 Successful Result Fields

When classification succeeds, the result must contain:

| Result field | Meaning |
|---|---|
| Predicted class | One of the eight agreed office-item class names. |
| Confidence | A confidence score when the selected model provides one. |
| Input source | Identifies whether the result came from an image file or camera frame. |
| Status | Indicates that the classification operation succeeded. |
| Error information | Indicates that no error occurred; the field may contain `None` or an equivalent empty value. |

A successful result must contain a valid predicted class from the eight supported categories.

The confidence field must be returned and displayed when it is available from the selected model. The application must not invent a confidence value when the model does not provide one.

A confidence score must not automatically be interpreted as a guarantee that the prediction is correct. Its interpretation depends on the selected model.

### 6.3 Failed Result Fields

When input acquisition, image opening, decoding or classification processing fails, the result must indicate failure.

A failed result must contain:

| Result field | Meaning |
|---|---|
| Predicted class | No predicted class must be returned. |
| Confidence | No confidence score must be presented as a valid prediction. |
| Input source | Identifies the attempted input source where known. |
| Status | Indicates that the operation failed. |
| Error information | A meaningful message describing the reason for failure. |

A failed operation must never display a previous prediction or an invented class as though the current input had been successfully classified.

### 6.4 Illustrative Result Examples

The following examples demonstrate the expected result information. They are illustrative only and are not actual model outputs or measured results.

**Example A — Successful result with confidence:**

```text
Predicted class: Mug
Confidence: 0.92
Input source: Image file
Status: Success
Error information: None
```

**Example B — Successful result without confidence:**

```text
Predicted class: Keyboard
Confidence: Not provided by the selected model
Input source: Standard-camera frame
Status: Success
Error information: None
```

**Example C — Failed image input:**

```text
Predicted class: None
Confidence: None
Input source: Image file
Status: Failure
Error information: The image file could not be opened or decoded.
```

The final program may use a suitable data structure or display format, but it must preserve the meaning of these result fields.

## 7. Functional Requirements

Functional requirements describe what the classifier and its application must do.

The priorities and verification stages below identify the intended importance of each requirement and when it should be checked. They do not indicate that implementation or testing has already taken place.

The step numbers refer to the later implementation and verification stages in the official project plan. They do not replace the official project-plan numbering. The current requirements and interface planning activity is separate from official Step 2, which is Environment Setup.

| ID | Functional requirement | Expected behaviour | Priority | Planned verification stage |
|---|---|---|---|---|
| FR-01 | Image-file input | The application must accept an image file as an input for classification. | Must-have | Step 3 — Baseline Classifier |
| FR-02 | Multiple file inputs | If multiple image files are supplied, each processed file must be handled independently and its result or failure information must remain associated with the correct file. The batch continue-or-stop policy after an individual failure remains open for team agreement; unprocessed files must not be reported as successfully classified. | Desirable | Step 7 — Robustness and Input-Handling Tests |
| FR-03 | Standard-camera input | The completed application must provide input from a standard camera for frame-based classification. | Must-have | Step 5 — Prediction Application |
| FR-04 | One-item classification | Each image or camera frame must be treated as containing one office item for classification. | Must-have | Steps 3, 5 and 7 |
| FR-05 | Eight-class output | A successful classification must return one of the eight supported office-item classes. | Must-have | Steps 3–6 |
| FR-06 | Confidence output | The classifier must return a confidence score when the selected model provides one. | Must-have | Steps 3–6 |
| FR-07 | Invalid image handling | Missing, unreadable, unsupported or undecodable image inputs must produce a clear failure result with no predicted class. | Must-have | Steps 3 and 7 |
| FR-08 | Camera error handling | The application must report camera-opening and frame-acquisition failures and must not return a prediction for a failed input. | Must-have | Steps 5 and 7 |
| FR-09 | Result presentation | The application must communicate the predicted class, confidence when available, input source, success/failure status and meaningful error information. | Must-have | Step 5 — Prediction Application |
| FR-10 | Safe termination | The user must be able to stop camera operation safely, and the application must release the camera resource when camera operation terminates. | Must-have | Steps 5 and 7 |

Multiple-file input is a desirable extension to the single-image workflow. If it is provided, each file must be handled independently as specified in FR-02.

## 8. Non-Functional Requirements

Non-functional requirements describe the quality, reliability and operating expectations of the classifier and its application.

| ID | Non-functional requirement | Expected behaviour | Priority | Planned verification stage |
|---|---|---|---|---|
| NFR-01 | Reliability | Valid image files and usable camera frames should be processed without unexpected application failures. | Must-have | Steps 3, 5, 7 and 11 |
| NFR-02 | Usability | The user should be able to understand how to provide an input and interpret the displayed classification result or failure message. | Must-have | Step 5 — Prediction Application |
| NFR-03 | Reproducibility | The project must provide sufficient setup and usage instructions for another member to run the application. | Must-have | Steps 8 and 11 |
| NFR-04 | Maintainability | Input handling, image preparation, classification, result handling and presentation should have clearly separated responsibilities. | Desirable | Steps 3 and 5 |
| NFR-05 | Error handling | Invalid files, failed decoding, unavailable cameras and unsuccessful frame acquisition must be handled with understandable error information. | Must-have | Steps 3, 5 and 7 |
| NFR-06 | Data integrity | The original verified dataset and its existing training, validation and testing splits must remain preserved. | Must-have | Steps 3, 4 and 6 |
| NFR-07 | Portability | The project should be documented so that it can be set up and verified on both members' computers using the agreed development environment. | Must-have | Steps 2, 8 and 11 |
| NFR-08 | Performance reporting | The actual classifier performance must be measured and reported using the agreed evaluation metrics rather than assumed in advance. | Must-have | Step 6 — Final Held-Out Evaluation |

No fixed minimum accuracy, macro-F1 score, processing time or frame-rate target has been established in the current project decisions.

Actual model performance must be measured during the relevant development and evaluation stages.

## 9. Acceptance Criteria

The following acceptance criteria describe how the requirements will be checked when the relevant implementation is available.

They are future verification conditions. They do not mean that the classifier, camera input or application has already been implemented or tested successfully.

| ID | Requirement area | Acceptance criterion | Planned verification stage |
|---|---|---|---|
| AC-01 | Class list | The classifier's supported output labels must match the eight agreed class names exactly. | Steps 3–6 |
| AC-02 | Image-file input | A valid, readable image file can be supplied to the classifier for processing. | Step 3 |
| AC-03 | Multiple files | If multiple files are supplied, each processed file receives its own correctly associated result or failure information. Unprocessed files are not reported as successfully classified; the batch continue-or-stop policy remains open for team agreement. | Step 7 |
| AC-04 | Standard-camera input | The completed application provides a way to obtain frames from a standard camera. | Step 5 |
| AC-05 | One-item scope | The classifier processes one office item per image or frame and does not claim to perform multi-object detection. | Steps 3, 5 and 7 |
| AC-06 | Successful result | A successful classification returns the predicted class, input source and success status. | Steps 3 and 5 |
| AC-07 | Confidence | A confidence value is returned and displayed when the selected model provides one. No confidence value is invented when it is unavailable. | Steps 3–6 |
| AC-08 | Failed processing | Failed input acquisition, file opening, decoding or classification produces a failure result with meaningful error information and no predicted class. | Steps 3, 5 and 7 |
| AC-09 | Input source and status | Each result identifies the input source and clearly distinguishes successful and failed operations. | Steps 3 and 5 |
| AC-10 | Camera failure | An unavailable camera or unsuccessful frame acquisition is reported clearly and does not produce a predicted class for the failed input. | Steps 5 and 7 |
| AC-11 | Safe camera shutdown | Stopping or terminating camera operation releases the camera resource safely. | Steps 5 and 7 |
| AC-12 | Usability | The user can follow the documented input procedure and understand a successful result or failure message. | Step 5 |
| AC-13 | Reproducibility and portability | Both members can set up and run the project using the documented instructions on their respective computers. | Steps 2, 8 and 11 |
| AC-14 | Dataset preservation | The original dataset and its assigned training, validation and testing splits remain unchanged. | Steps 3, 4 and 6 |
| AC-15 | Final evaluation | The selected classifier's held-out test evaluation reports accuracy, macro-F1, confusion matrix and error analysis. | Step 6 |
| AC-16 | Maintainability | The implementation has clearly identifiable responsibilities for input handling, image preparation, classification and result handling. | Steps 3 and 5 |

The acceptance criteria must be checked using actual implementation and test results at their planned stages. Any failed criterion must be recorded and addressed rather than reported as passed.

## 10. Evaluation Requirements

The classifier must be evaluated using the existing dataset splits.

The training split will be used to train candidate classifiers.

The validation split will be used during model development, comparison and selection.

The testing split must remain separate from training and model selection and will be used for the final evaluation of the selected model.

The final held-out test evaluation must report:

- Classification accuracy.
- Macro-averaged F1-score.
- Confusion matrix.
- Error analysis of incorrect predictions.

The evaluation must consider performance across all eight classes rather than relying only on overall accuracy.

No fixed minimum accuracy or macro-F1 target has been established in the current project decisions. Actual results must be reported honestly and interpreted in the context of the dataset's limitations.

## 11. Error Handling and Input Limitations

The application must distinguish between successful classification and unsuccessful input or processing operations.

Examples of failures include:

- An image file that cannot be found or opened.
- An image that cannot be decoded.
- An unsupported image format.
- An unavailable or inaccessible camera.
- A camera that cannot provide a usable frame.
- An input that cannot be processed by the selected classifier.

When processing fails, the application must provide meaningful error information and must not return or display a predicted class for that failed operation.

If multiple image files are supplied, each processed file must retain its own result or failure information, correctly associated with that file. A failure for one file must not corrupt, replace or be incorrectly attributed to another file's result. Whether the application continues with remaining files or stops the batch after an individual failure remains open for team agreement. Any files not processed must not be presented as successfully classified.

The current classification scope assumes one supported office item per image or camera frame. Detecting and separating several items in one image is not part of the agreed classifier scope.

The exact behaviour for images containing no supported item, multiple items or an uncertain prediction will require further team agreement.

## 12. Dataset Limitations and Project Constraints

The completed dataset audit confirmed that:

- All 1,142 images were successfully fully decoded.
- All inspected images were JPEG files with `.jpg` extensions.
- All inspected images had dimensions of 416 × 416 pixels.
- No invalid or unreadable images were identified.
- No unsupported files, misplaced files or unexpected directories were identified.
- No exact duplicate groups were detected using SHA-256 hashes.

However, the dataset has limitations that must be considered during development and evaluation.

### 12.1 Class Imbalance

The dataset is not perfectly balanced. For example, Scissors has 174 images, while Pencil has 96 images.

### 12.2 Small Test Split

The test split contains 103 images in total, with only 7 to 19 images per class. This relatively small test set may limit how confidently the final results can represent performance on a wider range of images.

### 12.3 Audit Limitations

The dataset audit checked file integrity, image properties, folder structure and exact duplicates. It did not visually verify that every image has the correct class label.

The duplicate check does not identify visually similar images that have different file contents.

The audit also did not establish whether the dataset contains sufficient visual variation for reliable real-world classification.

### 12.4 Project Constraints

The following constraints apply:

- The project will use the agreed eight classification classes.
- The classifier will process one office item per image or camera frame.
- The existing dataset splits must be preserved.
- The testing split must remain held out until final evaluation.
- ROS will not be used.
- The dataset source and licence must be acknowledged.
- The completed application must provide for image-file and standard-camera input.
- Failed processing must not produce a predicted class.
- Camera resources must be released safely when camera operation terminates.
- Implementation choices must remain consistent with the assessment requirements and the agreed project scope.

## 13. Items Requiring Further Team Agreement

The following details have not yet been established as approved project decisions:

1. The exact external image-file formats that the application will accept.
2. The camera hardware and method of obtaining camera frames.
3. Whether the application will use a command-line interface, graphical interface or another agreed interaction method.
4. The final display format for the confidence score when available.
5. Whether a confidence threshold or an uncertain-prediction response will be required.
6. The expected behaviour when an input contains no supported item or more than one item.
7. The exact behaviour when one file in a multiple-file workflow fails.
8. Any specific response-time or real-time performance target.
9. The final image dimensions, colour representation and preprocessing method required by the selected model.

These items should be reviewed with Member 2 during the application-interface and system-design activity. They must not be treated as approved project decisions until both members agree.

## 14. Requirements Summary

The office-item classifier must accept an image file or a frame from a standard camera containing one supported office item and predict its class from the eight agreed categories.

A successful result must identify the predicted class, input source and success status. A confidence score must also be returned and displayed when the selected model provides one.

A failed input acquisition or processing operation must return a failure status and meaningful error information, without returning a predicted class.

If multiple image files are supplied, each processed file must retain its own correctly associated result or failure information. The continue-or-stop policy after an individual failure remains open for team agreement, and files that are not processed must not be presented as successfully classified. Camera-opening and frame-acquisition failures must be handled appropriately, and camera resources must be released safely when camera operation ends.

The existing dataset and its training, validation and testing splits must be preserved. Model development and selection must use the training and validation splits, while the test split must be reserved for final evaluation.

The final evaluation must include accuracy, macro-F1 score, a confusion matrix and error analysis.

The functional requirements, non-functional requirements and acceptance criteria establish what must be implemented and how it will be verified during the later project stages.

This document defines the expected behaviour and boundaries of the classification component before classifier implementation, model training and application integration begin.

---

**Document prepared by:** Member 1 — Project Lead

**Status:** Approved requirements baseline, formally reviewed and merged through PR #5 at commit `3294c1e`. The agreed multiple-file clarification in this documentation-closeout update remains subject to the closeout pull request's review and merge. Implementation and future verification remain pending.
