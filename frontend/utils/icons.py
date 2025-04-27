from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QStyle,
)

HERE = Path(__file__).parent.parent / "resources"
ICON_MAP = {
    "watch": HERE / "icons/refresh.svg",
    "folder": HERE / "icons/folder.svg",
    "keys": HERE / "icons/key.svg",
    "settings": HERE / "icons/settings.svg",
    "login": HERE / "icons/user.svg",
    "search": HERE / "icons/search.svg",
    "file": HERE / "icons/file.svg",
}


def icon(name: str, size: int = 200) -> QIcon:
    path = ICON_MAP.get(name)
    print(path)
    if path and path.exists():
        return QIcon(str(path))
    # graceful fallback to built‑in if custom SVG missing
    return QApplication.style().standardIcon(getattr(QStyle, "SP_FileIcon", 0))