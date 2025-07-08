from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

import api.assoc
from settings import settings


class DestinationPage(QWidget):
    """Add & show destination folders for saving classified files."""

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(18)

        title = QLabel("Add Destination Folders")
        root.addWidget(title)

        # ---- input row ---------------------------------------------------
        row = QHBoxLayout()
        self.path_edit = QLineEdit(placeholderText="Enter folder path …")
        row.addWidget(self.path_edit, 1)

        buttons = [
            (QPushButton("Add"), self.handle_add),
            (QPushButton("Browse"), self.handle_browse),
        ]

        for button, handler in buttons:
            button.clicked.connect(handler)
            row.addWidget(button)

        root.addLayout(row)

        # ---- table of paths ------------------------------------------------
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Path", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.itemDoubleClicked.connect(self.handle_remove)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        root.addWidget(self.table, 1)

        self.update()

    def update(self, *args, **kwargs):
        """Load existing destination folders + descriptions into the table."""
        super().update(*args, **kwargs)
        self.table.setRowCount(0)
        for path, description in settings.get_folder_paths().items():
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(path))
            self.table.setItem(r, 1, QTableWidgetItem(description))

    def handle_browse(self):
        """Open a folder picker and prompt for description."""
        path = QFileDialog.getExistingDirectory(self, "Choose a destination folder")
        if path:
            self._add_path(path)

    def handle_add(self):
        """Manually add from the QLineEdit input."""
        raw = self.path_edit.text().strip()
        if not raw:
            return
        cleaned = str(Path(raw).expanduser().resolve())
        if self._add_path(cleaned):
            self.path_edit.clear()

    def _add_path(self, folder_path: str):
        """Default backend logic: uses assoc."""
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Folder Description")
        dialog.setLabelText("Describe this folder:")
        ok = dialog.exec()
        description = dialog.textValue()
        if not (ok and description.strip()):
            return False
        ok, err = api.assoc.add(folder_path, description)
        if err:
            QMessageBox.critical(
                self,
                "Add folder association failed",
                f"Adding folder association failed: {err}",
            )
        else:
            self.update()
        return ok

    def handle_remove(self, item: QTableWidgetItem):
        """Prompts the user for removal of an entry"""
        path_cell = self.table.item(item.row(), 0)
        if not path_cell:
            return
        path = path_cell.text()
        button = QMessageBox.question(
            self,
            "Remove folder association",
            f"Remove the folder association for the path '{path}'?",
        )
        if button == QMessageBox.StandardButton.Yes:
            api.assoc.remove(path_cell.text())
            self.update()
