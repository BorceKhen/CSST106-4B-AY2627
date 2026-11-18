"""
CSST 106 - Perception and Computer Vision
Computer Vision Laboratory Suite — Interactive Landing Hub (PyQt6)

Features crisp QPainter-rendered vector icons for every lab and button,
per-lab color accents, topic filter chips, search, live running-lab counter,
and one-click access to all UIs, Reports, and Manuals.
"""

from pathlib import Path
import subprocess
import sys
import webbrowser
from PyQt6.QtCore import Qt, QPointF, QRectF, QTimer, QUrl
from PyQt6.QtGui import QColor, QDesktopServices, QIcon, QPainter, QPen, QPixmap, QPolygonF
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

# Insert your Git/GitHub repository URL below once created (e.g., "https://github.com/username/csst106-cv-labs")
REPO_URL = "https://github.com/BorceKhen/CSST106-4B-AY2627"

LABS = [
    {
        "num": "Lab 01",
        "week": "Week 1–2",
        "category": "Image Processing",
        "accent": "#38bdf8",
        "hover": "#0284c7",
        "icon": "image",
        "title": "Image Representation & Manipulation",
        "desc": "Explore 2D/3D pixel arrays, BGR vs. grayscale, pixel editing, ROI cropping, resizing, and 90° rotation.",
        "folder": "Lab_01_Images",
        "script": "lab1_ui.py",
        "report": "Lab_01_Report.docx",
        "manual": "CSST106_Lab_Experiment_01_Images.docx",
    },
    {
        "num": "Lab 02",
        "week": "Week 3–4",
        "category": "Image Processing",
        "accent": "#a78bfa",
        "hover": "#7c3aed",
        "icon": "edges",
        "title": "Edge Detection (Sobel vs. Canny)",
        "desc": "Gaussian smoothing, Sobel directional X/Y gradients & magnitude, Canny hysteresis (T1/T2), and Q&A.",
        "folder": "Lab_02_Edge_Detection",
        "script": "lab2_ui.py",
        "report": "Lab_02_Report.docx",
        "manual": "CSST106_Lab_Experiment_02_Edge_Detection.docx",
    },
    {
        "num": "Lab 03",
        "week": "Week 4–5",
        "category": "Image Processing",
        "accent": "#34d399",
        "hover": "#059669",
        "icon": "histogram",
        "title": "Histogram Equalization & Contrast",
        "desc": "Global equalizeHist (Gray & YUV), linear contrast stretch, adaptive CLAHE tuning, and live histograms.",
        "folder": "Lab_03_Histogram",
        "script": "lab3_ui.py",
        "report": "Lab_03_Report.docx",
        "manual": "CSST106_Lab_Experiment_03_Histogram.docx",
    },
    {
        "num": "Lab 04",
        "week": "Week 6",
        "category": "Features & ML",
        "accent": "#fbbf24",
        "hover": "#d97706",
        "icon": "features",
        "title": "SURF, SIFT & ORB Feature Matching",
        "desc": "Rich keypoint detection, two-image BFMatcher matching, SIFT vs. ORB benchmark, and U-SURF notes.",
        "folder": "Lab_04_SURF_Feature_Detection",
        "script": "lab4_ui.py",
        "report": "Lab_04_Report.docx",
        "manual": "CSST106_Lab_Experiment_04_SURF_Feature_Detection.docx",
    },
    {
        "num": "Lab 05",
        "week": "Week 7–8",
        "category": "Features & ML",
        "accent": "#f472b6",
        "hover": "#db2777",
        "icon": "face",
        "title": "PCA Facial Recognition (Eigenfaces)",
        "desc": "LFW faces, Eigenfaces gallery, 90% variance curve, whitening comparison, RBF SVM, and failure analysis.",
        "folder": "Lab_05_PCA_in_CV",
        "script": "lab5_ui.py",
        "report": "Lab_05_Report.docx",
        "manual": "CSST106_Lab_Experiment_05_PCA_in_CV.docx",
    },
    {
        "num": "Lab 06",
        "week": "Week 8–9",
        "category": "Deep Learning",
        "accent": "#fb7185",
        "hover": "#e11d48",
        "icon": "yolo",
        "title": "YOLOv11 Real-Time Object Detection",
        "desc": "Pre-trained YOLOv11n inference on images & live webcam, confidence tuning, and custom dataset setup.",
        "folder": "Lab_06_YOLO_Object_Detection",
        "script": "lab6_ui.py",
        "report": "Lab_06_Report.docx",
        "manual": "CSST106_Lab_Experiment_06_YOLOV8_Object_Detection.docx",
    },
    {
        "num": "Lab 07",
        "week": "Week 13",
        "category": "Deep Learning",
        "accent": "#2dd4bf",
        "hover": "#0d9488",
        "icon": "segment",
        "title": "Image Segmentation Techniques",
        "desc": "Otsu/Adaptive thresholding, Region Growing & Watershed, Canny contours, DeepLabV3, and IoU metrics.",
        "folder": "Lab_07_Segmentation",
        "script": "lab7_ui.py",
        "report": "Lab_07_Report.docx",
        "manual": "CSST106_Lab_Experiment_07_Segmetation.docx",
    },
]


