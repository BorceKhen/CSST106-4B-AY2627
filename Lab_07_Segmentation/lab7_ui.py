"""
CSST106 - Perception and Computer Vision
Laboratory Exercise No. 7 (Activity 6): Segmentation Technique (PyQt6)

Covers all 4 segmentation methods from the Lab 7 manual:
  1. Thresholding Segmentation : Otsu's Global Thresholding vs. Adaptive Gaussian Thresholding
  2. Region-Based Segmentation : Interactive Seeded Region Growing + Watershed separation
  3. Edge-Based Segmentation   : Canny Edge Detection + Closed Contour extraction
  4. Semantic Segmentation     : Pre-trained DeepLabV3 (MobileNetV3-Large, PASCAL VOC 21 classes)
  + Quantitative IoU evaluation against the sample ground-truth foreground mask
  + Question & Conclusion tab for the A4 bond paper deliverable
"""

from collections import deque
from pathlib import Path
import shutil
import sys
import torch  # Import before PyQt6/cv2 on Windows to avoid c10.dll WinError 1114
from torchvision.models.segmentation import (
    DeepLabV3_MobileNet_V3_Large_Weights,
    deeplabv3_mobilenet_v3_large,
)
import cv2
import numpy as np
from PyQt6.QtCore import Qt, QPoint, QRect, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QDragEnterEvent, QDropEvent, QImage, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
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
from skimage.segmentation import watershed


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


def create_sample_images(objects_path: Path, scene_path: Path) -> np.ndarray:
    """Create a multi-object image (with touching objects + uneven light) and a scene image."""
    objects_path.parent.mkdir(parents=True, exist_ok=True)
    h, w = 420, 560
    gt_mask = np.zeros((h, w), dtype=np.uint8)

    # Background with smooth non-uniform illumination gradient (left darker -> right brighter)
    x_grad = np.linspace(35, 115, w, dtype=np.float32)
    y_grad = np.linspace(45, 80, h, dtype=np.float32)[:, None]
    bg = np.clip((x_grad[None, :] * 0.7 + y_grad * 0.6), 0, 255).astype(np.uint8)
    img = cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR)

    # Touching & distinct foreground objects (brighter than local background)
    objs = [
        ((155, 145), 55, (195, 205, 225)),
        ((240, 165), 52, (205, 210, 230)),  # touches first circle for watershed demo
        ((415, 130), 48, (215, 225, 235)),
        ((165, 315), 50, (190, 200, 215)),
        ((415, 305), 54, (220, 225, 235)),
    ]
    for center, rad, color in objs:
        cv2.circle(img, center, rad, color, -1)
        cv2.circle(gt_mask, center, rad, 255, -1)

    cv2.rectangle(img, (265, 265), (345, 345), (210, 215, 225), -1)
    cv2.rectangle(gt_mask, (265, 265), (345, 345), 255, -1)

    rng = np.random.default_rng(7)
    noise = rng.normal(0, 4.0, img.shape)
    img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    cv2.imwrite(str(objects_path), img)

    # Scene image for DeepLabV3 semantic segmentation (prefer Ultralytics bus.jpg if available)
    if not scene_path.exists():
        try:
            from ultralytics.utils import ASSETS

            bus = Path(ASSETS) / "bus.jpg"
            if bus.exists():
                shutil.copyfile(bus, scene_path)
            else:
                cv2.imwrite(str(scene_path), img)
        except Exception:
            cv2.imwrite(str(scene_path), img)

    return gt_mask


def compute_iou(pred_mask: np.ndarray, gt_mask: np.ndarray) -> float:
    """Compute binary Intersection over Union (IoU)."""
    p = pred_mask > 0
    g = gt_mask > 0
    union = np.logical_or(p, g).sum()
    if union == 0:
        return 0.0
    return float(np.logical_and(p, g).sum()) / float(union)


def region_growing(gray: np.ndarray, seed_yx: tuple[int, int], tolerance: int = 25) -> np.ndarray:
    """Simple BFS region growing starting from seed_yx within intensity tolerance."""
    h, w = gray.shape
    sy = min(max(0, seed_yx[0]), h - 1)
    sx = min(max(0, seed_yx[1]), w - 1)
    seed_val = int(gray[sy, sx])
    mask = np.zeros((h, w), dtype=np.uint8)
    visited = np.zeros((h, w), dtype=bool)

    q = deque([(sy, sx)])
    visited[sy, sx] = True
    while q:
        y, x = q.popleft()
        if abs(int(gray[y, x]) - seed_val) <= tolerance:
            mask[y, x] = 255
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))
    return mask


