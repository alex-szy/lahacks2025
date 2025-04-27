from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel,
    QListWidget, QListWidgetItem, QFrame
)

from frontend.utils.icons import icon
from frontend.ui.widgets.file_card import FileCard
from pathlib import Path


class HomePage(QWidget):
    """Original search-and-results view extracted into its own widget."""
    def __init__(self, on_search, on_open):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(24)

        self.search_edit = QLineEdit(placeholderText="Search for a file …")
        self.search_edit.setFixedHeight(46)
        self.search_edit.setStyleSheet(
            """
            QLineEdit {
                background:#ffffff; color:#222;
                font-family:"Poppins",sans-serif; font-size:14px;
                border:1px solid #d4d4d4; border-radius:23px; padding-left:48px;
            }
            QLineEdit:focus { border-color:#7a74ff; }
            QLineEdit::placeholder { color:#999; }
            """
        )
        mag = QLabel(self.search_edit)
        mag.setPixmap(icon("home", 24).pixmap(QSize(24, 24)))
        mag.move(16, 11)
        self.search_edit.textChanged.connect(on_search)
        lay.addWidget(self.search_edit)

        self.results = QListWidget(frameShape=QFrame.NoFrame, spacing=4)
        self.results.itemClicked.connect(on_open)
        self.results.setStyleSheet(
            """
            QListWidget { border:none; background:#fff; }
            QListWidget::item:selected{ background:#ebf0ff; border-radius:6px; }
            """
        )
        lay.addWidget(self.results)

        # quick demo content
        for p in list(Path(__file__).parent.parent.glob("*.py"))[:5]:
            card = FileCard(p)
            it = QListWidgetItem(self.results)
            it.setSizeHint(card.sizeHint())
            self.results.setItemWidget(it, card)
