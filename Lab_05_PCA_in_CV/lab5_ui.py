"""
CSST106 - Perception and Computer Vision
Laboratory Exercise No. 5: Facial Recognition using PCA (Eigenfaces) & SVM (PyQt6)

Implements all Lab 5 tasks interactively:
  - Task 1: Load LFW dataset (min_faces_per_person=70, resize=0.4) & 80/20 train/test split
  - Task 2: Fit PCA (svd_solver='randomized', tunable n_components & whiten)
  - Task 3: Visualize top Eigenfaces (and compare first 3 vs last 3 Eigenfaces)
  - Task 4: Train RBF SVM (class_weight='balanced') on PCA projections & evaluate
  - Post-Lab: Cumulative Explained Variance plot (90% marker), PCA face reconstruction,
              programmatic failure analysis gallery, and complete Q&A section
"""

from pathlib import Path
import sys
import time
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtCore import Qt, QRect, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QImage, QPainter, QPixmap
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
from sklearn.datasets import fetch_lfw_people
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def fig_to_bgr(fig: plt.Figure) -> np.ndarray:
    """Render a Matplotlib figure to an OpenCV BGR uint8 image."""
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    bgr = cv2.cvtColor(buf, cv2.COLOR_RGBA2BGR)
    plt.close(fig)
    return bgr


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


def run_pca_pipeline(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    target_names: np.ndarray,
    h: int,
    w: int,
    n_components: int = 150,
    whiten: bool = True,
) -> dict:
    """Fit randomized PCA and RBF SVM, then compute variance, predictions, and failures."""
    t_pca0 = time.perf_counter()
    pca = PCA(
        n_components=n_components,
        svd_solver="randomized",
        whiten=whiten,
        random_state=42,
    ).fit(X_train)
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)
    pca_time = time.perf_counter() - t_pca0

    t_svm0 = time.perf_counter()
    clf = SVC(kernel="rbf", class_weight="balanced", random_state=42)
    clf.fit(X_train_pca, y_train)
    y_pred = clf.predict(X_test_pca)
    svm_time = time.perf_counter() - t_svm0

    cum_var = np.cumsum(pca.explained_variance_ratio_)
    k90 = int(np.searchsorted(cum_var, 0.90) + 1) if cum_var[-1] >= 0.90 else -1
    acc = float(accuracy_score(y_test, y_pred))
    report = classification_report(y_test, y_pred, target_names=target_names, zero_division=0)
    eigenfaces = pca.components_.reshape((n_components, h, w))
    mis_indices = np.where(y_pred != y_test)[0]

    return {
        "pca": pca,
        "clf": clf,
        "X_train_pca": X_train_pca,
        "X_test_pca": X_test_pca,
        "y_pred": y_pred,
        "cum_var": cum_var,
        "k90": k90,
        "total_var": float(cum_var[-1]),
        "accuracy": acc,
        "report": report,
        "eigenfaces": eigenfaces,
        "mis_indices": mis_indices,
        "pca_time": pca_time,
        "svm_time": svm_time,
        "h": h,
        "w": w,
    }


def render_eigenfaces_figure(eigenfaces: np.ndarray, n_components: int) -> np.ndarray:
    """Plot top 9 Eigenfaces alongside the last 3 Eigenfaces for visual comparison."""
    fig, axes = plt.subplots(3, 4, figsize=(10.5, 7.6), facecolor="#0b1120")
    indices = list(range(min(9, n_components))) + list(range(max(0, n_components - 3), n_components))
    for ax, idx in zip(axes.ravel(), indices):
        ax.imshow(eigenfaces[idx], cmap="gray")
        tag = "Top" if idx < 9 else "Tail"
        ax.set_title(f"{tag}: Eigenface {idx}", color="#e2e8f0", fontsize=10, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])
    for ax in axes.ravel()[len(indices):]:
        ax.axis("off")
    fig.suptitle(
        f"Top 9 Eigenfaces vs. Last 3 Eigenfaces (out of {n_components})",
        color="#38bdf8",
        fontsize=12.5,
        fontweight="bold",
    )
    plt.tight_layout()
    return fig_to_bgr(fig)


