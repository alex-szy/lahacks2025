import os


def is_forbidden(path: str):
    return not os.access(path, os.R_OK | os.W_OK)
