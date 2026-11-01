# PDE3802 Assessment 1 — Application Interface Design

**Project:** Autonomous Office Item Organisation System
**Document owner:** Member 2 — Application and System Design Lead
**Status:** Draft proposal for Member 1 review
**Requirements baseline:** PR #5, merged at `3294c1e`

## 1. Purpose and scope

This document proposes how users provide inputs to the classification application and receive results. It follows `docs/step2-classifier-requirements.md`.

This is a planning document. The workflows described below have not yet been implemented or tested. The filename follows the team's requirements/interface planning roadmap; it does not replace official Step 2 — Environment Setup in `docs/docs/project-plan.md`.

The application will classify one office item per image file or standard-camera frame using these eight labels:

Bottle, Calculator, Keyboard, Mouse, Mug, Notebook, Pencil and Scissors.

The classifier returns an item's category. It does not provide bounding boxes, physical coordinates, navigation instructions or grasping commands. ROS will not be used.

## 2. Proposed interaction method

A command-line interface with an optional camera-preview window is proposed for team review.

The proposed interface would allow the user to:

- Select image-file mode or standard-camera mode.
- Supply an image-file path.
- Read a prediction or an explanation of failure.
- See confidence when the selected model provides it.
- Stop camera operation safely.
- Process several image files independently if the desirable multiple-file extension is implemented.

The interaction method, exact command syntax, camera selection method and preview controls require agreement. No application command, graphical interface or camera control described here is currently implemented.

## 3. Application and classifier responsibilities

| Component | Responsibility |
|---|---|
| User interface | Collect the input choice and present results, errors and stop controls. |
| File input handler | Resolve the supplied path, check access and obtain a decoded image. |
| Camera input handler | Open the selected standard camera, obtain frames and release its resources. |
| Image preparation | Convert file images and camera frames into the representation required by the selected model. |
| Classifier | Predict one of the eight classes and provide confidence when available. |
| Result handler | Associate each result with its input and distinguish success from failure. |

File images and camera frames must enter the same agreed image-preparation and prediction process. Final colour representation, dimensions, resizing and normalisation depend on the selected model and will be documented during implementation.

## 4. Image-file workflow

The proposed workflow is:

1. The user selects image-file mode and supplies a path.
2. The application checks that the file exists and can be accessed.
3. The application checks the agreed format and attempts to open and decode the image.
4. A valid image is prepared for the selected model.
5. The classifier processes the image.
6. The application presents the result associated with that input.

A missing, unreadable, unsupported or undecodable file produces a failure result with meaningful error information and no predicted class. A failure during prediction is also reported as failure.

The exact supported external image formats remain open for team agreement. JPG/JPEG and PNG are candidates, not confirmed application capabilities. The audited dataset's JPEG format does not itself establish application format support.
If multiple-file input is provided, each supplied file must be processed independently and receive its own result or failure information. A failure for one file must not corrupt, replace or be reported as another file's result, or cause another file's processing to fail. Whether the application continues with remaining files or stops the batch after reporting an individual failure remains open for team agreement. Results must never be assigned to the wrong file.

## 5. Standard-camera workflow

The proposed workflow is:

1. The user selects camera mode.
2. The application attempts to open the selected standard camera.
3. If opening succeeds, the application obtains a usable frame.
4. The user presents one supported office item in the frame.
5. The frame passes through image preparation and classification.
6. The application presents the result for that frame.
7. The user can stop camera operation.
8. The application releases the camera and closes any preview resources.

Camera-opening failures and unavailable cameras must produce a clear error. Failed frame acquisition must not produce a prediction or present a previous frame's result as current.

As a proposed fallback, a frame-acquisition failure ends the camera session with an explanatory message and resource cleanup. Retry behaviour, frame-selection frequency and manual versus continuous classification remain open for agreement.

Camera resources must be released on normal termination and when operation ends because of an unexpected error. The exact camera hardware, index, preview method and stop control have not been selected.

## 6. Input information

| Information | Meaning |
|---|---|
| Input source | Image file or standard-camera frame. |
| Image data | Successfully decoded image or usable camera frame. |
| Image dimensions | Width and height of the acquired image. |
| Image representation | Format and colour representation used by the agreed preparation process. |
| Input status | Whether acquisition and decoding succeeded. |

For a proposed multiple-file workflow, the application should also retain a source identifier, such as the file path, to associate each result with its input. Camera results should similarly remain associated with the frame being processed. These association details are proposed application metadata.

Only successfully acquired and decoded inputs proceed to prediction.

## 7. Result contract and presentation

The application must preserve the result meanings defined by the merged classifier requirements.

