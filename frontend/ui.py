"""Modern, light‑mode file browser UI using PySide6.
Run `python file_browser_ui.py` after `pip install PySide6`.
Hook the marked TODOs to your backend logic.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

# -----------------------------------------------------------------------------
# Helper widgets
# -----------------------------------------------------------------------------


class NavButton(QToolButton):
    """Icon‑only button for the sidebar."""

    def __init__(self, icon: QIcon, tooltip: str):
        super().__init__()
        self.setIcon(icon)
        self.setIconSize(QSize(22, 22))
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setCheckable(True)
        self.setAutoExclusive(True)  # radio‑button behaviour
        self.setStyleSheet(
            """
            QToolButton {
                border: none;
                padding: 10px;
                border-radius: 12px;
            }
            QToolButton:hover {
                background: #eeeeee;
            }
            QToolButton:checked {
                background: #e0e0e0;
            }
            """
        )


class FileCard(QWidget):
    """A rounded‑corner result row with file metadata."""

    def __init__(self, path: Path):
        super().__init__()
        self.path = path
        self.setStyleSheet(
            """
            QWidget {
                background:#ffffff;
                border: 1px solid #e5e5e5;
                border-radius: 16px;
            }
            """
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(18)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(
            QApplication.style().standardIcon(QStyle.SP_FileIcon).pixmap(32, 32)
        )
        layout.addWidget(icon_lbl)

        text_layout = QVBoxLayout()
        name_lbl = QLabel(path.name)
        name_lbl.setStyleSheet("font-weight:600; font-size:14px;")
        summary_lbl = QLabel("Summary of file …")  # TODO replace with real summary
        summary_lbl.setStyleSheet("color:#666666; font-size:11px;")
        text_layout.addWidget(name_lbl)
        text_layout.addWidget(summary_lbl)
        layout.addLayout(text_layout)
        layout.setStretchFactor(text_layout, 1)

        meta_lbl = QLabel(
            f"{path.stat().st_size/1024:.1f} KB  |  {path.stat().st_mtime:.0f}"
        )
        meta_lbl.setStyleSheet("color:#999999; font-size:11px;")
        layout.addWidget(meta_lbl)


# -----------------------------------------------------------------------------
# Main window
# -----------------------------------------------------------------------------


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semantic File Explorer")
        self.resize(1000, 650)
        self._build_ui()

    # ------------------------------ UI -------------------------------------

    def _build_ui(self):
        central = QWidget()
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)

        # Sidebar -----------------------------------------------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(80)
        sidebar.setStyleSheet("background:#fafafa; border-right:1px solid #e5e5e5;")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setAlignment(Qt.AlignTop)
        side_layout.setContentsMargins(10, 10, 10, 10)
        side_layout.setSpacing(8)

        style = QApplication.style()
        buttons = [
            (style.standardIcon(QStyle.SP_BrowserReload), "Watch Folders"),
            (style.standardIcon(QStyle.SP_DirOpenIcon), "Folders"),
            (style.standardIcon(QStyle.SP_FileDialogContentsView), "API Keys"),
            (style.standardIcon(QStyle.SP_FileDialogDetailedView), "Settings"),
            (style.standardIcon(QStyle.SP_DialogYesButton), "Login"),
        ]
        self.nav_buttons: list[NavButton] = []
        for icon, tip in buttons:
            btn = NavButton(icon, tip)
            side_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        side_layout.addStretch(1)

        # Main content ------------------------------------------------------
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 24, 32, 24)
        content_layout.setSpacing(22)

        # Search bar -------------------------------------------------------
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search …")
        self.search_edit.setFixedHeight(44)
        self.search_edit.setStyleSheet(
            """
            QLineEdit {
                border:1px solid #d0d0d0;
                border-radius:22px;
                padding-left:44px;
                background:#ffffff;
            }
            QLineEdit:focus {
                border-color:#6c63ff;
            }
            """
        )
        search_icon = QLabel(self.search_edit)
        search_icon.setPixmap(style.standardIcon(QStyle.SP_FileDialogStart).pixmap(20, 20))
        search_icon.move(16, 12)
        self.search_edit.textChanged.connect(self.on_search)
        content_layout.addWidget(self.search_edit)

        # Results list ------------------------------------------------------
        self.results_list = QListWidget()
        self.results_list.setFrameShape(QFrame.NoFrame)
        self.results_list.setSpacing(10)
        self.results_list.itemClicked.connect(self.open_item)
        self.results_list.setStyleSheet("QListWidget { border:none; background:#f9f9f9; }")
        content_layout.addWidget(self.results_list)

        # Compound layout ---------------------------------------------------
        root.addWidget(sidebar)
        root.addWidget(content)
        self.setCentralWidget(central)

        # Demo data ---------------------------------------------------------
        self.populate_demo()

    # ---------------------------------------------------------------------
    # Demo / backend hooks
    # ---------------------------------------------------------------------

    def populate_demo(self):
        """Populate list with dummy results. Replace with backend results."""
        sample_files = list(Path(__file__).parent.glob("*.py"))[:6]
        self.results_list.clear()
        for p in sample_files:
            widget = FileCard(p)
            item = QListWidgetItem(self.results_list)
            item.setSizeHint(widget.sizeHint())
            self.results_list.setItemWidget(item, widget)

    # --------------------------- Callbacks --------------------------------

    def on_search(self, text: str):
        # TODO: call semantic search backend & refresh list
        print("Searching for:", text)

    def open_item(self, item: QListWidgetItem):
        card = self.results_list.itemWidget(item)
        # TODO: open preview or emit path to backend
        print("Open", card.path)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # consistent cross‑platform look
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
