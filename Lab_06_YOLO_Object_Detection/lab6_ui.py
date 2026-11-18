"""
CSST106 - Perception and Computer Vision
Laboratory Exercise No. 6 (Activity 5): Object Detection with YOLOv11 (PyQt6)

Covers all Lab 6 parts interactively:
  - Part 1: Pre-trained YOLOv11 inference on images & live webcam feed (confidence slider,
            bounding boxes, labels, confidence scores, inference latency/FPS, object counts)
  - Part 2: Custom dataset folder scaffolding & data.yaml / YOLO label format guide
  - Part 3 & 4: Training & evaluation CLI/Python workflow reference
  - Question & Notes: Object detection vs. image classification with real-world example
"""

from pathlib import Path
import shutil
import sys
import time
import torch  # Import before PyQt6/cv2 on Windows to avoid c10.dll WinError 1114
import cv2
import numpy as np
from PyQt6.QtCore import Qt, QRect, QTimer
from PyQt6.QtGui import QColor, QDragEnterEvent, QDropEvent, QImage, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)


def ensure_sample_image(sample_path: Path) -> Path:
    """Use Ultralytics' bundled bus.jpg if available, else generate a fallback scene."""
    if sample_path.exists():
        return sample_path
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from ultralytics.utils import ASSETS

        bus = Path(ASSETS) / "bus.jpg"
        if bus.exists():
            shutil.copyfile(bus, sample_path)
            return sample_path
    except Exception:
        pass

    # Offline fallback image
    img = np.full((480, 640, 3), (210, 215, 220), dtype=np.uint8)
    cv2.rectangle(img, (120, 180), (520, 380), (45, 95, 185), -1)
    cv2.circle(img, (210, 390), 36, (40, 40, 40), -1)
    cv2.circle(img, (430, 390), 36, (40, 40, 40), -1)
    cv2.putText(img, "Sample Scene", (215, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (35, 45, 55), 2)
    cv2.imwrite(str(sample_path), img)
    return sample_path


def scaffold_yolo_dataset(base_dir: Path) -> Path:
    """Create the Lab 6 YOLO custom dataset folder layout and data.yaml template."""
    ds_dir = base_dir / "dataset"
    for sub in ["images/train", "images/val", "labels/train", "labels/val"]:
        (ds_dir / sub).mkdir(parents=True, exist_ok=True)
    yaml_path = ds_dir / "data.yaml"
    if not yaml_path.exists():
        yaml_path.write_text(
            "train: ./dataset/images/train\n"
            "val: ./dataset/images/val\n"
            "nc: 2\n"
            "names: ['class1', 'class2']\n",
            encoding="utf-8",
        )
    return ds_dir


def cv_to_qpixmap(img: np.ndarray) -> QPixmap:
    """Convert BGR uint8 array to QPixmap."""
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimg.copy())


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


