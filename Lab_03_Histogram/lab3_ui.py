"""
CSST106 - Perception and Computer Vision
Laboratory Exercise No. 3: Histogram Equalization and Contrast Adjustment (PyQt6)

Standalone interactive display UI covering all Lab 3 procedures:
  - Part 1: Grayscale & Color (YUV Luminance) Histogram Equalization (cv2.equalizeHist)
  - Part 2: Linear Contrast Stretching + Adaptive Histogram Equalization (CLAHE)
  - Live 256-bin histogram plots for every image panel
  - Question & Conclusion tab with Part 4 observations, all 5 Q&As, and Conclusion
"""

from pathlib import Path
import sys
import cv2
import numpy as np
from PyQt6.QtCore import Qt, QPointF, QRect
from PyQt6.QtGui import (
    QColor,
    QDragEnterEvent,
    QDropEvent,
    QImage,
    QPainter,
    QPen,
    QPixmap,
    QPolygonF,
)
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


def create_low_contrast_sample(save_path: Path, width: int = 640, height: int = 480) -> np.ndarray:
    """Create a synthetic low-contrast foggy scene whose intensities sit mostly in [65..145]."""
    rng = np.random.default_rng(42)
    img = np.full((height, width, 3), (125, 118, 110), dtype=np.uint8)

    # Misty sky gradient compressed into narrow dynamic range
    for y in range(280):
        t = y / 280.0
        img[y, :] = (int(142 - 18 * t), int(134 - 14 * t), int(124 - 10 * t))

    # Ground plane
    img[280:, :] = (92, 102, 88)

    # Distant low-contrast mountain ridge
    mountain = np.array([[0, 280], [130, 175], [260, 235], [410, 155], [560, 225], [640, 195], [640, 280]], np.int32)
    cv2.fillPoly(img, [mountain], (108, 108, 102))

    # Dim building with subtle window details
    cv2.rectangle(img, (190, 200), (410, 385), (105, 100, 95), -1)
    roof = np.array([[170, 200], [300, 130], [430, 200]], np.int32)
    cv2.fillPoly(img, [roof], (88, 86, 112))
    cv2.rectangle(img, (275, 295), (325, 385), (78, 76, 74), -1)
    cv2.rectangle(img, (215, 225), (255, 265), (128, 132, 126), -1)
    cv2.rectangle(img, (345, 225), (385, 265), (128, 132, 126), -1)

    # Subtle hazy sun
    cv2.circle(img, (525, 100), 42, (132, 140, 145), -1)

    # Subtle textured grass/road details + mild sensor noise to illustrate noise amplification
    for x in range(40, 600, 35):
        cv2.circle(img, (x, 420 + (x % 20)), 10, (82, 95, 80), -1)
    cv2.putText(img, "LOW CONTRAST", (30, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (145, 145, 142), 2, cv2.LINE_AA)

    noise = rng.normal(0, 2.5, size=img.shape)
    img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(save_path), img)
    return img


def cv_to_qpixmap(img: np.ndarray) -> QPixmap:
    """Convert grayscale or BGR uint8 image to QPixmap."""
    if img.ndim == 2:
        h, w = img.shape
        qimg = QImage(img.data, w, h, w, QImage.Format.Format_Grayscale8)
        return QPixmap.fromImage(qimg.copy())
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimg.copy())


def compute_intensity_hist(img: np.ndarray) -> np.ndarray:
    """Return 256-bin histogram of grayscale or Y-luminance intensity."""
    if img.ndim == 3:
        lum = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:, :, 0]
    else:
        lum = img
    hist = cv2.calcHist([lum], [0], None, [256], [0, 256]).ravel()
    return hist


