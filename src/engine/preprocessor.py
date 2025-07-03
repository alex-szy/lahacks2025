import logging
from io import BytesIO
from typing import Optional

import fitz  # PyMuPDF for PDF extraction
from docx import Document

from engine.watcher import File

SUPPORTED_TEXT_EXTENSIONS = [
    "txt",
    "md",
    "json",
    "csv",
    "tsv",
    "yaml",
    "yml",
    "ini",
    "xml",
    "html",
    "py",
    "java",
    "js",
    "cpp",
    "c",
    "h",
    "sh",
    "pdf",
    "docx",
]


class Preprocessor:
    def __init__(self, token_threshold: Optional[int] = None):
        self.token_threshold = token_threshold

    def preprocess(self, file: File) -> str:
        content = self._read_content(file)
        content = self._apply_preprocessing(content)
        return content

    def _read_content(self, file: File) -> str:
        if file.extension is None:
            raise ValueError("Cannot determine file type without extension.")

        ext = file.extension.lower()

        if ext == "pdf":
            return self._extract_text_from_pdf_bytes(file.content)

        if ext == "docx":
            return self._extract_text_from_docx_bytes(file.content)

        if ext in SUPPORTED_TEXT_EXTENSIONS:
            try:
                return file.content.decode("utf-8")
            except UnicodeDecodeError:
                logging.error(
                    f"[Warning] Failed to decode '{file.basename}' as UTF-8. Returning empty string."
                )
                return ""

        raise ValueError(f"Unsupported file extension: {file.extension}")

    def _extract_text_from_pdf_bytes(self, content: bytes) -> str:
        try:
            doc = fitz.open(stream=BytesIO(content), filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        except Exception as e:
            logging.error(f"[Warning] Failed to extract text from PDF: {str(e)}")
            return ""

    def _extract_text_from_docx_bytes(self, content: bytes) -> str:
        try:
            doc = Document(BytesIO(content))
            text = "\n".join(para.text for para in doc.paragraphs)
            return text
        except Exception as e:
            logging.error(f"[Warning] Failed to extract text from DOCX: {str(e)}")
            return ""

    def _apply_preprocessing(self, content: str) -> str:
        content = content.strip()
        content = " ".join(content.split())  # Normalize whitespace
        if self.token_threshold:
            content = self._truncate_content(content)
        return content

    def _truncate_content(self, content: str) -> str:
        # Simple truncation by character count for now
        return content[: self.token_threshold]
