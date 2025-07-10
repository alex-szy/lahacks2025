import os
import subprocess
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from api.find import find
from ui.widgets.file_card import FileCard


class HomePage(QWidget):
    """Search‑and‑results view.

    Parameters
    ----------
    on_search : Callable[[str], Iterable[Path] | None]
        Function invoked when the user presses *Return* or *Enter*. It should
        return an iterable of ``pathlib.Path`` objects (or strings) pointing to
        the matching files. If nothing matches, return an empty iterable or
        ``None``.
    on_open : Callable[[QListWidgetItem], None]
        Called when a user clicks a file card in the list.
    """

    def __init__(self):
        super().__init__()

        # ── Layout ────────────────────────────────────────────────────────────
        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(24)

        # ── Search bar ───────────────────────────────────────────────────────
        self.search_edit = QLineEdit(placeholderText="Search for a file …")

        # Trigger search *only* when user presses Return/Enter
        self.search_edit.returnPressed.connect(self._handle_search)
        lay.addWidget(self.search_edit)

        # ── Results list ──────────────────────────────────────────────────────
        self.results = QListWidget()
        self.results.itemDoubleClicked.connect(self._handle_open)
        lay.addWidget(self.results)

    # ── Internal helpers ─────────────────────────────────────────────────────
    def _handle_search(self):
        """Invoke external search callback and render its results."""
        query = self.search_edit.text().strip()
        if not query:
            return

        matches, err = find(query)
        if err:
            QMessageBox.critical(
                self, "Error searching", f"Error searching for file: {err}"
            )
            return

        self._render_results(matches)

    def _render_results(self, files):
        """Populate the QListWidget with FileCard widgets."""
        self.results.clear()
        if not files:
            empty = QListWidgetItem("No results found.")
            empty.setFlags(Qt.ItemFlag.ItemIsEnabled)  # non‑selectable label
            self.results.addItem(empty)
            return
        for file_obj in files:
            card = FileCard(file_obj)
            item = QListWidgetItem(listview=self.results)
            item.setSizeHint(card.sizeHint())
            self.results.setItemWidget(item, card)

    def _handle_open(self, item: QListWidgetItem):
        card = self.results.itemWidget(item)
        filepath = card.path
        if sys.platform == "darwin":  # macOS
            subprocess.call(("open", filepath))
        elif sys.platform == "win32":  # Windows
            os.startfile(filepath)
        else:  # linux variants
            subprocess.call(("xdg-open", filepath))
