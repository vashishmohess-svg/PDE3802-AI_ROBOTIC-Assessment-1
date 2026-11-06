# Step 3.1 — Visual and Label Review

**Review date:** 5 November 2026
**Project:** PDE3802 Assessment 1 — Autonomous Office Item Organisation System and Office-Goods Classification
**Reviewers:** Member 1 and Member 2
**Status:** Independent sample reviews and the full-resolution investigation completed; final document independently reviewed and approved by Member 2.

## 1. Purpose

This review examines a representative sample of the training images to identify visible class ambiguity, image-quality concerns and possible suitability issues before implementing the baseline classifier.

The review is intended to inform the baseline training process. It is not a complete manual inspection of every dataset image, and observations about image quality or secondary objects are not automatically treated as incorrect labels.

## 2. Dataset and review scope

- **Dataset:** office_home_dataset
- **Version:** 1
- **Creator:** stefanpublic
- **Source:** https://universe.roboflow.com/stefanpublic/office_home_dataset/dataset/1
- **Licence:** CC BY 4.0
- **Training split reviewed:** `dataset/train/`
- **Validation split:** `dataset/valid/` — not used for this visual sample review.
- **Test split:** `dataset/test/` — not used for this visual sample review and remains held out for final evaluation.

The audited dataset counts before any training-time exclusions were:

| Class | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| Bottle | 95 | 27 | 10 | 132 |
| Calculator | 104 | 31 | 19 | 154 |
| Keyboard | 122 | 37 | 14 | 173 |
| Mouse | 108 | 34 | 14 | 156 |
| Mug | 72 | 19 | 7 | 98 |
| Notebook | 117 | 27 | 15 | 159 |
| Pencil | 72 | 14 | 10 | 96 |
| Scissors | 126 | 34 | 14 | 174 |
| **Total** | **816** | **223** | **103** | **1142** |

The original audited training split therefore contains 816 images. This count is retained as the original dataset count in the project records.

## 3. Representative sample selection and inspection method

Six representative images were selected from each of the eight training class folders, giving:

- 8 classes;
- 6 selected images per class;
- 48 selected training images in total.

The selection process sorted the filenames case-insensitively and selected six evenly spaced samples from each class. Contact sheets were generated for visual inspection. The contact-sheet rendering process used Pillow to apply EXIF orientation correction and RGB conversion for display.

Member 1 generated the initial contact sheets. Member 2 independently generated contact sheets and compared them with Member 1's sheets. Member 2 reported that all eight pairs were byte-for-byte identical and confirmed that all 48 displayed filenames, arrangements and visual contents matched. No hash values are recorded in this document as independent hash evidence.

Both members independently examined the representative samples and then compared their observations. The same 48 selected paths were used for the joint review.

**Scope limitation:** This was a representative sample review of 48 images, not a manual inspection of all 816 training images. The review does not establish that every image in the dataset is correctly labelled or suitable.

## 4. Selected image paths

All paths below are relative to `dataset/train/`.

### Bottle

1. `Bottle/00001_jpg.rf.7d50e7e57d941fdcb0df860c2245e619.jpg`
2. `Bottle/00037_jpg.rf.b408683dff0ab20d13041fc6f0cf2168.jpg`
3. `Bottle/0798720e-2df1-4d12-b197-9291389ca1fb_jpg.rf.311d45342394e12e718cc71858beec8d.jpg`
4. `Bottle/4375c08b-e13d-4c26-a6ca-0eab82627950_jpg.rf.f9e355f7a140b91e434e2153cf6b615b.jpg`
5. `Bottle/9785fea8-c706-4fcd-be59-e254eb600e20_jpg.rf.75c15e54c35c98f067dc8573a70951f8.jpg`
6. `Bottle/ef370272-4ed1-4d15-b257-3b67d3763722_jpg.rf.5f13ffaba2a2f2963ed1c764e7dd9807.jpg`

### Calculator