def process_contrast_variants(
    bgr: np.ndarray,
    use_color: bool,
    clip_limit: float,
    tile_size: int,
    low_pct: int,
    high_pct: int,
) -> dict[str, np.ndarray]:
    """Compute Original, Linear Contrast Stretched, Global Equalized, and CLAHE variants."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))

    def stretch_channel(ch: np.ndarray) -> np.ndarray:
        lo = float(np.percentile(ch, low_pct))
        hi = float(np.percentile(ch, high_pct))
        if hi <= lo:
            return ch.copy()
        scaled = (ch.astype(np.float32) - lo) * (255.0 / (hi - lo))
        return np.clip(scaled, 0, 255).astype(np.uint8)

    if not use_color:
        orig = gray
        global_eq = cv2.equalizeHist(gray)
        clahe_out = clahe.apply(gray)
        stretched = stretch_channel(gray)
    else:
        orig = bgr.copy()

        def apply_on_yuv(fn) -> np.ndarray:
            yuv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV)
            yuv[:, :, 0] = fn(yuv[:, :, 0])
            return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

        global_eq = apply_on_yuv(cv2.equalizeHist)
        clahe_out = apply_on_yuv(clahe.apply)
        stretched = apply_on_yuv(stretch_channel)

    return {
        "orig": orig,
        "stretched": stretched,
        "global": global_eq,
        "clahe": clahe_out,
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

        pad = 6
        avail_w = max(1, self.width() - 2 * pad)
        avail_h = max(1, self.height() - 2 * pad)
        scale = min(avail_w / self._img_w, avail_h / self._img_h)
        dw = max(1, int(self._img_w * scale))
        dh = max(1, int(self._img_h * scale))
        ox = (self.width() - dw) // 2
        oy = (self.height() - dh) // 2
        painter.drawPixmap(QRect(ox, oy, dw, dh), self._pixmap)


class HistogramWidget(QWidget):
    """Lightweight, crisp 256-bin intensity histogram plot rendered with QPainter."""

    def __init__(self, accent: str = "#38bdf8") -> None:
        super().__init__()
        self.setFixedHeight(115)
        self._hist: np.ndarray | None = None
        self._accent = QColor(accent)

    def set_histogram(self, img: np.ndarray | None) -> None:
        self._hist = compute_intensity_hist(img) if img is not None else None
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0b1120"))

        w = self.width()
        h = self.height()
        pad_l, pad_r, pad_t, pad_b = 8, 8, 8, 18
        pw = max(1, w - pad_l - pad_r)
        ph = max(1, h - pad_t - pad_b)

        # Subtle baseline & gridlines
        painter.setPen(QPen(QColor("#1e293b"), 1))
        for frac in (0.25, 0.5, 0.75):
            y = int(pad_t + ph * frac)
            painter.drawLine(pad_l, y, pad_l + pw, y)
        painter.setPen(QPen(QColor("#334155"), 1))
        painter.drawLine(pad_l, pad_t + ph, pad_l + pw, pad_t + ph)

        # Axis labels 0, 128, 255
        painter.setPen(QColor("#64748b"))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(pad_l, h - 4, "0")
        painter.drawText(pad_l + pw // 2 - 10, h - 4, "128")
        painter.drawText(pad_l + pw - 20, h - 4, "255")

        if self._hist is None or self._hist.max() <= 0:
            return

        # Normalize using 99th percentile cap so spikes don't crush the whole curve
        cap = max(float(np.percentile(self._hist, 98.5)), float(self._hist.max()) * 0.35, 1.0)
        poly = QPolygonF()
        poly.append(QPointF(pad_l, pad_t + ph))
        for i in range(256):
            x = pad_l + (i / 255.0) * pw
            norm = min(1.0, float(self._hist[i]) / cap)
            y = pad_t + ph - norm * ph
            poly.append(QPointF(x, y))
        poly.append(QPointF(pad_l + pw, pad_t + ph))

        fill_color = QColor(self._accent)
        fill_color.setAlpha(95)
        painter.setBrush(fill_color)
        painter.setPen(QPen(self._accent, 1.5))
        painter.drawPolygon(poly)


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
"""


