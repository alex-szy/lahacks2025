from typing import Optional


class File:
    def __init__(
        self,
        name: str,
        path: str,
        summary: Optional[str] = None,
        extension: Optional[str] = None,
        size_bytes: Optional[int] = None,
        created_at: Optional[str] = None,
        modified_at: Optional[str] = None,
    ):
        if not name:
            raise ValueError("File name must not be empty.")

        self.name = name
        self.path = path
        self.extension = extension
        self.size_bytes = size_bytes
        self.created_at = created_at
        self.modified_at = modified_at
        self.summary = summary

    def __repr__(self):
        return f"File(name={self.name}, summary={self.summary}, extension={self.extension})"
