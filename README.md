# CSST106-4B-AY2627 — Computer Vision Laboratory Suite

**Course:** CSST 106 — Perception and Computer Vision  
**Student:** Ron Ken S. Borce  
**Section:** BSCS 4B  
**Academic Year:** 1st Semester, AY 2026–2027  

Interactive PyQt6 laboratory suite and written reports covering Labs 1 through 7.

---

## Quick Start

### Option 1: Live Interactive Web Suite (GitHub Pages)
Open **https://borcekhen.github.io/CSST106-4B-AY2627/** — all 7 labs run interactively in the browser (`HTML5 Canvas/JS` + `onnxruntime-web` for YOLOv11n & DeepLabV3).

### Option 2: Desktop PyQt6 Suite (`main.py`)
```bash
git clone https://github.com/BorceKhen/CSST106-4B-AY2627.git
cd CSST106-4B-AY2627
pip install -r requirements.txt
python main.py
```

---

## Laboratory Modules

| Lab | Week | Topic | Interactive UI | Report |
|---|---|---|---|---|
| **Lab 01** | 1–2 | Image Representation & Manipulation | `Lab_01_Images/lab1_ui.py` | `Lab_01_Images/Lab_01_Report.docx` |
| **Lab 02** | 3–4 | Edge Detection (Sobel & Canny) | `Lab_02_Edge_Detection/lab2_ui.py` | `Lab_02_Edge_Detection/Lab_02_Report.docx` |
| **Lab 03** | 4–5 | Histogram Equalization & Contrast Adjustment | `Lab_03_Histogram/lab3_ui.py` | `Lab_03_Histogram/Lab_03_Report.docx` |
| **Lab 04** | 6 | SURF, SIFT & ORB Feature Matching | `Lab_04_SURF_Feature_Detection/lab4_ui.py` | `Lab_04_SURF_Feature_Detection/Lab_04_Report.docx` |
| **Lab 05** | 7–8 | Facial Recognition using PCA (Eigenfaces) & SVM | `Lab_05_PCA_in_CV/lab5_ui.py` | `Lab_05_PCA_in_CV/Lab_05_Report.docx` |
| **Lab 06** | 8–9 | Object Detection with YOLOv11 | `Lab_06_YOLO_Object_Detection/lab6_ui.py` | `Lab_06_YOLO_Object_Detection/Lab_06_Report.docx` |
| **Lab 07** | 13 | Image Segmentation (Otsu, Watershed, Edge, DeepLabV3) | `Lab_07_Segmentation/lab7_ui.py` | `Lab_07_Segmentation/Lab_07_Report.docx` |

---

## Notes on Pre-Trained Models & Datasets

- **Lab 04 (SURF)**: Standard prebuilt `opencv-contrib-python` wheels exclude patented SURF (`OPENCV_ENABLE_NONFREE`). `lab4_ui.py` attempts `cv2.xfeatures2d.SURF_create` first and automatically falls back to **SIFT** and **ORB**.
- **Lab 05 (LFW Faces)**: `fetch_lfw_people` downloads and caches the LFW dataset on first run (~200 MB).
- **Lab 06 (YOLOv11)**: Uses `Lab_06_YOLO_Object_Detection/yolo11n.pt` (included) for image and live webcam detection.
- **Lab 07 (DeepLabV3)**: `deeplabv3_mobilenet_v3_large` weights (~42 MB) are cached automatically by `torchvision` on first semantic segmentation run.