def render_variance_figure(cum_var: np.ndarray, k90: int) -> np.ndarray:
    """Plot cumulative explained variance vs. number of principal components."""
    fig, ax = plt.subplots(figsize=(9.5, 5.6), facecolor="#0b1120")
    ax.set_facecolor("#0f172a")
    xs = np.arange(1, len(cum_var) + 1)
    ax.plot(xs, cum_var * 100.0, color="#38bdf8", linewidth=2.3, label="Cumulative Explained Variance")
    ax.axhline(90.0, color="#fbbf24", linestyle="--", linewidth=1.4, label="90% Variance Threshold")
    if k90 > 0:
        ax.axvline(k90, color="#34d399", linestyle="--", linewidth=1.4, label=f"90% reached at k = {k90}")
        ax.scatter([k90], [cum_var[k90 - 1] * 100.0], color="#34d399", s=65, zorder=5)
    ax.set_title("Cumulative Explained Variance vs. Number of Principal Components", color="#f8fafc", fontsize=12, fontweight="bold")
    ax.set_xlabel("Number of Principal Components", color="#cbd5e1")
    ax.set_ylabel("Cumulative Variance Retained (%)", color="#cbd5e1")
    ax.set_ylim(0, 102)
    ax.set_xlim(1, len(cum_var))
    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_color("#334155")
    ax.grid(color="#1e293b", linestyle="-", linewidth=0.8)
    ax.legend(facecolor="#1e293b", edgecolor="#334155", labelcolor="#f1f5f9")
    plt.tight_layout()
    return fig_to_bgr(fig)


def render_predictions_figure(
    X_test: np.ndarray,
    y_test: np.ndarray,
    y_pred: np.ndarray,
    target_names: np.ndarray,
    h: int,
    w: int,
    failures_only: bool = True,
) -> np.ndarray:
    """Render a 3x4 gallery of misclassified (or test) faces with True vs. Predicted names."""
    if failures_only:
        pool = np.where(y_pred != y_test)[0]
        header = f"Programmatic Failure Analysis ({len(pool)} misclassified out of {len(y_test)})"
    else:
        pool = np.arange(len(y_test))
        header = f"Sample Test Set Predictions (Accuracy: {(y_pred == y_test).mean() * 100:.1f}%)"

    fig, axes = plt.subplots(3, 4, figsize=(11, 7.8), facecolor="#0b1120")
    chosen = pool[:12]
    for ax, idx in zip(axes.ravel(), chosen):
        ax.imshow(X_test[idx].reshape((h, w)), cmap="gray")
        true_n = target_names[y_test[idx]].split()[-1]
        pred_n = target_names[y_pred[idx]].split()[-1]
        ok = y_test[idx] == y_pred[idx]
        col = "#34d399" if ok else "#f87171"
        ax.set_title(f"True: {true_n}\nPred: {pred_n}", color=col, fontsize=9.5, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])
    for ax in axes.ravel()[len(chosen):]:
        ax.axis("off")
    fig.suptitle(header, color="#38bdf8", fontsize=12.5, fontweight="bold")
    plt.tight_layout()
    return fig_to_bgr(fig)


def render_reconstruction_figure(
    X_test: np.ndarray,
    y_test: np.ndarray,
    target_names: np.ndarray,
    pca: PCA,
    X_test_pca: np.ndarray,
    sample_idx: int,
    h: int,
    w: int,
) -> np.ndarray:
    """Compare original test face with reconstructions using 10, 50, and all K components."""
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.6), facecolor="#0b1120")
    orig = X_test[sample_idx].reshape((h, w))
    axes[0].imshow(orig, cmap="gray")
    axes[0].set_title(f"Original (1850-D)\n{target_names[y_test[sample_idx]]}", color="#f8fafc", fontsize=9.5, fontweight="bold")
    axes[0].axis("off")

    max_k = X_test_pca.shape[1]
    ks = [min(10, max_k), min(50, max_k), max_k]
    for ax, k in zip(axes[1:], ks):
        proj_k = np.zeros_like(X_test_pca[sample_idx : sample_idx + 1])
        proj_k[0, :k] = X_test_pca[sample_idx, :k]
        recon = pca.inverse_transform(proj_k).reshape((h, w))
        ax.imshow(recon, cmap="gray")
        ax.set_title(f"Reconstructed\n(k = {k} components)", color="#38bdf8", fontsize=9.5, fontweight="bold")
        ax.axis("off")

    plt.tight_layout()
    return fig_to_bgr(fig)


