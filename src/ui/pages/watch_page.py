from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from api import watch


class WatchPage(QWidget):
    """Add & show folders that the backend will watch."""

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(18)

        title = QLabel("Add Watch Folders")
        title.setStyleSheet("font-size:18px; font-weight:600; color:#222;")
        root.addWidget(title)

        # ---- input row ---------------------------------------------------
        row = QHBoxLayout()
        self.path_edit = QLineEdit(placeholderText="Enter folder path …")
        self.path_edit.setMinimumWidth(350)
        self.path_edit.setStyleSheet(
            "border:1px solid #d4d4d4; padding:6px 8px;font-size:13px;"
        )
        row.addWidget(self.path_edit, 1)

        buttons = [
            (QPushButton("Browse"), self.handle_browse),
            (QPushButton("Add"), self.handle_add),
        ]

        for button, handler in buttons:
            button.setStyleSheet(
                """
                QPushButton {
                    background:#ffffff;
                    color:#222;                          /* visible text */
                    border:1px solid #d4d4d4;
                    border-radius:6px;
                    padding:6px 18px;
                    font-size:13px;
                }
                QPushButton:hover { background:#f7f7f7; }
                QPushButton:pressed { background:#ededed; }
                """
            )
            button.clicked.connect(handler)
            row.addWidget(button)

        root.addLayout(row)

        # ---- table of paths ---------------------------------------------
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Root Name", "Full Path"])
        self.table.setStyleSheet(
            """
            QTableWidget {
                border-radius:10px;
                gridline-color:#ececec;
                font-size:14px;
                color:#000000;                 /* ← pure black text */
            }
            """
        )
        self.table.setFrameStyle(QFrame.Shape.NoFrame)

        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )  # wider left column
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )  # right column stretches too
        self.table.setColumnWidth(0, int(self.width() * 0.35))
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        root.addWidget(self.table, 1)

        self.update()

    def update(self, *args, **kwargs):
        """Load previously watched paths and display them."""
        super().update(*args, **kwargs)
        self.table.setRowCount(0)
        self.table.clearContents()
        for path in watch.list():
            self._insert_path(path)

    def handle_browse(self):
        path = QFileDialog.getExistingDirectory(self, "Choose a folder to watch")
        if path:
            self._add_path(path)

    def handle_add(self):
        raw = self.path_edit.text().strip()
        if not raw:
            return
        cleaned = str(Path(raw).expanduser().resolve())
        if self._add_path(cleaned):
            self.path_edit.clear()

    def _add_path(self, path):
        ok, err = watch.add(path)
        if err:
            QMessageBox.critical(
                self, "Add watch path failed", f"Adding watch path failed: {err}"
            )
        self.update()
        return ok

    def _insert_path(self, p: str):
        rname = Path(p).name or p
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(rname))
        self.table.setItem(r, 1, QTableWidgetItem(p))
