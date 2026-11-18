"""
CSST 106 - Perception and Computer Vision
Web Deployment Suite (Streamlit) — All 7 Laboratories Interactive in the Browser

Deployable directly from https://github.com/BorceKhen/CSST106-4B-AY2627 on
Streamlit Community Cloud or Hugging Face Spaces.
"""

from collections import deque
from pathlib import Path
import time
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage.segmentation import watershed
from sklearn.datasets import fetch_lfw_people
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import streamlit as st
import torch
from torchvision.models.segmentation import (
    DeepLabV3_MobileNet_V3_Large_Weights,
    deeplabv3_mobilenet_v3_large,
)
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
REPO_URL = "https://github.com/BorceKhen/CSST106-4B-AY2627"

VOC_CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car",
    "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor",
]

VOC_PALETTE = np.array([
    [15, 23, 42], [128, 0, 0], [0, 128, 0], [128, 128, 0], [0, 0, 128],
    [128, 0, 128], [0, 128, 128], [128, 128, 128], [64, 0, 0], [192, 0, 0],
    [64, 128, 0], [192, 128, 0], [64, 0, 128], [192, 0, 128], [64, 128, 128],
    [56, 189, 248], [0, 64, 0], [128, 64, 0], [0, 192, 0], [128, 192, 0],
    [0, 64, 128],
], dtype=np.uint8)

