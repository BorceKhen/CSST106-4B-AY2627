"""
CSST106 - Perception and Computer Vision
Laboratory Exercise No. 1: Interactive Display UI (PyQt6)

Simple, tabbed desktop viewer covering every Lab 1 concept:
  - Properties : shape, dimensions, channels (BGR), dtype, click-to-inspect pixel
  - Grayscale  : 2D array conversion, shape & intensity statistics
  - Pixel Edit : click-to-select (y, x), pick color, patch size, before/after BGR values
  - Crop (ROI) : live crop box overlay, NumPy slice indices, cropped dimensions
  - Resize     : scale presets/slider, interpolation method, output shape
  - Rotate     : 90 CW / 180 / 270 CW rotation and swapped dimensions
"""

from pathlib import Path
import sys
import cv2
import numpy as np
from PyQt6.QtCore import Qt, QPoint, QRect, pyqtSignal
from PyQt6.QtGui import QColor, QDragEnterEvent, QDropEvent, QImage, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QColorDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


def create_sample_image(save_path: Path, width: int = 640, height: int = 480) -> np.ndarray:
    """Create a colorful synthetic scene if no sample image exists yet."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(300):
        blue = int(235 - (y / 300) * 40)
        green = int(190 - (y / 300) * 30)
        red = int(110 + (y / 300) * 40)
        img[y, :] = (blue, green, red)

    img[300:, :] = (50, 155, 60)
    cv2.circle(img, (520, 95), 48, (0, 220, 255), -1)

    cv2.rectangle(img, (180, 210), (410, 380), (180, 210, 235), -1)
    cv2.rectangle(img, (180, 210), (410, 380), (60, 80, 110), 3)

    roof_pts = np.array([[155, 210], [295, 115], [435, 210]], dtype=np.int32)
    cv2.fillPoly(img, [roof_pts], (40, 45, 200))
    cv2.polylines(img, [roof_pts], True, (30, 30, 120), 3)

    cv2.rectangle(img, (265, 285), (325, 380), (45, 75, 120), -1)
    cv2.circle(img, (315, 335), 4, (0, 215, 255), -1)

    cv2.rectangle(img, (205, 240), (250, 285), (245, 220, 150), -1)
    cv2.rectangle(img, (340, 240), (385, 285), (245, 220, 150), -1)

    cv2.rectangle(img, (80, 260), (110, 370), (40, 65, 100), -1)
    cv2.circle(img, (95, 225), 45, (35, 130, 35), -1)

    cv2.putText(img, "CSST106 Lab 1", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(save_path), img)
    return img


def cv_to_qpixmap(img: np.ndarray) -> QPixmap:
    """Convert an OpenCV BGR or grayscale uint8 array to QPixmap."""
    if img.ndim == 2:
        h, w = img.shape
        qimg = QImage(img.data, w, h, w, QImage.Format.Format_Grayscale8)
        return QPixmap.fromImage(qimg.copy())
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimg.copy())


class ImageCanvas(QWidget):
    """Aspect-ratio-preserving image viewer with optional pixel-click mapping and ROI overlay."""

    pixelClicked = pyqtSignal(int, int)

    def __init__(self, clickable: bool = False) -> None:
        super().__init__()
        self.clickable = clickable
        self._pixmap: QPixmap | None = None
        self._img_w = 0
        self._img_h = 0
        self._draw_rect = QRect()
        self.selected_yx: tuple[int, int] | None = None
        self.roi_norm: tuple[float, float, float, float] | None = None
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

        pad = 10
        avail_w = max(1, self.width() - 2 * pad)
        avail_h = max(1, self.height() - 2 * pad)
        scale = min(avail_w / self._img_w, avail_h / self._img_h)
        dw = max(1, int(self._img_w * scale))
        dh = max(1, int(self._img_h * scale))
        ox = (self.width() - dw) // 2
        oy = (self.height() - dh) // 2
        self._draw_rect = QRect(ox, oy, dw, dh)

        painter.drawPixmap(self._draw_rect, self._pixmap)

        if self.roi_norm is not None:
            y0, y1, x0, x1 = self.roi_norm
            rx = int(ox + x0 * dw)
            ry = int(oy + y0 * dh)
            rw = max(1, int((x1 - x0) * dw))
            rh = max(1, int((y1 - y0) * dh))
            painter.setPen(QPen(QColor("#fbbf24"), 2, Qt.PenStyle.DashLine))
            painter.drawRect(rx, ry, rw, rh)

        if self.selected_yx is not None and self.clickable:
            sy, sx = self.selected_yx
            cx = int(ox + (sx / max(1, self._img_w)) * dw)
            cy = int(oy + (sy / max(1, self._img_h)) * dh)
            painter.setPen(QPen(QColor("#38bdf8"), 2))
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
    font-size: 12px;
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
QSpinBox {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 5px;
    padding: 3px 6px;
}
QCheckBox {
    color: #e2e8f0;
    font-size: 12px;
}
"""


