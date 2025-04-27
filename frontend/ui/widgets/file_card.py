from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget

from frontend.utils.icons import icon
from models.file import File  # adjust import path if necessary


class FileCard(QWidget):
    """Visual row representing a single :class:`File` result."""

    _DATE_FMT = "%b %d %Y"  # e.g. "Apr 27 2025"

    def __init__(self, file: File):
        super().__init__()
        self._file = file
        self.setStyleSheet("background:transparent;")  # allow list‑item highlight

        lay = QHBoxLayout(self)
        lay.setContentsMargins(4, 6, 4, 6)
        lay.setSpacing(14)

        # ── File icon ────────────────────────────────────────────────────────
        ext = (file.extension or (Path(file.path).suffix[1:] if file.path else "")).lower()
        icn_key = ext if ext else "file"
        icon_lbl = QLabel()
        icon_lbl.setPixmap(icon(icn_key, 28).pixmap(QSize(28, 28)))
        lay.addWidget(icon_lbl)

        # ── Text column (name + summary) ─────────────────────────────────────
        text_col = QVBoxLayout()

        name_lbl = QLabel(file.name)
        name_lbl.setStyleSheet(
            """
            color: #222;
            font-family: "Poppins", sans-serif;
            font-weight: 600;
            font-size: 14px;
            """
        )

        summary_text = getattr(file, "summary", None) or "No summary available."
        sum_lbl = QLabel(summary_text)
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

        # ── Meta information (size • modified) ───────────────────────────────
        size_kb = self._resolve_size(file)
        mtime = self._resolve_mtime(file)
        meta_str = f"{size_kb:.1f} KB" + (f" · {mtime}" if mtime else "")

        meta_lbl = QLabel(meta_str)
        meta_lbl.setStyleSheet(
            """
            color: #777;
            font-family: "Poppins", sans-serif;
            font-size: 11px;
            """
        )
        lay.addWidget(meta_lbl)

    # ── Helpers ─────────────────────────────────────────────────────────────
    @staticmethod
    def _resolve_size(file: File) -> float:
        """Return file size in kilobytes, attempting fallbacks if needed."""
        if file.size_bytes is not None:
            return file.size_bytes / 1024
        if file.path:
            try:
                return Path(file.path).stat().st_size / 1024
            except (FileNotFoundError, OSError):
                pass
        # len(content) may be expensive but provides a final fallback
        return len(file.content) / 1024 if file.content else 0.0

    @classmethod
    def _resolve_mtime(cls, file: File) -> Optional[str]:
        """Return modified‑time string or *None* if unavailable."""
        if file.modified_at:
            try:
                # assume ISO8601 / RFC3339 style string
                ts = _dt.datetime.fromisoformat(file.modified_at)
                return ts.strftime(cls._DATE_FMT)
            except ValueError:
                return file.modified_at  # leave as‑is if parsing fails
        if file.path:
            try:
                ts = _dt.datetime.fromtimestamp(Path(file.path).stat().st_mtime)
                return ts.strftime(cls._DATE_FMT)
            except (FileNotFoundError, OSError):
                pass
        return None