st.set_page_config(
    page_title="CSST 106 — Computer Vision Lab Suite",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def bgr_to_rgb(img: np.ndarray) -> np.ndarray:
    return img if img.ndim == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def uploaded_to_bgr(uploaded_file) -> np.ndarray | None:
    if uploaded_file is None:
        return None
    data = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def encode_png(img: np.ndarray) -> bytes:
    ok, buf = cv2.imencode(".png", img)
    return buf.tobytes() if ok else b""


@st.cache_resource(show_spinner="Loading LFW faces dataset...")
def load_lfw_data():
    lfw = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
    n_samples, h, w = lfw.images.shape
    X_train, X_test, y_train, y_test = train_test_split(
        lfw.data, lfw.target, test_size=0.2, random_state=42
    )
    return {
        "n_samples": n_samples,
        "h": h,
        "w": w,
        "n_features": lfw.data.shape[1],
        "target_names": lfw.target_names,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }


@st.cache_resource(show_spinner="Loading YOLOv11n model...")
def load_yolo_model():
    weights = BASE_DIR / "Lab_06_YOLO_Object_Detection" / "yolo11n.pt"
    return YOLO(str(weights if weights.exists() else "yolo11n.pt"))


@st.cache_resource(show_spinner="Loading DeepLabV3-MobileNetV3...")
def load_deeplab_model():
    weights = DeepLabV3_MobileNet_V3_Large_Weights.DEFAULT
    model = deeplabv3_mobilenet_v3_large(weights=weights).eval()
    return model, weights.transforms()


# ==============================================================================
# PAGES
# ==============================================================================
def render_home():
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#172554,#1e293b);padding:22px 26px;border-radius:12px;border:1px solid #334155;margin-bottom:18px;">
          <span style="background:#f8fafc;color:#0f172a;padding:3px 10px;border-radius:6px;font-weight:700;font-size:12px;">CSST 106</span>
          <span style="color:#94a3b8;font-size:13px;margin-left:10px;">Perception and Computer Vision • 1st Semester, AY 2026–2027</span>
          <h1 style="margin:10px 0 6px 0;color:#f8fafc;font-size:28px;">Computer Vision Laboratory Suite</h1>
          <p style="margin:0;color:#cbd5e1;font-size:14px;"><b>Student:</b> Ron Ken S. Borce &nbsp;|&nbsp; <b>Section:</b> BSCS 4B</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labs = [
        ("Lab 01 • Week 1–2", "Image Manipulation", "BGR/grayscale arrays, pixel inspection/editing, ROI crop, resize, 90° rotation.", "Lab_01_Images/Lab_01_Report.docx"),
        ("Lab 02 • Week 3–4", "Edge Detection (Sobel & Canny)", "Gaussian blur, Sobel X/Y/Magnitude, Canny hysteresis T1/T2, and Q&A.", "Lab_02_Edge_Detection/Lab_02_Report.docx"),
        ("Lab 03 • Week 4–5", "Histogram Equalization & Contrast", "Global equalizeHist (Gray & YUV), contrast stretch, CLAHE, and histograms.", "Lab_03_Histogram/Lab_03_Report.docx"),
        ("Lab 04 • Week 6", "SURF / SIFT / ORB Matching", "Keypoints, BFMatcher matching, SIFT vs. ORB speed benchmark, and U-SURF.", "Lab_04_SURF_Feature_Detection/Lab_04_Report.docx"),
        ("Lab 05 • Week 7–8", "PCA Eigenfaces & SVM", "LFW dataset, 90% variance curve, whitening comparison, RBF SVM, and failure analysis.", "Lab_05_PCA_in_CV/Lab_05_Report.docx"),
        ("Lab 06 • Week 8–9", "YOLOv11 Object Detection", "Pre-trained YOLOv11n inference on images & camera, plus dataset guide.", "Lab_06_YOLO_Object_Detection/Lab_06_Report.docx"),
        ("Lab 07 • Week 13", "Image Segmentation Techniques", "Otsu/Adaptive, Region Growing & Watershed, Canny contours, DeepLabV3, and IoU.", "Lab_07_Segmentation/Lab_07_Report.docx"),
    ]

    cols = st.columns(2)
    for idx, (tag, title, desc, report_rel) in enumerate(labs):
        with cols[idx % 2]:
            with st.container(border=True):
                st.caption(tag)
                st.subheader(title)
                st.write(desc)
                rpath = BASE_DIR / report_rel
                if rpath.exists():
                    st.download_button(
                        label="Download Report (.docx)",
                        data=rpath.read_bytes(),
                        file_name=rpath.name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_{idx}",
                    )
    st.link_button("View GitHub Repository", REPO_URL)


def render_lab1():
    st.header("Lab 01: Image Representation & Manipulation")
    up = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg", "bmp", "webp"], key="l1_up")
    bgr = uploaded_to_bgr(up) if up else cv2.imread(str(BASE_DIR / "Lab_01_Images" / "sample_image.png"))
    if bgr is None:
        st.error("Sample image not found.")
        return
    h, w, c = bgr.shape

    col_ctrl, col_view = st.columns([1, 2.3])
    with col_ctrl:
        gray_mode = st.checkbox("Convert to Grayscale (2D array)", value=False)
        px_y = st.slider("Inspect / Edit Pixel Y", 0, h - 1, min(95, h - 1))
        px_x = st.slider("Inspect / Edit Pixel X", 0, w - 1, min(520, w - 1))
        apply_patch = st.checkbox("Modify Pixel / Patch Color", value=False)
        hex_col = st.color_picker("Patch Color", "#FF00FF")
        patch_sz = st.slider("Patch Size (px)", 1, 51, 25, step=2)

        crop_on = st.checkbox("Enable ROI Crop", value=False)
        y0_p, y1_p = st.slider("ROI Y %", 0, 100, (22, 82))
        x0_p, x1_p = st.slider("ROI X %", 0, 100, (22, 70))
        scale_pct = st.slider("Resize Scale %", 20, 200, 100)
        rot_deg = st.radio("Rotate", [0, 90, 180, 270], horizontal=True)

    working = bgr.copy()
    orig_px = working[px_y, px_x].tolist()
    if apply_patch:
        rgb_tuple = tuple(int(hex_col.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        bgr_tuple = (rgb_tuple[2], rgb_tuple[1], rgb_tuple[0])
        half = patch_sz // 2
        working[max(0, px_y - half) : min(h, px_y + half + 1), max(0, px_x - half) : min(w, px_x + half + 1)] = bgr_tuple

    out = working.copy()
    if crop_on:
        ry0, ry1 = int(h * y0_p / 100), max(int(h * y0_p / 100) + 1, int(h * y1_p / 100))
        rx0, rx1 = int(w * x0_p / 100), max(int(w * x0_p / 100) + 1, int(w * x1_p / 100))
        out = out[ry0:ry1, rx0:rx1]
    if scale_pct != 100:
        interp = cv2.INTER_AREA if scale_pct < 100 else cv2.INTER_CUBIC
        out = cv2.resize(out, (max(1, int(out.shape[1] * scale_pct / 100)), max(1, int(out.shape[0] * scale_pct / 100))), interpolation=interp)
    if rot_deg == 90:
        out = cv2.rotate(out, cv2.ROTATE_90_CLOCKWISE)
    elif rot_deg == 180:
        out = cv2.rotate(out, cv2.ROTATE_180)
    elif rot_deg == 270:
        out = cv2.rotate(out, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if gray_mode:
        out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)

    with col_view:
        c1, c2 = st.columns(2)
        c1.image(bgr_to_rgb(working), caption=f"Original {working.shape} | BGR at ({px_y},{px_x})={orig_px}", width="stretch")
        c2.image(bgr_to_rgb(out), caption=f"Processed {out.shape} (dtype={out.dtype})", width="stretch")
        st.download_button("Download Output PNG", encode_png(out), file_name="lab1_output.png", mime="image/png")


def render_lab2():
    st.header("Lab 02: Edge Detection (Sobel vs. Canny)")
    up = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg", "bmp", "webp"], key="l2_up")
    bgr = uploaded_to_bgr(up) if up else cv2.imread(str(BASE_DIR / "Lab_02_Edge_Detection" / "input.jpg"))
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    c1, c2, c3, c4 = st.columns(4)
    blur_k = c1.selectbox("Gaussian Blur", [1, 3, 5, 7], index=1)
    sobel_k = c2.selectbox("Sobel ksize", [1, 3, 5, 7], index=1)
    t1 = c3.slider("Canny T1 (Low)", 0, 255, 100)
    t2 = c4.slider("Canny T2 (High)", 0, 255, 200)

    blurred = cv2.GaussianBlur(gray, (blur_k, blur_k), 0) if blur_k > 1 else gray.copy()
    sx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=sobel_k)
    sy = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=sobel_k)
    mag = cv2.magnitude(sx, sy)
    sobel_u8 = np.uint8(np.clip(mag / max(1.0, mag.max()) * 255.0, 0, 255))
    canny = cv2.Canny(blurred, t1, t2)

    p1, p2, p3 = st.columns(3)
    p1.image(gray, caption=f"Original ({gray.shape[1]}×{gray.shape[0]})", width="stretch")
    p2.image(sobel_u8, caption=f"Sobel (Max={mag.max():.1f}, Mean={mag.mean():.1f})", width="stretch")
    p3.image(canny, caption=f"Canny ({np.count_nonzero(canny):,} edge px)", width="stretch")

    with st.expander("Question & Conclusion"):
        st.markdown(
            "**Differences:** Sobel produces continuous grayscale gradient magnitudes with thicker edge ridges and preserves directional responses (`Gx`, `Gy`), whereas Canny applies non-maximum suppression and dual-threshold hysteresis (`T1`, `T2`) to yield clean, 1-pixel-wide binary edges.\n\n"
            "**Conclusion:** Sobel excels when gradient strength/orientation is needed, while Canny yields cleaner boundaries for contour extraction and segmentation."
        )


def render_lab3():
    st.header("Lab 03: Histogram Equalization & Contrast Adjustment")
    up = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg", "bmp", "webp"], key="l3_up")
    bgr = uploaded_to_bgr(up) if up else cv2.imread(str(BASE_DIR / "Lab_03_Histogram" / "sample_low_contrast.png"))

    c1, c2, c3, c4 = st.columns(4)
    color_mode = c1.radio("Color Mode", ["Grayscale", "Color (YUV Luma)"], horizontal=True) == "Color (YUV Luma)"
    clip = c2.slider("CLAHE Clip Limit", 1.0, 10.0, 2.0, step=0.5)
    tile = c3.selectbox("CLAHE Tile Grid", [4, 8, 16], index=1)
    lo_p, hi_p = c4.slider("Linear Stretch %", 0, 100, (1, 99))

    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile))
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    def stretch(ch):
        lo, hi = np.percentile(ch, lo_p), np.percentile(ch, hi_p)
        return ch.copy() if hi <= lo else np.clip((ch.astype(np.float32) - lo) * (255.0 / (hi - lo)), 0, 255).astype(np.uint8)

    if not color_mode:
        orig, glob, adp, lin = gray, cv2.equalizeHist(gray), clahe.apply(gray), stretch(gray)
    else:
        orig = bgr.copy()
        def yuv_fn(fn):
            yuv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV)
            yuv[:, :, 0] = fn(yuv[:, :, 0])
            return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        glob, adp, lin = yuv_fn(cv2.equalizeHist), yuv_fn(clahe.apply), yuv_fn(stretch)

    cols = st.columns(4)
    for col, img, title in [
        (cols[0], orig, "Original"),
        (cols[1], lin, "Linear Stretch"),
        (cols[2], glob, "Global Equalization"),
        (cols[3], adp, "CLAHE"),
    ]:
        col.image(bgr_to_rgb(img), caption=title, width="stretch")
        lum = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:, :, 0] if img.ndim == 3 else img
        hist = cv2.calcHist([lum], [0], None, [256], [0, 256]).ravel()
        fig, ax = plt.subplots(figsize=(3.5, 1.8))
        ax.fill_between(np.arange(256), hist, color="#0284c7", alpha=0.6)
        ax.set_xlim(0, 255)
        ax.set_yticks([])
        plt.tight_layout()
        col.pyplot(fig)
        plt.close(fig)