class Lab1Window(QMainWindow):
    """Simple, uncluttered tabbed UI for CSST106 Lab 1."""

    TABS = [
        ("properties", "Properties"),
        ("grayscale", "Grayscale"),
        ("pixel", "Modify Pixel"),
        ("crop", "Crop (ROI)"),
        ("resize", "Resize"),
        ("rotate", "Rotate"),
    ]

    def __init__(self, lab_dir: Path) -> None:
        super().__init__()
        self.lab_dir = lab_dir
        self.sample_path = lab_dir / "sample_image.png"

        self.original_bgr: np.ndarray | None = None
        self.working_bgr: np.ndarray | None = None
        self.processed_img: np.ndarray | None = None
        self.current_filename = ""
        self.current_tab = "properties"

        self.selected_yx = (95, 520)
        self.paint_bgr = (255, 0, 255)  # Magenta in BGR
        self.last_pixel_change: tuple[tuple[int, int], list[int], list[int]] | None = None

        self.setWindowTitle("CSST106 Lab 1 — Image Manipulation")
        self.resize(1200, 720)
        self.setMinimumSize(940, 600)
        self.setAcceptDrops(True)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()

        if not self.sample_path.exists():
            create_sample_image(self.sample_path)
        self.load_image(self.sample_path)

    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        # 1. Compact Header Bar
        top_bar = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        lbl_title = QLabel("CSST106 Lab 1: Image Representation & Manipulation")
        lbl_title.setObjectName("Title")
        lbl_sub = QLabel("Click Original image to inspect pixel values, or drag & drop any image file.")
        lbl_sub.setObjectName("Muted")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        top_bar.addLayout(title_box, 1)

        for text, handler, accent in [
            ("Open Image...", self._on_open, False),
            ("Reset", self._on_reset, False),
            ("Save Output...", self._on_save, True),
        ]:
            btn = QPushButton(text)
            if accent:
                btn.setObjectName("AccentBtn")
            btn.clicked.connect(handler)
            top_bar.addWidget(btn)
        layout.addLayout(top_bar)

        # 2. Horizontal Mode Tab Strip
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
        self.tab_buttons["properties"].setChecked(True)
        layout.addWidget(tab_panel)

        # 3. Main Workspace: Dual Viewers (Left) + Compact Details/Controls Drawer (Right)
        body = QHBoxLayout()
        body.setSpacing(10)
        layout.addLayout(body, 1)

        # Original Panel
        orig_panel = QFrame()
        orig_panel.setObjectName("Panel")
        ol = QVBoxLayout(orig_panel)
        ol.setContentsMargins(10, 8, 10, 10)
        ol.setSpacing(6)
        oh = QHBoxLayout()
        o_lbl = QLabel("ORIGINAL (BGR)")
        o_lbl.setObjectName("Section")
        self.orig_dim_lbl = QLabel("-")
        self.orig_dim_lbl.setObjectName("Muted")
        oh.addWidget(o_lbl)
        oh.addStretch()
        oh.addWidget(self.orig_dim_lbl)
        ol.addLayout(oh)
        self.orig_canvas = ImageCanvas(clickable=True)
        self.orig_canvas.pixelClicked.connect(self._on_pixel_clicked)
        ol.addWidget(self.orig_canvas, 1)
        body.addWidget(orig_panel, 1)

        # Output Panel
        out_panel = QFrame()
        out_panel.setObjectName("Panel")
        outl = QVBoxLayout(out_panel)
        outl.setContentsMargins(10, 8, 10, 10)
        outl.setSpacing(6)
        outh = QHBoxLayout()
        self.out_heading_lbl = QLabel("OUTPUT")
        self.out_heading_lbl.setObjectName("Section")
        self.out_dim_lbl = QLabel("-")
        self.out_dim_lbl.setObjectName("Muted")
        outh.addWidget(self.out_heading_lbl)
        outh.addStretch()
        outh.addWidget(self.out_dim_lbl)
        outl.addLayout(outh)
        self.out_canvas = ImageCanvas(clickable=False)
        outl.addWidget(self.out_canvas, 1)
        body.addWidget(out_panel, 1)

        # Right Inspector & Controls Panel
        inspector = QFrame()
        inspector.setObjectName("Panel")
        inspector.setFixedWidth(290)
        il = QVBoxLayout(inspector)
        il.setContentsMargins(12, 10, 12, 12)
        il.setSpacing(8)
        det_hdr = QLabel("DETAILS & CONTROLS")
        det_hdr.setObjectName("Section")
        il.addWidget(det_hdr)

        self.stack = QStackedWidget()
        self._build_tab_pages()
        il.addWidget(self.stack, 1)
        body.addWidget(inspector)

        # 4. Compact Status Footer
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setObjectName("StatusBar")
        layout.addWidget(self.status_lbl)

    def _build_tab_pages(self) -> None:
        # 0: Properties
        p_prop = QWidget()
        lp = QVBoxLayout(p_prop)
        lp.setContentsMargins(0, 4, 0, 0)
        lp.setSpacing(8)
        self.prop_info = QLabel()
        self.prop_info.setObjectName("Mono")
        self.prop_info.setWordWrap(True)
        lp.addWidget(self.prop_info)
        lp.addStretch()
        self.stack.addWidget(p_prop)

        # 1: Grayscale
        p_gray = QWidget()
        lg = QVBoxLayout(p_gray)
        lg.setContentsMargins(0, 4, 0, 0)
        lg.setSpacing(8)
        self.gray_info = QLabel()
        self.gray_info.setObjectName("Mono")
        self.gray_info.setWordWrap(True)
        lg.addWidget(self.gray_info)
        lg.addStretch()
        self.stack.addWidget(p_gray)

        # 2: Modify Pixel
        p_pix = QWidget()
        lpx = QVBoxLayout(p_pix)
        lpx.setContentsMargins(0, 4, 0, 0)
        lpx.setSpacing(8)

        row_patch = QHBoxLayout()
        row_patch.addWidget(QLabel("Patch size (px):"))
        self.patch_spin = QSpinBox()
        self.patch_spin.setRange(1, 61)
        self.patch_spin.setSingleStep(2)
        self.patch_spin.setValue(25)
        row_patch.addStretch()
        row_patch.addWidget(self.patch_spin)
        lpx.addLayout(row_patch)

        self.click_paint_chk = QCheckBox("Paint on image click")
        lpx.addWidget(self.click_paint_chk)

        btns = QHBoxLayout()
        pick_btn = QPushButton("Pick Color")
        pick_btn.clicked.connect(self._on_pick_color)
        apply_btn = QPushButton("Apply at (y, x)")
        apply_btn.setObjectName("AccentBtn")
        apply_btn.clicked.connect(self._on_apply_pixel)
        btns.addWidget(pick_btn)
        btns.addWidget(apply_btn)
        lpx.addLayout(btns)

        self.pixel_info = QLabel()
        self.pixel_info.setObjectName("Mono")
        self.pixel_info.setWordWrap(True)
        lpx.addWidget(self.pixel_info)
        lpx.addStretch()
        self.stack.addWidget(p_pix)

        # 3: Crop ROI
        p_crop = QWidget()
        lc = QVBoxLayout(p_crop)
        lc.setContentsMargins(0, 4, 0, 0)
        lc.setSpacing(6)
        self.crop_sliders: dict[str, QSlider] = {}
        self.crop_vals: dict[str, QLabel] = {}
        for key, title, default in [("y0", "Y0", 22), ("y1", "Y1", 82), ("x0", "X0", 22), ("x1", "X1", 70)]:
            row = QHBoxLayout()
            lbl = QLabel(f"{title}:")
            lbl.setFixedWidth(24)
            sl = QSlider(Qt.Orientation.Horizontal)
            sl.setRange(0, 100)
            sl.setValue(default)
            sl.valueChanged.connect(self._update_view)
            vl = QLabel(f"{default}%")
            vl.setObjectName("Mono")
            vl.setFixedWidth(34)
            row.addWidget(lbl)
            row.addWidget(sl, 1)
            row.addWidget(vl)
            lc.addLayout(row)
            self.crop_sliders[key] = sl
            self.crop_vals[key] = vl

        self.crop_info = QLabel()
        self.crop_info.setObjectName("Mono")
        self.crop_info.setWordWrap(True)
        lc.addWidget(self.crop_info)
        lc.addStretch()
        self.stack.addWidget(p_crop)

        # 4: Resize
        p_res = QWidget()
        lrs = QVBoxLayout(p_res)
        lrs.setContentsMargins(0, 4, 0, 0)
        lrs.setSpacing(8)
        presets = QHBoxLayout()
        for pct in (50, 75, 125, 150):
            b = QPushButton(f"{pct}%")
            b.clicked.connect(lambda _chk, v=pct: self.resize_slider.setValue(v))
            presets.addWidget(b)
        lrs.addLayout(presets)

        sl_row = QHBoxLayout()
        sl_row.addWidget(QLabel("Scale:"))
        self.resize_slider = QSlider(Qt.Orientation.Horizontal)
        self.resize_slider.setRange(20, 200)
        self.resize_slider.setValue(50)
        self.resize_slider.valueChanged.connect(self._update_view)
        self.resize_val = QLabel("50%")
        self.resize_val.setObjectName("Mono")
        sl_row.addWidget(self.resize_slider, 1)
        sl_row.addWidget(self.resize_val)
        lrs.addLayout(sl_row)

        self.resize_info = QLabel()
        self.resize_info.setObjectName("Mono")
        self.resize_info.setWordWrap(True)
        lrs.addWidget(self.resize_info)
        lrs.addStretch()
        self.stack.addWidget(p_res)

        # 5: Rotate
        p_rot = QWidget()
        lr = QVBoxLayout(p_rot)
        lr.setContentsMargins(0, 4, 0, 0)
        lr.setSpacing(8)
        rbtns = QHBoxLayout()
        self.rot_group = QButtonGroup(self)
        self.rot_group.setExclusive(True)
        self.rot_angle = 90
        for deg, txt in [(90, "90° CW"), (180, "180°"), (270, "270° CW")]:
            b = QPushButton(txt)
            b.setObjectName("ChipBtn")
            b.setCheckable(True)
            if deg == 90:
                b.setChecked(True)
            b.clicked.connect(lambda _chk, d=deg: self._set_rotation(d))
            self.rot_group.addButton(b)
            rbtns.addWidget(b)
        lr.addLayout(rbtns)

        self.rot_info = QLabel()
        self.rot_info.setObjectName("Mono")
        self.rot_info.setWordWrap(True)
        lr.addWidget(self.rot_info)
        lr.addStretch()
        self.stack.addWidget(p_rot)

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
        img = cv2.imread(str(path))
        if img is None:
            return
        self.original_bgr = img
        self.working_bgr = img.copy()
        self.current_filename = path.name
        h, w = img.shape[:2]
        self.selected_yx = (min(95, h - 1), min(520, w - 1))
        self.last_pixel_change = None
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
        if self.original_bgr is None:
            return
        self.working_bgr = self.original_bgr.copy()
        self.last_pixel_change = None
        self.click_paint_chk.setChecked(False)
        self._update_view()

    def _on_save(self) -> None:
        if self.processed_img is None:
            return
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Output Image",
            str(self.lab_dir / f"output_{self.current_tab}.png"),
            "PNG (*.png);;JPEG (*.jpg);;All Files (*.*)",
        )
        if save_path:
            cv2.imwrite(save_path, self.processed_img)

    def _select_tab(self, key: str) -> None:
        self.current_tab = key
        idx = [k for k, _ in self.TABS].index(key)
        self.stack.setCurrentIndex(idx)
        self._update_view()

    def _set_rotation(self, deg: int) -> None:
        self.rot_angle = deg
        self._update_view()

    def _on_pick_color(self) -> None:
        init = QColor(self.paint_bgr[2], self.paint_bgr[1], self.paint_bgr[0])
        chosen = QColorDialog.getColor(init, self, "Choose Pixel Color")
        if chosen.isValid():
            self.paint_bgr = (chosen.blue(), chosen.green(), chosen.red())
            self._update_view()

    def _on_pixel_clicked(self, y: int, x: int) -> None:
        self.selected_yx = (y, x)
        if self.current_tab == "pixel" and self.click_paint_chk.isChecked():
            self._apply_pixel_at(y, x)
        else:
            self._update_view()

    def _on_apply_pixel(self) -> None:
        self._apply_pixel_at(*self.selected_yx)

    def _apply_pixel_at(self, y: int, x: int) -> None:
        if self.working_bgr is None:
            return
        h, w = self.working_bgr.shape[:2]
        before = [int(v) for v in self.working_bgr[y, x]]
        half = max(0, self.patch_spin.value() // 2)
        y0, y1 = max(0, y - half), min(h, y + half + 1)
        x0, x1 = max(0, x - half), min(w, x + half + 1)
        self.working_bgr[y0:y1, x0:x1] = self.paint_bgr
        self.last_pixel_change = ((y, x), before, list(self.paint_bgr))
        self._update_view()

    def _update_view(self) -> None:
        if self.working_bgr is None:
            return
        src = self.working_bgr
        h, w, c = src.shape
        sy, sx = self.selected_yx
        b, g, r = [int(v) for v in src[sy, sx]]
        gray_px = int(cv2.cvtColor(src[sy : sy + 1, sx : sx + 1], cv2.COLOR_BGR2GRAY)[0, 0])

        self.orig_canvas.selected_yx = self.selected_yx
        self.orig_canvas.roi_norm = None
        self.orig_dim_lbl.setText(f"{w}×{h} • shape=({h}, {w}, {c})")

        if self.current_tab == "properties":
            out = src.copy()
            self.out_heading_lbl.setText("PREVIEW (BGR)")
            self.prop_info.setText(
                f"File      : {self.current_filename}\n"
                f"img.shape : ({h}, {w}, {c})\n"
                f"Height    : {h} px\n"
                f"Width     : {w} px\n"
                f"Channels  : {c} (BGR order)\n"
                f"Dtype     : {src.dtype} (0–255)\n"
                f"Pixels    : {h * w:,}\n\n"
                f"Pixel (y={sy}, x={sx}):\n"
                f"  BGR  = [{b}, {g}, {r}]\n"
                f"  RGB  = ({r}, {g}, {b})\n"
                f"  Gray = {gray_px}"
            )

        elif self.current_tab == "grayscale":
            out = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            self.out_heading_lbl.setText("GRAYSCALE (2D)")
            self.gray_info.setText(
                f"cv2.cvtColor(..., BGR2GRAY)\n\n"
                f"Original  : ({h}, {w}, {c})\n"
                f"Gray shape: {out.shape}\n"
                f"Dtype     : {out.dtype}\n"
                f"Min / Max : {int(out.min())} / {int(out.max())}\n"
                f"Mean      : {out.mean():.1f}\n"
                f"At ({sy}, {sx}) : {int(out[sy, sx])}"
            )

        elif self.current_tab == "pixel":
            out = src.copy()
            self.out_heading_lbl.setText("PIXEL MODIFIED")
            change = ""
            if self.last_pixel_change is not None:
                (cy, cx), before, after = self.last_pixel_change
                change = f"\n\nLast Edit ({cy}, {cx}):\n  Before: {before}\n  After : {after}"
            self.pixel_info.setText(
                f"Selected : (y={sy}, x={sx})\n"
                f"Current  : BGR [{b}, {g}, {r}]\n"
                f"Gray     : {gray_px}\n"
                f"Paint BGR: {list(self.paint_bgr)}"
                f"{change}"
            )

        elif self.current_tab == "crop":
            y0_p, y1_p = sorted((self.crop_sliders["y0"].value(), self.crop_sliders["y1"].value()))
            x0_p, x1_p = sorted((self.crop_sliders["x0"].value(), self.crop_sliders["x1"].value()))
            for k, sl in self.crop_sliders.items():
                self.crop_vals[k].setText(f"{sl.value()}%")
            y0 = int(h * y0_p / 100)
            y1 = max(y0 + 1, int(h * y1_p / 100))
            x0 = int(w * x0_p / 100)
            x1 = max(x0 + 1, int(w * x1_p / 100))
            out = src[y0:y1, x0:x1].copy()
            self.orig_canvas.roi_norm = (y0 / h, y1 / h, x0 / w, x1 / w)
            self.out_heading_lbl.setText("CROPPED ROI")
            self.crop_info.setText(
                f"Slice   : img[{y0}:{y1}, {x0}:{x1}]\n"
                f"Before  : ({h}, {w}, {c})\n"
                f"Cropped : {out.shape}\n"
                f"Size    : {out.shape[1]}×{out.shape[0]} px"
            )

        elif self.current_tab == "resize":
            pct = self.resize_slider.value()
            self.resize_val.setText(f"{pct}%")
            nw = max(1, int(w * pct / 100))
            nh = max(1, int(h * pct / 100))
            interp = cv2.INTER_AREA if pct < 100 else cv2.INTER_CUBIC
            interp_name = "INTER_AREA" if pct < 100 else "INTER_CUBIC"
            out = cv2.resize(src, (nw, nh), interpolation=interp)
            self.out_heading_lbl.setText(f"RESIZED ({pct}%)")
            self.resize_info.setText(
                f"Scale  : {pct}%\n"
                f"Method : cv2.{interp_name}\n"
                f"Before : {w}×{h} ({h}, {w}, {c})\n"
                f"After  : {nw}×{nh} {out.shape}"
            )

        else:  # rotate
            rot_map = {
                90: (cv2.ROTATE_90_CLOCKWISE, "ROTATE_90_CLOCKWISE"),
                180: (cv2.ROTATE_180, "ROTATE_180"),
                270: (cv2.ROTATE_90_COUNTERCLOCKWISE, "ROTATE_90_COUNTERCLOCKWISE"),
            }
            code, name = rot_map[self.rot_angle]
            out = cv2.rotate(src, code)
            self.out_heading_lbl.setText(f"ROTATED {self.rot_angle}°")
            self.rot_info.setText(
                f"cv2.rotate(img, {name})\n\n"
                f"Before : ({h}, {w}, {c})\n"
                f"After  : {out.shape}\n"
                f"Note   : 90°/270° swaps height & width."
            )

        self.processed_img = out
        oh, ow = out.shape[:2]
        out_ch = "Gray (2D)" if out.ndim == 2 else f"BGR ({out.shape[2]}ch)"
        self.out_dim_lbl.setText(f"{ow}×{oh} • {out_ch}")
        self.status_lbl.setText(
            f"{self.current_filename} | Original: {src.shape} | Output: {out.shape} | "
            f"Pixel ({sy}, {sx}): BGR=[{b}, {g}, {r}] Gray={gray_px}"
        )

        self.orig_canvas.set_image(src)
        self.out_canvas.set_image(out)


def main() -> None:
    app = QApplication(sys.argv)
    win = Lab1Window(Path(__file__).resolve().parent)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
