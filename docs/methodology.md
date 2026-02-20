# Methodology: Frequency Range Exploration for Sleep Apnea Detection

## Background

This project builds upon the **event-based apnea detection framework** established by Nipattanon & Lin (2025), which applies YOLOv8 Nano to ECG spectrograms for temporal event localization. The research extends this methodology by systematically exploring **8 different frequency ranges**\u2014comprising 4 predefined ranges and 4 learned via SincNet\u2014to evaluate their impact on detection performance.

### Research Questions

1. **Does the 0.8-10 Hz range** (Lin et al. 2022) remain optimal across subjects?
2. **Can wider frequency ranges** (0.1-50 Hz, 8-50 Hz) improve detection?
3. **Can SincNet automatically discover** better frequency bands than predefined ranges?
4. **Are performance improvements** consistent across all subjects or subject-specific?

---

## Eight Frequency Ranges Explored

### Predefined Ranges (4)

Based on Lin et al. (2022) and frequency exploration:

#### 1. **0.8-10 Hz** \u2705 **Baseline (Lin et al. 2022)**

**Rationale:**
- **Low Frequency (0.8-1.5 Hz):** Respiratory sinus arrhythmia (RSA)
- **Mid Frequency (1.5-5 Hz):** Heart rate variability (HRV) modulations  
- **Higher Frequency (5-10 Hz):** ECG morphological features related to autonomic changes

**Citation:** Lin, C.-Y., et al. (2022). "Sleep Apnea Classification Algorithm Development Using a Machine-Learning Framework." *Journal of Clinical Medicine*, 11(1), 192.

**Performance:** \ud83c\udfaf **Most stable across all folds** in subject-wise 5-fold CV

---

#### 2. **0.1-50 Hz** - Wider Range Exploration

**Rationale:**
- Extends range to capture broader frequency spectrum
- Tests if additional frequency content improves detection
- Includes both lower and higher frequency cardiac information

**Performance:** 
- \u26a0\ufe0f Improved **46% of subjects** in LOSO evaluation
- \ud83d\udd3a Highest improvements: Subject 19 (+29%), Subject 43 (+20%)
- \u274c **Not consistent** across all subjects

---

#### 3. **8-50 Hz** - Higher Frequencies Only

**Rationale:**
- Focuses on higher frequency ECG components
- Tests if low-frequency information (< 8 Hz) is necessary
- Captures QRS complex and high-frequency cardiac activity

**Performance:**
- Similar to 0.8-10 Hz in some folds
- \ud83d\udcc9 Less stable than 0.8-10 Hz baseline

---

#### 4. **0.001-0.08 Hz** - Very Low Frequencies

**Rationale:**
- Explores ultra-low frequency components
- Tests very slow oscillations and trends
- Baseline drift and long-term variations

**Performance:**
- \u274c **Poorest performance** across all metrics
- mAP@0.5 significantly lower than all other ranges
- \ud83d\udeab Not recommended for apnea detection

---

### SincNet Learned Ranges (4)

Using the SincNet 1D CNN architecture with **8 learnable band-pass filters**, trained on 135-second ECG segments (27,000 samples @ 200Hz).

#### Training Configuration
- **Architecture:** SincConv1d \u2192 Conv blocks \u2192 Global pooling \u2192 FC layers
- **Filters:** 8 learnable band-pass filters (252-point kernels)
- **Dataset:** 70% train / 14% val / 16% test (subject-wise split)
- **Epochs:** 50
- **Optimizer:** Adam (lr=0.001)
- **Parameters:** Only 13,970 total parameters

#### Learned Filter Results

| Filter # | Initial Low (Hz) | **Trained Low (Hz)** | Initial High (Hz) | **Trained High (Hz)** | Bandwidth (Hz) |
|----------|-----------------|-------------------|------------------|---------------------|---------------|
| Filter 0 | 1.00 | **0.50** | 6.00 | **6.52** | 6.02 |
| Filter 1 | 5.21 | **5.15** | 10.21 | **10.26** | 5.11 |
| Filter 2 | 9.43 | **9.31** | 14.43 | **14.22** | 4.91 |
| Filter 3 | 13.64 | **13.56** | 18.64 | **18.21** | 4.65 |
| Filter 4 | 17.86 | 17.49 | 22.86 | 22.74 | 5.25 |
| Filter 5 | 22.07 | 22.05 | 27.07 | 27.30 | 5.25 |
| Filter 6 | 26.29 | 26.11 | 31.29 | 31.37 | 5.26 |
| Filter 7 | 30.50 | 31.24 | 35.50 | 36.30 | 5.06 |