def render_lab4():
    st.header("Lab 04: SURF, SIFT & ORB Feature Detection & Matching")
    u1, u2 = st.columns(2)
    up1 = u1.file_uploader("Image 1 (optional)", type=["png", "jpg", "jpeg"], key="l4_u1")
    up2 = u2.file_uploader("Image 2 (optional)", type=["png", "jpg", "jpeg"], key="l4_u2")
    b1 = uploaded_to_bgr(up1) if up1 else cv2.imread(str(BASE_DIR / "Lab_04_SURF_Feature_Detection" / "sample_image.jpg"))
    b2 = uploaded_to_bgr(up2) if up2 else cv2.imread(str(BASE_DIR / "Lab_04_SURF_Feature_Detection" / "sample_image_transformed.jpg"))
    g1, g2 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)

    c1, c2 = st.columns(2)
    det_choice = c1.radio("Detector", ["SIFT (128-D Float)", "ORB (32-B Binary)"], horizontal=True)
    orb_n = c2.slider("ORB Max Features", 100, 1500, 500)
    st.info("Note: Patented SURF (`cv2.xfeatures2d.SURF_create`) is excluded in standard OpenCV wheels (`OPENCV_ENABLE_NONFREE=OFF`); SIFT and ORB run live below.")

    det = cv2.SIFT_create() if det_choice.startswith("SIFT") else cv2.ORB_create(nfeatures=orb_n)
    t0 = time.perf_counter()
    kp1, d1 = det.detectAndCompute(g1, None)
    det_ms = (time.perf_counter() - t0) * 1000.0
    kp2, d2 = det.detectAndCompute(g2, None)

    good = []
    if d1 is not None and d2 is not None and len(d1) >= 2 and len(d2) >= 2:
        norm = cv2.NORM_HAMMING if d1.dtype == np.uint8 else cv2.NORM_L2
        for pair in cv2.BFMatcher(norm).knnMatch(d1, d2, k=2):
            if len(pair) == 2 and pair[0].distance < 0.75 * pair[1].distance:
                good.append(pair[0])

    vis_kp = cv2.drawKeypoints(g1, kp1, None, (255, 140, 0), cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    vis_m = cv2.drawMatches(g1, kp1, g2, kp2, sorted(good, key=lambda m: m.distance)[:45], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    v1, v2 = st.columns(2)
    v1.image(bgr_to_rgb(vis_kp), caption=f"{det_choice}: {len(kp1)} keypoints ({det_ms:.1f} ms)", width="stretch")
    v2.image(bgr_to_rgb(vis_m), caption=f"Good Matches: {len(good)}", width="stretch")


def render_lab5():
    st.header("Lab 05: Facial Recognition using PCA (Eigenfaces) & SVM")
    data = load_lfw_data()
    c1, c2 = st.columns(2)
    n_comp = c1.slider("PCA n_components", 20, 220, 150)
    whiten = c2.checkbox("whiten=True (unit variance components)", value=True)

    pca = PCA(n_components=n_comp, svd_solver="randomized", whiten=whiten, random_state=42).fit(data["X_train"])
    X_tr_p, X_te_p = pca.transform(data["X_train"]), pca.transform(data["X_test"])
    clf = SVC(kernel="rbf", class_weight="balanced", random_state=42).fit(X_tr_p, data["y_train"])
    y_pred = clf.predict(X_te_p)

    cum_var = np.cumsum(pca.explained_variance_ratio_)
    k90 = int(np.searchsorted(cum_var, 0.90) + 1) if cum_var[-1] >= 0.90 else -1
    acc = accuracy_score(data["y_test"], y_pred)

    m1, m2, m3 = st.columns(3)
    m1.metric("SVM Test Accuracy", f"{acc * 100:.2f}%")
    m2.metric("Retained Variance", f"{cum_var[-1] * 100:.2f}%")
    m3.metric("Components for 90%", f"{k90}" if k90 > 0 else f">{n_comp}")

    t1, t2, t3 = st.tabs(["Eigenfaces", "Variance Curve", "Failure Analysis & Report"])
    with t1:
        ef = pca.components_.reshape((n_comp, data["h"], data["w"]))
        fig, axes = plt.subplots(2, 6, figsize=(11, 4))
        for ax, i in zip(axes.ravel(), list(range(9)) + list(range(n_comp - 3, n_comp))):
            ax.imshow(ef[i], cmap="gray")
            ax.set_title(f"EF {i}", fontsize=9)
            ax.axis("off")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    with t2:
        fig, ax = plt.subplots(figsize=(8, 3.8))
        ax.plot(np.arange(1, n_comp + 1), cum_var * 100.0, linewidth=2)
        ax.axhline(90.0, color="orange", linestyle="--", label="90%")
        if k90 > 0:
            ax.axvline(k90, color="green", linestyle="--", label=f"k={k90}")
        ax.set_xlabel("Components")
        ax.set_ylabel("Cumulative Variance (%)")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    with t3:
        mis = np.where(y_pred != data["y_test"])[0]
        fig, axes = plt.subplots(2, 4, figsize=(10, 5))
        for ax, idx in zip(axes.ravel(), mis[:8]):
            ax.imshow(data["X_test"][idx].reshape((data["h"], data["w"])), cmap="gray")
            ax.set_title(f"T:{data['target_names'][data['y_test'][idx]].split()[-1]}\nP:{data['target_names'][y_pred[idx]].split()[-1]}", color="red", fontsize=9)
            ax.axis("off")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.text(classification_report(data["y_test"], y_pred, target_names=data["target_names"], zero_division=0))


def render_lab6():
    st.header("Lab 06: YOLOv11 Object Detection")
    model = load_yolo_model()
    src_mode = st.radio("Input Source", ["Sample Scene", "Upload Image", "Browser Camera"], horizontal=True)
    bgr = None
    if src_mode == "Sample Scene":
        bgr = cv2.imread(str(BASE_DIR / "Lab_06_YOLO_Object_Detection" / "sample_scene.jpg"))
    elif src_mode == "Upload Image":
        up = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "webp"], key="l6_up")
        bgr = uploaded_to_bgr(up)
    else:
        cam = st.camera_input("Take a photo for YOLOv11 detection")
        bgr = uploaded_to_bgr(cam)

    conf = st.slider("Confidence Threshold", 0.10, 0.90, 0.25, step=0.05)
    if bgr is None:
        st.info("Select or capture an image to run YOLOv11 inference.")
        return

    t0 = time.perf_counter()
    res = model.predict(bgr, conf=conf, verbose=False)[0]
    ms = (time.perf_counter() - t0) * 1000.0
    annot = res.plot()

    c1, c2 = st.columns(2)
    c1.image(bgr_to_rgb(bgr), caption="Input Image", width="stretch")
    c2.image(bgr_to_rgb(annot), caption=f"YOLOv11n Detections ({len(res.boxes)} objects • {ms:.1f} ms)", width="stretch")
    if len(res.boxes):
        rows = [{"Class": res.names[int(b.cls[0])], "Confidence": round(float(b.conf[0]), 2), "Box [x1,y1,x2,y2]": [int(v) for v in b.xyxy[0].tolist()]} for b in res.boxes]
        st.dataframe(rows, width="stretch")


