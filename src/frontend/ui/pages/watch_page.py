from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from commands import watch
from settings import settings


class WatchPage(QWidget):
    """Add & show folders that the backend will watch."""

    def __init__(self, add_callback):
        super().__init__()
        # self._add_cb = add_callback
        self._add_cb = watch._add

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
            "border:1px solid #d4d4d4; border-radius:6px; padding:6px 8px;"
            'font-size:13px;color:#000000;'
        )
        row.addWidget(self.path_edit, 1)

        select_btn = QPushButton("Select")
        select_btn.clicked.connect(self._browse)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self._add)

        for b in (select_btn, add_btn):
            b.setStyleSheet(
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

        row.addWidget(select_btn)
        row.addWidget(add_btn)

        root.addLayout(row)

        # ---- table of paths ---------------------------------------------
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Root Name", "Full Path"])
        self.table.setStyleSheet(
            """
            QTableWidget {
                border:1px solid #d4d4d4;
                border-radius:10px;
                gridline-color:#ececec;
                font-size:14px;
                color:#000000;                 /* ← pure black text */
            }
            QHeaderView::section {
                background:#f9f9f9;
                border:none;
                font-weight:600;
                padding:6px 10px;
                color:#000000;                 /* header text black as well */
            }
            """
        )

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

        self._load_existing_paths()

    def _load_existing_paths(self):
        """Load previously watched paths and display them."""
        for path in settings.get_watch_paths():
            self._insert_path(path)

    def _browse(self):
        # native Qt folder dialog (non-blocking)
        path = QFileDialog.getExistingDirectory(self, "Choose a folder to watch")
        # if path:
        #     self.path_edit.setText(path)
        print(path)
        if path:
            self._add_cb(path)
            self._insert_path(path)
            # Ask user for description
            # description, ok = QInputDialog.getText(self, "Enter Description", "Describe this folder:")
            # if ok and description.strip():
            #     self._insert_path(path)
            # self._add_cb("".join(list(str(path))), description)  # Notify backend (if needed for your app)

            # --- Save to assoc storage ---
            # self._add_cb(path)
            # cfg = FileSystemConfig()
            # cfg.append_entry(path, description)
            # else:
            #     print("No description provided. Skipped adding.")

    def _add(self):
        raw = self.path_edit.text().strip()
        if not raw:
            return
        self._insert_path(raw)
        self._add_cb(str(Path(raw).resolve()))  # let backend know
        self.path_edit.clear()

    def _insert_path(self, p: str):
        rname = Path(p).name or p
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(rname))
        self.table.setItem(r, 1, QTableWidgetItem(p))