def draw_vector_icon(kind: str, color_hex: str, size: int = 24, bg_hex: str | None = None) -> QPixmap:
    """Render a crisp custom vector icon using QPainter."""
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    if bg_hex:
        bg = QColor(bg_hex)
        bg.setAlpha(38)
        p.setBrush(bg)
        p.setPen(QPen(QColor(color_hex), 1.4))
        p.drawRoundedRect(QRectF(1, 1, size - 2, size - 2), size * 0.24, size * 0.24)

    fg = QColor(color_hex)
    pen = QPen(fg, max(1.6, size * 0.08), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    s = float(size)
    if kind == "vision":
        p.drawEllipse(QRectF(s * 0.14, s * 0.24, s * 0.72, s * 0.52))
        p.setBrush(fg)
        p.drawEllipse(QPointF(s * 0.5, s * 0.5), s * 0.15, s * 0.15)
        p.setBrush(QColor("#0f172a"))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(s * 0.54, s * 0.46), s * 0.045, s * 0.045)
    elif kind == "image":
        p.drawRoundedRect(QRectF(s * 0.2, s * 0.22, s * 0.6, s * 0.56), 3, 3)
        p.setBrush(fg)
        p.drawEllipse(QPointF(s * 0.36, s * 0.38), s * 0.06, s * 0.06)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPolyline(QPolygonF([
            QPointF(s * 0.25, s * 0.7), QPointF(s * 0.44, s * 0.5),
            QPointF(s * 0.56, s * 0.62), QPointF(s * 0.68, s * 0.45), QPointF(s * 0.76, s * 0.7),
        ]))
    elif kind == "edges":
        p.drawPolyline(QPolygonF([
            QPointF(s * 0.2, s * 0.68), QPointF(s * 0.36, s * 0.32),
            QPointF(s * 0.52, s * 0.66), QPointF(s * 0.66, s * 0.28), QPointF(s * 0.82, s * 0.54),
        ]))
    elif kind == "histogram":
        p.setBrush(fg)
        p.setPen(Qt.PenStyle.NoPen)
        bars = [(0.22, 0.54, 0.24), (0.37, 0.34, 0.44), (0.52, 0.24, 0.54), (0.67, 0.44, 0.34)]
        for bx, by, bh in bars:
            p.drawRoundedRect(QRectF(s * bx, s * by, s * 0.10, s * bh), 1.5, 1.5)
    elif kind == "features":
        pts = [(0.3, 0.35), (0.68, 0.28), (0.52, 0.58), (0.28, 0.72), (0.72, 0.7)]
        for a, b in [(0, 1), (0, 2), (2, 3), (2, 4), (1, 4)]:
            p.drawLine(QPointF(s * pts[a][0], s * pts[a][1]), QPointF(s * pts[b][0], s * pts[b][1]))
        p.setBrush(fg)
        for px, py in pts:
            p.drawEllipse(QPointF(s * px, s * py), s * 0.065, s * 0.065)
    elif kind == "face":
        p.drawRoundedRect(QRectF(s * 0.24, s * 0.2, s * 0.52, s * 0.6), 7, 7)
        p.setBrush(fg)
        p.drawEllipse(QPointF(s * 0.4, s * 0.44), s * 0.045, s * 0.045)
        p.drawEllipse(QPointF(s * 0.6, s * 0.44), s * 0.045, s * 0.045)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawArc(QRectF(s * 0.38, s * 0.5, s * 0.24, s * 0.18), 200 * 16, 140 * 16)
    elif kind == "yolo":
        for x0, y0, dx, dy in [(0.22, 0.22, 0.16, 0.16), (0.78, 0.22, -0.16, 0.16),
                               (0.22, 0.78, 0.16, -0.16), (0.78, 0.78, -0.16, -0.16)]:
            p.drawLine(QPointF(s * x0, s * y0), QPointF(s * (x0 + dx), s * y0))
            p.drawLine(QPointF(s * x0, s * y0), QPointF(s * x0, s * (y0 + dy)))
        p.drawEllipse(QPointF(s * 0.5, s * 0.5), s * 0.12, s * 0.12)
    elif kind == "segment":
        p.setBrush(QColor(fg.red(), fg.green(), fg.blue(), 90))
        p.drawEllipse(QRectF(s * 0.22, s * 0.26, s * 0.42, s * 0.42))
        p.setBrush(QColor(fg.red(), fg.green(), fg.blue(), 175))
        p.drawEllipse(QRectF(s * 0.38, s * 0.36, s * 0.40, s * 0.40))
    elif kind == "play":
        p.setBrush(fg)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(QPolygonF([QPointF(s * 0.28, s * 0.22), QPointF(s * 0.78, s * 0.5), QPointF(s * 0.28, s * 0.78)]))
    elif kind == "doc":
        p.drawRoundedRect(QRectF(s * 0.24, s * 0.16, s * 0.52, s * 0.68), 2.5, 2.5)
        for y in (0.38, 0.52, 0.66):
            p.drawLine(QPointF(s * 0.34, s * y), QPointF(s * 0.66, s * y))
    elif kind == "book":
        p.drawRoundedRect(QRectF(s * 0.22, s * 0.2, s * 0.56, s * 0.6), 2.5, 2.5)
        p.drawLine(QPointF(s * 0.36, s * 0.2), QPointF(s * 0.36, s * 0.8))
    elif kind == "git":
        p.drawLine(QPointF(s * 0.34, s * 0.26), QPointF(s * 0.34, s * 0.74))
        p.drawPolyline(QPolygonF([QPointF(s * 0.34, s * 0.58), QPointF(s * 0.66, s * 0.46), QPointF(s * 0.66, s * 0.32)]))
        p.setBrush(fg)
        for cx, cy in [(0.34, 0.26), (0.34, 0.74), (0.66, 0.32)]:
            p.drawEllipse(QPointF(s * cx, s * cy), s * 0.08, s * 0.08)

    p.end()
    return pm