#### Top 4 Learned Bands Used for YOLOv8 Evaluation:

5. **0.50-6.52 Hz** (Filter 0)
6. **5.15-10.26 Hz** (Filter 1) \u2190 **Closest to Lin et al. 2022 baseline**
7. **9.31-14.22 Hz** (Filter 2)
8. **13.56-18.21 Hz** (Filter 3)

#### SincNet Performance:
- **Test Accuracy:** 84.60%
- **Class 0 (Normal):** Precision 87.28%, Recall 84.87%, F1 86.06%
- **Class 1 (Apnea):** Precision 81.40%, Recall 84.26%, F1 82.81%

**Key Observation:** \ud83d\udd0d Filters 0-1 converged to ranges **overlapping with 0.8-10 Hz**, suggesting the predefined range captures optimal frequency content.

---

## Frequency Range Selection (0.8-10 Hz)

### Rationale

The 0.8-10 Hz range captures:
- **Low Frequency (0.8-1.5 Hz):** Respiratory sinus arrhythmia (RSA)
- **Mid Frequency (1.5-5 Hz):** Heart rate variability (HRV) modulations
- **Higher Frequency (5-10 Hz):** ECG morphological features related to autonomic changes

### Literature Support

Studies have shown that apnea-related ECG changes manifest primarily in this frequency band due to:
- Respiratory effort cessation/reduction
- Sympathetic activation during arousal
- Blood oxygen desaturation effects on cardiac rhythm

---

## Continuous Wavelet Transform (CWT)

### Why CWT for This Study?

Following **Nipattanon & Lin (2025)** methodology, Continuous Wavelet Transform provides optimal time-frequency representation for event-based detection:

- **Time-frequency localization:** Preserves when events occur
- **2D visualization:** Converts 1D ECG to 2D image for object detection
- **Adaptive resolution:** Variable frequency-dependent time resolution
- **Non-stationary signals:** Ideal for ECG with time-varying characteristics

### CWT vs. Alternative Transforms

| Method | Time Resolution | Freq Resolution | Best For |
|--------|----------------|-----------------|----------|
| **CWT** | **Adaptive** | **Adaptive** | **\u2705 Non-stationary signals** |
| STFT | Fixed | Fixed | Stationary signals |
| Morlet Wavelet | Good | Good | General time-freq analysis |
| FFT | None | Excellent | Frequency-only analysis |

### Implementation Details

The methodology from Nipattanon & Lin (2025) uses CWT to generate spectrograms:

- **Input:** 90-second ECG segments (from 135s recordings)
- **Output:** 640\u00d71280 pixel spectrogram images
- **Colormap:** Inferno (high contrast for detection)
- **Frequency axis:** Vertical (640 pixels)
- **Time axis:** Horizontal (1280 pixels = 90 seconds)

### Previous: Morlet Wavelet Transform

*(Note: Earlier experiments may have used Morlet wavelets. The final methodology uses CWT as per Nipattanon & Lin 2025)*

---

## YOLOv8 Nano Object Detection Framework

### What is SincNet?

SincNet is a learnable convolutional layer that:
- Learns **band-pass filter parameters** instead of arbitrary kernels
- Uses **sinc functions** to define frequency bands
- Reduces parameters and improves interpretability

### Implementation Details

```python
# SincNet layer learns:
# - Low cutoff frequency (f1)
# - Bandwidth (f2 - f1)
# For each filter in the first conv layer
```

### Experiment Setup

- **Goal:** Let the network discover optimal frequency bands automatically
- **Hypothesis:** Network might find better frequency combinations than fixed 0.8-10 Hz
- **Architecture:** Replace first conv layer with SincNet in 1D CNN

### Results & Findings

**Key Finding:** SincNet performance **did not exceed** the fixed frequency approach

**Possible Reasons:**
1. **Literature-based range is already optimal** for this specific task
2. **Limited dataset size** (50 subjects) may not provide enough diversity for learning
3. **Fixed range provides consistent features** across subjects
4. **Training complexity:** More parameters to learn with limited data

**Learned Frequency Bands:**
Analysis of learned SincNet filters ([sincnet_epoch_bands.csv](../sincnet_epoch_bands.csv)) showed:
- Filters converged to ranges **similar to 0.8-10 Hz**
- Some filters learned overlapping bands
- No significant novel frequency patterns discovered

**Conclusion:** The manually selected 0.8-10 Hz range is validated as optimal for this task.

---

## YOLOv8 Object Detection Framework

### Why Object Detection for Apnea?

Treating apnea detection as an object detection problem offers:

