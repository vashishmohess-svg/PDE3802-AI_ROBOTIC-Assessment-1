# Step 2 — Environment Setup

- **Project:** PDE3802 Assessment 1 — Autonomous Office Item Organisation System and Office-Goods Classification
- **Step:** 2 — Environment Setup
- **Project lead:** Member 1
- **Independent verification and review:** Member 2
- **Current status:** Technical environment setup and cross-computer verification completed; final documentation integration in progress.


---

## 1. Introduction and purpose

Before starting the office-item classifier, both members needed a reliable and consistent Python environment. Since the project is being developed on two different computers, it was important to agree on the Python version and dependencies so that the same project could be installed and tested on both systems.

This step covered the initial inspection of both computers, selection of a shared Python version, creation of separate virtual environments, installation of the required packages and verification of the software. Git was also used to review and integrate the dependency files into the shared repository.

The project uses Visual Studio Code, Python, Git and PowerShell on Windows. ROS is not being used because the lecturer instructed the team not to use it.

## 2. Initial computer and software inspection

Both members first inspected their existing computers and Python environments. This helped identify differences between the two systems before preparing the new shared environment.

### 2.1 Software inspection

| Item | Member 1 | Member 2 |
|---|---|---|
| Operating system | Windows 11, build 22631 | Windows 11, build 26300 |
| Terminal | PowerShell 5.1 | PowerShell 5.1 |
| Code editor | Visual Studio Code 1.143.1 | Visual Studio Code 1.144.0 |
| Git | 2.56.0.windows.2 | 2.56.0.windows.2 |
| Initial Python environment | Python 3.13.1 default; Python 3.12 also installed | Python 3.13.14, 64-bit |

The initial Python environments were not the same. Member 1's old virtual environment contained Pillow but did not have the other main project packages installed. Member 2 had more packages in the previous environment, but that environment was no longer suitable for the new shared setup after the original Python installation path became unavailable.

Both members therefore prepared new environments using the same Python release rather than relying on their previous installations.

### 2.2 Hardware inspection

| Hardware | Member 1 | Member 2 |
|---|---|---|
| Processor | Intel Core i5-8265U | Intel Core i5-1335U |
| CPU cores | 4 | 10 |
| Logical processors | 8 | 12 |
| Recorded RAM | 11.88 GB | 7.64 GB |
| Graphics | Intel UHD Graphics 620 and Radeon 520 | Intel UHD Graphics |
| Available C: drive space at inspection | 240.53 GB | 102.48 GB |

The hardware inspection was useful because the two computers have different processing capabilities and available memory. In particular, Member 2's computer has less recorded RAM. This needs to be considered during later model experiments, especially when selecting model sizes and batch sizes. The team should use manageable experiments and avoid assuming that both computers will perform at the same speed.

## 3. Python version selection

The team selected **Python 3.13.17, 64-bit** as the common Python version for the project.

Both members installed and verified this version independently.

The verified Python executable paths were:

**Member 1**

```text
C:\Users\Veeresh.Mohess\AppData\Local\Programs\Python\Python31317\python.exe
```

**Member 2**

```text
C:\Users\Nishant\AppData\Local\Programs\Python\Python31317\python.exe
```

Both members confirmed:

- Python version: `3.13.17`
- Architecture: 64-bit
- pip version: `26.2.2`
- Python launcher access using `py -3.13`

The previous virtual environments were archived rather than reused. Each member then created a new project-specific `.venv` environment using the selected Python installation.

### 3.1 Reproducing the environment

The following PowerShell commands show how the environment can be recreated in a fresh project checkout. They explicitly select and verify Python 3.13.17 before creating the virtual environment. The installation command uses the shared `requirements-lock.txt` file so that the complete pinned package set is installed.

These commands are provided as reproduction instructions and are not intended to claim that both members used this exact command sequence during the original environment creation.

Run the commands from the project root in the VS Code PowerShell terminal:

```powershell
# Locate the Python 3.13.17 installation
$python31317 = Join-Path $env:LOCALAPPDATA "Programs\Python\Python31317\python.exe"

# Confirm that the interpreter exists
if (-not (Test-Path $python31317)) {
    throw "Python 3.13.17 was not found at the expected installation path."
}

# Verify the exact Python version
$pythonVersion = & $python31317 --version

if ($pythonVersion -ne "Python 3.13.17") {
    throw "The selected interpreter is not Python 3.13.17."
}

# Create the project virtual environment
& $python31317 -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Verify Python and pip
python --version
python -m pip --version

# Install the complete locked dependency set
python -m pip install -r .\requirements-lock.txt

# Check dependency consistency
python -m pip check
```