def classical_segmentations(
    bgr: np.ndarray,
    seed_yx: tuple[int, int],
    grow_tol: int,
    canny_t1: int,
    canny_t2: int,
) -> dict[str, np.ndarray]:
    """Run Thresholding (Otsu + Adaptive), Region-Based (Grow + Watershed), and Edge-Based."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 1. Thresholding: Otsu & Adaptive
    _, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    adaptive = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5
    )

    # 2. Region-Based: Region Growing & Watershed (via scikit-image watershed)
    grown = region_growing(blur, seed_yx, tolerance=grow_tol)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(otsu, cv2.MORPH_OPEN, kernel, iterations=2)
    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.65 * dist.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    ws_labels = watershed(-dist, markers, mask=opening > 0)

    ws_vis = bgr.copy()
    rng = np.random.default_rng(123)
    label_colors = rng.integers(60, 245, size=(int(ws_labels.max()) + 1, 3), dtype=np.uint8)
    label_colors[0] = (15, 23, 42)
    ws_colored = label_colors[ws_labels]
    ws_vis = cv2.addWeighted(ws_vis, 0.45, ws_colored, 0.55, 0)
    ws_mask = np.uint8((ws_labels > 0) * 255)

    # 3. Edge-Based: Canny + Closing + Filled Closed Contours
    edges = cv2.Canny(blur, canny_t1, canny_t2)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edge_mask = np.zeros_like(gray)
    for cnt in contours:
        if cv2.contourArea(cnt) >= 120:
            cv2.drawContours(edge_mask, [cnt], -1, 255, -1)
    edge_vis = bgr.copy()
    cv2.drawContours(edge_vis, [c for c in contours if cv2.contourArea(c) >= 120], -1, (56, 189, 248), 2)

    return {
        "gray": gray,
        "otsu": otsu,
        "adaptive": adaptive,
        "grown": grown,
        "watershed_vis": ws_vis,
        "watershed_mask": ws_mask,
        "watershed_count": int(ws_labels.max()),
        "edges": edges,
        "edge_mask": edge_mask,
        "edge_vis": edge_vis,
    }


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


class SemanticWorker(QThread):
    """Loads DeepLabV3-MobileNetV3 once and runs semantic segmentation in background."""

    finished = pyqtSignal(object, object, object)  # (overlay_bgr, mask_u8, detected_classes)
    failed = pyqtSignal(str)

    def __init__(self, bgr: np.ndarray, cached_bundle: dict) -> None:
        super().__init__()
        self.bgr = bgr
        self.cached_bundle = cached_bundle

    def run(self) -> None:
        try:
            if "model" not in self.cached_bundle:
                weights = DeepLabV3_MobileNet_V3_Large_Weights.DEFAULT
                model = deeplabv3_mobilenet_v3_large(weights=weights).eval()
                self.cached_bundle["model"] = model
                self.cached_bundle["preprocess"] = weights.transforms()

            model = self.cached_bundle["model"]
            preprocess = self.cached_bundle["preprocess"]

            rgb = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2RGB)
            from PIL import Image

            pil_img = Image.fromarray(rgb)
            inp = preprocess(pil_img).unsqueeze(0)
            with torch.no_grad():
                out = model(inp)["out"][0]
            pred_small = out.argmax(0).byte().cpu().numpy()
            pred = cv2.resize(pred_small, (self.bgr.shape[1], self.bgr.shape[0]), interpolation=cv2.INTER_NEAREST)

            color_rgb = VOC_PALETTE[np.clip(pred, 0, len(VOC_PALETTE) - 1)]
            color_bgr = cv2.cvtColor(color_rgb, cv2.COLOR_RGB2BGR)
            overlay = cv2.addWeighted(self.bgr, 0.45, color_bgr, 0.55, 0)

            unique_ids = [int(i) for i in np.unique(pred) if i > 0 and i < len(VOC_CLASSES)]
            classes = [VOC_CLASSES[i] for i in unique_ids]
            self.finished.emit(overlay, pred, classes)
        except Exception as exc:
            self.failed.emit(str(exc))


class ImageCanvas(QWidget):
    """Aspect-ratio-preserving image viewer with optional click-to-set seed point."""

    pixelClicked = pyqtSignal(int, int)

    def __init__(self, clickable: bool = False) -> None:
        super().__init__()
        self.clickable = clickable
        self._pixmap: QPixmap | None = None
        self._img_w = 0
        self._img_h = 0
        self._draw_rect = QRect()
        self.seed_yx: tuple[int, int] | None = None
        if clickable:
            self.setCursor(Qt.CursorShape.CrossCursor)

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
        self._draw_rect = QRect(ox, oy, dw, dh)
        painter.drawPixmap(self._draw_rect, self._pixmap)

        if self.seed_yx is not None and self.clickable:
            sy, sx = self.seed_yx
            cx = int(ox + (sx / max(1, self._img_w)) * dw)
            cy = int(oy + (sy / max(1, self._img_h)) * dh)
            painter.setPen(QPen(QColor("#fbbf24"), 2))
            painter.drawEllipse(QPoint(cx, cy), 6, 6)

    def mousePressEvent(self, event) -> None:
        if not self.clickable or self._pixmap is None or not self._draw_rect.contains(event.pos()):
            return
        dx = event.pos().x() - self._draw_rect.x()
        dy = event.pos().y() - self._draw_rect.y()
        px = min(self._img_w - 1, max(0, int(dx * self._img_w / max(1, self._draw_rect.width()))))
        py = min(self._img_h - 1, max(0, int(dy * self._img_h / max(1, self._draw_rect.height()))))
        self.pixelClicked.emit(py, px)


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
"""


