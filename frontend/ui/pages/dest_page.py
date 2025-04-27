from __future__ import annotations
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QHeaderView,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QAbstractItemView, QInputDialog
)

from commands import assoc
from utilities.file_system_config import FileSystemConfig
# from commands.assoc import load_watch_paths


class DestinationPage(QWidget):
    """Add & show destination folders for saving classified files."""

    def __init__(self, add_callback=None):
        super().__init__()
        self._add_cb = add_callback or self._default_add_callback
        self.setStyleSheet('font-family:"Poppins",sans-serif;')

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(18)

        title = QLabel("Add Destination Folders")
        title.setStyleSheet("font-size:18px; font-weight:600; color:#222;")
        root.addWidget(title)

        # ---- input row ---------------------------------------------------
        row = QHBoxLayout()
        self.path_edit = QLineEdit(placeholderText="Enter folder path …")
        self.path_edit.setMinimumWidth(350)
        self.path_edit.setStyleSheet(
            "border:1px solid #d4d4d4; border-radius:6px; padding:6px 8px;"
            'font-family:"Poppins",sans-serif; font-size:13px;color:#000000;'
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
                    color:#222;
                    border:1px solid #d4d4d4;
                    border-radius:6px;
                    padding:6px 18px;
                    font-family:"Poppins",sans-serif;
                    font-size:13px;
                }
                QPushButton:hover { background:#f7f7f7; }
                QPushButton:pressed { background:#ededed; }
                """
            )

        row.addWidget(select_btn)
        row.addWidget(add_btn)

        root.addLayout(row)

        # ---- table of paths ------------------------------------------------
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Root Name", "Full Path"])
        self.table.setStyleSheet(
            """
            QTableWidget {
                border:1px solid #d4d4d4;
                border-radius:10px;
                gridline-color:#ececec;
                font-family:"Poppins",sans-serif;
                font-size:14px;
                color:#000000;
            }
            QHeaderView::section {
                background:#f9f9f9;
                border:none;
                font-weight:600;
                padding:6px 10px;
                color:#000000;
            }
            """
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        root.addWidget(self.table, 1)

        self._load_existing_destinations()

    def _load_existing_destinations(self):
        """Load existing destination folders + descriptions into the table."""
        cfg = FileSystemConfig()
        entries = cfg.read_all_entries()  # This returns a dict { folder_path: description }
        for folder_path, description in entries.items():
            self._insert_path(folder_path)

    def _browse(self):
        """Open a folder picker and prompt for description."""
        path = QFileDialog.getExistingDirectory(self, "Choose a destination folder")
        if path:
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Folder Description")
            dialog.setLabelText("Describe this folder:")
            dialog.setStyleSheet(
                """
                QInputDialog {
                    font-family: "Poppins", sans-serif;
                    font-size: 13px;
                    color: #000000;
                    background: #ffffff;
                }
                QLabel {
                    color: #000000;
                }
                QLineEdit {
                    color: #000000;
                    background: #ffffff;
                    border: 1px solid #d4d4d4;
                    border-radius: 6px;
                    padding: 6px 8px;
                }
                QPushButton {
                    font-family: "Poppins", sans-serif;
                    font-size: 13px;
                    color: #222;
                    background: #ffffff;
                    border: 1px solid #d4d4d4;
                    border-radius: 6px;
                    padding: 6px 18px;
                }
                QPushButton:hover { background: #f7f7f7; }
                QPushButton:pressed { background: #ededed; }
                """
            )
            ok = dialog.exec()
            description = dialog.textValue()
            if ok and description.strip():
                self._insert_path(path)
                self._add_cb(path, description.strip())
            else:
                print("No description provided. Skipped adding.")
        # if path:
        #     description, ok = QInputDialog.getText(self, "Folder Description", "Describe this folder:")
        #     if ok and description.strip():
        #         self._insert_path(path)
        #         self._add_cb(path, description.strip())
        #     else:
        #         print("No description provided. Skipped adding.")

    def _add(self):
        """Manually add from the QLineEdit input."""
        raw = self.path_edit.text().strip()
        if not raw:
            return
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Folder Description")
        dialog.setLabelText("Describe this folder:")
        dialog.setStyleSheet(
            """
            QInputDialog {
                font-family: "Poppins", sans-serif;
                font-size: 13px;
                color: #000000;
                background: #ffffff;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                color: #000000;
                background: #ffffff;
                border: 1px solid #d4d4d4;
                border-radius: 6px;
                padding: 6px 8px;
            }
            QPushButton {
                font-family: "Poppins", sans-serif;
                font-size: 13px;
                color: #222;
                background: #ffffff;
                border: 1px solid #d4d4d4;
                border-radius: 6px;
                padding: 6px 18px;
            }
            QPushButton:hover { background: #f7f7f7; }
            QPushButton:pressed { background: #ededed; }
            """
        )
        ok = dialog.exec()
        description = dialog.textValue()

        if ok and description.strip():
            self._insert_path(raw)
            self._add_cb(raw, description.strip())
            self.path_edit.clear()
        else:
            print("No description provided. Skipped adding.")
        # description, ok = QInputDialog.getText(self, "Folder Description", "Describe this folder:")
        # if ok and description.strip():
        #     self._insert_path(raw)
        #     self._add_cb(raw, description.strip())
        #     self.path_edit.clear()
        # else:
        #     print("No description provided. Skipped adding.")

    def _insert_path(self, p: str):
        """Insert new entry into the table."""
        rname = Path(p).name or p
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(rname))
        self.table.setItem(r, 1, QTableWidgetItem(p))

    def _default_add_callback(self, folder_path: str, description: str):
        """Default backend logic: uses assoc + config."""
        cfg = FileSystemConfig()
        cfg.append_entry(folder_path, description)