Both members subsequently verified that their project interpreter was Python 3.13.17, 64-bit, with pip 26.2.2, and that their virtual environment was separate from the base Python installation.

## 4. Shared Python dependencies

After selecting the Python version, the team agreed on six direct dependencies required for the project. These packages cover numerical operations, image handling, image processing, machine learning, deep learning and plotting.

### 4.1 Final `requirements.txt`

The shared `requirements.txt` contains the following pinned direct dependencies:

```text
# PDE3802 Assessment 1
# Shared direct dependencies
# Python 3.13.17 (64-bit Windows)

tensorflow==2.21.0
numpy==2.1.3
Pillow==13.0.0
opencv-python==4.14.0.94
scikit-learn==1.9.1
matplotlib==3.11.2
```

| Package | Version | Purpose in the project |
|---|---:|---|
| TensorFlow | 2.21.0 | Machine-learning and deep-learning framework |
| NumPy | 2.1.3 | Numerical operations and array handling |
| Pillow | 13.0.0 | Image loading and image handling |
| OpenCV-Python | 4.14.0.94 | Image processing and camera/image operations |
| scikit-learn | 1.9.1 | Conventional machine-learning models and evaluation |
| Matplotlib | 3.11.2 | Plotting and visualisation |

Keras is installed as part of the TensorFlow dependency set. Both members verified the installed Keras version as `3.15.1`. It is therefore included in the resolved dependency lock file rather than being added as a separate direct dependency in `requirements.txt`.

### 4.2 NumPy version decision

The team selected `numpy==2.1.3` as a conservative version for the shared TensorFlow environment. The TensorFlow 2.21 release requirements-updater information indicated a NumPy range below 2.2.0. The team therefore used NumPy 2.1.3 rather than retaining the newer NumPy version found in Member 2's original environment.

This provided a common version for both computers and avoided unnecessary differences in the main numerical dependency.

### 4.3 Dependency lock file

The team also created `requirements-lock.txt` to record the complete resolved package environment, including indirect dependencies.

The two files have different purposes:

| File | Purpose | Number of entries |
|---|---|---:|
| `requirements.txt` | Six direct project dependencies | 6 |
| `requirements-lock.txt` | Fully pinned resolved dependency set | 48 |

The lock file contains 48 pinned package entries, including `keras==3.15.1`. It allows both members to install the same resolved package versions rather than relying only on the six direct dependencies.

## 5. Dependency installation

The dependency files were added to the shared repository and reviewed through GitHub pull requests.

Member 1 installed the agreed direct dependencies using `requirements.txt`. Member 2 installed the shared locked package set using `requirements-lock.txt`. Both installations were carried out inside their own project virtual environments.

Before the dependency changes were merged, the package versions were reviewed to ensure that they matched the agreed environment. The lock file was also checked for the correct direct dependency versions, the expected Keras version, the total number of pinned entries and the absence of unrelated packages.

The installation was followed by import tests, functional smoke tests and package consistency checks on both computers.

## 6. Runtime and image-processing verification

After installation, both members tested the main libraries to confirm that they could be imported and used successfully. These were basic environment smoke tests. They were not the final training or evaluation of the office-item classifier.

### 6.1 Installed package versions

The following versions were verified:

| Component | Version |
|---|---:|
| Python | 3.13.17 |
| pip | 26.2.2 |
| TensorFlow | 2.21.0 |
| Keras | 3.15.1 |
| NumPy | 2.1.3 |
| Pillow | 13.0.0 |
| OpenCV package | 4.14.0.94 |
| scikit-learn | 1.9.1 |
| Matplotlib | 3.11.2 |

**OpenCV version note:** The installed package is pinned as `opencv-python==4.14.0.94`, while the imported library reports `cv2.__version__` as `4.14.0`. These refer to the package version and the library-reported version respectively, so they are not conflicting results.

### 6.2 TensorFlow and Keras test

Both members reported successful imports of TensorFlow and Keras.

The checks confirmed:

- TensorFlow reported version `2.21.0`.
- Keras reported version `3.15.1`.
- A TensorFlow CPU device was detected.
- A simple TensorFlow calculation returned `6`.

The tests used native Windows CPU execution. TensorFlow displayed a warning concerning GPU support on native Windows, but the CPU device was available and the calculation completed successfully.

**GPU acceleration was not configured or tested as part of this environment setup.** The verified TensorFlow execution was CPU-based.