class DatasetWorker(QThread):
    """Background loader so GUI opens immediately while LFW loads."""

    finished = pyqtSignal(object)
    failed = pyqtSignal(str)

    def run(self) -> None:
        try:
            lfw = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
            n_samples, h, w = lfw.images.shape
            X_train, X_test, y_train, y_test = train_test_split(
                lfw.data, lfw.target, test_size=0.2, random_state=42
            )
            self.finished.emit(
                {
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
            )
        except Exception as exc:
            self.failed.emit(str(exc))


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
    font-size: 11px;
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
QCheckBox {
    color: #e2e8f0;
    font-size: 12px;
}
"""


class Lab5Window(QMainWindow):
    """Tabbed interactive UI for CSST106 Lab 5 PCA Eigenfaces & SVM."""

    TABS = [
        ("eigenfaces", "Eigenfaces"),
        ("variance", "Variance Curve"),
        ("failures", "Predictions && Failures"),
        ("reconstruct", "Reconstruction"),
        ("qa", "Analysis && Q&&A"),
    ]

    def __init__(self, lab_dir: Path) -> None:
        super().__init__()
        self.lab_dir = lab_dir
        self.data: dict | None = None
        self.res: dict | None = None
        self.current_tab = "eigenfaces"
        self.current_plot_bgr: np.ndarray | None = None

        self.setWindowTitle("CSST106 Lab 5 — PCA Eigenfaces Facial Recognition")
        self.resize(1300, 770)
        self.setMinimumSize(1020, 640)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()
        self._start_loading()

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
        lbl_title = QLabel("CSST106 Lab 5: Facial Recognition using PCA (Eigenfaces) & SVM")
        lbl_title.setObjectName("Title")
        lbl_sub = QLabel("LFW dataset dimensionality reduction, cumulative explained variance, whitening, and failure analysis.")
        lbl_sub.setObjectName("Muted")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        top_bar.addLayout(title_box, 1)

        btn_reset = QPushButton("Reset Defaults")
        btn_reset.clicked.connect(self._on_reset)
        btn_save = QPushButton("Save Plot...")
        btn_save.setObjectName("AccentBtn")
        btn_save.clicked.connect(self._on_save)
        top_bar.addWidget(btn_reset)
        top_bar.addWidget(btn_save)
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
        self.tab_buttons["eigenfaces"].setChecked(True)
        layout.addWidget(tab_panel)

        # Body: Main Plot/QA Card + Right Inspector Drawer
        body = QHBoxLayout()
        body.setSpacing(10)
        layout.addLayout(body, 1)

        self.plot_card = QFrame()
        self.plot_card.setObjectName("Panel")
        pl = QVBoxLayout(self.plot_card)
        pl.setContentsMargins(10, 8, 10, 10)
        pl.setSpacing(6)
        ph = QHBoxLayout()
        self.plot_title = QLabel("LOADING LFW DATASET...")
        self.plot_title.setObjectName("Section")
        self.plot_badge = QLabel("-")
        self.plot_badge.setObjectName("Muted")
        ph.addWidget(self.plot_title)
        ph.addStretch()
        ph.addWidget(self.plot_badge)
        pl.addLayout(ph)
        self.canvas = ImageCanvas()
        pl.addWidget(self.canvas, 1)
        body.addWidget(self.plot_card, 1)

        # Q&A Scroll Card
        self.qa_card = QFrame()
        self.qa_card.setObjectName("Panel")
        qal = QVBoxLayout(self.qa_card)
        qal.setContentsMargins(16, 14, 16, 14)
        qal.setSpacing(8)
        qa_hdr = QLabel("LAB 5 — POST-LAB ANALYSIS & FOLLOW-UP QUESTIONS")
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

        # Right Controls & Report Drawer
        inspector = QFrame()
        inspector.setObjectName("Panel")
        inspector.setFixedWidth(365)
        il = QVBoxLayout(inspector)
        il.setContentsMargins(12, 10, 12, 12)
        il.setSpacing(8)

        hdr_p = QLabel("PCA & SVM PARAMETERS")
        hdr_p.setObjectName("Section")
        il.addWidget(hdr_p)

        self.comp_sl, self.comp_lbl = self._make_slider("PCA n_components:", 20, 220, 150)
        self.comp_sl["slider"].sliderReleased.connect(self._recompute_model)
        il.addWidget(self.comp_sl["wrap"])

        self.whiten_chk = QCheckBox("whiten=True (unit variance components)")
        self.whiten_chk.setChecked(True)
        self.whiten_chk.toggled.connect(self._recompute_model)
        il.addWidget(self.whiten_chk)

        self.fail_only_chk = QCheckBox("Show misclassified faces only (Failures tab)")
        self.fail_only_chk.setChecked(True)
        self.fail_only_chk.toggled.connect(self._render_active_tab)
        il.addWidget(self.fail_only_chk)

        self.sample_sl, self.sample_lbl = self._make_slider("Reconstruction Sample #:", 0, 257, 0)
        self.sample_sl["slider"].valueChanged.connect(self._render_active_tab)
        il.addWidget(self.sample_sl["wrap"])

        apply_btn = QPushButton("Re-run PCA + SVM")
        apply_btn.setObjectName("AccentBtn")
        apply_btn.clicked.connect(self._recompute_model)
        il.addWidget(apply_btn)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #334155;")
        il.addWidget(sep)

        metrics_scroll = QScrollArea()
        metrics_scroll.setWidgetResizable(True)
        metrics_scroll.setFrameShape(QFrame.Shape.NoFrame)
        metrics_scroll.setStyleSheet("background: transparent;")

        self.metrics_lbl = QLabel("Loading LFW dataset...")
        self.metrics_lbl.setObjectName("Mono")
        self.metrics_lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.metrics_lbl.setStyleSheet("font-size: 10px; background: transparent;")
        self.metrics_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        metrics_scroll.setWidget(self.metrics_lbl)
        il.addWidget(metrics_scroll, 1)

        body.addWidget(inspector)

        self.status_lbl = QLabel("Loading LFW dataset in background...")
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
        sl.valueChanged.connect(lambda v: val_lbl.setText(str(v)))
        vl.addWidget(sl)
        return {"wrap": wrap, "slider": sl}, val_lbl

    def _start_loading(self) -> None:
        self.worker = DatasetWorker()
        self.worker.finished.connect(self._on_data_loaded)
        self.worker.failed.connect(lambda err: self.status_lbl.setText(f"Dataset error: {err}"))
        self.worker.start()

    def _on_data_loaded(self, data: dict) -> None:
        self.data = data
        self.sample_sl["slider"].setMaximum(len(data["y_test"]) - 1)
        self._recompute_model()

    def _on_reset(self) -> None:
        self.comp_sl["slider"].setValue(150)
        self.whiten_chk.setChecked(True)
        self.fail_only_chk.setChecked(True)
        self.sample_sl["slider"].setValue(0)
        self._recompute_model()

    def _select_tab(self, key: str) -> None:
        self.current_tab = key
        self._render_active_tab()

    def _recompute_model(self) -> None:
        if self.data is None:
            return
        n_comp = self.comp_sl["slider"].value()
        whiten = self.whiten_chk.isChecked()
        self.res = run_pca_pipeline(
            self.data["X_train"],
            self.data["X_test"],
            self.data["y_train"],
            self.data["y_test"],
            self.data["target_names"],
            self.data["h"],
            self.data["w"],
            n_components=n_comp,
            whiten=whiten,
        )
        self._update_metrics()
        self._render_active_tab()

    def _update_metrics(self) -> None:
        if self.data is None or self.res is None:
            return
        d, r = self.data, self.res
        k90_str = f"{r['k90']}" if r["k90"] > 0 else f">{self.comp_sl['slider'].value()}"
        self.metrics_lbl.setText(
            f"LFW (min_faces=70, resize=0.4)\n"
            f"Samples  : {d['n_samples']} ({len(d['y_train'])} train / {len(d['y_test'])} test)\n"
            f"Image    : {d['h']}×{d['w']} ({d['n_features']} features)\n"
            f"Classes  : {len(d['target_names'])}\n\n"
            f"PCA (k={self.comp_sl['slider'].value()}, whiten={self.whiten_chk.isChecked()}):\n"
            f"  Retained Var : {r['total_var']*100:.2f}%\n"
            f"  90% Var at k : {k90_str}\n"
            f"  PCA + SVM    : {r['pca_time'] + r['svm_time']:.2f}s\n\n"
            f"SVM Accuracy   : {r['accuracy']*100:.2f}% ({len(r['mis_indices'])} errors)\n\n"
            f"{r['report']}"
        )
        self.status_lbl.setText(
            f"LFW {d['n_samples']} faces ({d['h']}×{d['w']}) | k={self.comp_sl['slider'].value()} "
            f"({r['total_var']*100:.2f}% var, 90% at k={k90_str}) | whiten={self.whiten_chk.isChecked()} | "
            f"SVM Accuracy={r['accuracy']*100:.2f}%"
        )

    def _render_active_tab(self) -> None:
        if self.data is None or self.res is None:
            return
        d, r = self.data, self.res
        n_comp = self.comp_sl["slider"].value()

        if self.current_tab == "qa":
            self.plot_card.hide()
            self.qa_card.show()
            k90_str = f"{r['k90']}" if r["k90"] > 0 else f">{n_comp}"
            self.qa_text_lbl.setText(
                f"""
                <h3 style="color:#38bdf8; margin-top:0;">Post-Lab Analysis (Tasks 1–4):</h3>
                <p><b>Q1. Dimensionality vs. Variance:</b><br>
                With <code>n_components={n_comp}</code> on the LFW dataset (<code>{d['n_features']}</code> raw pixel features, <code>{d['h']}×{d['w']}</code>), PCA retains <code>{r['total_var']*100:.2f}%</code> of total variance. To retain <b>90%</b> of the variance, <b><code>{k90_str}</code> principal components</b> are required (cutting dimensionality by ~95%).</p>

                <p><b>Q2. Visual Interpretation (First 3 vs. Last 3 Eigenfaces):</b><br>
                The <b>first 3 Eigenfaces</b> capture low-frequency global structure shared across the dataset—overall illumination direction (left/right lighting), head oval/jawline contour, and average eye/nose/mouth placement. The <b>last 3 Eigenfaces</b> (components {n_comp-3}–{n_comp-1}) capture high-frequency fine details, localized edge textures, expressions, and residual noise.</p>

                <p><b>Q3. The Importance of Whitening (<code>whiten=True</code>):</b><br>
                Mathematically, whitening divides each projected principal component by the square root of its eigenvalue (&radic;&lambda;<sub>i</sub>), giving all components <b>zero mean and unit variance</b>. Without whitening, the first few high-variance lighting components dominate Euclidean/RBF kernel distances in SVM; whitening puts all 150 facial features on equal footing so the RBF SVM achieves stronger class separation.</p>

                <p><b>Q4. Failure Analysis ({len(r['mis_indices'])} errors / {len(d['y_test'])} test faces):</b><br>
                Inspecting misclassified faces in the <b>Predictions &amp; Failures</b> tab shows that errors occur primarily under extreme <b>off-axis head poses/profiles</b>, <b>harsh uneven shadows/lighting</b>, <b>glasses or occlusions</b>, and class imbalance (smaller classes like Hugo Chavez/Ariel Sharon get confused with the majority George W Bush / Colin Powell classes) because global pixel-aligned Eigenfaces are sensitive to spatial misalignment and illumination shifts.</p>

                <h3 style="color:#38bdf8; margin-top:14px;">Follow-Up Questions:</h3>
                <p><b>1. Why is dimensionality reduction important in computer vision?</b><br>
                Raw images have thousands to millions of correlated pixels ("curse of dimensionality"). Dimensionality reduction removes redundancy, lowers memory/compute cost, prevents overfitting, and speeds up classifier training.</p>

                <p><b>2. Difference between the first and second principal components?</b><br>
                The <b>1st principal component</b> points in the direction of maximum variance across the data; the <b>2nd principal component</b> is strictly <b>orthogonal</b> to the 1st and captures the largest remaining variance.</p>

                <p><b>3. If PCA reduces 1,000 features to 100 components, what information might be lost?</b><br>
                The discarded 900 low-variance components hold fine high-frequency textures, sharp edges, subtle individual quirks, and sensor noise.</p>

                <p><b>4. How can PCA be applied to face recognition?</b><br>
                Training faces are centered and projected onto the top <i>k</i> eigenvectors (Eigenfaces) of the covariance matrix; a new face is projected into the same <i>k</i>-dimensional subspace and classified via SVM or nearest-neighbor distance.</p>

                <p><b>5. Why should image features generally be centered before applying PCA?</b><br>
                PCA computes variance around the origin; subtracting the mean face ensures principal components capture true variation <i>among</i> faces rather than the average brightness/mean face vector itself.</p>
                """
            )
            return

        self.qa_card.hide()
        self.plot_card.show()

        if self.current_tab == "eigenfaces":
            self.plot_title.setText("EIGENFACES GALLERY (TOP 9 VS. LAST 3)")
            self.plot_badge.setText(f"n_components={n_comp}")
            img = render_eigenfaces_figure(r["eigenfaces"], n_comp)
        elif self.current_tab == "variance":
            self.plot_title.setText("CUMULATIVE EXPLAINED VARIANCE")
            self.plot_badge.setText(f"90% @ k={r['k90']} • Total={r['total_var']*100:.2f}%")
            img = render_variance_figure(r["cum_var"], r["k90"])
        elif self.current_tab == "failures":
            self.plot_title.setText("SVM PREDICTIONS & PROGRAMMATIC FAILURE ANALYSIS")
            self.plot_badge.setText(f"Acc={r['accuracy']*100:.2f}% • Errors={len(r['mis_indices'])}")
            img = render_predictions_figure(
                d["X_test"],
                d["y_test"],
                r["y_pred"],
                d["target_names"],
                d["h"],
                d["w"],
                failures_only=self.fail_only_chk.isChecked(),
            )
        else:  # reconstruct
            idx = self.sample_sl["slider"].value()
            self.plot_title.setText("PCA EIGENFACE RECONSTRUCTION")
            self.plot_badge.setText(f"Test sample #{idx}")
            img = render_reconstruction_figure(
                d["X_test"],
                d["y_test"],
                d["target_names"],
                r["pca"],
                r["X_test_pca"],
                idx,
                d["h"],
                d["w"],
            )

        self.current_plot_bgr = img
        self.canvas.set_image(img)

    def _on_save(self) -> None:
        if self.current_plot_bgr is None:
            return
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Plot Figure",
            str(self.lab_dir / f"lab5_{self.current_tab}.png"),
            "PNG (*.png);;JPEG (*.jpg)",
        )
        if save_path:
            cv2.imwrite(save_path, self.current_plot_bgr)


def main() -> None:
    app = QApplication(sys.argv)
    win = Lab5Window(Path(__file__).resolve().parent)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
