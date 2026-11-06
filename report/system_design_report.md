# Autonomous Office Item Organisation System
## System Design Report

**PDE3802 Assessment 1**
**Date:** November 2026

---

## 1. System Overview

The Autonomous Office Item Organisation System is designed to identify, locate, and organise common office items in an office environment. The system uses computer vision to classify office items and integrates this classification capability into a wider robotic workflow for autonomous item organisation.

### 1.1 Mission

The system's primary mission is to autonomously identify and organise eight categories of office items: Bottle, Calculator, Keyboard, Mouse, Mug, Notebook, Pencil, and Scissors. The robot must be able to recognise these items from camera input, determine their location, and organise them into designated storage areas.

### 1.2 Scope

The current implementation focuses on the image classification component, which provides item category recognition. The system design describes how this classification component would integrate into a complete autonomous robot system for office item organisation.

**Note:** ROS (Robot Operating System) is not used in this implementation, in accordance with the lecturer's instruction.

---

## 2. Required Skills

### 2.1 Item Recognition Skill

**Input:** Camera frame or image file containing one office item  
**Output:** Predicted class (one of eight categories)  
**Success Criteria:**
- Classification accuracy ≥ 65% on held-out test set
- Processing time ≤ 500ms per image
- Successful handling of invalid inputs with appropriate error messages

**Implementation:** HOG + RBF SVM classifier with C=10.0, trained on 812 images.

### 2.2 Object Localization Skill

**Input:** Camera frame from robot's vision system  
**Output:** Bounding box coordinates and item class  
**Success Criteria:**
- Bounding box accuracy within ±20 pixels
- Detection of items within 2m range
- Multi-object detection capability

**Implementation:** Would require object detection model (e.g., YOLO, SSD) - not implemented in current scope.

### 2.3 Navigation Skill

**Input:** Target location coordinates  
**Output:** Path planning and movement commands  
**Success Criteria:**
- Path planning time ≤ 2 seconds
- Navigation accuracy within ±5cm
- Obstacle avoidance in dynamic environments

**Implementation:** Would require SLAM (Simultaneous Localization and Mapping) and path planning algorithms - not implemented in current scope.

### 2.4 Grasping Skill

**Input:** Object location and type  
**Output:** Grasp execution confirmation  
**Success Criteria:**
- Grasp success rate ≥ 80%
- Adaptation to different object shapes and sizes
- Safe handling without damage

**Implementation:** Would require robotic arm with inverse kinematics and force feedback - not implemented in current scope.

---

## 3. Hardware Components

### 3.1 Mobile Platform

**Primary Option:** Differential drive mobile robot base  
**Specifications:**
- Maximum speed: 0.5 m/s
- Payload capacity: ≥ 5 kg
- Battery life: ≥ 2 hours continuous operation
- Size: 50cm × 50cm × 30cm (L×W×H)

**Alternative Options:**
- Omnidirectional wheeled platform for enhanced maneuverability
- Tracked platform for uneven surfaces

### 3.2 Manipulation System

**Primary Option:** 6-DOF robotic arm with parallel gripper  
**Specifications:**
- Reach: 60cm
- Payload: 1 kg
- Gripper opening: 10cm maximum
- Degrees of freedom: 6

**Alternative Options:**
- Delta robot for faster pick-and-place operations
- Soft gripper for delicate items

### 3.3 Vision System

**Primary Option:** RGB camera mounted on robot arm  
**Specifications:**
- Resolution: 1920×1080
- Frame rate: 30 fps
- Field of view: 90°
- Auto-focus capability

**Alternative Options:**
- Stereo camera for depth perception
- Depth camera (e.g., Intel RealSense) for 3D object localization

### 3.4 Computing Hardware

**Primary Option:** Onboard computer with GPU  
**Specifications:**
- CPU: Intel i7 or equivalent
- RAM: 16 GB
- GPU: NVIDIA Jetson or equivalent for inference acceleration
- Storage: 500 GB SSD

### 3.5 Sensors

**Required Sensors:**
- Wheel encoders for odometry
- IMU (Inertial Measurement Unit) for orientation
- Ultrasonic or LiDAR sensors for obstacle detection
- Bump sensors for collision detection

---

## 4. System Architecture

### 4.1 Architecture Overview

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                   High-Level Planner                    │
│            (Task sequencing and coordination)            │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼─────────┐ ┌▼──────────────┐
│  Vision      │ │ Navigation │ │ Manipulation   │
│  Module      │ │  Module    │ │   Module      │
│              │ │            │ │               │
│ - Camera     │ │ - SLAM     │ │ - Inverse     │
│ - Classifier │ │ - Path     │ │   Kinematics  │
│ - Detection  │ │   Planning │ │ - Grasp       │
│              │ │ - Control  │ │   Control     │
└──────────────┘ └────────────┘ └───────────────┘
```

### 4.2 Classification Component Integration

The image classification component serves as the foundation for item recognition:

1. **Input Acquisition:** Camera captures frames at 30 fps
2. **Preprocessing:** Frames are resized to 128×128, converted to grayscale
3. **Feature Extraction:** HOG features (8,100 dimensions) extracted
4. **Classification:** RBF SVM predicts item
5. **Result Output:** Class label provided to higher-level planner

### 4.3 Data Flow

```
Camera Frame → Preprocessing → HOG Features → SVM Classifier → Class Label
                                                            ↓
                                                    High-Level Planner
                                                            ↓
                                            (Location, Grasp, Navigation)