class Lab3Window(QMainWindow):
    """Tabbed interactive UI for CSST106 Lab 3 Histogram Equalization & Contrast Adjustment."""

    TABS = [
        ("compare", "Compare (All 3)"),
        ("global", "Global Equalization"),
        ("stretch", "Contrast Stretching"),
        ("clahe", "CLAHE Tuning"),
        ("qa", "Questions && Conclusion"),
    ]

    def __init__(self, lab_dir: Path) -> None:
        super().__init__()
        self.lab_dir = lab_dir
        self.default_sample = lab_dir / "sample_low_contrast.png"

        self.bgr_img: np.ndarray | None = None
        self.results: dict[str, np.ndarray] = {}
        self.current_filename = ""
        self.current_tab = "compare"
        self.use_color = False
        self.tile_size = 8

        self.setWindowTitle("CSST106 Lab 3 — Histogram Equalization & Contrast Adjustment")
        self.resize(1300, 760)
        self.setMinimumSize(1000, 640)
        self.setAcceptDrops(True)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()

        if not self.default_sample.exists():
            create_low_contrast_sample(self.default_sample)
        self.load_image(self.default_sample)

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
        lbl_title = QLabel("CSST106 Lab 3: Histogram Equalization & Contrast Adjustment")
        lbl_title.setObjectName("Title")
        lbl_sub = QLabel("Compare Global Equalization, Linear Contrast Stretching, and Adaptive CLAHE with live histograms.")
        lbl_sub.setObjectName("Muted")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        top_bar.addLayout(title_box, 1)

        for text, handler, accent in [
            ("Open Image...", self._on_open, False),
            ("Reset", self._on_reset, False),
            ("Save Comparison...", self._on_save_comparison, True),
        ]:
            btn = QPushButton(text)
            if accent:
                btn.setObjectName("AccentBtn")
            btn.clicked.connect(handler)
            top_bar.addWidget(btn)
        layout.addLayout(top_bar)

        # Horizontal Tabs
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

        # Body: 3 Image+Histogram Panels + Right Parameters Panel
        body = QHBoxLayout()
        body.setSpacing(10)
        layout.addLayout(body, 1)

        self.view_cards: list[QFrame] = []
        self.view_titles: list[QLabel] = []
        self.view_badges: list[QLabel] = []
        self.canvases: list[ImageCanvas] = []
        self.hists: list[HistogramWidget] = []

        accents = ["#94a3b8", "#38bdf8", "#34d399"]
        for i in range(3):
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

            hist_lbl = QLabel("INTENSITY HISTOGRAM (0–255)")
            hist_lbl.setObjectName("Muted")
            cl.addWidget(hist_lbl)

            hist = HistogramWidget(accent=accents[i])
            cl.addWidget(hist)

            body.addWidget(card, 1)
            self.view_cards.append(card)
            self.view_titles.append(tlbl)
            self.view_badges.append(blbl)
            self.canvases.append(canvas)
            self.hists.append(hist)

        # Q&A and Conclusion Card
        self.qa_card = QFrame()
        self.qa_card.setObjectName("Panel")
        qal = QVBoxLayout(self.qa_card)
        qal.setContentsMargins(16, 14, 16, 14)
        qal.setSpacing(10)

        qa_hdr = QLabel("LAB 3 — OBSERVATIONS, QUESTIONS & CONCLUSION")
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

        # Right Controls & Contrast Metrics Drawer
        inspector = QFrame()
        inspector.setObjectName("Panel")
        inspector.setFixedWidth(300)
        il = QVBoxLayout(inspector)
        il.setContentsMargins(12, 10, 12, 12)
        il.setSpacing(9)

        hdr_p = QLabel("PARAMETERS & METRICS")
        hdr_p.setObjectName("Section")
        il.addWidget(hdr_p)

        # Color mode selector
        il.addWidget(QLabel("Image Mode:"))
        mode_row = QHBoxLayout()
        self.color_group = QButtonGroup(self)
        self.color_group.setExclusive(True)
        self.btn_gray_mode = QPushButton("Grayscale")
        self.btn_color_mode = QPushButton("Color (YUV Luma)")
        for b, is_col in [(self.btn_gray_mode, False), (self.btn_color_mode, True)]:
            b.setObjectName("ChipBtn")
            b.setCheckable(True)
            b.clicked.connect(lambda _chk, c=is_col: self._set_color_mode(c))
            self.color_group.addButton(b)
            mode_row.addWidget(b)
        self.btn_gray_mode.setChecked(True)
        il.addLayout(mode_row)

        # CLAHE Clip Limit slider (1.0 .. 10.0 mapped as 10..100)
        self.clip_sl, self.clip_lbl = self._make_slider("CLAHE Clip Limit:", 10, 100, 20, lambda v: f"{v / 10:.1f}")
        il.addWidget(self.clip_sl["wrap"])

        # CLAHE Tile Grid selector
        il.addWidget(QLabel("CLAHE Tile Grid Size:"))
        tile_row = QHBoxLayout()
        self.tile_group = QButtonGroup(self)
        self.tile_group.setExclusive(True)
        self.tile_buttons: dict[int, QPushButton] = {}
        for t in (4, 8, 16):
            b = QPushButton(f"{t}×{t}")
            b.setObjectName("ChipBtn")
            b.setCheckable(True)
            if t == 8:
                b.setChecked(True)
            b.clicked.connect(lambda _chk, val=t: self._set_tile_size(val))
            self.tile_group.addButton(b)
            self.tile_buttons[t] = b
            tile_row.addWidget(b)
        il.addLayout(tile_row)

        # Linear Contrast Stretch percentile sliders
        self.low_sl, self.low_lbl = self._make_slider("Stretch Low %:", 0, 20, 1, lambda v: f"{v}%")
        self.high_sl, self.high_lbl = self._make_slider("Stretch High %:", 80, 100, 99, lambda v: f"{v}%")
        il.addWidget(self.low_sl["wrap"])
        il.addWidget(self.high_sl["wrap"])

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

        # Bottom Status Bar
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setObjectName("StatusBar")
        layout.addWidget(self.status_lbl)

    def _make_slider(self, title: str, lo: int, hi: int, default: int, fmt) -> tuple[dict, QLabel]:
        wrap = QWidget()
        vl = QVBoxLayout(wrap)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(2)

        top = QHBoxLayout()
        top.addWidget(QLabel(title))
        val_lbl = QLabel(fmt(default))
        val_lbl.setObjectName("Mono")
        top.addStretch()
        top.addWidget(val_lbl)
        vl.addLayout(top)

        sl = QSlider(Qt.Orientation.Horizontal)
        sl.setRange(lo, hi)
        sl.setValue(default)
        sl.valueChanged.connect(self._update_view)
        vl.addWidget(sl)
        return {"wrap": wrap, "slider": sl, "fmt": fmt}, val_lbl

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if urls:
            path = Path(urls[0].toLocalFile())
            if path.is_file():
                self.load_image(path)

    def load_image(self, path: Path) -> None:
        bgr = cv2.imread(str(path))
        if bgr is None:
            return
        self.bgr_img = bgr
        self.current_filename = path.name
        self._update_view()

    def _on_open(self) -> None:
        chosen, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            str(self.lab_dir),
            "Images (*.png *.jpg *.jpeg *.bmp *.webp *.tif *.tiff)",
        )
        if chosen:
            self.load_image(Path(chosen))

    def _on_reset(self) -> None:
        self.use_color = False
        self.btn_gray_mode.setChecked(True)
        self.tile_size = 8
        self.tile_buttons[8].setChecked(True)
        self.clip_sl["slider"].setValue(20)
        self.low_sl["slider"].setValue(1)
        self.high_sl["slider"].setValue(99)
        self._update_view()

    def _select_tab(self, key: str) -> None:
        self.current_tab = key
        self._update_view()

    def _set_color_mode(self, is_color: bool) -> None:
        self.use_color = is_color
        self._update_view()

    def _set_tile_size(self, tile: int) -> None:
        self.tile_size = tile
        self._update_view()

    @staticmethod
    def _luma_stats(img: np.ndarray) -> tuple[int, int, float, float]:
        lum = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:, :, 0] if img.ndim == 3 else img
        return int(lum.min()), int(lum.max()), float(lum.mean()), float(lum.std())

    def _update_view(self) -> None:
        if self.bgr_img is None:
            return

        clip_limit = self.clip_sl["slider"].value() / 10.0
        low_pct = self.low_sl["slider"].value()
        high_pct = self.high_sl["slider"].value()
        self.clip_lbl.setText(f"{clip_limit:.1f}")
        self.low_lbl.setText(f"{low_pct}%")
        self.high_lbl.setText(f"{high_pct}%")

        self.results = process_contrast_variants(
            self.bgr_img, self.use_color, clip_limit, self.tile_size, low_pct, high_pct
        )
        h, w = self.bgr_img.shape[:2]

        s_orig = self._luma_stats(self.results["orig"])
        s_str = self._luma_stats(self.results["stretched"])
        s_glob = self._luma_stats(self.results["global"])
        s_clahe = self._luma_stats(self.results["clahe"])

        if self.current_tab == "qa":
            for card in self.view_cards:
                card.hide()
            self.qa_card.show()
            mode_name = "Color (YUV Luminance Y)" if self.use_color else "Grayscale"
            self.qa_text_lbl.setText(
                f"""
                <h3 style="color:#38bdf8; margin-top:0;">Part 4 — Observations ({self.current_filename}, {mode_name}):</h3>
                <ul>
                  <li><b>Contrast Spread:</b> Original intensity range is <code>[{s_orig[0]}, {s_orig[1]}]</code> (StdDev=<code>{s_orig[3]:.1f}</code>). Linear stretching expands it to <code>[{s_str[0]}, {s_str[1]}]</code> (StdDev=<code>{s_str[3]:.1f}</code>), Global Equalization expands it to <code>[{s_glob[0]}, {s_glob[1]}]</code> (StdDev=<code>{s_glob[3]:.1f}</code>), and CLAHE achieves StdDev=<code>{s_clahe[3]:.1f}</code>.</li>
                  <li><b>Global Equalization vs. CLAHE:</b> Standard <code>cv2.equalizeHist()</code> applies one global mapping across the entire image, which can over-brighten large uniform regions (sky/background) and wash out subtle mid-tone details. <b>CLAHE</b> operates on local <code>{self.tile_size}×{self.tile_size}</code> tiles with <code>clipLimit={clip_limit:.1f}</code>, revealing local structures (building windows, ridge lines, grass texture) without blowing out global brightness.</li>
                  <li><b>Noise Amplification:</b> Raising <code>clipLimit</code> or applying global equalization on flat/noisy sky regions amplifies minor sensor noise into visible grain.</li>
                </ul>

                <h3 style="color:#38bdf8; margin-top:12px;">Questions to Answer:</h3>
                <p><b>1. What is histogram equalization?</b><br>
                Histogram equalization is a point-processing contrast enhancement technique that redistributes pixel intensity values so the image's histogram becomes more uniformly spread across the full <code>0–255</code> dynamic range.</p>

                <p><b>2. Why do we need histogram equalization?</b><br>
                Images captured under poor lighting, fog, or narrow exposure often have pixel intensities clustered in a tight range, making details hard to distinguish. Equalization stretches those clustered intensities apart, improving visibility for human inspection and downstream vision algorithms.</p>

                <p><b>3. How does histogram equalization work?</b><br>
                It computes the image's intensity histogram, converts it to a normalized Probability Density Function (PDF), accumulates the Cumulative Distribution Function (CDF), and maps each input intensity <i>r</i> to <code>round((L - 1) × CDF(r))</code> (where <code>L = 256</code>). For color images, equalization is applied only to the luminance channel (e.g., <code>Y</code> in YUV or <code>V</code> in HSV) to avoid distorting hue/saturation.</p>

                <p><b>4. How does CLAHE work?</b><br>
                <b>Contrast Limited Adaptive Histogram Equalization (CLAHE)</b> divides the image into small rectangular tiles (e.g., <code>{self.tile_size}×{self.tile_size}</code>), clips each tile's histogram at a threshold (<code>clipLimit</code>) and redistributes the excess counts uniformly across all bins to prevent noise over-amplification, equalizes each tile locally, and bilinearly interpolates across tile boundaries so no artificial seams appear.</p>

                <p><b>5. What is a possible real-world application for histogram equalization?</b><br>
                Medical imaging (enhancing X-rays, CT scans, and MRI contrast to spot subtle tissue/bone anomalies), underwater or foggy surveillance/dashcam enhancement, satellite/aerial imagery, and low-light preprocessing for OCR or face detection.</p>

                <h3 style="color:#38bdf8; margin-top:12px;">Conclusion:</h3>
                <p>
                Histogram-based contrast adjustment is an essential preprocessing step in computer vision. While linear contrast stretching preserves the original histogram shape and global <code>cv2.equalizeHist()</code> maximizes overall dynamic range, <b>CLAHE</b> offers the best balance for complex scenes by boosting local contrast while limiting noise amplification via histogram clipping.
                </p>
                """
            )
        else:
            self.qa_card.hide()
            if self.current_tab == "compare":
                panels = [
                    ("ORIGINAL", f"σ={s_orig[3]:.1f}", self.results["orig"]),
                    ("GLOBAL EQUALIZATION", f"σ={s_glob[3]:.1f}", self.results["global"]),
                    (f"CLAHE (clip={clip_limit:.1f}, {self.tile_size}×{self.tile_size})", f"σ={s_clahe[3]:.1f}", self.results["clahe"]),
                ]
            elif self.current_tab == "global":
                panels = [
                    ("ORIGINAL", f"[{s_orig[0]}..{s_orig[1]}] σ={s_orig[3]:.1f}", self.results["orig"]),
                    ("GLOBAL EQUALIZATION", f"[{s_glob[0]}..{s_glob[1]}] σ={s_glob[3]:.1f}", self.results["global"]),
                ]
            elif self.current_tab == "stretch":
                panels = [
                    ("ORIGINAL", f"[{s_orig[0]}..{s_orig[1]}] σ={s_orig[3]:.1f}", self.results["orig"]),
                    (f"LINEAR STRETCH ({low_pct}%–{high_pct}%)", f"[{s_str[0]}..{s_str[1]}] σ={s_str[3]:.1f}", self.results["stretched"]),
                ]
            else:  # clahe
                panels = [
                    ("GLOBAL EQUALIZATION", f"σ={s_glob[3]:.1f}", self.results["global"]),
                    (f"CLAHE (clip={clip_limit:.1f}, {self.tile_size}×{self.tile_size})", f"σ={s_clahe[3]:.1f}", self.results["clahe"]),
                ]

            for i in range(3):
                if i < len(panels):
                    title, badge, img = panels[i]
                    self.view_cards[i].show()
                    self.view_titles[i].setText(title)
                    self.view_badges[i].setText(badge)
                    self.canvases[i].set_image(img)
                    self.hists[i].set_histogram(img)
                else:
                    self.view_cards[i].hide()

        space = "YUV (Y-channel)" if self.use_color else "Grayscale"
        self.details_lbl.setText(
            f"Input : {self.current_filename} ({w}×{h})\n"
            f"Space : {space}\n\n"
            f"Contrast (Min..Max | Mean | Std):\n"
            f"  Orig   : {s_orig[0]:>3}..{s_orig[1]:<3} | {s_orig[2]:5.1f} | {s_orig[3]:4.1f}\n"
            f"  Stretch: {s_str[0]:>3}..{s_str[1]:<3} | {s_str[2]:5.1f} | {s_str[3]:4.1f}\n"
            f"  Global : {s_glob[0]:>3}..{s_glob[1]:<3} | {s_glob[2]:5.1f} | {s_glob[3]:4.1f}\n"
            f"  CLAHE  : {s_clahe[0]:>3}..{s_clahe[1]:<3} | {s_clahe[2]:5.1f} | {s_clahe[3]:4.1f}"
        )

        self.status_lbl.setText(
            f"{self.current_filename} ({w}×{h}, {space}) | "
            f"Orig σ={s_orig[3]:.1f} | Stretch σ={s_str[3]:.1f} | "
            f"Global σ={s_glob[3]:.1f} | CLAHE(clip={clip_limit:.1f}, {self.tile_size}×{self.tile_size}) σ={s_clahe[3]:.1f}"
        )

    def _on_save_comparison(self) -> None:
        if not self.results:
            return
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Histogram Comparison",
            str(self.lab_dir / "histogram_comparison.png"),
            "PNG (*.png);;JPEG (*.jpg)",
        )
        if not save_path:
            return
        import matplotlib.pyplot as plt

        clip_limit = self.clip_sl["slider"].value() / 10.0
        fig, axes = plt.subplots(2, 3, figsize=(14, 7.5), gridspec_kw={"height_ratios": [2.2, 1.2]})
        cols = [
            ("orig", "Original Image", "#64748b"),
            ("global", "Global Histogram Equalization", "#0284c7"),
            ("clahe", f"CLAHE (clip={clip_limit:.1f}, {self.tile_size}×{self.tile_size})", "#10b981"),
        ]
        for col_idx, (key, title, color) in enumerate(cols):
            img = self.results[key]
            ax_img = axes[0, col_idx]
            if img.ndim == 2:
                ax_img.imshow(img, cmap="gray", vmin=0, vmax=255)
            else:
                ax_img.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            ax_img.set_title(title, fontsize=11, fontweight="bold")
            ax_img.axis("off")

            ax_hist = axes[1, col_idx]
            hist = compute_intensity_hist(img)
            ax_hist.fill_between(np.arange(256), hist, color=color, alpha=0.55)
            ax_hist.plot(np.arange(256), hist, color=color, linewidth=1.2)
            ax_hist.set_xlim(0, 255)
            ax_hist.set_xlabel("Pixel Intensity (0–255)")
            ax_hist.set_ylabel("Pixel Count" if col_idx == 0 else "")
            ax_hist.grid(alpha=0.25)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)


def main() -> None:
    app = QApplication(sys.argv)
    win = Lab3Window(Path(__file__).resolve().parent)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
