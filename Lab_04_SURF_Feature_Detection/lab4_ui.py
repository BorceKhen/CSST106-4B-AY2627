"""
CSST106 - Perception and Computer Vision
Laboratory Exercise No. 4: SURF Feature Detection, Matching & SIFT/ORB Comparison (PyQt6)

Covers all Lab 4 activities:
  - Attempts cv2.xfeatures2d.SURF_create(hessianThreshold=..., upright=...) first;
    if OpenCV excludes patented SURF (error -213 nonfree), reports status honestly
    and provides SIFT + ORB free alternatives automatically.
  - Keypoints         : Rich keypoints (scale & orientation) on Image 1
  - Feature Matching  : Descriptor matching between Image 1 and Image 2 (BFMatcher + ratio test)
  - SIFT vs ORB (SURF): Side-by-side detector comparison with live timing & descriptor stats
  - U-SURF / Upright  : Upright (non-rotation-invariant) vs rotation-invariant matching behavior
  - Questions & Notes : Answers to all 3 Lab 4 questions + OpenCV patent/ORB notes
"""

from pathlib import Path
import sys
import time
import cv2
import numpy as np
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor, QDragEnterEvent, QDropEvent, QImage, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)


def create_sample_pair(img1_path: Path, img2_path: Path, width: int = 640, height: int = 480) -> None:
    """Create a rich textured scene (Image 1) and a rotated/scaled view (Image 2) for matching."""
    img = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        t = y / height
        img[y, :] = (int(225 - 60 * t), int(205 - 40 * t), int(185 - 25 * t))

    # Textured checkerboard corner target (blob & corner features)
    for r in range(6):
        for c in range(6):
            col = (245, 245, 245) if (r + c) % 2 == 0 else (35, 45, 65)
            cv2.rectangle(img, (55 + c * 22, 55 + r * 22), (77 + c * 22, 77 + r * 22), col, -1)

    # Multi-scale circles (blob-like features ideal for Hessian/DoG detectors)
    for cx, cy, rad, col in [
        (320, 120, 44, (40, 120, 210)),
        (320, 120, 24, (240, 220, 90)),
        (490, 110, 36, (60, 175, 95)),
        (490, 110, 16, (250, 250, 250)),
        (530, 320, 52, (165, 75, 195)),
        (530, 320, 26, (30, 40, 60)),
    ]:
        cv2.circle(img, (cx, cy), rad, col, -1)

    # Distinct polygon landmarks & house-like silhouette
    pts1 = np.array([[95, 265], [195, 215], [295, 275], [260, 405], [115, 395]], np.int32)
    cv2.fillPoly(img, [pts1], (85, 110, 155))
    cv2.polylines(img, [pts1], True, (25, 35, 55), 3)
    cv2.rectangle(img, (150, 290), (235, 355), (235, 210, 145), -1)
    cv2.circle(img, (192, 322), 14, (45, 65, 115), -1)

    # Star / diamond marker
    star = np.array([[375, 260], [395, 315], [450, 330], [395, 345], [375, 400], [355, 345], [300, 330], [355, 315]], np.int32)
    cv2.fillPoly(img, [star], (30, 150, 230))
    cv2.polylines(img, [star], True, (20, 45, 85), 2)

    cv2.putText(img, "SURF / SIFT / ORB", (220, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (30, 35, 45), 2, cv2.LINE_AA)

    img1_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(img1_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])

    # Create Image 2: rotated 18 deg, scaled 0.88x, and shifted slightly
    center = (width / 2.0, height / 2.0)
    mat = cv2.getRotationMatrix2D(center, 18.0, 0.88)
    mat[0, 2] += 18.0
    mat[1, 2] -= 10.0
    img2 = cv2.warpAffine(img, mat, (width, height), borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(str(img2_path), img2, [cv2.IMWRITE_JPEG_QUALITY, 95])


def cv_to_qpixmap(img: np.ndarray) -> QPixmap:
    """Convert grayscale or BGR uint8 array to QPixmap."""
    if img.ndim == 2:
        h, w = img.shape
        qimg = QImage(img.data, w, h, w, QImage.Format.Format_Grayscale8)
        return QPixmap.fromImage(qimg.copy())
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimg.copy())