1. `Calculator/00002_jpg.rf.8b71e5aa64003311987dcfe0b1329a9e.jpg`
2. `Calculator/00034_jpg.rf.b12764711f86023ebc0038464905a15e.jpg`
3. `Calculator/00069_jpg.rf.c4dc2bacbaaf5da6986453891cfb3c34.jpg`
4. `Calculator/31afe9ba-97b8-42b9-9583-9f6dccd508c2_jpg.rf.f196155b1bbf29b2c6e6c6db266d6038.jpg`
5. `Calculator/9fa8ad0b-5327-4fec-bea6-aa8e592e7c36_jpg.rf.44a6d3ca3e21bb0222d876c236ad3dd0.jpg`
6. `Calculator/fefe712c-2cc8-438e-a0f9-8d04bcf79687_jpg.rf.8e3a4c9c126d8509826de566c373f809.jpg`

### Keyboard

1. `Keyboard/00001_jpg.rf.91162b2d2cc0e1ba5fd05e843f712b59.jpg`
2. `Keyboard/00042_jpg.rf.6fa387daeb3155a60fae019131b1054e.jpg`
3. `Keyboard/00074_jpg.rf.ae2e0e0dae8142a79852581b6ab21bcf.jpg`
4. `Keyboard/1314fd01-056c-4df4-9a89-b500a30f5831_jpg.rf.d3ecc4d102d7497ee2a8562bf6fdd9a5.jpg`
5. `Keyboard/8a76a414-5d20-48c4-a1b3-936f926ad712_jpg.rf.b17750bd4d811d454111ae0c43b86c3c.jpg`
6. `Keyboard/f949dee5-dd07-4391-b170-6347d0e122e8_jpg.rf.71957c39824507a20a45f7cfdca54de8.jpg`

### Mouse

1. `Mouse/00001_jpg.rf.bafc73b947d7322576b17919a89c7bbf.jpg`
2. `Mouse/00034_jpg.rf.d2a788cf5d15d4edbe4ae288e2fbf2e3.jpg`
3. `Mouse/00063_jpg.rf.7a4c17a3836db7d7462b257a5799cda4.jpg`
4. `Mouse/00094_jpg.rf.87802c7b722027dc82abe365a3e499be.jpg`
5. `Mouse/7af15b67-8631-4c6b-81ad-df493d9ca4e7_jpg.rf.5dce7bbad68f15398a993dddd437d1b5.jpg`
6. `Mouse/f9ce9a31-6d3e-4948-a637-5f413ce37d0f_jpg.rf.5ce8b475ab5da747c45200368f7ecca7.jpg`

### Mug

1. `Mug/00002_jpg.rf.e94f56382d72f757431869d896f3d6fd.jpg`
2. `Mug/00023_jpg.rf.af2b5a9ac34dc311a8575738bb7ebdb0.jpg`
3. `Mug/00038_jpg.rf.c9a3f40ea1b14494df8147a51a6d912c.jpg`
4. `Mug/495467e2-7b25-422f-a547-d763a5935c54_jpg.rf.e8b9a4ae32026cddbd3b0dacc16e1fe8.jpg`
5. `Mug/a299ebfb-d13e-4ec6-a3e5-362eb66f445c_jpg.rf.577e9f3a1ea4c45945f2274c9dcb9b1f.jpg`
6. `Mug/ffc9c7d4-9c71-454b-9da8-eed57e8db5bd_jpg.rf.939d9fc6076aea99bdd13672b0f24fc7.jpg`

### Notebook

1. `Notebook/00001_jpg.rf.29c4d1f1c0cee96ffed021be9a35d5b5.jpg`
2. `Notebook/00032_jpg.rf.520de6b04e51826dd04aefc5a7ed8a56.jpg`
3. `Notebook/00066_jpg.rf.7310a11406376e51a735caeb4de3315f.jpg`
4. `Notebook/17d4af50-6e35-41dd-8bc9-49a130aa6074_jpg.rf.202f3ea93b4038e0b379335cae61c635.jpg`
5. `Notebook/73801881-4cf4-4e48-945b-5e451594d2a6_jpg.rf.c8a9bcbc54cfc0ac6e9642157e4a5932.jpg`
6. `Notebook/feda25eb-06d3-4e81-840a-9bc7c506dcae_jpg.rf.95b0cb90478e7ae3ffb234a8f4ae8bbb.jpg`