### 6.3 scikit-learn test

A small Support Vector Machine (SVM) test was carried out to confirm that scikit-learn could be imported and used.

The reported predictions were:

```text
[0, 1]
```

This confirmed basic functionality of the installed library. It was only a smoke test and should not be confused with the project's baseline classifier or a final classification result.

### 6.4 Pillow and OpenCV image test

Both members tested Pillow and OpenCV using the same JPEG image from the project's training dataset.

The test image was:

```text
dataset\train\Bottle\00001_jpg.rf.7d50e7e57d941fdcb0df860c2245e619.jpg
```

The reported results were:

| Check | Result |
|---|---|
| Image format | JPEG |
| Width | 416 pixels |
| Height | 416 pixels |
| OpenCV array shape | `(416, 416, 3)` |

Both members reported successful image decoding using Pillow and OpenCV. This confirmed that the image-processing libraries could load the project's dataset image successfully in both environments.

### 6.5 Matplotlib test

Both members reported that a basic Matplotlib plotting test completed successfully. Member 1's plotting test used the non-interactive Agg backend.

This confirmed that Matplotlib could be imported and used for plotting in the new environment. It was not a plot of final classifier performance.

## 7. Package consistency and lock file verification

Both members checked that the installed packages were consistent with the shared dependency set.

### 7.1 `pip check`

Both members reported running:

```powershell
python -m pip check
```

The result was:

```text
No broken requirements found.
```

This indicated that pip did not detect broken package requirements in either environment.

### 7.2 Comparison against `requirements-lock.txt`

Member 1 compared the sorted entries in the lock file with the packages reported by `pip freeze`.

The comparison used:

```powershell
$expected = Get-Content .\requirements-lock.txt |
    Where-Object { $_ -and -not $_.StartsWith('#') } |
    Sort-Object

$actual = python -m pip freeze | Sort-Object

Compare-Object -ReferenceObject $expected -DifferenceObject $actual
```

The comparison produced no output, meaning that no differences were found.

Member 2 independently performed the corresponding comparison on their computer. Their original terminal outputs also showed no differences between the locked package set and the installed packages.

### 7.3 SHA-256 verification

Both members calculated the SHA-256 hash of `requirements-lock.txt` and reported the same result:

```text
99641B5F28BDE103918F0AA1E457E6C1386B6056BA68BF8D85DAFDA5A0A3E11D
```

The matching hash confirms that both members had identical lock file contents.

Together with the package comparisons, this supports that both computers used the same pinned package set.

The hash alone does not prove that the computers have identical hardware or performance. It verifies the file contents; the package comparisons provide the additional evidence about the installed environments.

## 8. Cross-computer verification summary

The following table summarises the results reported and independently checked by both members.

| Verification | Member 1 | Member 2 |
|---|---|---|
| Python 3.13.17, 64-bit | Verified | Verified |
| Project-specific `.venv` | Verified | Verified |
| Shared dependency installation | Verified | Verified |
| TensorFlow and Keras imports | Passed | Passed |
| TensorFlow CPU device and calculation | Passed | Passed |
| scikit-learn SVM smoke test | Passed | Passed |
| JPEG image decoding | Passed | Passed |
| Matplotlib plotting test | Passed | Passed |
| `pip check` | Clean | Clean |
| Lock file/package comparison | No differences | No differences |
| Lock file SHA-256 | Matching hash | Matching hash |

The tests were performed independently on the two computers. Both members reported successful results for the agreed environment checks, including the image-decoding test using the same dataset JPEG.

Member 1's results are supported by the terminal outputs supplied in the project handover. Member 2 has independently confirmed that their original terminal outputs support the results recorded in this document, including the common JPEG filename, dependency comparison and SHA-256 hash. Member 2's full raw terminal log is not reproduced in this document.

## 9. Hardware and platform considerations

Although both computers now use the same Python version and package set, their hardware specifications are different. Member 2's computer has 7.64 GB of recorded RAM, while Member 1's has 11.88 GB.

This difference is relevant when the team starts training and comparing models. The experiments should remain manageable on both computers. Small batch sizes and CPU-friendly experiments are suitable starting points, with resource usage monitored during development.

The TensorFlow checks were carried out using native Windows CPU execution. The team did not configure or verify native Windows GPU acceleration, and no CUDA or WSL2 setup was part of this environment step.

The same dependency versions provide consistency in the software environment, but they do not make the two computers identical in processing speed or available resources.

## 10. Git collaboration and dependency integration