class Lab7Window(QMainWindow):
    """Tabbed interactive UI for CSST106 Lab 7 Segmentation Techniques."""

    TABS = [
        ("compare", "Compare All 4"),
        ("threshold", "Thresholding"),
        ("region", "Region-Based"),
        ("edge", "Edge-Based"),
        ("semantic", "Semantic (DeepLabV3)"),
        ("qa", "Question && Conclusion"),
    ]

    def __init__(self, lab_dir: Path) -> None:
        super().__init__()
        self.lab_dir = lab_dir
        self.objects_path = lab_dir / "sample_objects.png"
        self.scene_path = lab_dir / "sample_scene.jpg"
        self.gt_mask = create_sample_images(self.objects_path, self.scene_path)

        self.bgr_img: np.ndarray | None = None
        self.current_filename = ""
        self.is_default_objects = True
        self.current_tab = "compare"
        self.seed_yx = (145, 155)

        self.res: dict = {}
        self.semantic_bundle: dict = {}
        self.semantic_overlay: np.ndarray | None = None
        self.semantic_classes: list[str] = []
        self.semantic_status = "Pending..."
        self._sem_worker: SemanticWorker | None = None

        self.setWindowTitle("CSST106 Lab 7 — Image Segmentation Techniques")
        self.resize(1320, 770)
        self.setMinimumSize(1020, 640)
        self.setAcceptDrops(True)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()
        self.load_image(self.objects_path, is_default_objects=True)

    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        # Header
        top_bar = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        lbl_title = QLabel("CSST106 Lab 7: Image Segmentation Techniques")
        lbl_title.setObjectName("Title")
        lbl_sub = QLabel("Thresholding (Otsu & Adaptive), Region-Based (Region Growing & Watershed), Edge-Based, and Semantic (DeepLabV3).")
        lbl_sub.setObjectName("Muted")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        top_bar.addLayout(title_box, 1)

        for text, handler, accent in [
            ("Objects Sample", lambda: self.load_image(self.objects_path, True), False),
            ("Scene Sample", lambda: self.load_image(self.scene_path, False), False),
            ("Open Image...", self._on_open, False),
            ("Save Comparison...", self._on_save_comparison, True),
        ]:
            btn = QPushButton(text)
            if accent:
                btn.setObjectName("AccentBtn")
            btn.clicked.connect(handler)
            top_bar.addWidget(btn)
        layout.addLayout(top_bar)

        # Tabs
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
        self.tab_buttons["compare"].setChecked(True)
        layout.addWidget(tab_panel)

        # Body
        body = QHBoxLayout()
        body.setSpacing(10)
        layout.addLayout(body, 1)

        self.view_cards: list[QFrame] = []
        self.view_titles: list[QLabel] = []
        self.view_badges: list[QLabel] = []
        self.canvases: list[ImageCanvas] = []
        for idx in range(4):
            card = QFrame()
            card.setObjectName("Panel")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(8, 7, 8, 8)
            cl.setSpacing(5)
            hdr = QHBoxLayout()
            tl = QLabel("-")
            tl.setObjectName("Section")
            bl = QLabel("-")
            bl.setObjectName("Muted")
            hdr.addWidget(tl)
            hdr.addStretch()
            hdr.addWidget(bl)
            cl.addLayout(hdr)
            canvas = ImageCanvas(clickable=(idx == 0))
            if idx == 0:
                canvas.pixelClicked.connect(self._on_seed_clicked)
            cl.addWidget(canvas, 1)
            body.addWidget(card, 1)
            self.view_cards.append(card)
            self.view_titles.append(tl)
            self.view_badges.append(bl)
            self.canvases.append(canvas)

        # Q&A Card
        self.qa_card = QFrame()
        self.qa_card.setObjectName("Panel")
        qal = QVBoxLayout(self.qa_card)
        qal.setContentsMargins(16, 14, 16, 14)
        qal.setSpacing(8)
        qa_hdr = QLabel("LAB 7 — QUESTION (A4 BOND PAPER) & CONCLUSION")
        qa_hdr.setObjectName("Section")
        qal.addWidget(qa_hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        il_inner = QVBoxLayout(inner)
        il_inner.setContentsMargins(0, 0, 8, 0)
        self.qa_text_lbl = QLabel()
        self.qa_text_lbl.setWordWrap(True)
        self.qa_text_lbl.setTextFormat(Qt.TextFormat.RichText)
        self.qa_text_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.qa_text_lbl.setStyleSheet("color: #e2e8f0; font-size: 13px; line-height: 1.5;")
        il_inner.addWidget(self.qa_text_lbl)
        il_inner.addStretch()
        scroll.setWidget(inner)
        qal.addWidget(scroll, 1)
        self.qa_card.hide()
        body.addWidget(self.qa_card, 1)

        # Right Controls & IoU Metrics Drawer
        inspector = QFrame()
        inspector.setObjectName("Panel")
        inspector.setFixedWidth(295)
        il = QVBoxLayout(inspector)
        il.setContentsMargins(12, 10, 12, 12)
        il.setSpacing(9)

        hdr_p = QLabel("PARAMETERS & METRICS")
        hdr_p.setObjectName("Section")
        il.addWidget(hdr_p)

        self.tol_sl, self.tol_lbl = self._make_slider("Region Grow Tolerance:", 5, 80, 30)
        self.c1_sl, self.c1_lbl = self._make_slider("Edge Canny T1:", 10, 200, 50)
        self.c2_sl, self.c2_lbl = self._make_slider("Edge Canny T2:", 20, 255, 140)
        il.addWidget(self.tol_sl["wrap"])
        il.addWidget(self.c1_sl["wrap"])
        il.addWidget(self.c2_sl["wrap"])

        sem_btn = QPushButton("Run DeepLabV3 Semantic")
        sem_btn.setObjectName("AccentBtn")
        sem_btn.clicked.connect(self._run_semantic_async)
        il.addWidget(sem_btn)

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
        sl.valueChanged.connect(self._update_classical)
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
                self.load_image(path, is_default_objects=False)

    def _on_open(self) -> None:
        chosen, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            str(self.lab_dir),
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if chosen:
            self.load_image(Path(chosen), is_default_objects=False)

    def load_image(self, path: Path, is_default_objects: bool = False) -> None:
        bgr = cv2.imread(str(path))
        if bgr is None:
            return
        self.bgr_img = bgr
        self.current_filename = path.name
        self.is_default_objects = is_default_objects
        h, w = bgr.shape[:2]
        self.seed_yx = (min(145, h // 2), min(155, w // 2))
        self.semantic_overlay = None
        self.semantic_classes = []
        self.semantic_status = "Click 'Run DeepLabV3 Semantic' or switch to Semantic tab"
        self._update_classical()
        if self.current_tab in ("semantic", "compare"):
            self._run_semantic_async()

    def _on_seed_clicked(self, y: int, x: int) -> None:
        self.seed_yx = (y, x)
        self._update_classical()

    def _select_tab(self, key: str) -> None:
        self.current_tab = key
        if key == "semantic" and self.semantic_overlay is None:
            self._run_semantic_async()
        self._render_view()

    def _run_semantic_async(self) -> None:
        if self.bgr_img is None:
            return
        if self._sem_worker is not None and self._sem_worker.isRunning():
            return
        self.semantic_status = "Running DeepLabV3..."
        self._render_view()
        self._sem_worker = SemanticWorker(self.bgr_img.copy(), self.semantic_bundle)
        self._sem_worker.finished.connect(self._on_semantic_done)
        self._sem_worker.failed.connect(self._on_semantic_err)
        self._sem_worker.start()

    def _on_semantic_done(self, overlay: np.ndarray, _mask: np.ndarray, classes: list[str]) -> None:
        self.semantic_overlay = overlay
        self.semantic_classes = classes
        self.semantic_status = ", ".join(classes) if classes else "background only"
        self._render_view()

    def _on_semantic_err(self, err: str) -> None:
        self.semantic_status = f"Error: {err}"
        self._render_view()

    def _update_classical(self) -> None:
        if self.bgr_img is None:
            return
        tol = self.tol_sl["slider"].value()
        t1 = self.c1_sl["slider"].value()
        t2 = self.c2_sl["slider"].value()
        self.tol_lbl.setText(str(tol))
        self.c1_lbl.setText(str(t1))
        self.c2_lbl.setText(str(t2))
        self.res = classical_segmentations(self.bgr_img, self.seed_yx, tol, t1, t2)
        self._render_view()

    def _render_view(self) -> None:
        if self.bgr_img is None or not self.res:
            return
        h, w = self.bgr_img.shape[:2]
        self.canvases[0].seed_yx = self.seed_yx if self.current_tab == "region" else None

        iou_txt = ""
        if self.is_default_objects and self.gt_mask.shape == (h, w):
            iou_otsu = compute_iou(self.res["otsu"], self.gt_mask)
            iou_adap = compute_iou(self.res["adaptive"], self.gt_mask)
            iou_ws = compute_iou(self.res["watershed_mask"], self.gt_mask)
            iou_edge = compute_iou(self.res["edge_mask"], self.gt_mask)
            iou_txt = (
                f"\nIoU vs. Ground Truth:\n"
                f"  Otsu Thresh : {iou_otsu:.3f}\n"
                f"  Adaptive    : {iou_adap:.3f}\n"
                f"  Watershed   : {iou_ws:.3f}\n"
                f"  Edge Contour: {iou_edge:.3f}"
            )

        if self.current_tab == "qa":
            for c in self.view_cards:
                c.hide()
            self.qa_card.show()
            self.qa_text_lbl.setText(
                """
                <h3 style="color:#38bdf8; margin-top:0;">Question (on A4 bond paper):</h3>
                <p><i>Explain the differences between thresholding, region-based, edge-based, and semantic segmentation techniques. Provide one advantage and one limitation for each method.</i></p>

                <h3 style="color:#38bdf8; margin-top:10px;">Answer:</h3>
                <p><b>1. Thresholding Segmentation (Global Otsu / Adaptive):</b><br>
                Partitions pixels purely by comparing intensity values against a global or local threshold into foreground/background.<br>
                • <i>Advantage:</i> Extremely fast, simple, and requires minimal computation.<br>
                • <i>Limitation:</i> Fails on complex textures or overlapping objects with similar intensities; global thresholds struggle under uneven lighting.</p>

                <p><b>2. Region-Based Segmentation (Region Growing / Watershed):</b><br>
                Groups neighboring pixels based on spatial connectivity and similarity criteria (region growing from seeds, or watershed treating intensity/distance as topography to separate touching objects).<br>
                • <i>Advantage:</i> Produces connected regions and effectively separates touching objects (e.g., Watershed).<br>
                • <i>Limitation:</i> Sensitive to seed selection and prone to over-segmentation in noisy/textured images.</p>

                <p><b>3. Edge-Based Segmentation (Canny + Closed Contours):</b><br>
                Locates abrupt intensity gradients/boundaries first, then links edges into closed object contours.<br>
                • <i>Advantage:</i> Works well when clear boundary contrast exists even if interior brightness varies.<br>
                • <i>Limitation:</i> Sensitive to noise and broken/incomplete edge chains that fail to form closed contours.</p>

                <p><b>4. Semantic Segmentation (DeepLabV3 / U-Net):</b><br>
                Uses deep convolutional neural networks to classify <i>every single pixel</i> into semantic object categories (e.g., person, bus, car) using learned high-level context.<br>
                • <i>Advantage:</i> Handles complex natural scenes and overlapping categories with high accuracy.<br>
                • <i>Limitation:</i> Computationally heavy and requires large pixel-annotated datasets (PASCAL VOC / COCO) for training.</p>

                <h3 style="color:#38bdf8; margin-top:10px;">Conclusion:</h3>
                <p>
                Classical methods (thresholding, region-based, edge-based) are lightweight and effective for controlled, high-contrast, or single-object tasks, while deep semantic segmentation (such as DeepLabV3) is necessary for rich multi-class scene understanding at higher computational cost.
                </p>
                """
            )
        else:
            self.qa_card.hide()
            sem_img = self.semantic_overlay if self.semantic_overlay is not None else self.bgr_img
            if self.current_tab == "compare":
                panels = [
                    ("1. THRESHOLDING (OTSU)", "Foreground/Bg", self.res["otsu"]),
                    ("2. REGION (WATERSHED)", f"{self.res['watershed_count']} regions", self.res["watershed_vis"]),
                    ("3. EDGE (CLOSED CONTOURS)", "Canny + Fill", self.res["edge_vis"]),
                    ("4. SEMANTIC (DEEPLABV3)", f"{len(self.semantic_classes)} cls", sem_img),
                ]
            elif self.current_tab == "threshold":
                panels = [
                    ("OTSU GLOBAL THRESHOLD", "Single threshold", self.res["otsu"]),
                    ("ADAPTIVE GAUSSIAN", "Local 35×35", self.res["adaptive"]),
                ]
            elif self.current_tab == "region":
                panels = [
                    ("INPUT (CLICK SEED)", f"Seed={self.seed_yx}", self.bgr_img),
                    ("REGION GROWING", f"tol={self.tol_sl['slider'].value()}", self.res["grown"]),
                    ("WATERSHED", f"{self.res['watershed_count']} objects", self.res["watershed_vis"]),
                ]
            elif self.current_tab == "edge":
                panels = [
                    ("CANNY EDGES", f"T=({self.c1_sl['slider'].value()}, {self.c2_sl['slider'].value()})", self.res["edges"]),
                    ("CLOSED CONTOUR MASK", "Filled regions", self.res["edge_mask"]),
                ]
            else:  # semantic
                panels = [
                    ("INPUT IMAGE", f"{w}×{h}", self.bgr_img),
                    ("DEEPLABV3 (PASCAL VOC)", self.semantic_status, sem_img),
                ]

            for i in range(4):
                if i < len(panels):
                    title, badge, img = panels[i]
                    self.view_cards[i].show()
                    self.view_titles[i].setText(title)
                    self.view_badges[i].setText(badge)
                    self.canvases[i].set_image(img)
                else:
                    self.view_cards[i].hide()

        self.details_lbl.setText(
            f"Image   : {self.current_filename} ({w}×{h})\n"
            f"Seed    : {self.seed_yx}\n"
            f"Watersh.: {self.res['watershed_count']} labeled objects\n"
            f"Semantic: {self.semantic_status}"
            f"{iou_txt}"
        )
        self.status_lbl.setText(
            f"{self.current_filename} ({w}×{h}) | Watershed={self.res['watershed_count']} objects | "
            f"Semantic={self.semantic_status}"
        )

    def _on_save_comparison(self) -> None:
        if not self.res:
            return
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Segmentation Comparison",
            str(self.lab_dir / "segmentation_comparison.png"),
            "PNG (*.png);;JPEG (*.jpg)",
        )
        if not save_path:
            return
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 4, figsize=(15, 4.2))
        sem_img = self.semantic_overlay if self.semantic_overlay is not None else self.bgr_img
        for ax, img, title in [
            (axes[0], self.res["otsu"], "1. Thresholding (Otsu)"),
            (axes[1], self.res["watershed_vis"], "2. Region (Watershed)"),
            (axes[2], self.res["edge_vis"], "3. Edge (Contours)"),
            (axes[3], sem_img, "4. Semantic (DeepLabV3)"),
        ]:
            if img.ndim == 2:
                ax.imshow(img, cmap="gray")
            else:
                ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            ax.set_title(title, fontsize=10.5, fontweight="bold")
            ax.axis("off")
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)


def main() -> None:
    app = QApplication(sys.argv)
    win = Lab7Window(Path(__file__).resolve().parent)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
