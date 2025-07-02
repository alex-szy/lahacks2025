from typing import List

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from commands.find import _find as r_find
from frontend.ui.widgets.file_card import FileCard
from frontend.utils.icons import icon
from engine.database import File


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

    def __init__(self, on_open):
        super().__init__()

        # ── Layout ────────────────────────────────────────────────────────────
        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(24)

        # ── Search bar ───────────────────────────────────────────────────────
        self.search_edit = QLineEdit(placeholderText="Search for a file …")
        self.search_edit.setFixedHeight(46)
        self.search_edit.setStyleSheet(
            """
            QLineEdit {
                background:#ffffff; color:#222;
                font-family:"Poppins",sans-serif; font-size:14px;
                border:1px solid #d4d4d4; border-radius:23px; padding-left:48px;
            }
            QLineEdit:focus { border-color:#7a74ff; }
            QLineEdit::placeholder { color:#999; }
            """
        )
        # leading magnifying‑glass icon
        mag = QLabel(self.search_edit)
        mag.setPixmap(icon("search", 24).pixmap(QSize(24, 24)))
        mag.move(16, 11)

        # Trigger search *only* when user presses Return/Enter
        self.search_edit.returnPressed.connect(self._handle_search)
        lay.addWidget(self.search_edit)

        # ── Results list ──────────────────────────────────────────────────────
        self.results = QListWidget(frameShape=QFrame.NoFrame, spacing=4)
        self.results.itemClicked.connect(on_open)
        self.results.setStyleSheet(
            """
            QListWidget { border:none; background:#fff; }
            QListWidget::item:selected{ background:#ebf0ff; border-radius:6px; }
            """
        )
        lay.addWidget(self.results)

    # ── Internal helpers ─────────────────────────────────────────────────────
    def _handle_search(self):
        """Invoke external search callback and render its results."""
        query = self.search_edit.text().strip()
        if not query:
            self._show_no_results()
            return

        try:
            matches: list[File] | None = r_find(query)
        except Exception as exc:  # defensive: don’t crash the UI
            print(f"search error: {exc}")
            matches = None

        self._render_results(matches or [])

    def _render_results(self, files: List[File]):
        """Populate the QListWidget with FileCard widgets."""
        self.results.clear()
        files = list(files or [])
        if not files:
            self._show_no_results()
            return
        for file_obj in files:
            card = FileCard(file_obj)
            item = QListWidgetItem()
            item.setSizeHint(card.sizeHint())
            self.results.addItem(item)
            self.results.setItemWidget(item, card)

    def _show_no_results(self):
        """Display a static list item indicating zero matches."""
        self.results.clear()
        empty = QListWidgetItem("No results found.")
        empty.setFlags(Qt.ItemIsEnabled)  # non‑selectable label
        self.results.addItem(empty)