STYLESHEET = """
QMainWindow, QWidget#Root {
    background-color: #0b1120;
    color: #e2e8f0;
    font-family: "Segoe UI", sans-serif;
}
QWidget#GridHost, QScrollArea#CardsScroll {
    background: transparent;
}
QFrame#HeroCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #172554, stop:0.55 #1e293b, stop:1 #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
}
QFrame#FilterBar {
    background-color: #131c31;
    border: 1px solid #25334d;
    border-radius: 9px;
}
QFrame#LabCard {
    background-color: #162033;
    border: 1px solid #29354d;
    border-radius: 11px;
}
QLabel#CourseBadge {
    background-color: #f8fafc;
    color: #0f172a;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
}
QLabel#Tag {
    background-color: #0f172a;
    color: #94a3b8;
    border: 1px solid #334155;
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 5px;
}
QLabel#HeroTitle {
    color: #f8fafc;
    font-size: 21px;
    font-weight: 700;
}
QLabel#CardTitle {
    color: #f8fafc;
    font-size: 14px;
    font-weight: 700;
}
QLabel#MetaLabel {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 600;
}
QLabel#MetaValue {
    color: #f1f5f9;
    font-size: 13px;
    font-weight: 700;
}
QLabel#Muted {
    color: #94a3b8;
    font-size: 12px;
}
QLabel#StatusBar {
    color: #cbd5e1;
    font-family: "Consolas", monospace;
    font-size: 11px;
    padding: 6px 10px;
    background-color: #131c31;
    border: 1px solid #25334d;
    border-radius: 7px;
}
QLineEdit#SearchBox {
    background-color: #0b1120;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}
QLineEdit#SearchBox:focus {
    border-color: #38bdf8;
}
QPushButton {
    background-color: #223047;
    color: #e2e8f0;
    border: 1px solid #354764;
    border-radius: 7px;
    padding: 7px 12px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #2d3f5e;
    border-color: #64748b;
}
QPushButton#ChipBtn {
    background-color: transparent;
    border: 1px solid transparent;
    color: #94a3b8;
    padding: 6px 12px;
}
QPushButton#ChipBtn:hover {
    background-color: #1e293b;
    color: #f8fafc;
}
QPushButton#ChipBtn:checked {
    background-color: #0284c7;
    color: #ffffff;
    border: 1px solid #38bdf8;
}
"""


