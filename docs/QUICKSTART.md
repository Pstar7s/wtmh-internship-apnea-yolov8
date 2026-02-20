# Quick Start Guide

This guide helps you get started with the Sleep Apnea Detection pipeline.

---

## Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended)
- At least 16GB RAM
- ~100GB storage for full dataset

---

## Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd 1DCNN
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Ultralytics (YOLOv8)
```bash
pip install ultralytics
```

---

## Dataset Setup

### 1. Obtain NCKUSH Dataset
- Place EDF files in: `data/raw/EDF_XML/`
- Place XML annotations in: `data/raw/EDF_XML/`

Expected structure:
```
data/raw/EDF_XML/
├── s1.edf
├── s1_re.XML
├── s2.edf
├── s2_re.XML
...
├── s50.edf
└── s50_re.XML
```

---

## Pipeline Execution

### Step 1: Preprocess ECG Signals

Open [preprocessing.ipynb](../preprocessing.ipynb) and run all cells.

**What it does:**
- Loads ECG from EDF files
- Applies high-pass filtering (0.5 Hz)
- Z-score normalization
- Saves to `preprocessed_ecg/*.npy`

**Output:**
```
preprocessed_ecg/
├── s1.npy
├── s2.npy
...
└── s50.npy
```

---

### Step 2: Generate Spectrograms

Open [A_generate_AHxN_fin.ipynb](../A_generate_AHxN_fin.ipynb).

#### 2a. Generate Spectrograms for Single Subject

Modify the `subjects` list:
```python
subjects = ['s1']  # Test with one subject first
```

Run the spectrogram generation section.

**What it does:**
- Applies Morlet Wavelet Transform (0.8-10 Hz)
- Creates 90-second segments
- Generates PNG images (640×1280)
- Creates YOLO format labels (.txt)

**Output:**
```
donothing_640_1280_s1_90s/
├── s1_segment_00000_to_00090_spectrogram.png
├── s1_segment_00000_to_00090_spectrogram.txt
├── s1_segment_00090_to_00180_spectrogram.png
├── s1_segment_00090_to_00180_spectrogram.txt
...
```

#### 2b. Generate for All Subjects

Update subjects list:
```python
subjects = [f's{i}' for i in range(1, 51)]  # All 50 subjects
```

⚠️ **Warning:** This will take several hours and generate ~100GB of data.

---

### Step 3: Organize LOSO Cross-Validation

In [A_generate_AHxN_fin.ipynb](../A_generate_AHxN_fin.ipynb), run the LOSO setup section.

**Configuration:**
```python
start_fold = 1
end_fold = 5  # Process folds 1-5
```

**What it does:**
- Creates fold directories (e.g., `re_loso_fold_s01_90s/`)
- Copies appropriate train/valid spectrograms
- Generates YAML config files

**Output structure:**
```
re_loso_fold_s01_90s/
├── train/
│   ├── images/
│   └── labels/
└── valid/
    ├── images/
    └── labels/
```

---

### Step 4: Train YOLOv8 Models

#### Option A: Google Colab (Recommended)

1. Upload [s1to5_LOSO_yolov8_*.ipynb](../s1to5_LOSO_yolov8_fine_tuning_90s_relabel_SGDbs32_adjustHW_rectF_yaml_and_pt.ipynb) to Colab
2. Mount Google Drive with dataset
3. Run cells sequentially for each fold

#### Option B: Local Training

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Pre-trained weights
model.train(
    data="re_loso_fold_s01_90s.yaml",
    epochs=100,
    batch=32,
    imgsz=(640, 1280),
    optimizer="SGD",
    name="LOSO_s01"
)
```

**Training time:** ~2-4 hours per fold on GPU

---

### Step 5: Evaluate Results

After training, check:
```
runs/detect/LOSO_s01/
├── weights/
│   ├── best.pt
│   └── last.pt
├── results.png
├── confusion_matrix.png
└── results.csv
```

**Key metrics:**
- Precision, Recall, F1-Score
- mAP@0.5, mAP@0.5:0.95
- Training curves

---

## Testing on New Data

### 1. Prepare Test Spectrogram
```python
# Generate spectrogram from new ECG
# (follow Step 2 pipeline)
```

### 2. Run Inference
```python
from ultralytics import YOLO

model = YOLO("runs/detect/LOSO_s01/weights/best.pt")
results = model.predict(
    source="path/to/test_spectrogram.png",
    imgsz=(640, 1280),
    conf=0.5
)
```

### 3. Parse Results
```python
for result in results:
    boxes = result.boxes
    for box in boxes:
        cls = int(box.cls[0])  # 0: Normal, 1: Apnea/Hypopnea
        conf = float(box.conf[0])
        x_center = float(box.xywhn[0][0])  # Normalized coordinates
        width = float(box.xywhn[0][2])
        
        # Convert to time
        start_time = (x_center - width/2) * 90  # seconds
        end_time = (x_center + width/2) * 90
        
        print(f"Detected: {'AH' if cls==1 else 'N'}, "
              f"Confidence: {conf:.2f}, "
              f"Time: {start_time:.1f}-{end_time:.1f}s")
```

---

## Troubleshooting

### Out of Memory (GPU)
- Reduce batch size: `batch=16` or `batch=8`
- Use smaller image size: `imgsz=(320, 640)`

### Training Not Converging
- Check learning rate: try `lr0=0.0001` (lower)
- Increase warmup epochs: `warmup_epochs=5`
- Verify data loading: check YAML paths are correct

### Low Performance
- Check data quality: visualize spectrograms
- Verify annotations: ensure XML parsing is correct
- Balance dataset: check class distribution

### Import Errors
```bash
pip install --upgrade ultralytics torch torchvision
```

---

## Common Modifications

### Change Frequency Range

In [A_generate_AHxN_fin.ipynb](../A_generate_AHxN_fin.ipynb):
```python
# Modify:
frequencies, spectrogram = tfa_morlet(
    segment_ecg, 
    samp_freq, 
    0.8,   # fmin (change this)
    10,    # fmax (change this)
    0.01   # fstep
)
```

### Change Segment Duration

```python
SEGMENT_DURATION_SEC = 60  # instead of 90
```

⚠️ Remember to adjust YAML and image size accordingly.

### Use Different YOLOv8 Model

```python
model = YOLO("yolov8s.pt")  # Small
model = YOLO("yolov8m.pt")  # Medium
model = YOLO("yolov8l.pt")  # Large
```

---

## Expected Outputs

After running the full pipeline:

```
1DCNN/
├── preprocessed_ecg/          # ~2GB
├── Dataset/                   # ~100GB (all spectrograms)
├── re_loso_fold_s*/          # Organized CV folds
├── runs/detect/              # Training results
└── results/                  # Summary CSVs
```

---

## Next Steps

1. ✅ Run on sample subject (s1)
2. ✅ Verify outputs look correct
3. ✅ Train one fold to test GPU setup
4. ✅ Scale to all 50 subjects
5. ✅ Analyze results and create visualizations

---

## Support

For issues or questions:
- Check [methodology.md](methodology.md) for detailed explanations
- Review notebook comments and docstrings
- Open GitHub issue (if repository is public)

---

**Last Updated:** January 2026  
**Author:** Faiz Henri Kurniawan
