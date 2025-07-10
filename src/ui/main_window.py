# near the top
import sys

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

from ui.pages.dest_page import DestinationPage
from ui.pages.home_page import HomePage
from ui.pages.watch_page import WatchPage
from ui.utils.icons import icon  # new helper name
from ui.widgets.nav_button import NavButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semantic File Explorer")
        self.resize(1050, 660)

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
            btn.clicked.connect(self.make_change_tab_to(i))

    def make_change_tab_to(self, index):
        """Returns a helper which switches to the correct page and updates it"""

        def inner():
            self.pages.setCurrentIndex(index)
            self.pages.widget(index).update()

        return inner


def main():
    app = QApplication(sys.argv)
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