```

### 4.4 Processing Pipeline

1. **Exploration Phase:** Robot scans environment using camera
2. **Detection Phase:** Items detected and classified
3. **Planning Phase:** Task sequence generated (e.g., "Pick up Bottle, place in storage A")
4. **Execution Phase:** Robot navigates, grasps, and places items
5. **Verification Phase:** Confirm item placement and update environment map

---

## 5. Safety Considerations

### 5.1 Operational Safety

**Collision Avoidance:**
- Multiple sensor redundancy (ultrasonic, LiDAR, bump sensors)
- Emergency stop functionality
- Speed reduction in proximity to humans
- Audible and visual warnings during operation

**Grasping Safety:**
- Force feedback to prevent excessive gripping force
- Slip detection during transport
- Secure transport with item verification

### 5.2 Human-Robot Interaction

**Safety Zones:**
- Defined operational areas where robot operates autonomously
- Human detection using sensors
- Automatic slowdown or stop when humans enter safety zones

**Emergency Controls:**
- Physical emergency stop button
- Remote emergency stop via software interface
- Clear visual indicators of robot state

### 5.3 Failure Modes

**Classification Failures:**
- Low-confidence predictions trigger manual verification
- Unknown items flagged for human intervention
- System logs classification errors for analysis

**Navigation Failures:**
- Path planning timeout triggers safe stop
- Obstacle detection failure activates emergency stop
- Lost localization triggers return-to-home procedure

**Grasping Failures:**
- Failed grasp attempts trigger retry (max 3 attempts)
- Persistent failures flag item for human intervention
- Dropped items trigger immediate stop and alert

---

## 6. Bill of Materials and Estimated Budget

### 6.1 Hardware Components

| Component | Specification | Estimated Cost |
|-----------|--------------|----------------|
| Mobile Robot Base | Differential drive, 5kg payload | $1,500 |
| Robotic Arm | 6-DOF, 1kg payload, 60cm reach | $3,000 |
| RGB Camera | 1080p, 30fps, 90° FOV | $200 |
| Onboard Computer | i7, 16GB RAM, GPU | $1,200 |
| Sensors (LiDAR, IMU, encoders) | Complete sensor suite | $800 |
| Power System | Batteries and power management | $500 |
| Gripper | Parallel jaw, 10cm opening | $400 |
| **Total Hardware** | | **$7,600** |

### 6.2 Software and Development

| Item | Estimated Cost |
|------|----------------|
| Operating System and Development Tools | $0 (open source) |
| Computer Vision Libraries | $0 (open source) |
| Development Time (200 hours @ $50/hr) | $10,000 |
| **Total Software/Development** | **$10,000** |

### 6.3 Total Estimated Budget

**Total Project Cost: $17,600**

---

## 7. Dataset and Model Approach

### 7.1 Dataset

**Source:** office_home_dataset from Roboflow Universe  
**Licence:** CC BY 4.0  
**Classes:** 8 office item categories  
**Total Images:** 1,142  
**Split:** 812 training, 226 validation, 103 test

### 7.2 Model Selection

**Selected Model:** HOG + RBF SVM (C=10.0, gamma=scale)

**Rationale:**
- Achieved highest validation accuracy (72.57%) among tested models
- Good balance between accuracy and computational efficiency
- Suitable for real-time inference on embedded hardware
- No probability estimates required for current application

**Performance:**
- Validation accuracy: 72.57%
- Validation macro-F1: 0.6831
- Test accuracy: 66.99%
- Test macro-F1: 0.6288
- Inference time: ~6.5ms per image (excluding HOG extraction)

### 7.3 Limitations

- Model processes one item per image (not multi-object detection)
- Pencil class has lowest performance (F1: 0.40)
- No confidence scores available (probability estimates disabled)
- Model trained on 416×416 images, may not generalize well to other resolutions

---

## 8. References

1. Dataset: office_home_dataset by stefanpublic, Roboflow Universe. https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1
2. Scikit-learn: Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.
3. OpenCV: Bradski, G., Dr. Dobb's Journal of Software Tools, 2000.
4. Dalal, N., & Triggs, B. (2005). Histograms of oriented gradients for human detection. CVPR 2005.

---

## 9. Team Contributions

**Member 1 (Project Lead and Dataset/Model Lead):**
- Project setup and Git workflow coordination
- Dataset inspection, preparation, and documentation
- Model development, training, and evaluation
- Model comparison and selection
- Final held-out test evaluation
- Classification error analysis

**Member 2 (Application and System Design Lead):**
- Development environment verification
- Prediction application development
- System design documentation
- Robustness and input-handling testing
- Application testing and integration support
- Documentation and final deliverables

---

*End of System Design Report*