def probe_surf_support() -> tuple[bool, str]:
    """Check whether cv2.xfeatures2d.SURF_create works in this OpenCV build."""
    try:
        if not hasattr(cv2, "xfeatures2d") or not hasattr(cv2.xfeatures2d, "SURF_create"):
            return False, "cv2.xfeatures2d.SURF_create is not present in this OpenCV build."
        _ = cv2.xfeatures2d.SURF_create(400)
        return True, "SURF available (OPENCV_ENABLE_NONFREE enabled)."
    except cv2.error as exc:
        msg = str(exc).splitlines()[-1] if str(exc) else "Patented nonfree module disabled."
        return False, f"SURF unavailable in OpenCV {cv2.__version__} (patented/nonfree disabled)."


def run_detector(
    gray: np.ndarray,
    method: str,
    hessian_threshold: int = 400,
    orb_nfeatures: int = 500,
    upright: bool = False,
) -> dict:
    """Detect keypoints & descriptors using SURF (if available), SIFT, or ORB."""
    t0 = time.perf_counter()
    note = ""
    effective_method = method

    if method == "SURF":
        try:
            det = cv2.xfeatures2d.SURF_create(hessianThreshold=hessian_threshold, upright=upright)
        except Exception:
            effective_method = "SIFT (Fallback)"
            note = "SURF requires OPENCV_ENABLE_NONFREE; falling back to SIFT/ORB."
            det = cv2.SIFT_create(nfeatures=0, contrastThreshold=max(0.01, hessian_threshold / 10000.0))
    elif method == "SIFT":
        det = cv2.SIFT_create()
    else:
        det = cv2.ORB_create(nfeatures=orb_nfeatures)

    kps, desc = det.detectAndCompute(gray, None)
    if upright and method != "SURF":
        # Demonstrate upright behavior (ignore orientation angle on keypoints for teaching comparison)
        kps_upright = [
            cv2.KeyPoint(kp.pt[0], kp.pt[1], kp.size, -1.0, kp.response, kp.octave, kp.class_id)
            for kp in kps
        ]
        kps, desc = det.compute(gray, kps_upright)
        note = "Upright mode: orientation fixed (faster, not rotation-invariant)."

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    vis = cv2.drawKeypoints(
        gray,
        kps,
        None,
        (255, 140, 0),
        cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS,
    )
    desc_shape = tuple(desc.shape) if desc is not None else (0, 0)
    return {
        "requested": method,
        "effective": effective_method,
        "keypoints": kps,
        "descriptors": desc,
        "count": len(kps),
        "desc_shape": desc_shape,
        "time_ms": elapsed_ms,
        "vis": vis,
        "note": note,
    }


