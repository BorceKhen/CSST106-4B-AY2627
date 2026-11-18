"""
CSST106 - Perception and Computer Vision
Laboratory Exercise No. 2 (Lab Activity 3): Edge Detection Technique (PyQt6)

Standalone interactive display UI implementing Sobel and Canny edge detection
with Gaussian blur preprocessing:
  - Compare (All 3) : Original Grayscale, Sobel Magnitude, and Canny Edges side by side
  - Gaussian Blur   : Original vs. Gaussian-blurred preprocessing
  - Sobel Details   : Sobel X (dx) vs. Sobel Y (dy) directional gradients
  - Canny Details   : Original vs. Canny binary edges with live T1/T2 hysteresis tuning
"""

from pathlib import Path
import sys
import cv2
import numpy as np
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor, QDragEnterEvent, QDropEvent, QImage, QPainter, QPixmap
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


def create_sample_input(save_path: Path, width: int = 640, height: int = 480) -> np.ndarray:
    """Create a synthetic 'input.jpg' with crisp shapes, curves, and gradients for edge detection."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Smooth background gradient
    for y in range(height):
        val = int(215 - (y / height) * 70)
        img[y, :] = (val, val - 10, val - 20)

    # Buildings / geometric blocks with clear vertical, horizontal, and diagonal edges
    cv2.rectangle(img, (55, 170), (225, 410), (70, 90, 120), -1)
    cv2.rectangle(img, (55, 170), (225, 410), (35, 45, 65), 3)
    for wy in range(200, 380, 55):
        for wx in (85, 145):
            cv2.rectangle(img, (wx, wy), (wx + 35, wy + 35), (210, 230, 245), -1)

    # Triangle roof / pyramid for diagonal edges
    pts = np.array([[270, 390], [385, 165], [500, 390]], dtype=np.int32)
    cv2.fillPoly(img, [pts], (95, 130, 175))
    cv2.polylines(img, [pts], True, (40, 55, 80), 3)

    # Concentric circles and curved rings
    cv2.circle(img, (520, 125), 62, (60, 175, 230), -1)
    cv2.circle(img, (520, 125), 42, (235, 240, 245), 4)
    cv2.circle(img, (520, 125), 20, (50, 80, 130), -1)

    # Fine checkerboard strip to highlight Sobel vs Canny edge thickness
    cell = 16
    for r in range(4):
        for c in range(10):
            color = (240, 240, 240) if (r + c) % 2 == 0 else (40, 40, 40)
            x0, y0 = 260 + c * cell, 40 + r * cell
            cv2.rectangle(img, (x0, y0), (x0 + cell, y0 + cell), color, -1)

    cv2.putText(img, "EDGE TEST", (55, 95), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (35, 45, 60), 3, cv2.LINE_AA)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(save_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])
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


class ImageCanvas(QWidget):
    """Aspect-ratio-preserving image canvas."""

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


def compute_edge_maps(
    gray: np.ndarray, blur_ksize: int, sobel_ksize: int, canny_t1: int, canny_t2: int
) -> dict[str, np.ndarray]:
    """Run Gaussian blur, Sobel (X, Y, Magnitude), and Canny edge detection."""
    if blur_ksize > 1:
        blurred = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    else:
        blurred = gray.copy()

    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=sobel_ksize)
    sobel_mag_f = cv2.magnitude(sobelx, sobely)

    sobelx_u8 = cv2.convertScaleAbs(sobelx)
    sobely_u8 = cv2.convertScaleAbs(sobely)
    sobel_u8 = np.uint8(np.clip(sobel_mag_f / max(1.0, sobel_mag_f.max()) * 255.0, 0, 255))

    canny = cv2.Canny(blurred, canny_t1, canny_t2)
    return {
        "gray": gray,
        "blurred": blurred,
        "sobelx": sobelx_u8,
        "sobely": sobely_u8,
        "sobel_mag_f": sobel_mag_f,
        "sobel": sobel_u8,
        "canny": canny,
    }


class Lab2Window(QMainWindow):
    """Simple, tabbed UI for CSST106 Lab 2 Edge Detection (Sobel & Canny)."""

    TABS = [
        ("compare", "Compare (All 3)"),
        ("blur", "Gaussian Blur"),
        ("sobel", "Sobel X / Y"),
        ("canny", "Canny Thresholds"),
        ("qa", "Question && Conclusion"),
    ]

    def __init__(self, lab_dir: Path) -> None:
        super().__init__()
        self.lab_dir = lab_dir
        self.default_input = lab_dir / "input.jpg"

        self.gray_img: np.ndarray | None = None
        self.results: dict[str, np.ndarray] = {}
        self.current_filename = ""
        self.current_tab = "compare"

        self.blur_ksize = 3
        self.sobel_ksize = 3

        self.setWindowTitle("CSST106 Lab 2 — Edge Detection (Sobel & Canny)")
        self.resize(1280, 720)
        self.setMinimumSize(980, 600)
        self.setAcceptDrops(True)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()

        if not self.default_input.exists():
            create_sample_input(self.default_input)
        self.load_image(self.default_input)

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
        lbl_title = QLabel("CSST106 Lab 2: Edge Detection (Sobel vs. Canny)")
        lbl_title.setObjectName("Title")
        lbl_sub = QLabel("Gaussian smoothing preprocessing, Sobel gradient magnitude, and Canny hysteresis thresholding.")
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
        self.tab_buttons["compare"].setChecked(True)
        layout.addWidget(tab_panel)

        # Body: Image Viewers + Right Controls/Details Panel
        body = QHBoxLayout()
        body.setSpacing(10)
        layout.addLayout(body, 1)

        # 3 Viewer Cards (Panel 3 hides cleanly in 2-panel tabs)
        self.view_cards: list[QFrame] = []
        self.view_titles: list[QLabel] = []
        self.view_badges: list[QLabel] = []
        self.canvases: list[ImageCanvas] = []

        for _ in range(3):
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

        # Q&A and Conclusion Card (shown when 'Question & Conclusion' tab is active)
        self.qa_card = QFrame()
        self.qa_card.setObjectName("Panel")
        qal = QVBoxLayout(self.qa_card)
        qal.setContentsMargins(16, 14, 16, 14)
        qal.setSpacing(10)

        qa_hdr = QLabel("LAB ACTIVITY 3 — QUESTION & CONCLUSION")
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
        qacl.setSpacing(10)

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

        # Right Inspector & Parameters Drawer
        inspector = QFrame()
        inspector.setObjectName("Panel")
        inspector.setFixedWidth(295)
        il = QVBoxLayout(inspector)
        il.setContentsMargins(12, 10, 12, 12)
        il.setSpacing(10)

        hdr_p = QLabel("PARAMETERS & DETAILS")
        hdr_p.setObjectName("Section")
        il.addWidget(hdr_p)

        # Gaussian Blur kernel selector
        il.addWidget(QLabel("Gaussian Blur Kernel:"))
        blur_row = QHBoxLayout()
        self.blur_group = QButtonGroup(self)
        self.blur_group.setExclusive(True)
        self.blur_buttons: dict[int, QPushButton] = {}
        for k, label in [(1, "Off"), (3, "3×3"), (5, "5×5"), (7, "7×7")]:
            b = QPushButton(label)
            b.setObjectName("ChipBtn")
            b.setCheckable(True)
            if k == 3:
                b.setChecked(True)
            b.clicked.connect(lambda _chk, val=k: self._set_blur(val))
            self.blur_group.addButton(b)
            self.blur_buttons[k] = b
            blur_row.addWidget(b)
        il.addLayout(blur_row)

        # Sobel kernel selector
        il.addWidget(QLabel("Sobel Kernel Size:"))
        sobel_row = QHBoxLayout()
        self.sobel_group = QButtonGroup(self)
        self.sobel_group.setExclusive(True)
        self.sobel_buttons: dict[int, QPushButton] = {}
        for k in (1, 3, 5, 7):
            b = QPushButton(f"{k}×{k}")
            b.setObjectName("ChipBtn")
            b.setCheckable(True)
            if k == 3:
                b.setChecked(True)
            b.clicked.connect(lambda _chk, val=k: self._set_sobel(val))
            self.sobel_group.addButton(b)
            self.sobel_buttons[k] = b
            sobel_row.addWidget(b)
        il.addLayout(sobel_row)

        # Canny T1 & T2 sliders
        self.t1_slider, self.t1_lbl = self._make_slider("Canny T1 (Low):", 100)
        self.t2_slider, self.t2_lbl = self._make_slider("Canny T2 (High):", 200)
        il.addWidget(self.t1_slider["row"])
        il.addWidget(self.t2_slider["row"])

        # Separator
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

    def _make_slider(self, title: str, default: int) -> tuple[dict, QLabel]:
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
        sl.setRange(0, 255)
        sl.setValue(default)
        sl.valueChanged.connect(self._update_view)
        vl.addWidget(sl)
        return {"row": wrap, "slider": sl}, val_lbl

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
        gray = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if gray is None:
            return
        self.gray_img = gray
        self.current_filename = path.name
        self._update_view()

    def _on_open(self) -> None:
        chosen, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            str(self.lab_dir),
            "Images (*.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff)",
        )
        if chosen:
            self.load_image(Path(chosen))

    def _on_reset(self) -> None:
        self.blur_ksize = 3
        self.sobel_ksize = 3
        self.blur_buttons[3].setChecked(True)
        self.sobel_buttons[3].setChecked(True)
        self.t1_slider["slider"].setValue(100)
        self.t2_slider["slider"].setValue(200)
        self._update_view()

    def _select_tab(self, key: str) -> None:
        self.current_tab = key
        self._update_view()

    def _set_blur(self, val: int) -> None:
        self.blur_ksize = val
        self._update_view()

    def _set_sobel(self, val: int) -> None:
        self.sobel_ksize = val
        self._update_view()

    def _update_view(self) -> None:
        if self.gray_img is None:
            return

        t1 = self.t1_slider["slider"].value()
        t2 = self.t2_slider["slider"].value()
        self.t1_lbl.setText(str(t1))
        self.t2_lbl.setText(str(t2))

        self.results = compute_edge_maps(self.gray_img, self.blur_ksize, self.sobel_ksize, t1, t2)
        h, w = self.gray_img.shape
        sobel_f = self.results["sobel_mag_f"]
        canny_edges = self.results["canny"]
        edge_pixels = int(np.count_nonzero(canny_edges))
        edge_pct = edge_pixels / (h * w) * 100.0
        blur_txt = f"({self.blur_ksize}, {self.blur_ksize})" if self.blur_ksize > 1 else "Off"

        if self.current_tab == "qa":
            for card in self.view_cards:
                card.hide()
            self.qa_card.show()
            self.qa_text_lbl.setText(
                f"""
                <h3 style="color:#38bdf8; margin-top:0;">Question:</h3>
                <p style="color:#cbd5e1;">
                Write a Python program to perform edge detection on an image using both the Sobel and Canny edge detection methods.<br>
                <b>1.</b> Explain the differences between the edge maps produced by each method. Use the provided image
                <code>input.jpg</code> and display the original image, Sobel edges, and Canny edges side by side.
                </p>

                <h3 style="color:#38bdf8; margin-top:14px;">Answer — Differences Between Sobel and Canny Edge Maps:</h3>
                <p>On <b>{self.current_filename}</b> (<code>{w}×{h}</code> grayscale, Blur={blur_txt}), the <b>Compare (All 3)</b> tab displays the original image, Sobel edge map, and Canny edge map side by side:</p>
                <ul style="margin-top:4px;">
                  <li><b>Output Type &amp; Intensity:</b> <b>Sobel</b> outputs a <i>continuous grayscale gradient magnitude</i> image (current Max=<code>{sobel_f.max():.1f}</code>, Mean=<code>{sobel_f.mean():.1f}</code>) where brighter pixels mean steeper intensity changes. <b>Canny</b> outputs a <i>strict binary edge map</i> (<code>0</code> or <code>255</code>), currently marking <code>{edge_pixels:,}</code> edge pixels (<code>{edge_pct:.2f}%</code> of the image).</li>
                  <li><b>Edge Thickness &amp; Localization:</b> <b>Sobel</b> produces thicker, multi-pixel blurred ridges along object boundaries. <b>Canny</b> applies <i>non-maximum suppression</i> to thin gradients down to crisp <b>1-pixel-wide</b> boundaries.</li>
                  <li><b>Thresholding &amp; Noise Suppression:</b> <b>Sobel</b> has no built-in thresholding, so subtle gradients and background texture remain faintly visible. <b>Canny</b> uses dual <i>hysteresis thresholds</i> (<code>T1={t1}</code> Low, <code>T2={t2}</code> High): magnitudes above <code>T2</code> are strong edges, below <code>T1</code> are discarded, and values between <code>T1</code> and <code>T2</code> are kept only if connected to a strong edge.</li>
                  <li><b>Directional Sensitivity:</b> <b>Sobel</b> explicitly computes separate horizontal (<code>Gx</code>, vertical edges) and vertical (<code>Gy</code>, horizontal edges) derivatives before combining them via <code>cv2.magnitude(sobelx, sobely)</code>, whereas <b>Canny</b> returns unified final contours.</li>
                </ul>

                <h3 style="color:#38bdf8; margin-top:14px;">Conclusion:</h3>
                <p>
                Both Sobel and Canny identify regions of rapid intensity change after Gaussian smoothing, but they serve complementary purposes.
                <b>Sobel</b> is fast and preserves continuous gradient strength and direction (<code>Gx</code>, <code>Gy</code>), making it useful when gradient magnitude or orientation is needed.
                <b>Canny</b> adds non-maximum suppression and dual-threshold hysteresis, producing cleaner, thinner, noise-resistant object boundaries that are better suited for contour detection, shape analysis, and segmentation.
                </p>
                """
            )
        else:
            self.qa_card.hide()
            if self.current_tab == "compare":
                panels = [
                    ("ORIGINAL (GRAYSCALE)", f"{w}×{h}", self.results["gray"]),
                    ("SOBEL EDGE DETECTION", f"k={self.sobel_ksize}", self.results["sobel"]),
                    ("CANNY EDGE DETECTION", f"T=({t1}, {t2})", self.results["canny"]),
                ]
            elif self.current_tab == "blur":
                panels = [
                    ("ORIGINAL GRAYSCALE", f"{w}×{h}", self.results["gray"]),
                    ("GAUSSIAN BLURRED", f"k={self.blur_ksize}×{self.blur_ksize}" if self.blur_ksize > 1 else "Off", self.results["blurred"]),
                ]
            elif self.current_tab == "sobel":
                panels = [
                    ("SOBEL X (VERTICAL EDGES)", f"dx=1, k={self.sobel_ksize}", self.results["sobelx"]),
                    ("SOBEL Y (HORIZONTAL EDGES)", f"dy=1, k={self.sobel_ksize}", self.results["sobely"]),
                    ("SOBEL COMBINED MAGNITUDE", "sqrt(Gx² + Gy²)", self.results["sobel"]),
                ]
            else:  # canny
                panels = [
                    ("GAUSSIAN INPUT", f"blur={self.blur_ksize}×{self.blur_ksize}" if self.blur_ksize > 1 else "raw", self.results["blurred"]),
                    ("CANNY BINARY EDGES", f"T1={t1}, T2={t2}", self.results["canny"]),
                ]

            for i in range(3):
                if i < len(panels):
                    title, badge, img = panels[i]
                    self.view_cards[i].show()
                    self.view_titles[i].setText(title)
                    self.view_badges[i].setText(badge)
                    self.canvases[i].set_image(img)
                else:
                    self.view_cards[i].hide()

        self.details_lbl.setText(
            f"Input      : {self.current_filename}\n"
            f"Shape      : ({h}, {w}) grayscale\n"
            f"Blur       : {blur_txt}\n\n"
            f"Sobel (CV_64F):\n"
            f"  ksize    = {self.sobel_ksize}\n"
            f"  Max Mag  = {sobel_f.max():.1f}\n"
            f"  Mean Mag = {sobel_f.mean():.1f}\n"
            f"  Output   = Continuous intensity\n\n"
            f"Canny:\n"
            f"  T1 / T2  = {t1} / {t2}\n"
            f"  Edge px  = {edge_pixels:,} ({edge_pct:.2f}%)\n"
            f"  Output   = Thin 1-px binary"
        )

        self.status_lbl.setText(
            f"{self.current_filename} ({w}×{h}) | Blur={blur_txt} | "
            f"Sobel k={self.sobel_ksize} (mean={sobel_f.mean():.1f}) | "
            f"Canny T=({t1}, {t2}) -> {edge_pct:.2f}% edge pixels"
        )

    def _on_save_comparison(self) -> None:
        if not self.results:
            return
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Side-by-Side Comparison",
            str(self.lab_dir / "edge_detection_comparison.png"),
            "PNG (*.png);;JPEG (*.jpg)",
        )
        if not save_path:
            return
        import matplotlib.pyplot as plt

        t1 = self.t1_slider["slider"].value()
        t2 = self.t2_slider["slider"].value()
        fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
        for ax, key, title in [
            (axes[0], "gray", "Original Image"),
            (axes[1], "sobel", f"Sobel Edge Detection (k={self.sobel_ksize})"),
            (axes[2], "canny", f"Canny Edge Detection (T={t1}, {t2})"),
        ]:
            ax.imshow(self.results[key], cmap="gray")
            ax.set_title(title, fontsize=11, fontweight="bold")
            ax.axis("off")
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)


def main() -> None:
    app = QApplication(sys.argv)
    win = Lab2Window(Path(__file__).resolve().parent)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