Git and GitHub were used to share, review and merge the environment dependency files.

The dependency work was integrated through two pull requests:

| Pull request | Description | Result |
|---|---|---|
| PR #8 | Add shared Python dependencies | Merged |
| PR #9 | Add resolved Python dependency lock file | Merged |

The recorded merge commits are:

| Pull request | Merge commit |
|---|---|
| PR #8 | `9a985b2` |
| PR #9 | `b2e0aaa` |

Member 1 prepared the dependency files and submitted the changes for review. Member 2 independently reviewed and approved PR #8 and PR #9. The review included checking the six direct dependency versions, NumPy 2.1.3, Keras 3.15.1, the 48 pinned entries and the absence of unintended package changes.

After PR #9 was merged, Member 1 switched back to `main`, pulled the latest changes from `origin/main` and confirmed that the working tree was clean at commit `b2e0aaa`.

The remaining environment documentation work was started on the following branch:

```text
member1/step2-environment-documentation
```

## 11. Member contributions

### Member 1 — Project Lead

Member 1 carried out the main environment preparation and dependency integration work. This included inspecting the original computer environment, recording the hardware and software specifications, installing and verifying Python 3.13.17, preserving the previous package information, archiving the old virtual environment and creating a new project-specific `.venv`.

Member 1 prepared the shared `requirements.txt`, installed and tested the agreed dependencies, generated and checked `requirements-lock.txt`, and completed the package consistency and SHA-256 checks. Member 1 also created and submitted PR #8 and PR #9, synchronised the repository after the merges and started the environment documentation branch.

### Member 2 — Independent verification and review

Member 2 independently inspected the original computer environment, collected the hardware and software specifications, preserved the previous package inventory, archived the old virtual environment and installed and verified Python 3.13.17. Member 2 also created and tested a new project-specific `.venv`.

Member 2 independently installed all 48 pinned packages from `requirements-lock.txt`, performed the package import and runtime tests, tested TensorFlow CPU execution and scikit-learn SVM functionality, and successfully tested Pillow, OpenCV and Matplotlib.

Member 2 also checked dependency consistency using `pip check`, compared the installed packages against the lock file, verified the matching SHA-256 hash and independently reviewed and approved PR #8 and PR #9. The independent checks helped confirm that the shared environment could be installed and used on both computers.

## 12. Limitations of the environment tests

The checks in this step were intended to verify the software environment. They do not represent the final performance evaluation of the office-item classifier.

The following limitations should therefore be noted:

- The TensorFlow calculation was a basic runtime test.
- The SVM predictions `[0, 1]` came from a small smoke test, not the completed office-item classifier.
- The JPEG test confirmed image decoding, not correct classification.
- The Matplotlib test confirmed basic plotting functionality, not the quality of the final evaluation graphs.
- The matching SHA-256 hash confirmed identical lock file contents, not identical hardware or computer performance.
- Native Windows TensorFlow GPU execution was not configured or verified.
- No final classifier accuracy, macro-F1 score or confusion matrix was produced during this environment step.

Training, model comparison and held-out test evaluation remain separate stages of the project.

## 13. Step 2 outcome and current status

Both members have successfully completed the technical environment installation and cross-computer verification. The two computers now use Python 3.13.17, separate project virtual environments and the same pinned dependency set.

The package imports, TensorFlow CPU test, SVM smoke test, image decoding, Matplotlib test and dependency consistency checks were reported as successful. The shared dependency files were also reviewed and merged through PR #8 and PR #9.

The remaining work under Step 2.7 is to complete the documentation update, review it and merge the documentation branch. The current status section in `docs/project-plan.md` must also be reconciled with the completed dependency pull requests and the current environment documentation work. The existing project roadmap should be retained rather than unnecessarily rewritten.

**The technical setup is complete, but Step 2 should not be formally closed until the documentation update has been reviewed and merged.**

Once the documentation work is approved and merged, the team can proceed to:

**Step 3 — Baseline Classifier**

---

## 14. Related project files

The environment setup is supported by the following repository files:

```text
requirements.txt
requirements-lock.txt
docs/project-plan.md
docs/step2-classifier-requirements.md
docs/step2-application-interface.md
docs/step2-system-design-outline.md
docs/step2-environment-setup.md
```

`requirements.txt` records the six direct dependencies, while `requirements-lock.txt` records the complete pinned package set. The other documentation files describe the project plan, classifier requirements, application interface and system design.

---

**Document status:** Environment verification completed; documentation review and integration pending.