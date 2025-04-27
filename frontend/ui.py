"""Modern file browser UI mock‑up using PySide6.
Run `python file_browser_ui.py` (after `pip install PySide6`) to launch.
Hook up the `TODO:` marked signals to your backend.
"""

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
    QSizePolicy,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class NavButton(QToolButton):
    """Reusable icon‑only navigation button."""

    def __init__(self, icon: QIcon, tooltip: str):
        super().__init__()
        self.setIcon(icon)
        self.setIconSize(QSize(22, 22))
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setCheckable(True)
        # auto‑exclusive makes a radio‑button‑like sidebar
        self.setAutoExclusive(True)
        self.setStyleSheet(
            """
            NavButton {
                border: none;
                padding: 10px;
            }
            NavButton:checked {
                background: #36454F;
                border‑radius: 8px;
            }
            """
        )


class FileCard(QWidget):
    """Simple widget representing a single search result/file."""

    def __init__(self, path: Path):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(14)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(
            QApplication.style().standardIcon(QStyle.SP_FileIcon).pixmap(32, 32)
        )
        layout.addWidget(icon_lbl)

        text_layout = QVBoxLayout()
        name_lbl = QLabel(path.name)
        name_lbl.setStyleSheet("font‑weight:600;")
        summary_lbl = QLabel("Summary of file …")
        summary_lbl.setStyleSheet("color:gray; font‑size:11px;")
        text_layout.addWidget(name_lbl)
        text_layout.addWidget(summary_lbl)
        layout.addLayout(text_layout)

        meta_lbl = QLabel(
            f"{path.stat().st_size/1024:.1f} KB  |  {path.stat().st_mtime:.0f}"
        )
        meta_lbl.setStyleSheet("color:gray; font‑size:11px;")
        layout.addWidget(meta_lbl)
        layout.setStretch(1, 1)

        # Click handling can propagate via parent list widget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semantic File Explorer")
        self.resize(980, 640)
        self._build_ui()

    # -------- UI building helpers --------

    def _build_ui(self):
        central = QWidget()
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar -----------------------------------------------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(72)
        sidebar.setStyleSheet("background:#222; color:white;")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setAlignment(Qt.AlignTop)

        style = QApplication.style()
        buttons = [
            (style.standardIcon(QStyle.SP_BrowserReload), "Watch Folders"),
            (style.standardIcon(QStyle.SP_DirOpenIcon), "Folders"),
            (style.standardIcon(QStyle.SP_FileDialogContentsView), "API Keys"),
            (style.standardIcon(QStyle.SP_FileDialogDetailedView), "Settings"),
            (style.standardIcon(QStyle.SP_DialogYesButton), "Login"),
        ]
        self.nav_buttons = []
        for icon, tip in buttons:
            btn = NavButton(icon, tip)
            side_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        side_layout.addStretch(1)

        # Vertical separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("color:#333;")

        # Main content ------------------------------------------------------
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(18)

        # Search bar
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search …")
        self.search_edit.setFixedHeight(40)
        self.search_edit.setStyleSheet(
            "QLineEdit { border:1px solid #ccc; border‑radius:20px; padding‑left:36px; }"
        )
        # Magnifier icon overlay
        search_icon = QLabel(self.search_edit)
        search_icon.setPixmap(style.standardIcon(QStyle.SP_FileDialogStart).pixmap(18, 18))
        search_icon.move(12, 11)
        self.search_edit.textChanged.connect(self.on_search)
        content_layout.addWidget(self.search_edit)

        # Results list
        self.results_list = QListWidget()
        self.results_list.setFrameShape(QFrame.NoFrame)
        self.results_list.setSpacing(6)
        self.results_list.itemClicked.connect(self.open_item)
        content_layout.addWidget(self.results_list)

        # assemble layouts
        root_layout.addWidget(sidebar)
        root_layout.addWidget(separator)
        root_layout.addWidget(content)
        self.setCentralWidget(central)

        self.populate_demo()

    # -------- Backend hooks / demo data --------

    def populate_demo(self):
        """Populate list with dummy files – replace w/ backend results."""
        sample_files = list(Path(__file__).parent.glob("*.py"))[:4]
        self.results_list.clear()
        for p in sample_files:
            widget = FileCard(p)
            item = QListWidgetItem(self.results_list)
            item.setSizeHint(widget.sizeHint())
            self.results_list.setItemWidget(item, widget)

    # -------- Callbacks --------

    def on_search(self, text: str):
        # TODO: Call your semantic‑search backend and repopulate results_list.
        print("Search:", text)

    def open_item(self, item: QListWidgetItem):
        widget = self.results_list.itemWidget(item)
        # TODO: open file / show preview / forward to backend
        print("Clicked", widget.findChild(QLabel).text())


# ---------------------------------------------------------------------------

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
