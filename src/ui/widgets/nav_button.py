from __future__ import annotations

from PySide6.QtCore import QSize
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
        self.setCheckable(True)
        self.setAutoExclusive(True)
