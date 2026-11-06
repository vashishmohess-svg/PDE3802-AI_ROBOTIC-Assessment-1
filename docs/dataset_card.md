# Dataset Card: Office Home Dataset Subset

## Dataset Overview

This dataset is a selected subset of the `office_home_dataset` from Roboflow Universe, used for training an office-item classification system as part of the PDE3802 Assessment 1 project.

## Dataset Source and Attribution

- **Dataset name:** office_home_dataset
- **Creator:** stefanpublic
- **Source:** https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1
- **Dataset version:** 1
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)

This project uses a selected subset of eight office-item categories from the downloaded dataset. The original dataset creator and source are acknowledged in accordance with the CC BY 4.0 licence.

## Dataset Description

The dataset contains images of eight common office items, organized into training, validation, and testing subsets. All images are JPEG format with dimensions of 416 × 416 pixels.

### Object Categories

The eight object categories are:

1. Bottle
2. Calculator
3. Keyboard
4. Mouse
5. Mug
6. Notebook
7. Pencil
8. Scissors

### Dataset Distribution

**Original Physical Dataset Folders**

| Original split | Number of images |
|---|---:|
| Training (`train`) | 816 |
| Validation (`valid`) | 223 |
| Testing (`test`) | 103 |
| **Total** | **1,142** |

**Approved Logical Dataset Splits**

Following the group-aware dataset review (Decision D014), the approved manifest-based logical allocation is:

| Logical split | Number of images |
|---|---:|
| Training allocation | 813 |
| Validation | 226 |
| Testing | 103 |
| **Total** | **1,142** |

The classifier uses the approved manifest located at:
`docs/evidence/step3.5.5J/step3.5.5K3_full_split_manifest_proposal.csv`

One severely pixelated Pencil image is excluded from model fitting. Therefore, the effective training count is **812 images**.

### Class Distribution

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

### Dataset Folder Structure

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

## Dataset Characteristics

### Image Properties

- **Format:** JPEG (.jpg)
- **Dimensions:** 416 × 416 pixels
- **Color:** RGB (converted to grayscale for model training)
- **Total images:** 1,142

### Dataset Quality

The completed dataset audit confirmed:
- All 1,142 images were successfully decoded
- All images are JPEG files with `.jpg` extensions
- All images have dimensions of 416 × 416 pixels
- No invalid or unreadable images were identified
- No unsupported files, misplaced files, or unexpected directories were identified
- No exact duplicate groups were detected using SHA-256 hashes

### Known Limitations

1. **Class Imbalance:** The dataset is not perfectly balanced. For example, Scissors has 174 images, while Pencil has 96 images.

2. **Small Test Split:** The test split contains 103 images in total, with only 7 to 19 images per class. This relatively small test set may limit how confidently the final results can represent performance on a wider range of images.

3. **Audit Limitations:** The dataset audit checked file integrity, image properties, folder structure, and exact duplicates. It did not visually verify that every image has the correct class label. The duplicate check does not identify visually similar images that have different file contents.

## Dataset Usage

### Preprocessing Pipeline

The approved preprocessing pipeline applied to all images:

1. Apply EXIF orientation correction
2. Convert the image to grayscale
3. Resize to 128 × 128 pixels using OpenCV `INTER_AREA` interpolation
4. Convert to uint8 NumPy array

### Feature Extraction

Histogram of Oriented Gradients (HOG) is used to represent image structure:

- Window size: 128 × 128
- Block size: 16 × 16
- Block stride: 8 × 8
- Cell size: 8 × 8
- Orientation bins: 9
- Features per image: 8,100

### Model Training

The selected model is HOG + RBF SVM with C = 10.0, trained on 812 eligible training images (after excluding one severely pixelated Pencil image).

### Evaluation Results

**Validation Results (226 images):**
- Accuracy: 72.57%
- Macro-F1: 0.6831

**Test Results (103 images):**
- Accuracy: 66.99%
- Macro-F1: 0.6288

## Dataset Integrity

The original physical dataset folders and image files remain unchanged. The approved manifest determines the logical assignments used by the classifier. The test dataset remains held out from training and model selection and is reserved for final evaluation.

## License and Citation

This dataset is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license.

When using this dataset, please cite the original source:

```
Dataset: office_home_dataset
Creator: stefanpublic
Source: https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1
License: CC BY 4.0
```

## Contact and Support

For questions about this dataset in the context of the PDE3802 project, please refer to the project documentation in the `docs/` directory.
