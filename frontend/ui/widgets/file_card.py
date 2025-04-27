from __future__ import annotations

from pathlib import Path
from frontend.utils.icons import icon

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
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
        name_lbl.setStyleSheet(
            """
            color: #666;
            font-family: "Poppins", sans-serif;
            font-weight: 600;
            font-size: 14px;
            """
        )

        sum_lbl = QLabel("Summary of file …")  # TODO real summary
        sum_lbl.setStyleSheet(
            """
            color: #666;
            font-family: "Poppins", sans-serif;
            font-size: 12px;
            """
        )
        sum_lbl.setWordWrap(True)
        text_col.addWidget(name_lbl)
        text_col.addWidget(sum_lbl)
        lay.addLayout(text_col, 1)

        meta_lbl = QLabel(f"{path.stat().st_size/1024:.1f} KB · {path.stat().st_mtime:.0f}")
        meta_lbl.setStyleSheet(
            """
            color: #777;
            font-family: "Poppins", sans-serif;
            font-size: 11px;
            """
        )

        lay.addWidget(meta_lbl)