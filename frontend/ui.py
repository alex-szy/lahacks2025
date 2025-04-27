"""Sleeker minimal‑theme PySide6 UI for Semantic File Explorer.
Icons are flat (no bubbles), rows have no surrounding rectangles, and all text sits directly on the canvas.
Run with `python file_browser_ui.py` (after `pip install PySide6`).
Place any custom SVG icons in an `icons/` folder next to this file and update the `ICON_MAP` dict below.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QStyle,
)

# -----------------------------------------------------------------------------
# Simple icon helper (optional SVG replacements for a unified look)
# -----------------------------------------------------------------------------
HERE = Path(__file__).parent
ICON_MAP = {
    "watch": HERE / "icons/refresh.svg",
    "folder": HERE / "icons/folder.svg",
    "keys": HERE / "icons/key.svg",
    "settings": HERE / "icons/settings.svg",
    "login": HERE / "icons/user.svg",
    "search": HERE / "icons/search.svg",
    "file": HERE / "icons/file.svg",
}


def icon(name: str, size: int = 20) -> QIcon:
    path = ICON_MAP.get(name)
    if path and path.exists():
        return QIcon(str(path))
    # graceful fallback to built‑in if custom SVG missing
    return QApplication.style().standardIcon(getattr(QStyle, "SP_FileIcon", 0))


# -----------------------------------------------------------------------------
# Helper widgets
# -----------------------------------------------------------------------------


class NavButton(QToolButton):
    """Flat sidebar button with only an icon."""

    def __init__(self, icon: QIcon, tooltip: str):
        super().__init__()
        self.setIcon(icon)
        self.setIconSize(QSize(22, 22))
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setStyleSheet(
            """
            QToolButton { border:none; background:transparent; padding:6px; }
            QToolButton:hover { background:#f2f2f2; border-radius:6px; }
            QToolButton:checked { background:#ebf0ff; border-radius:6px; }
            """
        )


class FileCard(QWidget):
    """Single result row without outer rectangles."""

    def __init__(self, path: Path):
        super().__init__()
        self.path = path
        # transparent background lets list widget style show through
        self.setStyleSheet("background:transparent;")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(4, 6, 4, 6)
        lay.setSpacing(14)

        icon_lbl = QLabel()
        file_icn = icon("file", 28).pixmap(28, 28)
        icon_lbl.setPixmap(file_icn)
        lay.addWidget(icon_lbl)

        text_col = QVBoxLayout()
        name_lbl = QLabel(path.name)
        name_lbl.setStyleSheet("font-weight:600; font-size:14px;")
        sum_lbl = QLabel("Summary of file …")  # TODO real summary
        sum_lbl.setStyleSheet("color:#666; font-size:12px;")
        sum_lbl.setWordWrap(True)
        text_col.addWidget(name_lbl)
        text_col.addWidget(sum_lbl)
        lay.addLayout(text_col, 1)

        meta_lbl = QLabel(f"{path.stat().st_size/1024:.1f} KB · {path.stat().st_mtime:.0f}")
        meta_lbl.setStyleSheet("color:#777; font-size:11px;")
        lay.addWidget(meta_lbl)


# -----------------------------------------------------------------------------
# Main window
# -----------------------------------------------------------------------------


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semantic File Explorer")
        self.resize(1050, 660)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)

        # Sidebar -----------------------------------------------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(72)
        sidebar.setStyleSheet("background:#fafafa; border-right:1px solid #e7e7e7;")
        side_lay = QVBoxLayout(sidebar)
        side_lay.setAlignment(Qt.AlignTop)
        side_lay.setContentsMargins(12, 16, 12, 16)
        side_lay.setSpacing(10)

        btn_info = [
            (icon("watch"), "Watch Folders"),
            (icon("folder"), "Folders"),
            (icon("keys"), "API Keys"),
            (icon("settings"), "Settings"),
            (icon("login"), "Login"),
        ]
        self.nav_btns = []
        for icn, tip in btn_info:
            b = NavButton(icn, tip)
            side_lay.addWidget(b)
            self.nav_btns.append(b)
        side_lay.addStretch(1)

        # Content -----------------------------------------------------------
        content = QWidget()
        c_lay = QVBoxLayout(content)
        c_lay.setContentsMargins(32, 24, 32, 24)
        c_lay.setSpacing(24)

        # Search bar -------------------------------------------------------
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search …")
        self.search_edit.setFixedHeight(46)
        self.search_edit.setStyleSheet(
            """
            QLineEdit { border:1px solid #d4d4d4; border-radius:23px; padding-left:48px; }
            QLineEdit:focus { border-color:#7a74ff; }
            """
        )
        magnifier = QLabel(self.search_edit)
        magnifier.setPixmap(icon("search", 20).pixmap(20, 20))
        magnifier.move(16, 13)
        self.search_edit.textChanged.connect(self.on_search)
        c_lay.addWidget(self.search_edit)

        # Results list ------------------------------------------------------
        self.results_list = QListWidget()
        self.results_list.setFrameShape(QFrame.NoFrame)
        self.results_list.setSpacing(4)
        self.results_list.itemClicked.connect(self.open_item)
        self.results_list.setStyleSheet(
            """
            QListWidget { border:none; background:#ffffff; }
            QListWidget::item:selected { background:#ebf0ff; border-radius:6px; }
            """
        )
        c_lay.addWidget(self.results_list)

        # Assemble ---------------------------------------------------------
        root.addWidget(sidebar)
        root.addWidget(content)
        self.setCentralWidget(central)

        self.populate_demo()

    # --------------------------- Demo / Backend ---------------------------

    def populate_demo(self):
        sample = list(Path(__file__).parent.glob("*.py"))[:6]
        self.results_list.clear()
        for p in sample:
            card = FileCard(p)
            item = QListWidgetItem(self.results_list)
            item.setSizeHint(card.sizeHint())
            self.results_list.setItemWidget(item, card)

    # --------------------------- Callbacks --------------------------------

    def on_search(self, text: str):
        # TODO: backend search integration
        print("Search:", text)

    def open_item(self, item: QListWidgetItem):
        card = self.results_list.itemWidget(item)
        print("Open", card.path)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Helvetica Neue", 10))
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()