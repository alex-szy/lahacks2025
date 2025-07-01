from typing import Optional
import os


class File:
    def __init__(self, content: bytes, name: str, summary: Optional[str] = None, extension: Optional[str] = None,
                 path: Optional[str] = None, size_bytes: Optional[int] = None,
                 created_at: Optional[str] = None, modified_at: Optional[str] = None):
        if not name:
            raise ValueError("File name must not be empty.")

        self.content = content
        self.name = name
        self.extension = extension or self._infer_extension()
        self.path = path
        self.size_bytes = size_bytes
        self.created_at = created_at
        self.modified_at = modified_at
        self.summary = summary

    def add_summary(self, summary: str) -> None:
        self.summary = summary

    def _infer_extension(self) -> Optional[str]:
        _, ext = os.path.splitext(self.name)
        return ext.lstrip('.') if ext else None

    def __repr__(self):
        return f"File(name={self.name}, summary={self.summary}, extension={self.extension})"
