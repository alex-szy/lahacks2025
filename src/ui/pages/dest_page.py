from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from settings import settings


class DestinationPage(QWidget):
    """Add & show destination folders for saving classified files."""

    def __init__(self, add_callback=None):
        super().__init__()
        self._add_cb = add_callback or self._default_add_callback

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(18)

        title = QLabel("Add Destination Folders")
        root.addWidget(title)

        # ---- input row ---------------------------------------------------
        row = QHBoxLayout()
        self.path_edit = QLineEdit(placeholderText="Enter folder path …")
        row.addWidget(self.path_edit, 1)

        select_btn = QPushButton("Select")
        select_btn.clicked.connect(self._browse)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self._add)

        row.addWidget(select_btn)
        row.addWidget(add_btn)

        root.addLayout(row)

        # ---- table of paths ------------------------------------------------
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Root Name", "Full Path"])
        root.addWidget(self.table, 1)

        self._load_existing_destinations()

    def _load_existing_destinations(self):
        """Load existing destination folders + descriptions into the table."""
        for folder_path in settings.get_folder_paths().keys():
            self._insert_path(folder_path)

    def _browse(self):
        """Open a folder picker and prompt for description."""
        path = QFileDialog.getExistingDirectory(self, "Choose a destination folder")
        if path:
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Folder Description")
            dialog.setLabelText("Describe this folder:")
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
        ok = dialog.exec()
        description = dialog.textValue()

        if ok and description.strip():
            self._insert_path(raw)
            self._add_cb(raw, description.strip())
            self.path_edit.clear()
        else:
            print("No description provided. Skipped adding.")

    def _insert_path(self, p: str):
        """Insert new entry into the table."""
        rname = Path(p).name or p
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(rname))
        self.table.setItem(r, 1, QTableWidgetItem(p))

    def _default_add_callback(self, folder_path: str, description: str):
        """Default backend logic: uses assoc + config."""
        folder_path = str(Path(folder_path).resolve())
        paths = settings.get_folder_paths()
        paths[folder_path] = description
        settings.set_folder_paths(paths)
