from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from frontend.utils.icons import icon
from models.file import File  # adjust import path if necessary

# Extensions we want to show custom icons for (svg files must exist under
# your icon theme with the same *key* name).
SUPPORTED_TEXT_EXTENSIONS = [
    "txt",
    "md",
    "json",
    "csv",
    "tsv",
    "yaml",
    "yml",
    "ini",
    "xml",
    "html",
    "py",
    "java",
    "js",
    "cpp",
    "c",
    "h",
    "sh",
    "pdf",
    "docx",
]


class FileCard(QWidget):
    """Visual row representing a single :class:`File` result.

    Only *name*, *summary*, and *extension* are guaranteed to exist on the
    incoming ``File`` instance. All other attributes – *path*, *size_bytes*,
    *created_at*, *modified_at*, *content* – may be ``None`` or missing.
    The widget therefore handles every piece of metadata defensively.
    """

    _DATE_FMT = "%b %d %Y"  # e.g. "Apr 27 2025"

    def __init__(self, file: File):
        super().__init__()
        self.setStyleSheet("background:transparent;")  # allow list‑item highlight

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 6, 4, 6)
        layout.setSpacing(14)

        # ── File icon ───────────────────────────────────────────────────────
        ext = (getattr(file, "extension", "") or "").lstrip(".").lower()
        icon_key = ext if ext in SUPPORTED_TEXT_EXTENSIONS else "file"
        icon_lbl = QLabel()
        qicon = icon(icon_key, 28).pixmap(QSize(28, 28))
        icon_lbl.setPixmap(qicon)
        layout.addWidget(icon_lbl)

        # ── Text column (name + summary) ─────────────────────────────────────
        text_col = QVBoxLayout()

        name_lbl = QLabel(getattr(file, "name", "Unnamed file"))
        name_lbl.setStyleSheet(
            """
            color: #222;
            font-family: "Poppins", sans-serif;
            font-weight: 600;
            font-size: 14px;
            """
        )

        summary_lbl = QLabel(getattr(file, "summary", "No summary available."))
        summary_lbl.setWordWrap(True)
        summary_lbl.setStyleSheet(
            """
            color: #666;
            font-family: "Poppins", sans-serif;
            font-size: 12px;
            """
        )

        text_col.addWidget(name_lbl)
        text_col.addWidget(summary_lbl)
        layout.addLayout(text_col, 1)

        # ── Meta information (size • modified) ───────────────────────────────
        meta_str = self._build_meta_string(file)
        if meta_str:
            meta_lbl = QLabel(meta_str)
            meta_lbl.setStyleSheet(
                """
                color: #777;
                font-family: "Poppins", sans-serif;
                font-size: 11px;
                """
            )
            layout.addWidget(meta_lbl)

    # ── Helper methods ──────────────────────────────────────────────────────
    def _build_meta_string(self, file: File) -> str:
        """Safely build the *size • modified* string."""
        size_kb = self._resolve_size(file)
        mtime = self._resolve_mtime(file)
        parts: list[str] = []
        if size_kb is not None:
            parts.append(f"{size_kb:.1f} KB")
        if mtime:
            parts.append(mtime)
        return " · ".join(parts)

    @staticmethod
    def _resolve_size(file: File) -> Optional[float]:
        """Return file size in kilobytes if determinable."""
        # Attribute may not exist – use getattr defensively
        size_bytes = getattr(file, "size_bytes", None)
        if size_bytes is not None:
            return size_bytes / 1024
        path_str = getattr(file, "path", None)
        if path_str:
            try:
                return Path(path_str).stat().st_size / 1024
            except (FileNotFoundError, OSError):
                pass
        # Fallback to content length if provided
        content = getattr(file, "content", None)
        if content:
            return len(content) / 1024
        return None

    def _resolve_mtime(self, file: File) -> Optional[str]:
        """Return modified‑time string or *None* if unavailable."""
        mtime_raw = getattr(file, "modified_at", None)
        if mtime_raw:
            # Try ISO-8601 first; fallback to raw string
            try:
                ts = _dt.datetime.fromisoformat(mtime_raw)
                return ts.strftime(self._DATE_FMT)
            except ValueError:
                return str(mtime_raw)
        path_str = getattr(file, "path", None)
        if path_str:
            try:
                ts = _dt.datetime.fromtimestamp(Path(path_str).stat().st_mtime)
                return ts.strftime(self._DATE_FMT)
            except (FileNotFoundError, OSError):
                pass
        return None