### Pencil

1. `Pencil/00001_jpg.rf.b6e867789918265e7889d52415c0c3fb.jpg`
2. `Pencil/00020_jpg.rf.129866b9a82628b5af5964df41c0da9c.jpg`
3. `Pencil/00038_jpg.rf.7f94c208054cb0f13467f3967c7ed71c.jpg`
4. `Pencil/40cc6db0-0fe6-4a8b-8da3-0205ceb0aa5c_jpg.rf.1d9f2f0934aebc915f1431080d4dc577.jpg`
5. `Pencil/99325b5d-10f5-447b-ad9a-366f90cf32ef_jpg.rf.d7d3f1972b1482c0086e14a5a3bc7b95.jpg`
6. `Pencil/ffe484f1-a73a-469a-b14a-f2f7e20ba6d1_jpg.rf.4a9b1ee842b5e523bc2047e65ee8b273.jpg`

### Scissors

1. `Scissors/00001_jpg.rf.ba55f47f314cfc71284bd56d763e3965.jpg`
2. `Scissors/00037_jpg.rf.9ea9927d8e4fe32ad2633765d015e440.jpg`
3. `Scissors/00070_jpg.rf.80618c69a6a51041668c647716a90957.jpg`
4. `Scissors/0952cccf-10b6-4028-b026-974634ad3ba0_jpg.rf.3e1c26e34af96229618a6f2b43c44cd9.jpg`
5. `Scissors/76944c3d-97aa-419f-80b9-956175c038c7_jpg.rf.fea63ea79d7ac916006a293a1bd49798.jpg`
6. `Scissors/fec0d684-6125-4ee8-91be-47350d1e3175_jpg.rf.3b1a1c4f2cf4fc78992b2a9eea9a5f66.jpg`

## 5. Joint observations from the 48 representative images

Both members independently inspected the selected images and agreed on the following observations:

| Class | Observations |
|---|---|
| Bottle | Selected image 5 contains a bottle and a drinking glass. |
| Calculator | All six selected images show calculators. Selected image 5 contains two views of a calculator. |
| Keyboard | Selected image 3 contains a keyboard and mice. Selected image 6 has strong blue lighting. |
| Mouse | Selected image 3 contains three mice. |
| Mug | Selected image 1 shows a travel mug, with a possible visual overlap with the Bottle category. |
| Notebook | Selected image 1 contains six notebooks; image 2 contains two notebooks; image 6 includes a pen. Images 4 and 5 show open notebooks with written notes and are somewhat soft in focus. |
| Pencil | Selected image 2 shows an ambiguous writing instrument; image 3 is severely pixelated; image 4 contains multiple writing instruments. |
| Scissors | Selected image 1 contains multiple pairs of scissors. |

These observations identify possible visual complexity, secondary objects, image-quality limitations and category overlap. The presence of multiple objects or a secondary object does not by itself establish that the assigned class label is wrong.

No incorrect class label was conclusively established from the representative sample review.

## 6. Full-resolution investigation of the priority Pencil image

The following image was identified as the highest-priority image for further inspection:

`dataset/train/Pencil/00038_jpg.rf.7f94c208054cb0f13467f3967c7ed71c.jpg`

Both members opened and inspected this original image at full resolution. They independently agreed that:

- The object can be identified as a pencil.
- The image is excessively stylised/animated.
- The image is genuinely pixelated or blurry at its original resolution.
- The object is not sufficiently clear or visible to provide a suitable baseline classifier training example.
- The image should be excluded from baseline classifier training because of image quality and suitability.

