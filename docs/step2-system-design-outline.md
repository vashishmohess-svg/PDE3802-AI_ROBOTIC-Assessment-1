# PDE3802 Assessment 1 — System Design Outline

**Project:** Autonomous Office Item Organisation System
**Document owner:** Member 2 — Application and System Design Lead
**Status:** Original system-design outline reviewed and merged through PR #6 at commit `b25e047`; this documentation-closeout revision remains subject to pull-request review and merge. System-design proposals remain subject to team agreement and technical validation; implementation and verification are pending.
**Requirements baseline:** PR #5, merged at `3294c1e`

## 1. Purpose and planning status

This document outlines how an autonomous system could find, identify and organise office items in an indoor office.

It complements `docs/step2-classifier-requirements.md` and `docs/step2-application-interface.md`. It is a preliminary design, not an implemented robot or evidence of successful testing.

The filename follows the team's requirements/interface planning roadmap. This activity does not replace official Step 2 — Environment Setup. The later system-design report belongs to official Step 9 and must satisfy its separate length requirement.

Hardware, navigation, manipulation and safety arrangements below are proposals requiring review and validation. No component purchase or physical robot construction is authorised by this document.

## 2. Mission and scope

The proposed mission is to receive an organisation request, find a candidate office item, identify its category, establish its position, and transfer it to an agreed destination when safe and feasible.

The eight supported classification categories are:

Bottle, Calculator, Keyboard, Mouse, Mug, Notebook, Pencil and Scissors.

The classifier processes one supported item per image or camera frame. It does not perform multi-object detection, determine physical coordinates or control movement.

The wider system therefore needs separate functions for finding candidate items, obtaining a suitable image, estimating position, planning actions and verifying completion.

ROS will not be used.

## 3. Operating assumptions and boundaries

The proposed operating environment is an indoor office with people, furniture and potentially obstructed routes.

The initial design assumes:

- The operating area and permitted destinations are agreed in advance.
- Items are accessible within the selected platform's validated reach and load limits.
- Classification receives an image containing one supported item.
- Candidate-item finding and physical localisation use capabilities separate from the classifier.
- People can stop the system and assist when autonomous operation is unsuitable.
- Motion and manipulation require independent safety checks.
- Classification success alone does not establish that an action is safe.

Item dimensions, payload, workspace, lighting, floor conditions and permitted operating speeds require later specification and validation.

Unsupported items, empty scenes and images containing multiple items are outside the classifier's established input assumption. Automatic detection or rejection of these situations is not an approved capability.

The organisation task is non-time-critical: it does not require completion within a strict time limit after the user submits a request. Safe operation and correct task handling take priority over speed. This does not remove the need for responsive stop controls or timely safety responses. No numerical completion-time or frame-rate target is established here.
## 4. Proposed mission sequence

1. Receive a request and confirm the permitted operating area.
2. Check system readiness, stop controls and required sensors.
3. Establish the robot's position within an available map or workspace representation.
4. Plan and follow a safe route to the search area.
5. Find a candidate item using a separate perception or assisted-selection function.
6. Obtain an image suitable for one-item classification.
7. Classify the image and inspect the returned status.
8. Establish the item's position and accessibility using separate localisation information.
9. Select an agreed destination for the predicted category.
10. Check handling suitability, route feasibility and current safety conditions.
11. Pick up and transport the item using validated hardware, or request human assistance.
12. Place the item and verify the outcome.
13. Record completion, failure or the need for assistance.

The order can include re-observation where information becomes unsuitable or outdated. Exact retry limits and task-recovery policies remain open.

A failed classification, unavailable location, blocked route or unsafe handling condition prevents progression to the affected physical action.

## 5. Proposed software architecture

The design uses separate modules communicating through ordinary function calls or structured messages. The final implementation mechanism remains undecided.

| Module | Main responsibility |
|---|---|
| User/application interface | Receive requests, show results and provide stop and assistance controls. |
| Task manager | Coordinate the mission sequence and track task state. |
| Input acquisition | Obtain image files or standard-camera frames. |
| Image preparation and classifier | Prepare a valid image and return its category and confidence when available. |
| Candidate perception | Find or select candidate items separately from classification. |
| Mapping and robot localisation | Maintain workspace information and estimate the robot's position. |
| Item localisation | Estimate candidate-item position in a defined reference frame. |
| Destination manager | Associate an agreed category with an approved storage location. |
| Route and action planning | Determine feasible routes and handling actions. |
| Motion and manipulation control | Execute validated movement and handling commands. |
| Safety supervisor | Inhibit or stop actions when safety conditions are not satisfied. |
| Outcome verification | Check whether transport and placement achieved the requested result. |
| Event record | Record task states, errors, assistance requests and completion evidence. |

The safety supervisor must be able to inhibit actions regardless of classifier output. A physical stop arrangement and hardware-level protection would require separate engineering and validation; software checks alone are insufficient.

## 6. Information and data flow

The proposed main flow is:

User request → task manager → search and observation → classification and item localisation → destination selection → safety and feasibility checks → movement and handling → outcome verification → user feedback.

