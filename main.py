"""
CSST 106 - Perception and Computer Vision
Computer Vision Laboratory Suite — Interactive Landing Hub (PyQt6)

Features crisp QPainter-rendered vector icons for every lab and button,
per-lab color accents, topic filter chips, search, live running-lab counter,
and one-click access to all UIs, Reports, and Manuals.
"""

import importlib.metadata
import math
from pathlib import Path
import subprocess
import sys
import webbrowser
from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QRectF, Qt, QTimer, QUrl
from PyQt6.QtGui import QColor, QDesktopServices, QIcon, QPainter, QPen, QPixmap, QPolygonF
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
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
        "report": "Borce_Lab_01_Report.docx",
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
        "report": "Borce_Lab_02_Report.docx",
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
        "report": "Borce_Lab_03_Report.docx",
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
        "report": "Borce_Lab_04_Report.docx",
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
        "report": "Borce_Lab_05_Report.docx",
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
        "report": "Borce_Lab_06_Report.docx",
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
        "report": "Borce_Lab_07_Report.docx",
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
    elif kind == "sun":
        p.drawEllipse(QPointF(s * 0.5, s * 0.5), s * 0.18, s * 0.18)
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            p.drawLine(
                QPointF(s * (0.5 + 0.28 * math.cos(rad)), s * (0.5 + 0.28 * math.sin(rad))),
                QPointF(s * (0.5 + 0.38 * math.cos(rad)), s * (0.5 + 0.38 * math.sin(rad))),
            )
    elif kind == "moon":
        p.setBrush(fg)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(s * 0.48, s * 0.5), s * 0.29, s * 0.29)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        p.drawEllipse(QPointF(s * 0.61, s * 0.41), s * 0.24, s * 0.24)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
    elif kind == "search":
        p.drawEllipse(QPointF(s * 0.43, s * 0.43), s * 0.23, s * 0.23)
        p.drawLine(QPointF(s * 0.60, s * 0.60), QPointF(s * 0.80, s * 0.80))
    elif kind == "env":
        p.drawRoundedRect(QRectF(s * 0.26, s * 0.26, s * 0.48, s * 0.48), 3, 3)
        for t in (0.38, 0.62):
            p.drawLine(QPointF(s * t, s * 0.14), QPointF(s * t, s * 0.26))
            p.drawLine(QPointF(s * t, s * 0.74), QPointF(s * t, s * 0.86))
            p.drawLine(QPointF(s * 0.14, s * t), QPointF(s * 0.26, s * t))
            p.drawLine(QPointF(s * 0.74, s * t), QPointF(s * 0.86, s * t))
        p.setBrush(fg)
        p.drawEllipse(QPointF(s * 0.5, s * 0.5), s * 0.08, s * 0.08)

    p.end()
    return pm


