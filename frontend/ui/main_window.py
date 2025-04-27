# near the top
import sys

from PySide6.QtWidgets import QStackedWidget
from frontend.ui.pages.home_page import HomePage
from frontend.ui.pages.watch_page import WatchPage
from frontend.ui.widgets.nav_button import NavButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from pathlib import Path
from frontend.utils.icons import icon    # new helper name
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QListWidgetItem,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QApplication,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semantic File Explorer")
        self.resize(1050, 660)
        self._build_ui()
    
    def on_search(self, text: str):
        # TODO: backend search integration
        print("Search:", text)

    def open_item(self, item: QListWidgetItem):
        card = self.results_list.itemWidget(item)
        print("Open", card.path)
    
    def backend_add_watch(self, path: Path):
        print(">> Watch this folder in backend:", path)
        # TODO: plug into your FileSystemConfig / observer logic

    def _build_ui(self):
        central = QWidget()
        central.setStyleSheet("background: #ffffff;")
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)

        # ---------- Sidebar --------------------------------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(72)
        sidebar.setStyleSheet("background:#ffffff; border-right:1px solid #ffffff;")
        side_lay = QVBoxLayout(sidebar)
        side_lay.setAlignment(Qt.AlignTop)
        side_lay.setContentsMargins(12, 16, 12, 16)
        side_lay.setSpacing(10)

        btn_info = [
            ("search",     "Search"),          # ← new home button
            ("watch",    "Watch Folders"),
            ("folder",   "Folders"),
            ("keys",     "API Keys"),
            ("settings", "Settings"),
            ("login",    "Login"),
        ]
        self.nav_btns = []
        for key, tip in btn_info:
            b = NavButton(icon(key), tip)
            side_lay.addWidget(b)
            self.nav_btns.append(b)
        side_lay.addStretch(1)

        # ---------- Stacked pages --------------------------------------
        self.pages = QStackedWidget()
        self.home   = HomePage(self.on_search, self.open_item)
        self.watch  = WatchPage(self.backend_add_watch)  # pass your backend hook
        self.pages.addWidget(self.home)   # index 0
        self.pages.addWidget(self.watch)  # index 1
        # add more pages later …

        root.addWidget(sidebar)
        root.addWidget(self.pages)        # ← replace “content” with pages
        self.setCentralWidget(central)

        # default to Home
        self.nav_btns[0].setChecked(True)
        for i, btn in enumerate(self.nav_btns):
            btn.clicked.connect(lambda _, ix=i: self.pages.setCurrentIndex(ix))

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Helvetica Neue", 10))
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()