def render_lab7():
    st.header("Lab 07: Image Segmentation Techniques")
    choice = st.radio("Input Source", ["Objects Sample", "Scene Sample", "Upload Image"], horizontal=True)
    if choice == "Objects Sample":
        bgr = cv2.imread(str(BASE_DIR / "Lab_07_Segmentation" / "sample_objects.png"))
    elif choice == "Scene Sample":
        bgr = cv2.imread(str(BASE_DIR / "Lab_07_Segmentation" / "sample_scene.jpg"))
    else:
        up = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "webp"], key="l7_up")
        bgr = uploaded_to_bgr(up)
    if bgr is None:
        st.info("Upload an image to segment.")
        return

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    opening = cv2.morphologyEx(otsu, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.65 * dist.max(), 255, 0)
    _, markers = cv2.connectedComponents(np.uint8(sure_fg))
    ws_labels = watershed(-dist, markers, mask=opening > 0)
    rng = np.random.default_rng(123)
    pal = rng.integers(60, 245, size=(int(ws_labels.max()) + 1, 3), dtype=np.uint8)
    pal[0] = (15, 23, 42)
    ws_vis = cv2.addWeighted(bgr, 0.45, pal[ws_labels], 0.55, 0)

    edges = cv2.Canny(blur, 50, 140)
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edge_vis = bgr.copy()
    cv2.drawContours(edge_vis, [c for c in contours if cv2.contourArea(c) >= 120], -1, (56, 189, 248), 2)

    sem_model, preprocess = load_deeplab_model()
    pil_img = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    with torch.no_grad():
        out = sem_model(preprocess(pil_img).unsqueeze(0))["out"][0]
    pred = cv2.resize(out.argmax(0).byte().cpu().numpy(), (bgr.shape[1], bgr.shape[0]), interpolation=cv2.INTER_NEAREST)
    sem_bgr = cv2.cvtColor(VOC_PALETTE[np.clip(pred, 0, len(VOC_PALETTE) - 1)], cv2.COLOR_RGB2BGR)
    sem_vis = cv2.addWeighted(bgr, 0.45, sem_bgr, 0.55, 0)
    classes = [VOC_CLASSES[int(i)] for i in np.unique(pred) if 0 < i < len(VOC_CLASSES)]

    c1, c2, c3, c4 = st.columns(4)
    c1.image(otsu, caption="1. Thresholding (Otsu)", width="stretch")
    c2.image(bgr_to_rgb(ws_vis), caption=f"2. Region (Watershed: {int(ws_labels.max())} obj)", width="stretch")
    c3.image(bgr_to_rgb(edge_vis), caption="3. Edge (Closed Contours)", width="stretch")
    c4.image(bgr_to_rgb(sem_vis), caption=f"4. DeepLabV3 ({', '.join(classes) if classes else 'background'})", width="stretch")


# ==============================================================================
# NAVIGATION
# ==============================================================================
PAGES = {
    "Home (Suite Overview)": render_home,
    "Lab 01: Image Manipulation": render_lab1,
    "Lab 02: Edge Detection": render_lab2,
    "Lab 03: Histogram & Contrast": render_lab3,
    "Lab 04: Feature Matching": render_lab4,
    "Lab 05: PCA Eigenfaces": render_lab5,
    "Lab 06: YOLOv11 Detection": render_lab6,
    "Lab 07: Segmentation": render_lab7,
}

with st.sidebar:
    st.title("CSST 106 Labs")
    st.caption("Ron Ken S. Borce • BSCS 4B")
    selected = st.radio("Navigate", list(PAGES.keys()))
    st.divider()
    st.link_button("GitHub Repository", REPO_URL, width="stretch")

PAGES[selected]()
