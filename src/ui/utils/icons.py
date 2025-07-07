from __future__ import annotations

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QStyle,
)

from settings import ASSETS_DIR

ICONS_DIR = ASSETS_DIR / "icons"
ICON_MAP = {
    "watch": ICONS_DIR / "refresh.svg",
    "folder": ICONS_DIR / "folder.svg",
    "keys": ICONS_DIR / "key.svg",
    "settings": ICONS_DIR / "settings.svg",
    "login": ICONS_DIR / "user.svg",
    "search": ICONS_DIR / "search.svg",
    ".pdf": ICONS_DIR / "pdf.svg",
    ".txt": ICONS_DIR / "txt.svg",
    ".csv": ICONS_DIR / "csv.svg",
}


def icon(name: str, size: int = 200) -> QIcon:
    path = ICON_MAP.get(name)
    if path and path.exists():
        return QIcon(str(path))
    # graceful fallback to built‑in if custom SVG missing
    return QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
