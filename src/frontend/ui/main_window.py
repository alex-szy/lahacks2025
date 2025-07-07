# near the top
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from frontend.ui.pages.dest_page import DestinationPage
from frontend.ui.pages.home_page import HomePage
from frontend.ui.pages.watch_page import WatchPage
from frontend.ui.widgets.nav_button import NavButton
from frontend.utils.icons import icon  # new helper name


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

        # ---------- Sidebar --------------------------------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(72)
        side_lay = QVBoxLayout(sidebar)
        side_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        side_lay.setContentsMargins(12, 16, 12, 16)
        side_lay.setSpacing(10)

        btn_info = [
            ("search", "Search"),
            ("watch", "Watch Folders"),
            ("folder", "Destination Folders"),
        ]
        self.nav_btns: list[NavButton] = []
        for key, tip in btn_info:
            b = NavButton(icon(key), tip)
            side_lay.addWidget(b)
            self.nav_btns.append(b)
        side_lay.addStretch(1)

        # ---------- Stacked pages --------------------------------------
        self.pages = QStackedWidget()
        self.home = HomePage()
        self.watch = WatchPage()
        self.dest = DestinationPage()
        self.pages.addWidget(self.home)  # index 0
        self.pages.addWidget(self.watch)  # index 1
        self.pages.addWidget(self.dest)  # index 2
        # add more pages later …

        root.addWidget(sidebar)
        root.addWidget(self.pages)  # ← replace “content” with pages
        self.setCentralWidget(central)

        # default to Home
        self.nav_btns[0].setChecked(True)
        for i, btn in enumerate(self.nav_btns):
            btn.clicked.connect(lambda _, ix=i: self.pages.setCurrentIndex(ix))

        self.pages.currentChanged.connect(self.on_page_change)

    def on_page_change(self, index):
        widget = self.pages.widget(index)
        widget.update()


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.setStyleSheet(
        """
        font: "Helvetica Neue";
        font-size: 10px;
        color: #000000;
        background: #ffffff;
        border: none;
        border-radius: 6px;
        """
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