def match_features(
    gray1: np.ndarray,
    gray2: np.ndarray,
    method: str,
    hessian_threshold: int,
    orb_nfeatures: int,
    upright: bool,
    max_draw: int = 45,
) -> dict:
    """Detect and match features between Image 1 and Image 2."""
    r1 = run_detector(gray1, method, hessian_threshold, orb_nfeatures, upright)
    r2 = run_detector(gray2, method, hessian_threshold, orb_nfeatures, upright)

    d1, d2 = r1["descriptors"], r2["descriptors"]
    good_matches = []
    t0 = time.perf_counter()

    if d1 is not None and d2 is not None and len(d1) >= 2 and len(d2) >= 2:
        is_binary = d1.dtype == np.uint8
        norm = cv2.NORM_HAMMING if is_binary else cv2.NORM_L2
        bf = cv2.BFMatcher(norm)
        knn = bf.knnMatch(d1, d2, k=2)
        for pair in knn:
            if len(pair) == 2:
                m, n = pair
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
        good_matches.sort(key=lambda m: m.distance)

    match_ms = (time.perf_counter() - t0) * 1000.0
    drawn = good_matches[:max_draw]
    vis_matches = cv2.drawMatches(
        gray1,
        r1["keypoints"],
        gray2,
        r2["keypoints"],
        drawn,
        None,
        matchColor=(56, 189, 248),
        singlePointColor=(148, 163, 184),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    return {
        "r1": r1,
        "r2": r2,
        "good_count": len(good_matches),
        "match_ms": match_ms,
        "vis": vis_matches,
    }


class ImageCanvas(QWidget):
    """Aspect-ratio-preserving image viewer."""

    def __init__(self) -> None:
        super().__init__()
        self._pixmap: QPixmap | None = None
        self._img_w = 0
        self._img_h = 0

    def set_image(self, img: np.ndarray | None) -> None:
        if img is None:
            self._pixmap = None
            self._img_w = 0
            self._img_h = 0
        else:
            self._img_h, self._img_w = img.shape[:2]
            self._pixmap = cv_to_qpixmap(img)
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.fillRect(self.rect(), QColor("#0b1120"))

        if self._pixmap is None or self._img_w == 0 or self._img_h == 0:
            return

        pad = 8
        avail_w = max(1, self.width() - 2 * pad)
        avail_h = max(1, self.height() - 2 * pad)
        scale = min(avail_w / self._img_w, avail_h / self._img_h)
        dw = max(1, int(self._img_w * scale))
        dh = max(1, int(self._img_h * scale))
        ox = (self.width() - dw) // 2
        oy = (self.height() - dh) // 2
        painter.drawPixmap(QRect(ox, oy, dw, dh), self._pixmap)


STYLESHEET = """
QMainWindow, QWidget#Root {
    background-color: #0f172a;
    color: #e2e8f0;
    font-family: "Segoe UI", sans-serif;
}
QFrame#Panel {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
}
QLabel#Title {
    color: #f8fafc;
    font-size: 16px;
    font-weight: 700;
}
QLabel#Section {
    color: #38bdf8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
QLabel#Muted {
    color: #94a3b8;
    font-size: 12px;
}
QLabel#Warn {
    color: #fbbf24;
    font-size: 11.5px;
}
QLabel#Mono {
    color: #f1f5f9;
    font-family: "Consolas", monospace;
    font-size: 11.5px;
}
QLabel#StatusBar {
    color: #cbd5e1;
    font-family: "Consolas", monospace;
    font-size: 11px;
    padding: 4px 8px;
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
}
QPushButton {
    background-color: #273549;
    color: #e2e8f0;
    border: 1px solid #3b4c66;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #334155;
}
QPushButton#AccentBtn {
    background-color: #0284c7;
    color: #ffffff;
    border: 1px solid #38bdf8;
}
QPushButton#AccentBtn:hover {
    background-color: #0369a1;
}
QPushButton#TabBtn {
    background-color: transparent;
    border: 1px solid transparent;
    color: #94a3b8;
    padding: 7px 14px;
}
QPushButton#TabBtn:hover {
    color: #f8fafc;
    background-color: #273549;
}
QPushButton#TabBtn:checked {
    background-color: #0284c7;
    color: #ffffff;
    border: 1px solid #38bdf8;
}
QPushButton#ChipBtn:checked {
    background-color: #0284c7;
    color: #ffffff;
    border: 1px solid #38bdf8;
}
QSlider::groove:horizontal {
    height: 4px;
    background: #334155;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #38bdf8;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QCheckBox {
    color: #e2e8f0;
    font-size: 12px;
}
"""


class Lab4Window(QMainWindow):
    """Tabbed interactive UI for CSST106 Lab 4 SURF / SIFT / ORB Feature Detection."""

    TABS = [
        ("keypoints", "Keypoints"),
        ("matching", "Feature Matching"),
        ("compare", "SIFT vs ORB (SURF)"),
        ("qa", "Questions && Notes"),
    ]

    def __init__(self, lab_dir: Path) -> None:
        super().__init__()
        self.lab_dir = lab_dir
        self.sample1 = lab_dir / "sample_image.jpg"
        self.sample2 = lab_dir / "sample_image_transformed.jpg"

        self.surf_available, self.surf_msg = probe_surf_support()
        self.gray1: np.ndarray | None = None
        self.gray2: np.ndarray | None = None
        self.name1 = ""
        self.name2 = ""

        self.current_tab = "keypoints"
        self.detector_name = "SURF" if self.surf_available else "SIFT"
        self.last_vis: np.ndarray | None = None

        self.setWindowTitle("CSST106 Lab 4 — SURF Feature Detection, Matching & Comparison")
        self.resize(1300, 750)
        self.setMinimumSize(1000, 620)
        self.setAcceptDrops(True)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()

        if not self.sample1.exists() or not self.sample2.exists():
            create_sample_pair(self.sample1, self.sample2)
        self.load_images(self.sample1, self.sample2)

    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        # Header Bar
        top_bar = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        lbl_title = QLabel("CSST106 Lab 4: SURF Feature Detection & Descriptor Matching")
        lbl_title.setObjectName("Title")
        lbl_sub = QLabel("Detect keypoints & descriptors, match across views, and compare SURF, SIFT, and ORB.")
        lbl_sub.setObjectName("Muted")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        top_bar.addLayout(title_box, 1)

        for text, handler, accent in [
            ("Open Image 1...", lambda: self._on_open(1), False),
            ("Open Image 2...", lambda: self._on_open(2), False),
            ("Reset", self._on_reset, False),
            ("Save Output...", self._on_save, True),
        ]:
            btn = QPushButton(text)
            if accent:
                btn.setObjectName("AccentBtn")
            btn.clicked.connect(handler)
            top_bar.addWidget(btn)
        layout.addLayout(top_bar)

        # Horizontal Tab Strip
        tab_panel = QFrame()
        tab_panel.setObjectName("Panel")
        tab_row = QHBoxLayout(tab_panel)
        tab_row.setContentsMargins(6, 5, 6, 5)
        tab_row.setSpacing(4)

        self.tab_group = QButtonGroup(self)
        self.tab_group.setExclusive(True)
        self.tab_buttons: dict[str, QPushButton] = {}
        for key, label in self.TABS:
            btn = QPushButton(label)
            btn.setObjectName("TabBtn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _chk, k=key: self._select_tab(k))
            self.tab_group.addButton(btn)
            self.tab_buttons[key] = btn
            tab_row.addWidget(btn)
        tab_row.addStretch()
        self.tab_buttons["keypoints"].setChecked(True)
        layout.addWidget(tab_panel)

        # Body: 2 Viewer Cards + Q&A Card + Right Parameters Panel
        body = QHBoxLayout()
        body.setSpacing(10)
        layout.addLayout(body, 1)

        self.view_cards: list[QFrame] = []
        self.view_titles: list[QLabel] = []
        self.view_badges: list[QLabel] = []
        self.canvases: list[ImageCanvas] = []

        for _ in range(2):
            card = QFrame()
            card.setObjectName("Panel")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(10, 8, 10, 10)
            cl.setSpacing(6)
            hdr = QHBoxLayout()
            tlbl = QLabel("-")
            tlbl.setObjectName("Section")
            blbl = QLabel("-")
            blbl.setObjectName("Muted")
            hdr.addWidget(tlbl)
            hdr.addStretch()
            hdr.addWidget(blbl)
            cl.addLayout(hdr)
            canvas = ImageCanvas()
            cl.addWidget(canvas, 1)
            body.addWidget(card, 1)
            self.view_cards.append(card)
            self.view_titles.append(tlbl)
            self.view_badges.append(blbl)
            self.canvases.append(canvas)

        # Q&A Card
        self.qa_card = QFrame()
        self.qa_card.setObjectName("Panel")
        qal = QVBoxLayout(self.qa_card)
        qal.setContentsMargins(16, 14, 16, 14)
        qal.setSpacing(10)
        qa_hdr = QLabel("LAB 4 — QUESTIONS FOR STUDENTS & TECHNICAL NOTES")
        qa_hdr.setObjectName("Section")
        qal.addWidget(qa_hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        qa_content = QWidget()
        qa_content.setStyleSheet("background: transparent;")
        qacl = QVBoxLayout(qa_content)
        qacl.setContentsMargins(0, 0, 8, 0)
        self.qa_text_lbl = QLabel()
        self.qa_text_lbl.setWordWrap(True)
        self.qa_text_lbl.setTextFormat(Qt.TextFormat.RichText)
        self.qa_text_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.qa_text_lbl.setStyleSheet("color: #e2e8f0; font-size: 13px; line-height: 1.5;")
        qacl.addWidget(self.qa_text_lbl)
        qacl.addStretch()
        scroll.setWidget(qa_content)
        qal.addWidget(scroll, 1)
        self.qa_card.hide()
        body.addWidget(self.qa_card, 1)

        # Right Controls & Metrics Drawer
        inspector = QFrame()
        inspector.setObjectName("Panel")
        inspector.setFixedWidth(305)
        il = QVBoxLayout(inspector)
        il.setContentsMargins(12, 10, 12, 12)
        il.setSpacing(9)

        hdr_p = QLabel("DETECTOR & METRICS")
        hdr_p.setObjectName("Section")
        il.addWidget(hdr_p)

        # SURF build status note
        surf_note = QLabel(self.surf_msg)
        surf_note.setObjectName("Warn" if not self.surf_available else "Muted")
        surf_note.setWordWrap(True)
        il.addWidget(surf_note)

        # Detector selector
        il.addWidget(QLabel("Active Detector:"))
        det_row = QHBoxLayout()
        self.det_group = QButtonGroup(self)
        self.det_group.setExclusive(True)
        self.det_buttons: dict[str, QPushButton] = {}
        for name in ("SURF", "SIFT", "ORB"):
            b = QPushButton(name)
            b.setObjectName("ChipBtn")
            b.setCheckable(True)
            if name == self.detector_name:
                b.setChecked(True)
            b.clicked.connect(lambda _chk, n=name: self._set_detector(n))
            self.det_group.addButton(b)
            self.det_buttons[name] = b
            det_row.addWidget(b)
        il.addLayout(det_row)

        self.hess_sl, self.hess_lbl = self._make_slider("Hessian Threshold:", 100, 1200, 400)
        self.orb_sl, self.orb_lbl = self._make_slider("ORB Max Features:", 100, 1500, 500)
        il.addWidget(self.hess_sl["wrap"])
        il.addWidget(self.orb_sl["wrap"])

        self.upright_chk = QCheckBox("Upright Mode (U-SURF / No Orientation)")
        self.upright_chk.toggled.connect(self._update_view)
        il.addWidget(self.upright_chk)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #334155;")
        il.addWidget(sep)

        self.details_lbl = QLabel()
        self.details_lbl.setObjectName("Mono")
        self.details_lbl.setWordWrap(True)
        il.addWidget(self.details_lbl)
        il.addStretch()

        body.addWidget(inspector)

        # Status Footer
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setObjectName("StatusBar")
        layout.addWidget(self.status_lbl)

    def _make_slider(self, title: str, lo: int, hi: int, default: int) -> tuple[dict, QLabel]:
        wrap = QWidget()
        vl = QVBoxLayout(wrap)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(2)
        top = QHBoxLayout()
        top.addWidget(QLabel(title))
        val_lbl = QLabel(str(default))
        val_lbl.setObjectName("Mono")
        top.addStretch()
        top.addWidget(val_lbl)
        vl.addLayout(top)
        sl = QSlider(Qt.Orientation.Horizontal)
        sl.setRange(lo, hi)
        sl.setValue(default)
        sl.valueChanged.connect(self._update_view)
        vl.addWidget(sl)
        return {"wrap": wrap, "slider": sl}, val_lbl

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if urls:
            path = Path(urls[0].toLocalFile())
            if path.is_file():
                gray = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
                if gray is not None:
                    self.gray1 = gray
                    self.name1 = path.name
                    self._update_view()

    def load_images(self, path1: Path, path2: Path) -> None:
        g1 = cv2.imread(str(path1), cv2.IMREAD_GRAYSCALE)
        g2 = cv2.imread(str(path2), cv2.IMREAD_GRAYSCALE)
        if g1 is not None:
            self.gray1 = g1
            self.name1 = path1.name
        if g2 is not None:
            self.gray2 = g2
            self.name2 = path2.name
        self._update_view()

    def _on_open(self, slot: int) -> None:
        chosen, _ = QFileDialog.getOpenFileName(
            self,
            f"Open Image {slot}",
            str(self.lab_dir),
            "Images (*.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff)",
        )
        if not chosen:
            return
        p = Path(chosen)
        g = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        if g is None:
            return
        if slot == 1:
            self.gray1, self.name1 = g, p.name
        else:
            self.gray2, self.name2 = g, p.name
        self._update_view()

    def _on_reset(self) -> None:
        self.hess_sl["slider"].setValue(400)
        self.orb_sl["slider"].setValue(500)
        self.upright_chk.setChecked(False)
        self.detector_name = "SURF" if self.surf_available else "SIFT"
        self.det_buttons[self.detector_name].setChecked(True)
        self.load_images(self.sample1, self.sample2)

    def _select_tab(self, key: str) -> None:
        self.current_tab = key
        self._update_view()

    def _set_detector(self, name: str) -> None:
        self.detector_name = name
        self._update_view()

    def _update_view(self) -> None:
        if self.gray1 is None or self.gray2 is None:
            return

        hess = self.hess_sl["slider"].value()
        orb_n = self.orb_sl["slider"].value()
        upright = self.upright_chk.isChecked()
        self.hess_lbl.setText(str(hess))
        self.orb_lbl.setText(str(orb_n))

        res_active = run_detector(self.gray1, self.detector_name, hess, orb_n, upright)
        res_sift = run_detector(self.gray1, "SIFT", hess, orb_n, upright)
        res_orb = run_detector(self.gray1, "ORB", hess, orb_n, upright)
        match_res = match_features(self.gray1, self.gray2, self.detector_name, hess, orb_n, upright)

        h1, w1 = self.gray1.shape

        if self.current_tab == "qa":
            for c in self.view_cards:
                c.hide()
            self.qa_card.show()
            self.last_vis = res_active["vis"]
            self.qa_text_lbl.setText(
                f"""
                <h3 style="color:#38bdf8; margin-top:0;">Questions for Students (Lab 4):</h3>

                <p><b>1. What effect does changing the Hessian threshold have on the number of detected keypoints?</b><br>
                Increasing the <code>hessianThreshold</code> makes the detector stricter, so <b>fewer, stronger, and more prominent</b> keypoints are detected.
                Lowering the Hessian threshold relaxes the acceptance criterion, resulting in <b>more keypoints</b> (including weaker corners/blobs and potential background noise).</p>

                <p><b>2. What are the descriptors in SURF used for, and why are they important?</b><br>
                SURF descriptors encode the local intensity gradient pattern (Haar wavelet responses along <i>dx</i> and <i>dy</i> inside sub-regions around each keypoint) into a compact <b>64-dimensional</b> (or 128-D extended) feature vector.
                They are essential because they give each keypoint a distinctive, scale- and rotation-invariant numerical "fingerprint" that enables reliable <b>feature matching</b> across different viewpoints, illumination changes, object recognition, and image stitching.</p>

                <p><b>3. How does SURF compare to SIFT and ORB in feature detection and speed?</b><br>
                <ul>
                  <li><b>SURF vs. SIFT:</b> Both detect blob-like scale-space keypoints, but SURF approximates Laplacian of Gaussian with <b>box filters + integral images</b> (and Haar wavelets), making it ~3× faster than SIFT while using a shorter 64-D descriptor vs. SIFT's 128-D. SIFT is slightly more accurate under large scale/affine changes.</li>
                  <li><b>SURF vs. ORB:</b> ORB uses FAST corners + BRIEF binary descriptors (256-bit / 32-byte), making ORB <b>orders of magnitude faster</b> and patent-free, though slightly less invariant to big scale shifts than SURF/SIFT.</li>
                  <li><b>Measured on {self.name1} ({w1}×{h1}):</b> SIFT found <code>{res_sift['count']}</code> keypoints in <code>{res_sift['time_ms']:.1f} ms</code> (desc <code>{res_sift['desc_shape']}</code>); ORB found <code>{res_orb['count']}</code> keypoints in <code>{res_orb['time_ms']:.1f} ms</code> (desc <code>{res_orb['desc_shape']}</code>).</li>
                </ul></p>

                <h3 style="color:#38bdf8; margin-top:12px;">U-SURF (Upright SURF) &amp; OpenCV Notes:</h3>
                <ul>
                  <li><b>U-SURF (<code>upright=True</code>):</b> Skips dominant orientation assignment for each keypoint. This makes detection faster and works well when camera roll/rotation is minimal (e.g., upright documents, street-level panoramas), at the cost of losing rotation invariance.</li>
                  <li><b>OpenCV Licensing Note:</b> {self.surf_msg} Per the lab manual notes, <b>ORB</b> (and modern patent-expired <b>SIFT</b>) are free built-in alternatives in OpenCV.</li>
                </ul>
                """
            )
        else:
            self.qa_card.hide()
            if self.current_tab == "keypoints":
                panels = [
                    (f"INPUT ({self.name1})", f"{w1}×{h1} gray", self.gray1),
                    (f"{res_active['effective']} RICH KEYPOINTS", f"{res_active['count']} kp • {res_active['time_ms']:.1f} ms", res_active["vis"]),
                ]
                self.last_vis = res_active["vis"]
            elif self.current_tab == "matching":
                panels = [
                    (
                        f"FEATURE MATCHING ({res_active['effective']}: {self.name1} ↔ {self.name2})",
                        f"{match_res['good_count']} good matches • {match_res['match_ms']:.1f} ms",
                        match_res["vis"],
                    )
                ]
                self.last_vis = match_res["vis"]
            else:  # compare
                panels = [
                    ("SIFT KEYPOINTS (128-D Float)", f"{res_sift['count']} kp • {res_sift['time_ms']:.1f} ms", res_sift["vis"]),
                    ("ORB KEYPOINTS (32-B Binary)", f"{res_orb['count']} kp • {res_orb['time_ms']:.1f} ms", res_orb["vis"]),
                ]
                self.last_vis = res_sift["vis"]

            for i in range(2):
                if i < len(panels):
                    title, badge, img = panels[i]
                    self.view_cards[i].show()
                    self.view_titles[i].setText(title)
                    self.view_badges[i].setText(badge)
                    self.canvases[i].set_image(img)
                else:
                    self.view_cards[i].hide()

        self.details_lbl.setText(
            f"Image 1  : {self.name1} ({w1}×{h1})\n"
            f"Image 2  : {self.name2}\n"
            f"Mode     : {'Upright' if upright else 'Rotation-Invariant'}\n\n"
            f"Active ({res_active['effective']}):\n"
            f"  Keypoints : {res_active['count']}\n"
            f"  Desc Shape: {res_active['desc_shape']}\n"
            f"  Detect ms : {res_active['time_ms']:.1f} ms\n"
            f"  Matches   : {match_res['good_count']} good\n\n"
            f"Comparison on Image 1:\n"
            f"  SIFT : {res_sift['count']:>4} kp | {res_sift['time_ms']:5.1f} ms\n"
            f"  ORB  : {res_orb['count']:>4} kp | {res_orb['time_ms']:5.1f} ms"
        )

        self.status_lbl.setText(
            f"{self.name1} ({w1}×{h1}) | Active={res_active['effective']} ({res_active['count']} kp, "
            f"{match_res['good_count']} matches) | SIFT={res_sift['count']} kp ({res_sift['time_ms']:.1f} ms) | "
            f"ORB={res_orb['count']} kp ({res_orb['time_ms']:.1f} ms)"
        )

    def _on_save(self) -> None:
        if self.last_vis is None:
            return
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Feature Visualization",
            str(self.lab_dir / f"lab4_{self.current_tab}.png"),
            "PNG (*.png);;JPEG (*.jpg)",
        )
        if save_path:
            cv2.imwrite(save_path, self.last_vis)


def main() -> None:
    app = QApplication(sys.argv)
    win = Lab4Window(Path(__file__).resolve().parent)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
