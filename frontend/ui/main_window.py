from __future__ import annotations

import sys
from pathlib import Path

from frontend.ui.widgets.file_card import FileCard
from frontend.ui.widgets.nav_button import NavButton
from frontend.utils.icons import icon

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


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


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Helvetica Neue", 10))
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()