class LandingWindow(QMainWindow):
    """Fun, icon-rich landing hub for CSST 106 Computer Vision Labs 1–7."""

    CATEGORIES = ["All", "Image Processing", "Features & ML", "Deep Learning"]

    def __init__(self, base_dir: Path) -> None:
        super().__init__()
        self.base_dir = base_dir
        self.processes: list[tuple[str, subprocess.Popen]] = []
        self.card_widgets: list[tuple[dict, QFrame]] = []
        self.active_category = "All"

        self.setWindowTitle("CSST 106 — Computer Vision Laboratory Suite")
        self.setWindowIcon(QIcon(draw_vector_icon("vision", "#38bdf8", 32, "#0f172a")))
        self.resize(1240, 800)
        self.setMinimumSize(980, 640)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()

        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self._refresh_running_count)
        self.poll_timer.start(1500)

    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(16, 14, 16, 14)
        outer.setSpacing(10)

        # 1. Hero Header Card
        hero = QFrame()
        hero.setObjectName("HeroCard")
        hl = QHBoxLayout(hero)
        hl.setContentsMargins(20, 16, 20, 16)
        hl.setSpacing(16)

        # App Vision Logo on the left
        logo_lbl = QLabel()
        logo_lbl.setPixmap(draw_vector_icon("vision", "#38bdf8", 58, "#0284c7"))
        hl.addWidget(logo_lbl)

        left_col = QVBoxLayout()
        left_col.setSpacing(5)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(8)
        course_badge = QLabel("CSST 106")
        course_badge.setObjectName("CourseBadge")
        sem_tag = QLabel("Perception and Computer Vision • 1st Semester, AY 2026–2027")
        sem_tag.setObjectName("Tag")
        badge_row.addWidget(course_badge)
        badge_row.addWidget(sem_tag)
        badge_row.addStretch()
        left_col.addLayout(badge_row)

        hero_title = QLabel("Computer Vision Laboratory Suite")
        hero_title.setObjectName("HeroTitle")
        left_col.addWidget(hero_title)

        info_row = QHBoxLayout()
        info_row.setSpacing(24)
        for label_txt, val_txt in [("Student", "Ron Ken S. Borce"), ("Section", "BSCS 4B")]:
            pair = QVBoxLayout()
            pair.setSpacing(1)
            l_k = QLabel(label_txt)
            l_k.setObjectName("MetaLabel")
            l_v = QLabel(val_txt)
            l_v.setObjectName("MetaValue")
            pair.addWidget(l_k)
            pair.addWidget(l_v)
            info_row.addLayout(pair)
        info_row.addStretch()
        left_col.addLayout(info_row)
        hl.addLayout(left_col, 1)

        # Right Action Buttons
        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        right_col.setSpacing(8)

        repo_btn = QPushButton("View Repository")
        repo_btn.setIcon(QIcon(draw_vector_icon("git", "#e2e8f0", 16)))
        repo_btn.clicked.connect(self._on_view_repo)
        right_col.addWidget(repo_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.live_badge = QLabel(f"{len(LABS)} / {len(LABS)} Labs Ready • 0 Running")
        self.live_badge.setObjectName("Tag")
        right_col.addWidget(self.live_badge, alignment=Qt.AlignmentFlag.AlignRight)

        hl.addLayout(right_col)
        outer.addWidget(hero)

        # 2. Filter & Search Bar
        filter_bar = QFrame()
        filter_bar.setObjectName("FilterBar")
        fl = QHBoxLayout(filter_bar)
        fl.setContentsMargins(10, 6, 10, 6)
        fl.setSpacing(6)

        self.cat_group = QButtonGroup(self)
        self.cat_group.setExclusive(True)
        for cat in self.CATEGORIES:
            b = QPushButton(cat.replace("&", "&&"))
            b.setObjectName("ChipBtn")
            b.setCheckable(True)
            if cat == "All":
                b.setChecked(True)
            b.clicked.connect(lambda _chk, c=cat: self._set_category(c))
            self.cat_group.addButton(b)
            fl.addWidget(b)

        fl.addStretch()
        self.search_box = QLineEdit()
        self.search_box.setObjectName("SearchBox")
        self.search_box.setPlaceholderText("Filter labs (e.g., Canny, YOLO, PCA, Segmentation)...")
        self.search_box.setFixedWidth(290)
        self.search_box.textChanged.connect(self._apply_filters)
        fl.addWidget(self.search_box)
        outer.addWidget(filter_bar)

        # 3. Scrollable 2-Column Lab Cards Grid
        scroll = QScrollArea()
        scroll.setObjectName("CardsScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.grid_host = QWidget()
        self.grid_host.setObjectName("GridHost")
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(0, 0, 4, 0)
        self.grid.setSpacing(12)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)

        for lab in LABS:
            card = self._make_lab_card(lab)
            self.card_widgets.append((lab, card))

        self._relayout_cards(LABS)
        scroll.setWidget(self.grid_host)
        outer.addWidget(scroll, 1)

        # 4. Status Bar
        self.status_lbl = QLabel("Pick any lab card to launch its interactive UI or open its Report/Manual.")
        self.status_lbl.setObjectName("StatusBar")
        outer.addWidget(self.status_lbl)

    def _make_lab_card(self, lab: dict) -> QFrame:
        accent = lab["accent"]
        hover = lab["hover"]

        card = QFrame()
        card.setObjectName("LabCard")
        card.setStyleSheet(
            f"QFrame#LabCard {{ background-color: #162033; border: 1px solid #29354d; "
            f"border-left: 4px solid {accent}; border-radius: 11px; }}"
            f"QFrame#LabCard:hover {{ border-color: {accent}; background-color: #1a263c; }}"
        )

        cl = QVBoxLayout(card)
        cl.setContentsMargins(15, 13, 15, 13)
        cl.setSpacing(8)

        # Header row: icon + Lab badge + Week + Category
        top = QHBoxLayout()
        top.setSpacing(10)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(draw_vector_icon(lab["icon"], accent, 38, accent))
        top.addWidget(icon_lbl)

        meta_col = QVBoxLayout()
        meta_col.setSpacing(3)
        badges = QHBoxLayout()
        badges.setSpacing(6)

        b_num = QLabel(lab["num"])
        b_num.setStyleSheet(
            f"background-color: {accent}; color: #0f172a; font-size: 11px; "
            f"font-weight: 700; padding: 2px 8px; border-radius: 5px;"
        )
        b_week = QLabel(lab["week"])
        b_week.setObjectName("Tag")
        b_cat = QLabel(lab["category"])
        b_cat.setObjectName("Tag")
        badges.addWidget(b_num)
        badges.addWidget(b_week)
        badges.addWidget(b_cat)
        badges.addStretch()
        meta_col.addLayout(badges)

        title = QLabel(lab["title"])
        title.setObjectName("CardTitle")
        title.setWordWrap(True)
        meta_col.addWidget(title)
        top.addLayout(meta_col, 1)
        cl.addLayout(top)

        desc = QLabel(lab["desc"])
        desc.setObjectName("Muted")
        desc.setWordWrap(True)
        cl.addWidget(desc, 1)

        # Action Buttons with icons
        actions = QHBoxLayout()
        actions.setSpacing(8)

        launch_btn = QPushButton("Launch UI")
        launch_btn.setIcon(QIcon(draw_vector_icon("play", "#0f172a", 14)))
        launch_btn.setStyleSheet(
            f"QPushButton {{ background-color: {accent}; color: #0f172a; border: 1px solid {accent}; "
            f"border-radius: 7px; padding: 7px 12px; font-weight: 700; }}"
            f"QPushButton:hover {{ background-color: {hover}; color: #ffffff; border-color: {hover}; }}"
        )
        launch_btn.clicked.connect(lambda _chk, item=lab: self._launch_lab(item))

        report_btn = QPushButton("Report")
        report_btn.setIcon(QIcon(draw_vector_icon("doc", "#cbd5e1", 14)))
        report_btn.clicked.connect(lambda _chk, item=lab: self._open_doc(item, "report"))

        manual_btn = QPushButton("Manual")
        manual_btn.setIcon(QIcon(draw_vector_icon("book", "#cbd5e1", 14)))
        manual_btn.clicked.connect(lambda _chk, item=lab: self._open_doc(item, "manual"))

        actions.addWidget(launch_btn, 2)
        actions.addWidget(report_btn, 1)
        actions.addWidget(manual_btn, 1)
        cl.addLayout(actions)
        return card

    def _set_category(self, category: str) -> None:
        self.active_category = category
        self._apply_filters()

    def _apply_filters(self) -> None:
        query = self.search_box.text().strip().lower()
        visible_labs = []
        for lab, card in self.card_widgets:
            cat_ok = self.active_category == "All" or lab["category"] == self.active_category
            text_ok = not query or (
                query in lab["title"].lower()
                or query in lab["desc"].lower()
                or query in lab["num"].lower()
                or query in lab["category"].lower()
            )
            if cat_ok and text_ok:
                visible_labs.append(lab)
            else:
                card.hide()
        self._relayout_cards(visible_labs)

    def _relayout_cards(self, visible_labs: list[dict]) -> None:
        while self.grid.count():
            self.grid.takeAt(0)
        visible_nums = {lab["num"] for lab in visible_labs}
        idx = 0
        for lab, card in self.card_widgets:
            if lab["num"] in visible_nums:
                card.show()
                self.grid.addWidget(card, idx // 2, idx % 2)
                idx += 1

    def _launch_lab(self, lab: dict) -> None:
        script_path = self.base_dir / lab["folder"] / lab["script"]
        if not script_path.exists():
            QMessageBox.warning(self, "Missing Script", f"Could not find:\n{script_path}")
            return
        proc = subprocess.Popen(
            [sys.executable, "-B", str(script_path)],
            cwd=str(script_path.parent),
        )
        self.processes.append((lab["num"], proc))
        self._refresh_running_count()
        self.status_lbl.setText(f"Launched {lab['num']}: {lab['title']} (PID {proc.pid})")

    def _refresh_running_count(self) -> None:
        self.processes = [(n, p) for n, p in self.processes if p.poll() is None]
        self.live_badge.setText(f"{len(LABS)} / {len(LABS)} Labs Ready • {len(self.processes)} Running")

    def _open_doc(self, lab: dict, kind: str) -> None:
        doc_path = self.base_dir / lab["folder"] / lab[kind]
        if not doc_path.exists():
            QMessageBox.warning(self, "File Not Found", f"Could not find:\n{doc_path}")
            return
        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(doc_path))):
            QMessageBox.warning(self, "Open Failed", f"Could not open:\n{doc_path}")
            return
        self.status_lbl.setText(f"Opened {lab['num']} {kind}: {doc_path.name}")

    def _on_view_repo(self) -> None:
        if REPO_URL.strip():
            webbrowser.open(REPO_URL.strip())
            self.status_lbl.setText(f"Opened repository: {REPO_URL.strip()}")
        else:
            QMessageBox.information(
                self,
                "Repository Link Not Set",
                "The repository has not been linked yet.\n\n"
                "Once created, set REPO_URL at the top of main.py:\n"
                'REPO_URL = "https://github.com/your-username/your-repo"',
            )
            self.status_lbl.setText("Repository link pending — set REPO_URL in main.py once created.")


def main() -> None:
    app = QApplication(sys.argv)
    win = LandingWindow(Path(__file__).resolve().parent)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