### 6.1 Label interpretation

The agreed conclusion is that this is an unsuitable image for baseline training, not a confirmed incorrect class label. The original `Pencil` folder assignment is preserved. The exclusion is based on the image's visual quality and suitability, not on a decision to relabel the object.

### 6.2 Agreed exclusion decision

**Both Member 1 and Member 2 approved the following decision:**

1. Exclude this exact image from the baseline classifier's training input.
2. Preserve the original image file in `dataset/train/Pencil/`.
3. Do not rename, move, edit, delete or relabel the original image.
4. Record the exclusion explicitly and apply it reproducibly in the baseline training pipeline.
5. Do not silently alter the original dataset or its physical folder structure.

**Original physical training count at the time of review:**

The original `dataset/train/` folder contained 816 images. Before the later group-aware logical allocation was approved, excluding this one image would have resulted in an expected training count of 815 images.

**Updated effective training count following D014 approval on 6 November 2026:**

The approved manifest-based logical allocation assigns 813 images to training, 226 to validation and 103 to the held-out test split.

The pixelated Pencil image is excluded from the logical training allocation. Therefore, the actual effective baseline training input contains **812 images**.

The earlier expectation of 815 images is superseded by the D014-approved manifest allocation and must not be used as the current training count.

The original physical dataset remains unchanged: the image is still present in its original folder, and the original training folder still contains 816 files. The validation and test logical assignments are determined by the approved manifest.

Refer to `docs/decisions.md` D014 and the approved manifest under `docs/evidence/step3.5.5J/`.

## 7. Dataset preservation and handling rules

- The original dataset files, physical folder structure, filenames and class folders must remain unchanged.
- No image was deleted, moved, renamed, edited or relabelled during the visual review or baseline implementation.
- The excluded pixelated Pencil image remains physically present in its original `dataset/train/Pencil/` folder.
- The approved D014 manifest determines the logical training, validation and test assignments. It maps each image to its original physical location using `Original_Split`, `Class` and `Filename`, and uses `Proposed_Split` for logical assignment.
- Baseline fitting must use only the 812 training records marked `Effective_Training_Eligible=YES`.
- All 226 proposed validation images must remain separate from model fitting and be used for validation.
- The 103 proposed test images must remain held out during Steps 3 and 4 and must only be accessed for final evaluation in Step 6.
- The training pipeline must apply the approved exclusion reproducibly rather than changing or deleting the source image.
- Any additional proposed exclusions or label changes must be recorded, justified and approved by both members before implementation.
- The original physical dataset counts and the approved logical split counts must be reported separately to avoid confusion.

Refer to `docs/decisions.md` D014 and the approved manifest and supporting evidence under `docs/evidence/step3.5.5J/`.

## 8. Conclusion and handover to baseline development

The representative visual review covered 48 selected training images across all eight classification classes. Both members independently reviewed the samples and agreed on the observations recorded in this document.

One Pencil image was inspected by both members at full resolution and judged unsuitable for baseline training because of its severe pixelation and image quality. Both members approved its exclusion from model fitting while preserving the original image and its class-folder assignment.

Following approval of decision D014 on 6 November 2026, the group-aware logical dataset allocation was applied through the approved manifest. The original physical dataset folders and image files remain unchanged. The effective baseline training set contains 812 images after the approved exclusion, with 226 validation images and 103 held-out test images.

The baseline data loader applies the exclusion reproducibly. The HOG + Linear SVM baseline was subsequently trained using the approved training data and evaluated using the validation data. The held-out test images were not accessed.

The visual-review findings, image-quality observations and agreed exclusion decision informed the baseline implementation. This review remains a representative sample inspection of 48 images and does not establish that every image in the dataset has been manually inspected or that every class label is correct.

For the baseline configuration and results, refer to `docs/step3-baseline-results.md`. For the approved logical dataset allocation, refer to decision D014 and the evidence under `docs/evidence/step3.5.5J/`.