class Lab6Window(QMainWindow):
    """Tabbed interactive UI for CSST106 Lab 6 YOLOv11 Object Detection."""

    TABS = [
        ("detect", "Object Detection"),
        ("dataset", "Dataset && Training Guide"),
        ("qa", "Question && Notes"),
    ]

    def __init__(self, lab_dir: Path) -> None:
        super().__init__()
        self.lab_dir = lab_dir
        self.sample_path = ensure_sample_image(lab_dir / "sample_scene.jpg")
        self.weights_path = lab_dir / "yolo11n.pt"

        self.model = None
        self.model_error = ""
        self.bgr_img: np.ndarray | None = None
        self.annotated_img: np.ndarray | None = None
        self.current_filename = ""
        self.current_tab = "detect"

        self.cap: cv2.VideoCapture | None = None
        self.cam_timer = QTimer(self)
        self.cam_timer.timeout.connect(self._on_webcam_tick)

        self.setWindowTitle("CSST106 Lab 6 — YOLOv11 Object Detection")
        self.resize(1280, 750)
        self.setMinimumSize(980, 620)
        self.setAcceptDrops(True)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()
        self._load_yolo_model(str(self.weights_path))
        self.load_image(self.sample_path)

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
        lbl_title = QLabel("CSST106 Lab 6: Object Detection with YOLOv11")
        lbl_title.setObjectName("Title")
        lbl_sub = QLabel("Pre-trained YOLOv11n inference (image & webcam), custom YOLO dataset setup, and training workflow.")
        lbl_sub.setObjectName("Muted")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        top_bar.addLayout(title_box, 1)

        self.webcam_btn = QPushButton("Start Webcam")
        self.webcam_btn.clicked.connect(self._toggle_webcam)
        top_bar.addWidget(self.webcam_btn)

        for text, handler, accent in [
            ("Open Image...", self._on_open_image, False),
            ("Load Weights...", self._on_open_weights, False),
            ("Save Output...", self._on_save, True),
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
        self.tab_buttons["detect"].setChecked(True)
        layout.addWidget(tab_panel)

        # Body
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
            tl = QLabel("-")
            tl.setObjectName("Section")
            bl = QLabel("-")
            bl.setObjectName("Muted")
            hdr.addWidget(tl)
            hdr.addStretch()
            hdr.addWidget(bl)
            cl.addLayout(hdr)
            canvas = ImageCanvas()
            cl.addWidget(canvas, 1)
            body.addWidget(card, 1)
            self.view_cards.append(card)
            self.view_titles.append(tl)
            self.view_badges.append(bl)
            self.canvases.append(canvas)

        # Text card for Dataset/Training & Question
        self.text_card = QFrame()
        self.text_card.setObjectName("Panel")
        tcl = QVBoxLayout(self.text_card)
        tcl.setContentsMargins(16, 14, 16, 14)
        tcl.setSpacing(8)
        self.text_hdr = QLabel("GUIDE")
        self.text_hdr.setObjectName("Section")
        tcl.addWidget(self.text_hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        il_inner = QVBoxLayout(inner)
        il_inner.setContentsMargins(0, 0, 8, 0)
        self.text_body = QLabel()
        self.text_body.setWordWrap(True)
        self.text_body.setTextFormat(Qt.TextFormat.RichText)
        self.text_body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.text_body.setStyleSheet("color: #e2e8f0; font-size: 13px; line-height: 1.5;")
        il_inner.addWidget(self.text_body)
        il_inner.addStretch()
        scroll.setWidget(inner)
        tcl.addWidget(scroll, 1)
        self.text_card.hide()
        body.addWidget(self.text_card, 1)

        # Right Controls & Detections Drawer
        inspector = QFrame()
        inspector.setObjectName("Panel")
        inspector.setFixedWidth(305)
        il = QVBoxLayout(inspector)
        il.setContentsMargins(12, 10, 12, 12)
        il.setSpacing(9)

        hdr_p = QLabel("INFERENCE & DATASET")
        hdr_p.setObjectName("Section")
        il.addWidget(hdr_p)

        # Confidence threshold slider (10..90 -> 0.10..0.90)
        conf_top = QHBoxLayout()
        conf_top.addWidget(QLabel("Confidence Threshold:"))
        self.conf_lbl = QLabel("0.25")
        self.conf_lbl.setObjectName("Mono")
        conf_top.addStretch()
        conf_top.addWidget(self.conf_lbl)
        il.addLayout(conf_top)

        self.conf_slider = QSlider(Qt.Orientation.Horizontal)
        self.conf_slider.setRange(10, 90)
        self.conf_slider.setValue(25)
        self.conf_slider.valueChanged.connect(self._on_conf_changed)
        il.addWidget(self.conf_slider)

        scaffold_btn = QPushButton("Scaffold Custom dataset/ Folder")
        scaffold_btn.clicked.connect(self._on_scaffold_dataset)
        il.addWidget(scaffold_btn)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #334155;")
        il.addWidget(sep)

        det_scroll = QScrollArea()
        det_scroll.setWidgetResizable(True)
        det_scroll.setFrameShape(QFrame.Shape.NoFrame)
        det_scroll.setStyleSheet("background: transparent;")
        self.det_lbl = QLabel("Ready")
        self.det_lbl.setObjectName("Mono")
        self.det_lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.det_lbl.setWordWrap(True)
        det_scroll.setWidget(self.det_lbl)
        il.addWidget(det_scroll, 1)

        body.addWidget(inspector)

        self.status_lbl = QLabel("Ready")
        self.status_lbl.setObjectName("StatusBar")
        layout.addWidget(self.status_lbl)

    def _load_yolo_model(self, weights_ref: str) -> None:
        try:
            from ultralytics import YOLO

            self.model = YOLO(weights_ref)
            self.model_error = ""
        except Exception as exc:
            self.model = None
            self.model_error = str(exc)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if urls:
            path = Path(urls[0].toLocalFile())
            if path.is_file():
                self.load_image(path)

    def _on_open_image(self) -> None:
        self._stop_webcam()
        chosen, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            str(self.lab_dir),
            "Images (*.jpg *.jpeg *.png *.bmp *.webp)",
        )
        if chosen:
            self.load_image(Path(chosen))

    def _on_open_weights(self) -> None:
        chosen, _ = QFileDialog.getOpenFileName(
            self,
            "Load YOLO Weights (.pt)",
            str(self.lab_dir),
            "PyTorch Weights (*.pt)",
        )
        if chosen:
            self._load_yolo_model(chosen)
            self._run_detection_and_update()

    def _on_scaffold_dataset(self) -> None:
        ds = scaffold_yolo_dataset(self.lab_dir)
        QMessageBox.information(
            self,
            "Dataset Folder Created",
            f"Created YOLO dataset skeleton at:\n{ds}\n\nIncludes images/train, images/val, labels/train, labels/val, and data.yaml.",
        )

    def _toggle_webcam(self) -> None:
        if self.cam_timer.isActive():
            self._stop_webcam()
        else:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.cap.release()
                self.cap = None
                QMessageBox.warning(self, "Webcam", "Could not open default webcam (index 0).")
                return
            self.webcam_btn.setText("Stop Webcam")
            self.current_filename = "Webcam (0)"
            self.cam_timer.start(40)

    def _stop_webcam(self) -> None:
        if self.cam_timer.isActive():
            self.cam_timer.stop()
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.webcam_btn.setText("Start Webcam")

    def _on_webcam_tick(self) -> None:
        if self.cap is None:
            return
        ok, frame = self.cap.read()
        if ok and frame is not None:
            self.bgr_img = frame
            self._run_detection_and_update()

    def load_image(self, path: Path) -> None:
        bgr = cv2.imread(str(path))
        if bgr is None:
            return
        self.bgr_img = bgr
        self.current_filename = path.name
        self._run_detection_and_update()

    def _on_conf_changed(self, val: int) -> None:
        self.conf_lbl.setText(f"{val / 100:.2f}")
        self._run_detection_and_update()

    def _select_tab(self, key: str) -> None:
        self.current_tab = key
        self._run_detection_and_update()

    def _run_detection_and_update(self) -> None:
        if self.bgr_img is None:
            return
        conf = self.conf_slider.value() / 100.0
        h, w = self.bgr_img.shape[:2]

        detections: list[tuple[str, float, tuple[int, int, int, int]]] = []
        infer_ms = 0.0

        if self.model is not None:
            t0 = time.perf_counter()
            results = self.model.predict(self.bgr_img, conf=conf, verbose=False)
            infer_ms = (time.perf_counter() - t0) * 1000.0
            res0 = results[0]
            self.annotated_img = res0.plot()
            names = res0.names
            if res0.boxes is not None:
                for box in res0.boxes:
                    cls_id = int(box.cls[0])
                    score = float(box.conf[0])
                    x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                    detections.append((names[cls_id], score, (x1, y1, x2, y2)))
        else:
            self.annotated_img = self.bgr_img.copy()

        # Tab display
        if self.current_tab == "detect":
            self.text_card.hide()
            for c in self.view_cards:
                c.show()
            self.view_titles[0].setText(f"INPUT ({self.current_filename})")
            self.view_badges[0].setText(f"{w}×{h}")
            self.canvases[0].set_image(self.bgr_img)

            self.view_titles[1].setText("YOLOv11 DETECTIONS")
            self.view_badges[1].setText(f"{len(detections)} objects • {infer_ms:.1f} ms")
            self.canvases[1].set_image(self.annotated_img)
        else:
            for c in self.view_cards:
                c.hide()
            self.text_card.show()
            if self.current_tab == "dataset":
                self.text_hdr.setText("PART 2–4: CUSTOM DATASET PREPARATION, TRAINING & EVALUATION")
                self.text_body.setText(
                    """
                    <h3 style="color:#38bdf8; margin-top:0;">Part 2: Preparing a Custom Dataset</h3>
                    <p>Annotate images using <b>LabelImg</b> or <b>Roboflow</b> in YOLO format (one <code>.txt</code> per image with normalized coordinates):</p>
                    <pre style="background:#0b1120; padding:8px; border-radius:6px; color:#f1f5f9;">class_id x_center y_center width height</pre>
                    <p>Organize folders and create <code>data.yaml</code> (use the <b>Scaffold Custom dataset/ Folder</b> button on the right to generate this layout):</p>
                    <pre style="background:#0b1120; padding:8px; border-radius:6px; color:#f1f5f9;">/dataset
├── /images/{train, val}
├── /labels/{train, val}
└── data.yaml  (train, val, nc, names)</pre>

                    <h3 style="color:#38bdf8; margin-top:10px;">Part 3: Training YOLOv11</h3>
                    <pre style="background:#0b1120; padding:8px; border-radius:6px; color:#f1f5f9;">yolo task=detect mode=train model=yolo11n.pt data=data.yaml epochs=100 imgsz=640</pre>
                    <p>Or programmatically in Python:</p>
                    <pre style="background:#0b1120; padding:8px; border-radius:6px; color:#f1f5f9;">from ultralytics import YOLO
model = YOLO('yolo11n.pt')
model.train(data='data.yaml', epochs=100, imgsz=640)</pre>

                    <h3 style="color:#38bdf8; margin-top:10px;">Part 4: Validation &amp; Inference</h3>
                    <pre style="background:#0b1120; padding:8px; border-radius:6px; color:#f1f5f9;">yolo task=detect mode=val model=runs/detect/train/weights/best.pt data=data.yaml</pre>
                    """
                )
            else:
                self.text_hdr.setText("LAB 6 — QUESTION & REFERENCES")
                self.text_body.setText(
                    """
                    <h3 style="color:#38bdf8; margin-top:0;">Question:</h3>
                    <p><i>What is object detection in computer vision, and how does it differ from image classification? Explain your answer using a real-world example.</i></p>

                    <h3 style="color:#38bdf8; margin-top:10px;">Answer:</h3>
                    <p><b>Image classification</b> assigns a single overall label to an entire image (answering <i>"What is in this image?"</i>), without telling you where objects are located or how many exist.</p>
                    <p><b>Object detection</b> performs both <b>classification</b> and <b>localization</b> simultaneously (answering <i>"What objects are in this image, and exactly where is each one?"</i>). It outputs bounding-box coordinates <code>(x1, y1, x2, y2)</code>, a class label, and a confidence score for every detected instance.</p>
                    <p><b>Real-World Example (Autonomous Driving / Traffic Monitoring):</b><br>
                    An image classifier looking at a dashcam frame might only label it <code>"street"</code> or <code>"car"</code>. An object detector like <b>YOLOv11</b> draws separate bounding boxes around every <i>person</i>, <i>car</i>, <i>bus</i>, and <i>traffic light</i> in the frame simultaneously, allowing the vehicle to compute distances, avoid pedestrians, and obey traffic signals in real time.</p>
                    """
                )

        # Right inspector summary
        counts: dict[str, int] = {}
        for name, _sc, _box in detections:
            counts[name] = counts.get(name, 0) + 1
        summary_lines = [f"Model   : yolo11n.pt" if self.model else f"Model Error: {self.model_error}",
                         f"Input   : {self.current_filename} ({w}×{h})",
                         f"Conf    : {conf:.2f}",
                         f"Latency : {infer_ms:.1f} ms",
                         f"Objects : {len(detections)}",
                         ""]
        if counts:
            summary_lines.append("Class Counts:")
            for k, v in sorted(counts.items()):
                summary_lines.append(f"  {k:<14}: {v}")
            summary_lines.append("")
            summary_lines.append("Boxes (label | conf | xyxy):")
            for name, sc, (x1, y1, x2, y2) in detections[:15]:
                summary_lines.append(f"  {name} ({sc:.2f}) [{x1},{y1},{x2},{y2}]")
        self.det_lbl.setText("\n".join(summary_lines))

        fps = (1000.0 / infer_ms) if infer_ms > 0 else 0.0
        self.status_lbl.setText(
            f"{self.current_filename} ({w}×{h}) | Conf={conf:.2f} | "
            f"Detections={len(detections)} | {infer_ms:.1f} ms ({fps:.1f} FPS)"
        )

    def _on_save(self) -> None:
        if self.annotated_img is None:
            return
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Detection Output",
            str(self.lab_dir / "yolo_detection_output.png"),
            "PNG (*.png);;JPEG (*.jpg)",
        )
        if save_path:
            cv2.imwrite(save_path, self.annotated_img)

    def closeEvent(self, event) -> None:
        self._stop_webcam()
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    win = Lab6Window(Path(__file__).resolve().parent)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
