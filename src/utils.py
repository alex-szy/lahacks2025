import os


def is_forbidden(path: str):
    return not os.access(path, os.R_OK | os.W_OK)


SUPPORTED_TEXT_EXTENSIONS = [
    ".txt",
    ".md",
    ".json",
    ".csv",
    ".tsv",
    ".yaml",
    ".yml",
    ".ini",
    ".xml",
    ".html",
    ".py",
    ".java",
    ".js",
    ".cpp",
    ".c",
    ".h",
    ".sh",
    ".pdf",
    ".docx",
]