Supporting information flows include:

- Workspace sensors supply mapping, robot localisation and obstacle information.
- A camera supplies images for candidate perception and classification.
- The classifier supplies category information, not physical position.
- Item localisation supplies position, reference frame and suitability information.
- The task manager combines category, position, destination and current task state.
- The safety supervisor receives relevant sensor and controller states and can inhibit actions.
- Controllers return execution status and errors.
- Outcome verification supplies completion evidence or a recovery request.

Observations and results must remain associated with the same candidate item. Outdated or mismatched information must not be used to authorise movement.

## 7. Classifier and application contract

The system must preserve the meanings defined in the approved classifier requirements.

| Field | Success | Failure |
|---|---|---|
| Predicted class | One of the eight agreed class names. | No prediction; absent or `None`. |
| Confidence | Model-provided score when available. | No valid prediction confidence. |
| Input source | Image file or standard-camera frame. | Attempted source where known. |
| Status | Success. | Failure. |
| Error information | Empty or `None`. | Meaningful explanation. |

The system must not invent confidence values or reuse a previous prediction as the result of a failed operation.

A confidence score does not guarantee correctness or establish physical safety. Confidence thresholds and uncertainty behaviour require team agreement and later validation.

The application must handle file errors, camera-opening failures and unsuccessful frame acquisition. Camera resources must be released on normal termination and when operation ends because of an unexpected error.

## 8. Required system skills

These are proposed capabilities for the wider system. Their presence in this table does not mean they have been implemented.

| Skill | Inputs | Outputs | Proposed success criterion | Failure response |
|---|---|---|---|---|
| Receive task | User request and allowed operating area. | Validated task or clarification request. | Task is understandable and within permitted scope. | Request clarification or reject unsupported work. |
| Check readiness | Sensor, controller, power and stop-system states. | Ready/not-ready status and reasons. | All required checks meet validated operating conditions. | Inhibit mission start. |
| Map and localise | Workspace observations and available map. | Robot pose and map state. | Pose is sufficiently reliable for the planned action. | Stop motion and request recovery or assistance. |
| Navigate | Robot pose, destination and obstacle information. | Motion commands and route status. | Agreed destination is reached within validated conditions. | Stop, replan where safe or request assistance. |
| Find candidate | Search-area observations or assisted selection. | Candidate identity and observation region. | A candidate can be observed for the next stage. | Continue search within agreed limits or request help. |
| Acquire image | File path or camera source. | Decoded image/frame or failure. | A usable input is obtained. | Report failure with no prediction. |
| Classify item | Prepared one-item image. | Classifier result contract. | Processing succeeds with a valid agreed label. | Inhibit category-dependent action and report failure. |
| Localise item | Candidate observations and sensor calibration. | Item position, reference frame and validity information. | Position is suitable for the planned handling action. | Re-observe or request assistance. |
| Select destination | Predicted category and agreed destination mapping. | Approved destination or failure. | A permitted destination exists for the category. | Request a destination decision. |
| Check handling | Item properties, pose, hardware limits and safety state. | Handling permitted/not permitted. | The proposed action meets validated handling conditions. | Inhibit manipulation and request assistance. |
| Pick and place | Valid target pose, destination and permitted action. | Execution status and errors. | Item is transferred without a detected unsafe condition. | Stop safely and request recovery. |
| Verify outcome | Placement observations and task goal. | Verified completion or discrepancy. | Evidence supports correct placement at the agreed destination. | Record incomplete task and request review. |
| Stop safely | Stop request, fault or unsafe condition. | Inhibited actions and stopped-state feedback. | Relevant actions cease according to validated stopping behaviour. | Escalate to the independent stop arrangement. |

Numerical tolerances, timing limits and confidence limits are not set here. They depend on hardware selection, risk assessment and later testing.

## 9. Preliminary hardware categories and alternatives

No final hardware model or purchase decision is made by this outline.

| Category | Possible options | Selection considerations |
|---|---|---|
| Computing | Laptop, single-board computer or embedded accelerator. | Model compatibility, processing load, power, interfaces and maintainability. |
| Classification camera | Integrated webcam or external USB camera. | Standard-camera access, image quality, lighting and mounting. |
| Depth/item-position sensing | Depth camera, calibrated stereo or another validated position-estimation method. | Required range, calibration, reference frames and handling accuracy. |
| Workspace/obstacle sensing | Range sensors, depth sensing, lidar, bump sensors or suitable combinations. | Coverage, blind spots, office conditions and stopping behaviour. |
| Robot localisation | Wheel odometry with supporting sensors, visual localisation or a suitable mapped method. | Drift, floor conditions, map availability and reliability. |
| Mobile platform | Suitable wheeled base or an existing educational platform. | Stability, payload, footprint, control access and operating surface. |
| Manipulation | Arm/gripper, another validated transfer mechanism or human assistance. | Reach, item variation, pinch hazards, load and placement control. |
| Storage | Marked bins, shelves or designated locations. | Accessibility, category mapping and placement verification. |
| Power and stop equipment | Suitable protected supply, isolation and independent stop arrangement. | Electrical compatibility, safe shutdown and controller behaviour. |

