from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QToolButton,
)


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