| Field | Successful operation | Failed operation |
|---|---|---|
| Predicted class | One of the eight agreed labels. | No prediction; absent or `None`. |
| Confidence | Model-provided score when available; otherwise clearly unavailable. | No valid prediction confidence. |
| Input source | Image file or camera frame. | Attempted source where known. |
| Status | Success. | Failure. |
| Error information | Empty or `None`. | Meaningful explanation of the failure. |

The interface must present class names exactly as agreed. It must not invent confidence values or treat a confidence score as a guarantee of correctness. Its interpretation depends on the selected model.

A failed operation must not display a previous prediction as the result of the failed input.

### Illustrative successful result

Input source: Image file
Predicted class: Mug
Confidence: 0.92
Status: Success
Error information: None

### Illustrative result without confidence

Input source: Standard-camera frame
Predicted class: Keyboard
Confidence: Not provided by the selected model
Status: Success
Error information: None

### Illustrative failed result

Input source: Image file
Predicted class: None
Confidence: None
Status: Failure
Error information: The image could not be opened or decoded.

These examples are illustrative. They are not measured predictions, implemented output syntax or test results.

## 8. Failure handling and scope limitations

| Situation | Required or proposed response |
|---|---|
| Missing or inaccessible file | Report failure with no prediction. |
| Unsupported or undecodable image | Explain the problem and return no prediction. |
| Camera cannot be opened | Report failure and release any acquired resources. |
| Camera frame cannot be obtained | Return no prediction; ending the session safely is proposed. |
| Prediction processing fails | Report failure without reusing an earlier result. |
| Camera operation stops or terminates | Release camera resources safely. |
| Model cannot be loaded | Proposed startup failure message; classification remains unavailable. |
| Multiple-file input contains a failed file | Keep results independent; continue-or-stop policy requires agreement. |

The classifier assumes one supported item per input. It has not been established that it can detect an empty scene, multiple items or an unsupported object.

A confident prediction must not be treated as proof that the input meets that assumption. Automatic rejection of unsupported scenes and confidence-based uncertainty handling remain unresolved. Until agreed capabilities exist, the interface must explain the input assumption without claiming automatic detection.

No confidence threshold, response-time target or frame-rate target is approved by this document.

## 9. Relationship to the wider system

The proposed wider system can consume the class, confidence when available, input source, status and error information.

Classification success alone does not authorise physical movement or manipulation. Separate system functions must establish item position, task suitability and safe action conditions. Failed classification must prevent the proposed system from acting on a fabricated or stale category.

The wider architecture, hardware alternatives, skills and safety measures will be described in `docs/step2-system-design-outline.md`.

## 10. Future verification

The following are planned checks, not completed tests.

| Check | Requirements | Official project stage |
|---|---|---|
| A valid image can be supplied and classified. | FR-01, FR-04, FR-05; AC-01, AC-02 | Steps 3 and 5 |
| Results preserve the agreed fields and conditional confidence. | FR-06, FR-09; AC-06, AC-07, AC-09 | Steps 3 and 5 |
| Invalid images produce failure without a prediction. | FR-07; AC-08 | Steps 3 and 7 |
| Standard-camera frames can be acquired and processed. | FR-03; AC-04 | Step 5 |
| Camera failures are reported and resources released. | FR-08, FR-10; AC-10, AC-11 | Steps 5 and 7 |
| Multiple files remain independent if that extension is provided. | FR-02; AC-03 | Step 7 |
| Usage instructions are understandable and reproducible on both computers. | NFR-02, NFR-03, NFR-07; AC-12, AC-13 | Steps 2, 5, 8 and 11 |

Original dataset files and splits must remain preserved. The held-out test split must not be used for interface development, troubleshooting or model selection; its role remains final evaluation.

## 11. Proposals and open questions

The following require team agreement or later model-development evidence:

- Command-line versus graphical interaction and any camera-preview window.
- Exact input syntax, camera selection and stop controls.
- Supported external image formats.
- Camera hardware and acquisition method.
- Manual versus continuous frame classification.
- Camera retry policy.
- Multiple-file support and continue-or-stop behaviour.
- Confidence display format and any uncertainty threshold.
- Behaviour for empty scenes, unsupported objects and multiple items.
- Final model-specific image preparation.
- Any response-time or frame-rate target.

Descriptions marked as proposals are not approved decisions. Only mutually approved choices should be added to the decision log.

## 12. References and review status

- `docs/step2-classifier-requirements.md` — approved requirements merged through PR #5.
- `docs/docs/project-plan.md` — official stages and team responsibilities.
- `docs/docs/docs/decisions.md` — existing decisions D001–D012.

Member 1 review, joint consistency review and integration of this draft remain pending.
