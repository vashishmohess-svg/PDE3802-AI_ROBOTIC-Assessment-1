"""Convert System Design Report from Markdown to Word format."""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path

def create_word_document():
    # Create a new Document
    doc = Document()
    
    # Title
    title = doc.add_heading('Autonomous Office Item Organisation System', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_heading('System Design Report', 1)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add member information
    doc.add_paragraph('PDE3802 Assessment 1')
    doc.add_paragraph('Date: November 2026')
    doc.add_paragraph()
    
    # Member information
    doc.add_heading('Team Members', 2)
    p = doc.add_paragraph()
    p.add_run('Member 1: KOSHAL MOHESS (Team Leader)\n')
    p.add_run('Student ID: M00943654\n\n')
    p.add_run('Member 2: NISHANT HAULKHORY\n')
    p.add_run('Student ID: M01004090')
    
    doc.add_page_break()
    
    # Section 1: System Overview
    doc.add_heading('1. System Overview', 2)
    doc.add_paragraph(
        'The Autonomous Office Item Organisation System is designed to identify, locate, and organise '
        'common office items in an office environment. The system uses computer vision to classify '
        'office items and integrates this classification capability into a wider robotic workflow for '
        'autonomous item organisation.'
    )
    
    doc.add_heading('1.1 Mission', 3)
    doc.add_paragraph(
        'The system\'s primary mission is to autonomously identify and organise eight categories of '
        'office items: Bottle, Calculator, Keyboard, Mouse, Mug, Notebook, Pencil, and Scissors. '
        'The robot must be able to recognise these items from camera input, determine their location, '
        'and organise them into designated storage areas.'
    )
    
    doc.add_heading('1.2 Scope', 3)
    doc.add_paragraph(
        'The current implementation focuses on the image classification component, which provides '
        'item category recognition. The system design describes how this classification component would '
        'integrate into a complete autonomous robot system for office item organisation.'
    )
    doc.add_paragraph('Note: ROS (Robot Operating System) is not used in this implementation.')
    
    doc.add_page_break()
    
    # Section 2: Required Skills
    doc.add_heading('2. Required Skills', 2)
    
    doc.add_heading('2.1 Item Recognition Skill', 3)
    doc.add_paragraph('Input: Camera frame or image file containing one office item')
    doc.add_paragraph('Output: Predicted class (one of eight categories)')
    doc.add_paragraph('Success Criteria:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Classification accuracy ≥ 65% on held-out test set')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Processing time ≤ 500ms per image')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Successful handling of invalid inputs with appropriate error messages')
    doc.add_paragraph('Implementation: HOG + RBF SVM classifier with C=10.0, trained on 812 images.')
    
    doc.add_heading('2.2 Object Localization Skill', 3)
    doc.add_paragraph('Input: Camera frame from robot\'s vision system')
    doc.add_paragraph('Output: Bounding box coordinates and item class')
    doc.add_paragraph('Success Criteria:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Bounding box accuracy within ±20 pixels')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Detection of items within 2m range')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Multi-object detection capability')
    doc.add_paragraph('Implementation: Would require object detection model (e.g., YOLO, SSD) - not implemented in current scope.')
    
    doc.add_heading('2.3 Navigation Skill', 3)
    doc.add_paragraph('Input: Target location coordinates')
    doc.add_paragraph('Output: Path planning and movement commands')
    doc.add_paragraph('Success Criteria:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Path planning time ≤ 2 seconds')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Navigation accuracy within ±5cm')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Obstacle avoidance in dynamic environments')
    doc.add_paragraph('Implementation: Would require SLAM and path planning algorithms - not implemented in current scope.')
    
    doc.add_heading('2.4 Grasping Skill', 3)
    doc.add_paragraph('Input: Object location and type')
    doc.add_paragraph('Output: Grasp execution confirmation')
    doc.add_paragraph('Success Criteria:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Grasp success rate ≥ 80%')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Adaptation to different object shapes and sizes')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Safe handling without damage')
    doc.add_paragraph('Implementation: Would require robotic arm with inverse kinematics and force feedback - not implemented in current scope.')
    
    doc.add_page_break()
    
    # Section 3: Hardware Components
    doc.add_heading('3. Hardware Components', 2)
    
    doc.add_heading('3.1 Mobile Platform', 3)
    doc.add_paragraph('Primary Option: Differential drive mobile robot base')
    doc.add_paragraph('Specifications:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Maximum speed: 0.5 m/s')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Payload capacity: ≥ 5 kg')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Battery life: ≥ 2 hours continuous operation')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Size: 50cm × 50cm × 30cm (L×W×H)')
    
    doc.add_heading('3.2 Manipulation System', 3)
    doc.add_paragraph('Primary Option: 6-DOF robotic arm with parallel gripper')
    doc.add_paragraph('Specifications:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Reach: 60cm')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Payload: 1 kg')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Gripper opening: 10cm maximum')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Degrees of freedom: 6')
    
    doc.add_heading('3.3 Vision System', 3)
    doc.add_paragraph('Primary Option: RGB camera mounted on robot arm')
    doc.add_paragraph('Specifications:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Resolution: 1920×1080')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Frame rate: 30 fps')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Field of view: 90°')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Auto-focus capability')
    
    doc.add_heading('3.4 Computing Hardware', 3)
    doc.add_paragraph('Primary Option: Onboard computer with GPU')
    doc.add_paragraph('Specifications:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('CPU: Intel i7 or equivalent')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('RAM: 16 GB')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('GPU: NVIDIA Jetson or equivalent for inference acceleration')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Storage: 500 GB SSD')
    
    doc.add_heading('3.5 Sensors', 3)
    doc.add_paragraph('Required Sensors:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Wheel encoders for odometry')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('IMU (Inertial Measurement Unit) for orientation')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Ultrasonic or LiDAR sensors for obstacle detection')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Bump sensors for collision detection')
    
    doc.add_page_break()
    
    # Section 4: System Architecture
    doc.add_heading('4. System Architecture', 2)
    
    doc.add_heading('4.1 Architecture Overview', 3)
    doc.add_paragraph('The system follows a modular architecture with clear separation of concerns:')
    doc.add_paragraph('High-Level Planner: Task sequencing and coordination')
    doc.add_paragraph('Vision Module: Camera, Classifier, Detection')
    doc.add_paragraph('Navigation Module: SLAM, Path Planning, Control')
    doc.add_paragraph('Manipulation Module: Inverse Kinematics, Grasp Control')
    
    doc.add_heading('4.2 Classification Component Integration', 3)
    doc.add_paragraph('The image classification component serves as the foundation for item recognition:')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Input Acquisition: Camera captures frames at 30 fps')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Preprocessing: Frames are resized to 128×128, converted to grayscale')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Feature Extraction: HOG features (8,100 dimensions) extracted')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Classification: RBF SVM predicts item')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Result Output: Class label provided to higher-level planner')
    
    doc.add_heading('4.3 Data Flow', 3)
    doc.add_paragraph('Camera Frame → Preprocessing → HOG Features → SVM Classifier → Class Label → High-Level Planner → (Location, Grasp, Navigation)')
    
    doc.add_heading('4.4 Processing Pipeline', 3)
    p = doc.add_paragraph(style='List Number')
    p.add_run('Exploration Phase: Robot scans environment using camera')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Detection Phase: Items detected and classified')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Planning Phase: Task sequence generated')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Execution Phase: Robot navigates, grasps, and places items')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Verification Phase: Confirm item placement and update environment map')
    
    doc.add_page_break()
    
    # Section 5: Safety Considerations
    doc.add_heading('5. Safety Considerations', 2)
    
    doc.add_heading('5.1 Operational Safety', 3)
    doc.add_paragraph('Collision Avoidance:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Multiple sensor redundancy (ultrasonic, LiDAR, bump sensors)')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Emergency stop functionality')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Speed reduction in proximity to humans')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Audible and visual warnings during operation')
    
    doc.add_paragraph('Grasping Safety:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Force feedback to prevent excessive gripping force')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Slip detection during transport')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Secure transport with item verification')
    
    doc.add_heading('5.2 Human-Robot Interaction', 3)
    doc.add_paragraph('Safety Zones:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Defined operational areas where robot operates autonomously')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Human detection using sensors')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Automatic slowdown or stop when humans enter safety zones')
    
    doc.add_paragraph('Emergency Controls:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Physical emergency stop button')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Remote emergency stop via software interface')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Clear visual indicators of robot state')
    
    doc.add_heading('5.3 Failure Modes', 3)
    doc.add_paragraph('Classification Failures:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Low-confidence predictions trigger manual verification')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Unknown items flagged for human intervention')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('System logs classification errors for analysis')
    
    doc.add_paragraph('Navigation Failures:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Path planning timeout triggers safe stop')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Obstacle detection failure activates emergency stop')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Lost localization triggers return-to-home procedure')
    
    doc.add_paragraph('Grasping Failures:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Failed grasp attempts trigger retry (max 3 attempts)')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Persistent failures flag item for human intervention')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Dropped items trigger immediate stop and alert')
    
    doc.add_page_break()
    
    # Section 6: Bill of Materials and Estimated Budget
    doc.add_heading('6. Bill of Materials and Estimated Budget', 2)
    
    doc.add_heading('6.1 Hardware Components', 3)
    
    # Create table
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Component'
    hdr_cells[1].text = 'Estimated Cost'
    
    data = [
        ('Mobile Robot Base', '$1,500'),
        ('Robotic Arm', '$3,000'),
        ('RGB Camera', '$200'),
        ('Onboard Computer', '$1,200'),
        ('Sensors (LiDAR, IMU, encoders)', '$800'),
        ('Power System', '$500'),
        ('Gripper', '$400'),
        ('Total Hardware', '$7,600'),
    ]
    
    for item, cost in data:
        row_cells = table.add_row().cells
        row_cells[0].text = item
        row_cells[1].text = cost
    
    doc.add_paragraph()
    doc.add_heading('6.2 Software and Development', 3)
    
    table2 = doc.add_table(rows=1, cols=2)
    table2.style = 'Table Grid'
    hdr_cells2 = table2.rows[0].cells
    hdr_cells2[0].text = 'Item'
    hdr_cells2[1].text = 'Estimated Cost'
    
    data2 = [
        ('Operating System and Development Tools', '$0 (open source)'),
        ('Computer Vision Libraries', '$0 (open source)'),
        ('Development Time (200 hours @ $50/hr)', '$10,000'),
        ('Total Software/Development', '$10,000'),
    ]
    
    for item, cost in data2:
        row_cells = table2.add_row().cells
        row_cells[0].text = item
        row_cells[1].text = cost
    
    doc.add_paragraph()
    doc.add_heading('6.3 Total Estimated Budget', 3)
    doc.add_paragraph('Total Project Cost: $17,600')
    
    doc.add_page_break()
    
    # Section 7: Dataset and Model Approach
    doc.add_heading('7. Dataset and Model Approach', 2)
    
    doc.add_heading('7.1 Dataset', 3)
    doc.add_paragraph('Source: office_home_dataset from Roboflow Universe')
    doc.add_paragraph('Licence: CC BY 4.0')
    doc.add_paragraph('Classes: 8 office item categories')
    doc.add_paragraph('Total Images: 1,142')
    doc.add_paragraph('Split: 812 training, 226 validation, 103 test')
    
    doc.add_heading('7.2 Model Selection', 3)
    doc.add_paragraph('Selected Model: HOG + RBF SVM (C=10.0, gamma=scale)')
    doc.add_paragraph('Rationale:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Achieved highest validation accuracy (72.57%) among tested models')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Good balance between accuracy and computational efficiency')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Suitable for real-time inference on embedded hardware')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('No probability estimates required for current application')
    
    doc.add_paragraph('Performance:')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Validation accuracy: 72.57%')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Validation macro-F1: 0.6831')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Test accuracy: 66.99%')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Test macro-F1: 0.6288')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Inference time: ~6.5ms per image (excluding HOG extraction)')
    
    doc.add_heading('7.3 Limitations', 3)
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Model processes one item per image (not multi-object detection)')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Pencil class has lowest performance (F1: 0.40)')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('No confidence scores available (probability estimates disabled)')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Model trained on 416×416 images, may not generalize well to other resolutions')
    
    doc.add_page_break()
    
    # Section 8: References
    doc.add_heading('8. References', 2)
    p = doc.add_paragraph(style='List Number')
    p.add_run('Dataset: office_home_dataset by stefanpublic, Roboflow Universe. https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Scikit-learn: Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.')
    p = doc.add_paragraph(style='List Number')
    p.add_run('OpenCV: Bradski, G., Dr. Dobb\'s Journal of Software Tools, 2000.')
    p = doc.add_paragraph(style='List Number')
    p.add_run('Dalal, N., & Triggs, B. (2005). Histograms of oriented gradients for human detection. CVPR 2005.')
    
    doc.add_page_break()
    
    # Section 9: Team Contributions
    doc.add_heading('9. Team Contributions', 2)
    
    doc.add_paragraph('Member 1 (Project Lead and Dataset/Model Lead):')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Project setup and Git workflow coordination')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Dataset inspection, preparation, and documentation')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Model development, training, and evaluation')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Model comparison and selection')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Final held-out test evaluation')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Classification error analysis')
    
    doc.add_paragraph('Member 2 (Application and System Design Lead):')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Development environment verification')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Prediction application development')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('System design documentation')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Robustness and input-handling testing')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Application testing and integration support')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Documentation and final deliverables')
    
    # Save the document
    output_path = Path('C:/Users/Nishant/OneDrive/Desktop/Submission_Folder/Report_Submission/System_Design_Report.docx')
    doc.save(output_path)
    print(f"Word document saved to: {output_path}")

if __name__ == "__main__":
    create_word_document()