A fixed observation and sorting station could simplify an early demonstration, but it would not by itself fulfil the complete mobile office-search mission. Any such limitation must be stated explicitly.

## 10. Handling concept and human assistance

An arm with a suitable gripper is a possible autonomous handling approach. It has not been selected or shown capable of handling all eight classes.

The classes vary substantially in shape and handling difficulty. Classification alone does not establish whether an item is empty, fragile, sharp, unusually heavy or safe to grip.

A proposed fallback is to stop at the handling stage and request human assistance when:

- Position or accessibility is uncertain.
- The item is outside validated hardware limits.
- Safe grasping cannot be established.
- An item is hazardous or unsuitable for the selected mechanism.
- Transport or placement cannot be completed safely.

Human-assisted transfers must be recorded as assisted outcomes. They must not be reported as fully autonomous mission completion.

The final balance between autonomous manipulation and assistance remains a team decision.

## 11. Safety and failure behaviour

The proposed design must address the following risks before any physical implementation.

| Risk or failure | Proposed response |
|---|---|
| Person or obstacle enters the route | Inhibit movement or stop using validated sensing and stopping behaviour. |
| Localisation becomes unreliable | Stop motion and recover localisation or request help. |
| Item position is missing or unsuitable | Do not issue manipulation commands. |
| Classification fails | Return failure with no predicted class and prevent category-dependent handling. |
| Unsupported or ambiguous scene | Request a suitable one-item observation or human review; do not claim automatic rejection unless implemented and validated. |
| Camera fails | Report failure, release resources and suspend dependent tasks. |
| Grasp is unsuitable or item slips | Stop the affected action safely and request recovery. |
| Destination is blocked | Suspend placement and obtain a safe alternative or assistance. |
| Communication or controller fault | Inhibit further action and enter a validated safe condition. |
| Low power or electrical fault | Stop the mission according to a validated power-failure procedure. |
| Stop request | Give stopping priority over mission progress. |

Handling scissors, liquid-containing containers, fragile objects and other unsuitable items requires specific consideration. Category recognition does not resolve these hazards.

Safe speed, separation distances, stopping distances, payload limits and permitted handling conditions require later assessment and testing. No safety certification or validated physical safety performance is claimed.

## 12. Dataset and evaluation boundaries

The classifier uses the existing eight-class subset of `office_home_dataset`, version 1, by `stefanpublic`, under CC BY 4.0.

The verified distribution remains:

- Training: 816 images.
- Validation: 223 images.
- Testing: 103 images.
- Total: 1,142 images.

The original dataset and split assignments must remain unchanged. Training and validation support model development and selection. The test split remains held out for final evaluation.

The final evaluation must report accuracy, macro-F1, confusion matrix and error analysis. Its small test split and the audit's limitations must be acknowledged.

Classifier evaluation does not demonstrate navigation accuracy, grasp success, physical safety or complete mission performance. Those require separate evidence if implemented.

## 13. Future design verification

The following are planned review or testing activities, not completed results:

- Check agreement across the requirements, application interface and this outline.
- Verify exact class labels, conditional confidence and failure-result handling.
- Check that category prediction is separate from robot and item localisation.
- Confirm that no module depends on ROS.
- Review skill inputs, outputs, success criteria and failure paths.
- Review hardware suitability and alternatives before selection.
- Define and validate safety conditions before physical operation.
- Test the application and error handling at the official implementation stages.
- Prepare the later system-design report under official Step 9.
- Record the limits of any demonstration honestly.

The current planning review must not be used to mark future implementation or acceptance tests as passed.

## 14. Open questions and approval status

The following remain open for team agreement or later technical evidence:

- Final application interaction method and camera controls.
- Supported external image formats.
- Confidence display and any uncertainty policy.
- Behaviour for unsupported, empty or multi-item scenes.
- Candidate-item finding method.
- Robot and item localisation methods.
- Map creation, calibration and reference-frame conventions.
- Hardware selection and operating limits.
- Autonomous handling versus human assistance.
- Destination mapping for each category.
- Retry, recovery and mission-completion rules.
- Safety measures and their validation.
- Response-time or frame-rate targets, if justified.

Only mutually approved choices should be added as new entries in the decision log. Existing decisions D001–D013 must be preserved.

PR #6, which included this document and the application-interface document, was approved and merged into `main` at commit `b25e047`. Both members subsequently synchronised their local `main` branches at that commit and confirmed clean working trees.

The joint consistency review found the main technical scope of the three planning documents consistent. The agreed multiple-file processing clarification has been incorporated into the classifier requirements and application-interface documents through this documentation-closeout revision.

The design proposals and open questions listed above remain unapproved until explicitly agreed and, where necessary, technically validated. No physical robot construction, system implementation or system testing is claimed as completed.

## 15. References

- `docs/step2-classifier-requirements.md`
- `docs/step2-application-interface.md`
- `docs/project-plan.md`
- `docs/decisions.md`
- `docs/dataset-audit.md`
- `docs/member2-dataset-verification.md`
- `results/dataset_audit/`