def probe_env_packages() -> list[tuple[str, str | None]]:
    """Return quick metadata version checks without heavy DLL imports."""
    pkgs = [
        ("Python", None),
        ("PyQt6", "PyQt6"),
        ("OpenCV", "opencv-python"),
        ("NumPy", "numpy"),
        ("PyTorch", "torch"),
        ("Ultralytics", "ultralytics"),
        ("scikit-learn", "scikit-learn"),
    ]
    out: list[tuple[str, str | None]] = []
    for label, dist in pkgs:
        if dist is None:
            out.append((label, f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"))
            continue
        try:
            ver = importlib.metadata.version(dist)
        except importlib.metadata.PackageNotFoundError:
            ver = None
        out.append((label, ver))
    return out


def build_stylesheet(theme: str) -> str:
    """Return dark or light QSS stylesheet for the Landing Suite."""
    if theme == "light":
        return """
        QMainWindow, QWidget#Root { background-color: #f1f5f9; color: #1e293b; font-family: "Segoe UI", sans-serif; }
        QWidget#GridHost, QScrollArea#CardsScroll { background: transparent; }
        QFrame#HeroCard {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #dbeafe, stop:0.55 #eff6ff, stop:1 #ffffff);
            border: 1px solid #93c5fd; border-radius: 12px;
        }
        QFrame#FilterBar { background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 9px; }
        QFrame#StatusFrame { background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; }
        QFrame#ThemeSwitch { background-color: #e2e8f0; border: 1px solid #cbd5e1; border-radius: 8px; }
        QPushButton#SegBtn {
            background: transparent; border: none; border-radius: 6px; padding: 5px 8px; color: #475569;
        }
        QPushButton#SegBtn:hover { background-color: rgba(15, 23, 42, 0.06); }
        QPushButton#SegBtn:checked { background-color: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; }
        QLabel#CourseBadge { background-color: #0f172a; color: #f8fafc; font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 6px; }
        QLabel#Tag { background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-size: 11px; padding: 2px 8px; border-radius: 5px; }
        QLabel#TelemetryPill { background-color: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; font-family: "Consolas", monospace; font-size: 11px; font-weight: 600; padding: 2px 9px; border-radius: 9px; }
        QLabel#HeroTitle { color: #0f172a; font-size: 19px; font-weight: 700; }
        QLabel#CardTitle { color: #0f172a; font-size: 13.5px; font-weight: 700; }
        QLabel#MetaLabel { color: #475569; font-size: 10.5px; font-weight: 600; }
        QLabel#MetaValue { color: #0f172a; font-size: 12.5px; font-weight: 700; }
        QLabel#Muted { color: #475569; font-size: 11.5px; }
        QLabel#StatusBar { color: #475569; font-family: "Consolas", monospace; font-size: 11px; }
        QLineEdit#SearchBox { background-color: #f8fafc; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 7px; padding: 5px 10px; font-size: 12px; }
        QLineEdit#SearchBox:focus { border-color: #0284c7; }
        QPushButton { background-color: #e2e8f0; color: #1e293b; border: 1px solid #cbd5e1; border-radius: 7px; padding: 6px 12px; font-size: 12px; font-weight: 600; }
        QPushButton:hover { background-color: #cbd5e1; }
        QPushButton#LaunchBtn {
            background-color: #0284c7; color: #ffffff; border: 1px solid #38bdf8;
            border-radius: 7px; padding: 6px 11px; font-size: 12px; font-weight: 700;
        }
        QPushButton#LaunchBtn:hover { background-color: #0369a1; border-color: #7dd3fc; }
        QPushButton#GhostBtn {
            background-color: transparent; color: #475569; border: 1px solid #cbd5e1;
            border-radius: 7px; padding: 6px 9px; font-size: 11.5px; font-weight: 600;
        }
        QPushButton#GhostBtn:hover { background-color: #e2e8f0; color: #0f172a; border-color: #94a3b8; }
        QPushButton#ChipBtn { background-color: transparent; border: 1px solid transparent; color: #475569; padding: 5px 11px; font-size: 12px; }
        QPushButton#ChipBtn:hover { background-color: #e2e8f0; color: #0f172a; }
        QPushButton#ChipBtn:checked { background-color: #0284c7; color: #ffffff; border: 1px solid #38bdf8; }
        """
    return """
    QMainWindow, QWidget#Root { background-color: #0b1120; color: #e2e8f0; font-family: "Segoe UI", sans-serif; }
    QWidget#GridHost, QScrollArea#CardsScroll { background: transparent; }
    QFrame#HeroCard {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #172554, stop:0.55 #1e293b, stop:1 #0f172a);
        border: 1px solid #334155; border-radius: 12px;
    }
    QFrame#FilterBar { background-color: #131c31; border: 1px solid #25334d; border-radius: 9px; }
    QFrame#StatusFrame { background-color: #131c31; border: 1px solid #25334d; border-radius: 8px; }
    QFrame#ThemeSwitch { background-color: #0f172a; border: 1px solid #334155; border-radius: 8px; }
    QPushButton#SegBtn {
        background: transparent; border: none; border-radius: 6px; padding: 5px 8px; color: #94a3b8;
    }
    QPushButton#SegBtn:hover { background-color: #1e293b; }
    QPushButton#SegBtn:checked { background-color: #1e293b; color: #f8fafc; border: 1px solid #475569; }
    QLabel#CourseBadge { background-color: #f8fafc; color: #0f172a; font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 6px; }
    QLabel#Tag { background-color: #0f172a; color: #94a3b8; border: 1px solid #334155; font-size: 11px; padding: 2px 8px; border-radius: 5px; }
    QLabel#TelemetryPill { background-color: rgba(16, 185, 129, 0.12); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.35); font-family: "Consolas", monospace; font-size: 11px; font-weight: 600; padding: 2px 9px; border-radius: 9px; }
    QLabel#HeroTitle { color: #f8fafc; font-size: 19px; font-weight: 700; }
    QLabel#CardTitle { color: #f8fafc; font-size: 13.5px; font-weight: 700; }
    QLabel#MetaLabel { color: #94a3b8; font-size: 10.5px; font-weight: 600; }
    QLabel#MetaValue { color: #f1f5f9; font-size: 12.5px; font-weight: 700; }
    QLabel#Muted { color: #94a3b8; font-size: 11.5px; }
    QLabel#StatusBar { color: #94a3b8; font-family: "Consolas", monospace; font-size: 11px; }
    QLineEdit#SearchBox { background-color: #0b1120; color: #f8fafc; border: 1px solid #334155; border-radius: 7px; padding: 5px 10px; font-size: 12px; }
    QLineEdit#SearchBox:focus { border-color: #38bdf8; }
    QPushButton { background-color: #223047; color: #e2e8f0; border: 1px solid #354764; border-radius: 7px; padding: 6px 12px; font-size: 12px; font-weight: 600; }
    QPushButton:hover { background-color: #2d3f5e; border-color: #64748b; }
    QPushButton#LaunchBtn {
        background-color: #0284c7; color: #ffffff; border: 1px solid #38bdf8;
        border-radius: 7px; padding: 6px 11px; font-size: 12px; font-weight: 700;
    }
    QPushButton#LaunchBtn:hover { background-color: #0369a1; border-color: #7dd3fc; }
    QPushButton#GhostBtn {
        background-color: transparent; color: #94a3b8; border: 1px solid #2b3b55;
        border-radius: 7px; padding: 6px 9px; font-size: 11.5px; font-weight: 600;
    }
    QPushButton#GhostBtn:hover { background-color: rgba(148, 163, 184, 0.12); color: #f8fafc; border-color: #475569; }
    QPushButton#ChipBtn { background-color: transparent; border: 1px solid transparent; color: #94a3b8; padding: 5px 11px; font-size: 12px; }
    QPushButton#ChipBtn:hover { background-color: #1e293b; color: #f8fafc; }
    QPushButton#ChipBtn:checked { background-color: #0284c7; color: #ffffff; border: 1px solid #38bdf8; }
    """


class LandingWindow(QMainWindow):
    """Fun, icon-rich landing hub for CSST 106 Computer Vision Labs 1–7."""

    CATEGORIES = ["All", "Image Processing", "Features & ML", "Deep Learning"]

    def __init__(self, base_dir: Path) -> None:
        super().__init__()
        self.base_dir = base_dir
        self.processes: list[tuple[str, subprocess.Popen]] = []
        self.card_widgets: list[tuple[dict, QFrame]] = []
        self.card_status: dict[str, QLabel] = {}
        self.launch_buttons: list[QPushButton] = []
        self.doc_buttons: list[tuple[QPushButton, QPushButton]] = []
        self.active_category = "All"
        self.theme = "dark"
        self.grid_cols = 3
        self._compact_hdr = False

        self.setWindowTitle("CSST 106 — Computer Vision Laboratory Suite")
        self.setWindowIcon(QIcon(draw_vector_icon("vision", "#38bdf8", 32, "#0f172a")))
        self.resize(1240, 800)
        self.setMinimumSize(460, 600)

        self._build_ui()
        self._apply_theme(animate=False)

        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self._refresh_running_count)
        self.poll_timer.start(1500)

    def _build_ui(self) -> None:
        self.root_widget = QWidget()
        self.root_widget.setObjectName("Root")
        self.setCentralWidget(self.root_widget)
        self.opacity_fx = QGraphicsOpacityEffect(self.root_widget)
        self.opacity_fx.setOpacity(1.0)
        self.root_widget.setGraphicsEffect(self.opacity_fx)

        outer = QVBoxLayout(self.root_widget)
        outer.setContentsMargins(14, 10, 14, 10)
        outer.setSpacing(8)

        # 1. Hero Header Card (responsive grid: side-by-side wide, stacked compact)
        hero = QFrame()
        hero.setObjectName("HeroCard")
        self.hero_grid = QGridLayout(hero)
        self.hero_grid.setContentsMargins(16, 11, 16, 11)
        self.hero_grid.setHorizontalSpacing(14)
        self.hero_grid.setVerticalSpacing(8)

        self.hero_left = QWidget()
        hl = QHBoxLayout(self.hero_left)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(12)

        logo_lbl = QLabel()
        logo_lbl.setPixmap(draw_vector_icon("vision", "#38bdf8", 48, "#0284c7"))
        hl.addWidget(logo_lbl)

        left_col = QVBoxLayout()
        left_col.setSpacing(3)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(8)
        course_badge = QLabel("CSST 106")
        course_badge.setObjectName("CourseBadge")
        course_badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.sem_tag = QLabel("Perception & Computer Vision • 1st Sem, AY 2026–2027")
        self.sem_tag.setObjectName("Tag")
        self.sem_tag.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        badge_row.addWidget(course_badge)
        badge_row.addWidget(self.sem_tag)
        badge_row.addStretch(1)
        left_col.addLayout(badge_row)

        hero_title = QLabel("Computer Vision Laboratory Suite")
        hero_title.setObjectName("HeroTitle")
        hero_title.setWordWrap(True)
        left_col.addWidget(hero_title)

        info_row = QHBoxLayout()
        info_row.setSpacing(20)
        for label_txt, val_txt in [("Student", "Ron Ken S. Borce"), ("Section", "BSCS 4B")]:
            pair = QVBoxLayout()
            pair.setSpacing(0)
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

        # Action Controls: Segmented Theme Switch + View Repository
        self.hero_right = QWidget()
        self.right_col = QHBoxLayout(self.hero_right)
        self.right_col.setContentsMargins(0, 0, 0, 0)
        self.right_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.right_col.setSpacing(8)

        theme_switch = QFrame()
        theme_switch.setObjectName("ThemeSwitch")
        sw_lay = QHBoxLayout(theme_switch)
        sw_lay.setContentsMargins(3, 3, 3, 3)
        sw_lay.setSpacing(2)
        self.theme_group = QButtonGroup(self)
        self.theme_group.setExclusive(True)
        self.seg_dark = QPushButton()
        self.seg_dark.setObjectName("SegBtn")
        self.seg_dark.setCheckable(True)
        self.seg_dark.setChecked(True)
        self.seg_dark.setToolTip("Dark Mode")
        self.seg_dark.clicked.connect(lambda: self._set_theme("dark"))
        self.seg_light = QPushButton()
        self.seg_light.setObjectName("SegBtn")
        self.seg_light.setCheckable(True)
        self.seg_light.setToolTip("Light Mode")
        self.seg_light.clicked.connect(lambda: self._set_theme("light"))
        self.theme_group.addButton(self.seg_dark)
        self.theme_group.addButton(self.seg_light)
        sw_lay.addWidget(self.seg_dark)
        sw_lay.addWidget(self.seg_light)

        self.repo_btn = QPushButton("View Repository")
        self.repo_btn.clicked.connect(self._on_view_repo)
        self.right_col.addWidget(theme_switch)
        self.right_col.addWidget(self.repo_btn)

        self.hero_grid.addWidget(self.hero_left, 0, 0)
        self.hero_grid.addWidget(self.hero_right, 0, 1)
        self.hero_grid.setColumnStretch(0, 1)
        outer.addWidget(hero)

        # 2. Filter & Search Bar (lab counts on chips + magnifying-glass search)
        filter_bar = QFrame()
        filter_bar.setObjectName("FilterBar")
        self.filter_grid = QGridLayout(filter_bar)
        self.filter_grid.setContentsMargins(10, 5, 10, 5)
        self.filter_grid.setHorizontalSpacing(8)
        self.filter_grid.setVerticalSpacing(6)

        self.chips_wrap = QWidget()
        chips_lay = QHBoxLayout(self.chips_wrap)
        chips_lay.setContentsMargins(0, 0, 0, 0)
        chips_lay.setSpacing(4)

        self.cat_group = QButtonGroup(self)
        self.cat_group.setExclusive(True)
        for cat in self.CATEGORIES:
            cnt = len(LABS) if cat == "All" else sum(1 for l in LABS if l["category"] == cat)
            b = QPushButton(f"{cat.replace('&', '&&')} ({cnt})")
            b.setObjectName("ChipBtn")
            b.setCheckable(True)
            if cat == "All":
                b.setChecked(True)
            b.clicked.connect(lambda _chk, c=cat: self._set_category(c))
            self.cat_group.addButton(b)
            chips_lay.addWidget(b)
        chips_lay.addStretch()

        self.search_box = QLineEdit()
        self.search_box.setObjectName("SearchBox")
        self.search_box.setPlaceholderText("Filter labs by name or topic...")
        self.search_box.setMinimumWidth(240)
        self.search_box.setMaximumWidth(290)
        self.search_action = self.search_box.addAction(
            QIcon(draw_vector_icon("search", "#94a3b8", 14)),
            QLineEdit.ActionPosition.LeadingPosition,
        )
        self.search_box.textChanged.connect(self._apply_filters)

        self.filter_grid.addWidget(self.chips_wrap, 0, 0)
        self.filter_grid.addWidget(self.search_box, 0, 1)
        self.filter_grid.setColumnStretch(0, 1)
        outer.addWidget(filter_bar)

        # 3. Scrollable Responsive Lab Cards Grid (3-col wide, 2-col medium, 1-col mobile)
        scroll = QScrollArea()
        scroll.setObjectName("CardsScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.grid_host = QWidget()
        self.grid_host.setObjectName("GridHost")
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(0, 0, 2, 0)
        self.grid.setSpacing(10)

        for lab in LABS:
            card = self._make_lab_card(lab)
            self.card_widgets.append((lab, card))
        self.util_card = self._make_utility_card()

        self._relayout_cards(LABS)
        scroll.setWidget(self.grid_host)
        outer.addWidget(scroll, 1)

        # 4. Bottom Status Bar (helper message left + live telemetry pill right)
        status_frame = QFrame()
        status_frame.setObjectName("StatusFrame")
        self.sf_grid = QGridLayout(status_frame)
        self.sf_grid.setContentsMargins(10, 5, 10, 5)
        self.sf_grid.setHorizontalSpacing(10)
        self.sf_grid.setVerticalSpacing(4)
        self.status_lbl = QLabel("Pick any lab card to launch its interactive UI or open its Report/Manual.")
        self.status_lbl.setObjectName("StatusBar")
        self.status_lbl.setWordWrap(True)
        self.live_badge = QLabel(f"● {len(LABS)} / {len(LABS)} Labs Ready • 0 Running")
        self.live_badge.setObjectName("TelemetryPill")
        self.live_badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.sf_grid.addWidget(self.status_lbl, 0, 0)
        self.sf_grid.addWidget(self.live_badge, 0, 1, Qt.AlignmentFlag.AlignRight)
        self.sf_grid.setColumnStretch(0, 1)
        outer.addWidget(status_frame)

    def _make_lab_card(self, lab: dict) -> QFrame:
        accent = lab["accent"]

        card = QFrame()
        card.setObjectName("LabCard")

        cl = QVBoxLayout(card)
        cl.setContentsMargins(13, 10, 13, 10)
        cl.setSpacing(6)

        # Header row: icon + Lab badge + Week + Category + Quick Status pill
        top = QHBoxLayout()
        top.setSpacing(9)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(draw_vector_icon(lab["icon"], accent, 34, accent))
        top.addWidget(icon_lbl)

        meta_col = QVBoxLayout()
        meta_col.setSpacing(2)
        badges = QHBoxLayout()
        badges.setSpacing(5)

        b_num = QLabel(lab["num"])
        b_num.setStyleSheet(
            f"background-color: {accent}; color: #0f172a; font-size: 10.5px; "
            f"font-weight: 700; padding: 2px 7px; border-radius: 5px;"
        )
        b_week = QLabel(lab["week"])
        b_week.setObjectName("Tag")
        b_cat = QLabel(lab["category"])
        b_cat.setObjectName("Tag")

        st_pill = QLabel("● Ready")
        st_pill.setStyleSheet(
            "background-color: rgba(34, 197, 94, 0.12); color: #4ade80; "
            "border: 1px solid rgba(74, 222, 128, 0.28); font-size: 10px; "
            "font-weight: 600; padding: 1px 7px; border-radius: 9px;"
        )
        self.card_status[lab["num"]] = st_pill

        badges.addWidget(b_num)
        badges.addWidget(b_week)
        badges.addWidget(b_cat)
        badges.addStretch()
        badges.addWidget(st_pill)
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

        # Action Buttons: unified primary Launch + ghost Report / Manual
        actions = QHBoxLayout()
        actions.setSpacing(6)

        launch_btn = QPushButton("Launch UI")
        launch_btn.setObjectName("LaunchBtn")
        launch_btn.setIcon(QIcon(draw_vector_icon("play", "#ffffff", 13)))
        launch_btn.clicked.connect(lambda _chk, item=lab: self._launch_lab(item))
        self.launch_buttons.append(launch_btn)

        report_btn = QPushButton("Report")
        report_btn.setObjectName("GhostBtn")
        report_btn.clicked.connect(lambda _chk, item=lab: self._open_doc(item, "report"))

        manual_btn = QPushButton("Manual")
        manual_btn.setObjectName("GhostBtn")
        manual_btn.clicked.connect(lambda _chk, item=lab: self._open_doc(item, "manual"))
        self.doc_buttons.append((report_btn, manual_btn))

        actions.addWidget(launch_btn, 2)
        actions.addWidget(report_btn, 1)
        actions.addWidget(manual_btn, 1)
        cl.addLayout(actions)
        return card

    def _make_utility_card(self) -> QFrame:
        """Create Environment & Dependencies Check card to balance row gaps."""
        card = QFrame()
        card.setObjectName("UtilCard")

        ul = QVBoxLayout(card)
        ul.setContentsMargins(13, 10, 13, 10)
        ul.setSpacing(7)

        top = QHBoxLayout()
        top.setSpacing(9)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(draw_vector_icon("env", "#38bdf8", 34, "#38bdf8"))
        top.addWidget(icon_lbl)

        meta_col = QVBoxLayout()
        meta_col.setSpacing(2)
        badges = QHBoxLayout()
        badges.setSpacing(5)
        b_sys = QLabel("Environment")
        b_sys.setStyleSheet(
            "background-color: #38bdf8; color: #0f172a; font-size: 10.5px; "
            "font-weight: 700; padding: 2px 7px; border-radius: 5px;"
        )
        b_note = QLabel("Local Runtime Check")
        b_note.setObjectName("Tag")
        badges.addWidget(b_sys)
        badges.addWidget(b_note)
        badges.addStretch()
        meta_col.addLayout(badges)

        title = QLabel("Environment & Dependencies Check")
        title.setObjectName("CardTitle")
        meta_col.addWidget(title)
        top.addLayout(meta_col, 1)
        ul.addLayout(top)

        self.env_pills_wrap = QWidget()
        self.pills_grid = QGridLayout(self.env_pills_wrap)
        self.pills_grid.setContentsMargins(0, 2, 0, 2)
        self.pills_grid.setHorizontalSpacing(6)
        self.pills_grid.setVerticalSpacing(5)
        self.env_pill_labels: list[tuple[QLabel, bool]] = []
        for idx, (pkg_name, ver) in enumerate(probe_env_packages()):
            ok = ver is not None
            txt = f"● {pkg_name} {ver}" if ok else f"○ {pkg_name} missing"
            lbl = QLabel(txt)
            self.env_pill_labels.append((lbl, ok))
            self.pills_grid.addWidget(lbl, idx // 4, idx % 4)
        ul.addWidget(self.env_pills_wrap, 1)

        note = QLabel("All 7 Borce_Lab_0X_Report.docx & Manuals linked cleanly • OpenCV + Torch/YOLO ready.")
        note.setObjectName("Muted")
        note.setWordWrap(True)
        ul.addWidget(note)
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
        cols = self.grid_cols
        for c in range(3):
            self.grid.setColumnStretch(c, 1 if c < cols else 0)
        idx = 0
        for lab, card in self.card_widgets:
            if lab["num"] in visible_nums:
                card.show()
                self.grid.addWidget(card, idx // cols, idx % cols)
                idx += 1

        show_util = self.active_category == "All" and not self.search_box.text().strip()
        if show_util:
            self.util_card.show()
            span = (cols - (idx % cols)) if (idx % cols) != 0 else cols
            self.grid.addWidget(self.util_card, idx // cols, idx % cols, 1, span)
            env_cols = 4 if span >= 2 else 2
            while self.pills_grid.count():
                self.pills_grid.takeAt(0)
            for p_idx, (lbl, _ok) in enumerate(self.env_pill_labels):
                self.pills_grid.addWidget(lbl, p_idx // env_cols, p_idx % env_cols)
        else:
            self.util_card.hide()

    def _relayout_chrome(self, compact: bool) -> None:
        """Stack hero actions, search bar, and telemetry when window is compact."""
        self.hero_grid.removeWidget(self.hero_left)
        self.hero_grid.removeWidget(self.hero_right)
        self.filter_grid.removeWidget(self.chips_wrap)
        self.filter_grid.removeWidget(self.search_box)
        self.sf_grid.removeWidget(self.status_lbl)
        self.sf_grid.removeWidget(self.live_badge)

        if compact:
            self.hero_grid.addWidget(self.hero_left, 0, 0)
            self.hero_grid.addWidget(self.hero_right, 1, 0)
            self.hero_grid.setColumnStretch(1, 0)
            self.right_col.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.sem_tag.setWordWrap(True)
            self.filter_grid.addWidget(self.chips_wrap, 0, 0)
            self.filter_grid.addWidget(self.search_box, 1, 0)
            self.filter_grid.setColumnStretch(1, 0)
            self.search_box.setMinimumWidth(0)
            self.search_box.setMaximumWidth(16777215)
            self.sf_grid.addWidget(self.status_lbl, 0, 0)
            self.sf_grid.addWidget(self.live_badge, 1, 0, Qt.AlignmentFlag.AlignLeft)
        else:
            self.hero_grid.addWidget(self.hero_left, 0, 0)
            self.hero_grid.addWidget(self.hero_right, 0, 1)
            self.hero_grid.setColumnStretch(1, 0)
            self.right_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.sem_tag.setWordWrap(False)
            self.filter_grid.addWidget(self.chips_wrap, 0, 0)
            self.filter_grid.addWidget(self.search_box, 0, 1)
            self.filter_grid.setColumnStretch(1, 0)
            self.search_box.setMinimumWidth(240)
            self.search_box.setMaximumWidth(290)
            self.sf_grid.addWidget(self.status_lbl, 0, 0)
            self.sf_grid.addWidget(self.live_badge, 0, 1, Qt.AlignmentFlag.AlignRight)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        compact_hdr = self.width() < 780
        if compact_hdr != self._compact_hdr:
            self._compact_hdr = compact_hdr
            self._relayout_chrome(compact_hdr)
        new_cols = 1 if self.width() < 720 else (2 if self.width() < 1100 else 3)
        if new_cols != self.grid_cols:
            self.grid_cols = new_cols
            self._apply_filters()

    def _set_theme(self, theme: str) -> None:
        if theme == self.theme:
            return
        self.theme = theme
        self._apply_theme(animate=True)

    def _apply_theme(self, animate: bool = True) -> None:
        self.setStyleSheet(build_stylesheet(self.theme))
        is_dark = self.theme == "dark"
        self.seg_dark.setChecked(is_dark)
        self.seg_light.setChecked(not is_dark)

        card_bg = "#162033" if is_dark else "#ffffff"
        card_bd = "#29354d" if is_dark else "#cbd5e1"
        card_hv = "#1a263c" if is_dark else "#f8fafc"
        icon_fg = "#94a3b8" if is_dark else "#475569"
        hero_fg = "#e2e8f0" if is_dark else "#1e293b"

        for lab, card in self.card_widgets:
            accent = lab["accent"]
            card.setStyleSheet(
                f"QFrame#LabCard {{ background-color: {card_bg}; border: 1px solid {card_bd}; "
                f"border-left: 4px solid {accent}; border-radius: 11px; }}"
                f"QFrame#LabCard:hover {{ border-color: {accent}; background-color: {card_hv}; }}"
            )
        self.util_card.setStyleSheet(
            f"QFrame#UtilCard {{ background-color: {card_bg}; border: 1px solid {card_bd}; "
            f"border-left: 4px solid #38bdf8; border-radius: 11px; }}"
        )
        for lbl, ok in self.env_pill_labels:
            if ok:
                lbl.setStyleSheet(
                    "background-color: rgba(16, 185, 129, 0.12); color: #10b981; "
                    "border: 1px solid rgba(16, 185, 129, 0.28); font-size: 11px; "
                    "font-family: 'Consolas', monospace; padding: 3px 7px; border-radius: 6px;"
                    if not is_dark else
                    "background-color: rgba(16, 185, 129, 0.10); color: #6ee7b7; "
                    "border: 1px solid rgba(52, 211, 153, 0.28); font-size: 11px; "
                    "font-family: 'Consolas', monospace; padding: 3px 7px; border-radius: 6px;"
                )
            else:
                lbl.setStyleSheet(
                    "background-color: rgba(245, 158, 11, 0.12); color: #b45309; "
                    "border: 1px solid rgba(245, 158, 11, 0.3); font-size: 11px; "
                    "font-family: 'Consolas', monospace; padding: 3px 7px; border-radius: 6px;"
                )

        for rep_b, man_b in self.doc_buttons:
            rep_b.setIcon(QIcon(draw_vector_icon("doc", icon_fg, 13)))
            man_b.setIcon(QIcon(draw_vector_icon("book", icon_fg, 13)))

        self.search_action.setIcon(QIcon(draw_vector_icon("search", icon_fg, 14)))
        self.repo_btn.setIcon(QIcon(draw_vector_icon("git", hero_fg, 15)))
        self.seg_dark.setIcon(QIcon(draw_vector_icon("moon", "#f8fafc" if is_dark else "#475569", 15)))
        self.seg_light.setIcon(QIcon(draw_vector_icon("sun", "#fbbf24" if not is_dark else "#94a3b8", 15)))
        self._refresh_running_count()

        if animate:
            anim = QPropertyAnimation(self.opacity_fx, b"opacity", self)
            anim.setDuration(260)
            anim.setStartValue(0.65)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim.start()
            self._theme_anim = anim

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
        running_nums = {n for n, _ in self.processes}
        self.live_badge.setText(f"● {len(LABS)} / {len(LABS)} Labs Ready • {len(self.processes)} Running")
        is_dark = self.theme == "dark"
        for lab_num, st_lbl in self.card_status.items():
            if lab_num in running_nums:
                st_lbl.setText("● Running")
                st_lbl.setStyleSheet(
                    "background-color: rgba(14, 165, 233, 0.16); color: #38bdf8; "
                    "border: 1px solid rgba(56, 189, 248, 0.45); font-size: 10px; "
                    "font-weight: 700; padding: 1px 7px; border-radius: 9px;"
                )
            else:
                st_lbl.setText("● Ready")
                fg = "#4ade80" if is_dark else "#15803d"
                bg = "rgba(34, 197, 94, 0.12)" if is_dark else "#dcfce7"
                bd = "rgba(74, 222, 128, 0.28)" if is_dark else "#86efac"
                st_lbl.setStyleSheet(
                    f"background-color: {bg}; color: {fg}; border: 1px solid {bd}; "
                    "font-size: 10px; font-weight: 600; padding: 1px 7px; border-radius: 9px;"
                )

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