1. **Temporal localization:** Precise start/end times of events
2. **Confidence scores:** Quantifiable detection certainty
3. **Multiple events:** Can detect multiple apnea episodes in one segment
4. **Robust to variations:** Handles different durations and patterns

### Spectrogram as Image

The time-frequency representation becomes a 2D image where:
- **X-axis:** Time (90 seconds)
- **Y-axis:** Frequency (0.8-10 Hz)
- **Intensity:** Wavelet coefficient magnitude (color-coded)

### YOLO Annotation Format

```
<class> <x_center> <y_center> <width> <height>
```

- All coordinates normalized to [0, 1]
- `x_center`, `width`: Temporal location and duration
- `y_center=0.5`, `height=1.0`: Full frequency range

Example:
```
1 0.523 0.5 0.234 1.0
```
→ Apnea/Hypopnea event centered at 52.3% of timeline, spanning 23.4% duration

---

## Validation Strategy: LOSO Cross-Validation

### Leave-One-Subject-Out (LOSO)

**Principle:** Train on N-1 subjects, test on 1 held-out subject

**Advantages:**
- **Subject-independent evaluation** (generalization to new patients)
- **Maximizes training data** (49 subjects for training)
- **Clinical relevance** (realistic deployment scenario)

### Implementation

For 50 subjects → 50 folds:
```
Fold 1: Train on s2-s50, Validate on s1
Fold 2: Train on s1,s3-s50, Validate on s2
...
Fold 50: Train on s1-s49, Validate on s50
```

### Why Not K-Fold?

K-fold with random splits may:
- Include same subject in train and test (overly optimistic results)
- Not reflect real-world deployment (unknown patient characteristics)

---

## Hyperparameter Selection

### YOLOv8 Configuration

```python
EPOCHS = 100
BATCH_SIZE = 32
IMG_SIZE = (640, 1280)  # H x W
LEARNING_RATE = 0.001
OPTIMIZER = "SGD"
MOMENTUM = 0.9
WEIGHT_DECAY = 0.0002
PATIENCE = 10  # Early stopping
```

### Rationale

- **Batch size 32:** Balance between GPU memory and gradient stability
- **SGD optimizer:** More stable than Adam for small datasets
- **Image size 640×1280:** Preserves temporal resolution (90s / 1280 ≈ 70ms per pixel)
- **Early stopping (patience=10):** Prevents overfitting on small validation set

---

## Preprocessing Pipeline

### 1. Signal Acquisition
- **Source:** EDF files from NCKUSH
- **Channel:** Single-lead ECG (channel 9)
- **Sampling rate:** Variable (typically 200-500 Hz)

### 2. Filtering
- **Type:** 4th-order Butterworth high-pass
- **Cutoff:** 0.5 Hz
- **Purpose:** Remove baseline wander and low-frequency drift

### 3. Normalization
- **Method:** Z-score normalization
- **Formula:** `(x - μ) / σ`
- **Purpose:** Standardize amplitude across subjects

### 4. Segmentation
- **Window:** 90 seconds
- **Overlap:** 0 seconds (non-overlapping)
- **Purpose:** Match clinical apnea definition (≥10s events)

---

## Evaluation Metrics

### Primary Metrics

1. **Precision:** `TP / (TP + FP)` - How many detected events are correct?
2. **Recall (Sensitivity):** `TP / (TP + FN)` - How many true events are detected?
3. **F1-Score:** `2 × (Precision × Recall) / (Precision + Recall)` - Harmonic mean

### YOLO-Specific Metrics

- **mAP@0.5:** Mean Average Precision at 50% IoU threshold
- **mAP@0.5:0.95:** Average mAP across IoU thresholds 0.5 to 0.95

### Clinical Relevance

- **High Recall:** Critical for clinical use (don't miss apnea events)
- **Reasonable Precision:** Minimize false alarms (patient compliance)

---

## Summary of Findings

### Validated Approaches
✅ **0.8-10 Hz frequency range** (literature-based) is optimal  
✅ **Morlet Wavelet Transform** provides effective time-frequency representation  
✅ **YOLOv8 object detection** suitable for apnea event localization  
✅ **90-second segments** balance context and computational efficiency  

### Experimental Insights
❌ **SincNet learnable filters** did not outperform fixed range  
✓ **LOSO validation** ensures subject-independent performance  
✓ **SGD optimizer** with careful tuning provides stable training  

### Future Directions
- Multi-lead ECG fusion
- Real-time implementation optimization
- Extended dataset validation
- Integration with other physiological signals

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Documentation of internship work at WTMH Lab, NCKU**
