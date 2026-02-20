# Sleep Apnea-Hypopnea Detection using ECG Signals and Deep Learning

> **⚠️ PUBLIC REPOSITORY NOTICE**  
> This repository contains **code, notebooks, and documentation only**. The NCKUSH dataset is **NOT included** due to privacy restrictions. All results are presented in aggregated form.

**Internship Documentation**  
**Lab:** WTMH Lab, National Cheng Kung University (NCKU)  
**Duration:** August 2025 - January 2026 (6 months)

> This repository documents work performed during a 6-month internship at WTMH Lab, NCKU.  
> Building upon existing research methodologies for archival and educational purposes.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Research Problem](#research-problem)
- [Methodology](#methodology)
- [Dataset](#dataset)
- [Implementation](#implementation)
- [Results](#results)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Weekly Progress](#weekly-progress)
- [Publications & Presentations](#publications--presentations)
- [Acknowledgments](#acknowledgments)

---

## 🔬 Overview

This repository contains the implementation of frequency range exploration for sleep apnea-hypopnea detection from single-lead ECG signals. Building upon the **YOLOv8-based event detection framework** by Nipattanon & Lin (2025), this project explores **8 different frequency ranges**—including 4 predefined ranges and 4 learned via SincNet—to evaluate their impact on apnea detection performance.

### Key Highlights
- ✅ **50 subjects** from NCKUSH dataset (LOSO + 5-fold CV)
- ✅ **8 frequency ranges explored:** 4 manual + 4 SincNet-learned bands
- ✅ **Building on** Nipattanon & Lin (2025) YOLOv8 Nano methodology
- ✅ **Continuous Wavelet Transform** (CWT) for time-frequency representation
- ✅ **YOLOv8 Nano** object detection for temporal event localization
- ✅ **SincNet learnable filters** - validated that fixed 0.8-10 Hz remains optimal
- ✅ **Comprehensive evaluation:** LOSO + subject-wise 5-fold cross-validation
- ✅ **Key finding:** 0.8-10 Hz (Lin et al. 2022) provides most stable performance

---

## 🎯 Research Problem

**Sleep Apnea-Hypopnea Syndrome (SAHS)** is a common sleep disorder affecting millions worldwide. Traditional diagnosis relies on polysomnography (PSG), which is:
- Expensive and time-consuming
- Requires overnight hospital stay
- Involves multiple sensors

**Our Approach:** Building on established YOLOv8 framework with frequency exploration:
- **Base methodology:** Nipattanon & Lin (2025) event-based detection
- **Frequency exploration:** 8 ranges tested (4 predefined + 4 SincNet-learned)
- **Time-frequency analysis:** Continuous Wavelet Transform (CWT)
- **Detection:** YOLOv8 Nano object detection on spectrograms
- **Validation:** Compare learned vs. predefined frequency ranges
- **Result:** 0.8-10 Hz (Lin et al. 2022) remains most stable

---

## 🔧 Methodology

### Pipeline Overview

```
ECG Signal (EDF Format from NCKUSH)
    ↓
[1] Preprocessing (135s segments, 27,000 samples @ 200Hz)
    - Segmentation from raw recordings
    - Normalization
    ↓
[2] Dual Pathway Exploration:

    Path A: SincNet (1D CNN)
    → 8 learnable band-pass filters
    → Extract frequency characteristics
    → 4 learned frequency bands
    
    Path B: Continuous Wavelet Transform (CWT)
    → Time-frequency spectrograms
    → 4 predefined frequency ranges tested
    → Image size: 640×1280 pixels
    ↓
[3] YOLOv8 Nano Object Detection
    - Input: CWT spectrograms
    - Classes: Normal (N) vs Apnea/Hypopnea (AH)
    - Event-based temporal localization
    ↓
[4] Comprehensive Evaluation
    - LOSO Cross-Validation (50 subjects)
    - Subject-wise 5-fold CV
    - Compare 8 frequency ranges
    ↓
[5] Performance Analysis
    - Mean Average Precision (mAP@0.5)
    - Per-subject and per-class metrics
    - Stability analysis across ranges
```

### Technical Details

#### 1. **Preprocessing** ([preprocessing.ipynb](preprocessing.ipynb))
- Load ECG from EDF files (channel 9)
- Apply 4th-order Butterworth high-pass filter (0.5 Hz cutoff)
- Z-score normalization: `(x - μ) / σ`
- Save preprocessed signals as `.npy` files

#### 2. **Spectrogram Generation** ([A_generate_AHxN_fin.ipynb](A_generate_AHxN_fin.ipynb))
- **Continuous Wavelet Transform (CWT)** for time-frequency representation
- **8 Frequency Ranges Explored:**

  **Predefined Ranges (4):**
  1. **0.8-10 Hz** - Baseline from Lin et al. (2022) ✅ Most stable
  2. **0.1-50 Hz** - Wider frequency exploration
  3. **8-50 Hz** - Higher frequencies only
  4. **0.001-0.08 Hz** - Very low frequencies (poor performance)
  
  **SincNet Learned Ranges (4):**
  5. **0.50-6.52 Hz** - Filter 0 learned from training
  6. **5.15-10.26 Hz** - Filter 1 learned from training
  7. **9.31-14.22 Hz** - Filter 2 learned from training
  8. **13.56-18.21 Hz** - Filter 3 learned from training

- **Parameters:**
  - Segment duration: 90 seconds (no overlap)
  - Image output: 640×1280 pixels
  - Colormap: Inferno
- **Annotations:** Parse XML labels for Apnea/Hypopnea events
- **Output:** PNG spectrograms + YOLO format labels (.txt)

#### 3. **LOSO Cross-Validation Setup** ([A_generate_AHxN_fin.ipynb](A_generate_AHxN_fin.ipynb))
- **5-Fold Subject-Wise CV** for initial testing
- **50-Fold LOSO** for final evaluation
- Automatic YAML configuration generation
- Train/Valid/Test split organization

#### 4. **YOLOv8 Training** ([s1to5_LOSO_yolov8_...ipynb](s1to5_LOSO_yolov8_fine_tuning_90s_relabel_SGDbs32_adjustHW_rectF_yaml_and_pt.ipynb))
- **Model:** YOLOv8-nano
- **Hyperparameters:**
  - Epochs: 100 (with early stopping patience=10)
  - Batch size: 32
  - Learning rate: 0.001
  - Optimizer: SGD (momentum=0.9, weight_decay=0.0002)
  - Warmup: 3 epochs
  - Image size: 640×1280
- **Two initialization strategies:**
  - Pre-trained weights (yolov8n.pt)
  - From YAML architecture (yolov8n_ori.yaml)

#### 5. **SincNet Frequency Learning**

**SincNet 1D CNN ([sincnet_learning_proof.py](sincnet_learning_proof.py), [main_train.ipynb](main_train.ipynb))**
- **Architecture:** 8 learnable band-pass filters (SincConv layer)
- **Purpose:** Discover optimal frequency bands from raw ECG
- **Training:** 50 epochs on 135-second ECG segments (27,000 samples @ 200Hz)
- **Dataset Split:** 70% train / 14% validation / 16% test (subject-wise)

**Learned Filter Results (Page 14 of presentation):**

| Filter | Initial Low (Hz) | Trained Low (Hz) | Initial High (Hz) | Trained High (Hz) |
|--------|-----------------|-----------------|------------------|------------------|
| Filter 0 | 1.00 | **0.50** | 6.00 | **6.52** |
| Filter 1 | 5.21 | **5.15** | 10.21 | **10.26** |
| Filter 2 | 9.43 | **9.31** | 14.43 | **14.22** |
| Filter 3 | 13.64 | **13.56** | 18.64 | **18.21** |
| Filter 4 | 17.86 | 17.49 | 22.86 | 22.74 |
| Filter 5 | 22.07 | 22.05 | 27.07 | 27.30 |
| Filter 6 | 26.29 | 26.11 | 31.29 | 31.37 |
| Filter 7 | 30.50 | 31.24 | 35.50 | 36.30 |

**Key Findings:**
- ✅ SincNet achieved **84.60% accuracy** on test set
- ⚠️ Learned bands showed **comparable but not superior** performance to 0.8-10 Hz
- ✅ **Validates Lin et al. (2022)** predefined range as optimal
- 📊 Filter 0-1 converged near the 0.8-10 Hz range

**1D CNN Baseline ([main_train.ipynb](main_train.ipynb))**
- Direct raw ECG processing
- Comparison with spectrogram-based approach

---

## 📊 Dataset

### ⚠️ Data Privacy Notice

**IMPORTANT:** The NCKUSH (National Cheng Kung University Hospital Sleep Center) dataset used in this research is **NOT publicly available** and contains sensitive patient information.

- 🔒 **Dataset is NOT included** in this repository
- 🚫 **Do NOT upload** any EDF, XML, or patient data files
- ✅ Only code, documentation, and aggregated results are shared
- 📋 Data access requires IRB approval from NCKUHSC

### NCKUSH Sleep Dataset
- **Total subjects:** 50 (private dataset)
- **Source:** National Cheng Kung University Hospital Sleep Center
- **Format:** EDF (ECG) + XML (annotations)
- **Access:** Restricted - Contact NCKUHSC for data use inquiries
- **Severity distribution:**
  - Severe: 18 subjects
  - Moderate: 10 subjects
  - Mild: 13 subjects
  - No apnea: 9 subjects

### Data Organization
```
Dataset/
├── s1/ (subject 1 spectrograms + labels)
├── s2/
...
├── s50/
```

### Annotation Format (YOLO)
```
<class> <x_center> <y_center> <width> <height>
```
- Class 0: Normal (N)
- Class 1: Apnea/Hypopnea (AH)

---

## 💻 Implementation

### Core Notebooks

1. **[preprocessing.ipynb](preprocessing.ipynb)**
   - Load and preprocess ECG signals from EDF files
   - Apply filtering and normalization
   - Save to `preprocessed_ecg/` directory

2. **[A_generate_AHxN_fin.ipynb](A_generate_AHxN_fin.ipynb)**
   - Generate Morlet wavelet spectrograms
   - Create YOLO format annotations
   - Organize LOSO cross-validation folds
   - Generate YAML configuration files

3. **[s1to5_LOSO_yolov8_...ipynb](s1to5_LOSO_yolov8_fine_tuning_90s_relabel_SGDbs32_adjustHW_rectF_yaml_and_pt.ipynb)**
   - YOLOv8 training for subjects 1-5 (LOSO)
   - Both pre-trained and from-scratch experiments
   - Complete training pipeline with hyperparameter tuning

4. **[main_train.ipynb](main_train.ipynb)**
   - 1D CNN baseline model
   - Direct signal processing approach

### Additional Notebooks
- **[preview.ipynb](preview.ipynb)**: Dataset visualization and exploration
- **[sincnet_learning_proof.py](sincnet_learning_proof.py)**: SincNet learnable filter experiments
  - 8 band-pass filters with learned cutoff frequencies
  - 84.60% test accuracy, 84.76% validation accuracy
  - Finding: Comparable to but not superior than 0.8-10 Hz baseline

---

## 📈 Results

### Model Checkpoints
Trained models are saved in [checkpoint_epoch/](checkpoint_epoch/):
- Epoch-wise checkpoints (1, 5, 10, ..., 50)
- Best accuracy model: `model_best_acc.pt`
- Best overall model: `model_best.pt`

### Performance Summary

Results from comprehensive evaluation:

**SincNet 1D CNN (Classification Task):**
- Test Accuracy: **84.60%**
- Class 0 (Normal): Precision 87.28%, Recall 84.87%, F1 86.06%
- Class 1 (Apnea): Precision 81.40%, Recall 84.26%, F1 82.81%

**YOLOv8 Nano (Object Detection Task - Subject-wise 5-Fold CV):**

Comparison of frequency ranges (mAP@0.5):

| Fold | 0.8-10 Hz (Baseline) | 0.1-50 Hz | 8-50 Hz | 0.001-0.08 Hz | SincNet Filters |
|------|---------------------|-----------|---------|--------------|----------------|
| 1 | **0.56** | 0.52 | 0.54 | 0.32 | 0.50-0.54 |
| 2 | **0.56** | 0.51 | 0.49 | 0.34 | 0.49-0.51 |
| 3 | **0.68** | 0.66 | 0.68 | 0.48 | 0.63-0.66 |
| 4 | **0.84** | 0.81 | 0.80 | 0.69 | 0.79-0.80 |
| 5 | **0.72** | 0.69 | 0.61 | 0.56 | 0.69-0.71 |

**Key Observations:**
- ✅ **0.8-10 Hz consistently most stable** across all folds
- ⚠️ Wider range (0.1-50 Hz) improved **46% of subjects** in LOSO but not consistent
- 📉 Very low frequency (0.001-0.08 Hz) performed poorly across all metrics
- 🔄 SincNet-learned bands: comparable to predefined ranges but no superior performance

**LOSO Cross-Validation Insights:**
- Some subjects showed +29% improvement with 0.1-50 Hz (e.g., subject 19)
- Performance improvements were **subject-specific, not generalizable**
- 0.8-10 Hz baseline maintained best **overall stability**

---

## 📁 Repository Structure

```
1DCNN/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
│
├── notebooks/                         # Main implementation notebooks
│   ├── preprocessing.ipynb
│   ├── A_generate_AHxN_fin.ipynb
│   ├── main_train.ipynb
│   ├── s1to5_LOSO_yolov8_*.ipynb
│   └── preview.ipynb
│
├── src/                               # Source code modules
│   ├── preprocessing.py               # ECG preprocessing functions
│   ├── spectrogram.py                 # Morlet wavelet transform
│   ├── dataset.py                     # Dataset utilities
│   └── sincnet_learning_proof.py      # SincNet experiments
│
├── config/                            # Configuration files
│   └── training_config.yaml           # Training hyperparameters
│
├── data/                              # Data directory (not tracked)
│   ├── raw/                           # Original EDF + XML files
│   ├── preprocessed_ecg/              # Processed ECG signals (.npy)
│   └── spectrograms/                  # Generated spectrograms + labels
│
├── models/                            # Model architectures & checkpoints
│   ├── checkpoint_epoch/              # Training checkpoints
│   │   ├── model_best.pt
│   │   └── model_best_acc.pt
│   └── yolov8n_ori.yaml              # YOLOv8 architecture config
│
├── results/                           # Experimental results
│   ├── model_results_summary.csv
│   ├── training_history.csv
│   ├── cnn_architecture_table.csv
│   ├── cnn_weight_statistics_table.csv
│   ├── learned_frequency_bands.csv
│   ├── sincconv_filter_table.csv
│   ├── sincnet_epoch_bands.csv
│   └── segment_labels.csv
│
├── docs/                              # Documentation
│   ├── Draft_Final_Presentation.pdf   # Final presentation
│   ├── weekly_reports/                # Weekly progress reports (PPT)
│   └── methodology.md                 # Detailed methodology
│
└── figures/                           # Visualization outputs
    ├── spectrograms/
    └── results_plots/
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (recommended for YOLOv8 training)
- Google Colab (if running on cloud)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd 1DCNN
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Ultralytics (YOLOv8)**
```bash
pip install ultralytics
```

4. **Install additional packages**
```bash
pip install pyedflib  # For EDF file reading
```

### Dependencies
```
numpy
scipy
matplotlib
torch
torchvision
ultralytics
pyedflib
opencv-python
pandas
pyyaml
scikit-learn
seaborn
```

---

## 🎮 Usage

### 1. Preprocess ECG Signals
```python
# Run preprocessing.ipynb
# Input: Raw EDF files
# Output: preprocessed_ecg/*.npy files
```

### 2. Generate Spectrograms & Annotations
```python
# Run A_generate_AHxN_fin.ipynb
# Configure subjects list and parameters
# Output: Spectrogram images + YOLO labels
```

### 3. Setup LOSO Cross-Validation
```python
# Run LOSO setup section in A_generate_AHxN_fin.ipynb
# Generates fold directories and YAML configs
```

### 4. Train YOLOv8 Models
```python
# Run s1to5_LOSO_yolov8_*.ipynb
# Choose: Pre-trained (yolov8n.pt) or From-scratch (YAML)
# Adjust hyperparameters as needed
```

### 5. Evaluate Results
```python
# Check results/ directory for performance metrics
# Analyze training_history.csv and model_results_summary.csv
```

---

## 📅 Weekly Progress

During the 6-month internship (August 2025 - January 2026), weekly progress was documented in PowerPoint presentations:

📂 **[Weekly Reports (Google Drive)](https://drive.google.com/drive/folders/1M7JNwbry5GhsMVI0oxU5HKJM2K2PDxaz?usp=sharing)**

*Weekly presentations document progress, experiments, challenges, and findings throughout the internship period.*

### Timeline Highlights

**Month 1 (August):** Literature review, dataset exploration, frequency range investigation

**Month 2 (September):** Preprocessing pipeline, Morlet wavelet implementation

**Month 3 (October):** Spectrogram generation, YOLOv8 integration

**Month 4 (November):** SincNet experimentation, frequency learning exploration

**Month 5 (December):** LOSO cross-validation, full 50-subject evaluation

**Month 6 (January):** Result analysis, final presentation preparation

---

## 📄 Publications & Presentations

### Final Presentation
- **[Draft Final Presentation [Autosaved].pdf](docs/Draft_Final_Presentation.pdf)**
- Presented: January 2026

### Potential Publications
- *In preparation*: "Sleep Apnea Detection from Single-Lead ECG using YOLOv8 and Morlet Wavelet Transform"

---

## � References

### Core Methodology

1. **Nipattanon, P., & Lin, C.-W. (2025).** "Event-based Detection of Obstructive Sleep Apnea via YOLOv8 Nano and ECG Spectrograms: Integration with Home Sleep Apnea Test and Edge Computing." *2025 IEEE Conference on Computational Intelligence in Bioinformatics and Computational Biology (CIBCB)*, Tainan, Taiwan, pp. 1-7. doi: 10.1109/CIBCB66090.2025.11177074
   - 🎯 **Base methodology for this project**
   - YOLOv8 Nano architecture and event-based detection framework
   - Continuous Wavelet Transform for spectrogram generation

2. **Lin, C.-Y., Wang, Y.-W., Setiawan, F., Trang, N. T. H., & Lin, C.-W. (2022).** "Sleep Apnea Classification Algorithm Development Using a Machine-Learning Framework and Bag-of-Features Derived from Electrocardiogram Spectrograms." *Journal of Clinical Medicine*, 11(1), 192. https://doi.org/10.3390/jcm11010192
   - 📊 **Source of 0.8-10 Hz frequency range**
   - Established optimal frequency bands for ECG-based apnea detection

### SincNet and Learnable Filters

3. **Ravanelli, M., & Bengio, Y. (2018).** "Speaker Recognition from Raw Waveform with SincNet." *2018 IEEE Spoken Language Technology Workshop (SLT)*, pp. 1021-1028. doi: 10.1109/SLT.2018.8639585
   - Original SincNet architecture with learnable band-pass filters

4. **Śmigiel, S., Pałczyński, K., & Ledziński, D. (2021).** "ECG Signal Classification Using Deep Learning Techniques Based on the PTB-XL Dataset." *Entropy*, 23(9), 1121. https://doi.org/10.3390/e23091121
   - Application of sinc-based filters to ECG analysis
   - Interpretability and optimization of CNN with SINC-Convolution

### Sleep Apnea and ECG Analysis

5. **Penzel, T., et al. (2016).** "Modulations of Heart Rate, ECG, and Cardio-Respiratory Coupling Observed in Polysomnography." *Frontiers in Physiology*, 7:460. doi: 10.3389/fphys.2016.00460
   - Physiological basis for ECG-based apnea detection

6. **Wang, Y., Liu, Q., Min, F., & Wang, H. (2026).** "PSG-MAE: Robust Multitask Sleep Event Monitoring Using Multichannel PSG Reconstruction and Inter-Channel Contrastive Learning." *IEEE Transactions on Neural Systems and Rehabilitation Engineering*, 34, pp. 274-286.
   - Modern approaches to sleep disorder detection

---

## �🙏 Acknowledgments

This work was performed during an internship at **WTMH Lab, National Cheng Kung University (NCKU)**, Taiwan.

- WTMH Lab for supervision and guidance
- NCKUSH for dataset access
- NCKU for computational resources

---

## 📧 Contact

For inquiries about this work:
- Contact WTMH Lab, NCKU

---

## 📜 License

This repository documents internship work at NCKU WTMH Lab.  
For any usage or inquiries, please contact WTMH Lab, NCKU.

---

**Last Updated:** January 2026
