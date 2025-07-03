import logging
import shutil
from pathlib import Path

from watchdog.events import FileSystemEventHandler


class WatcherHandler(FileSystemEventHandler):
    def __init__(self, saveprocessor):
        super().__init__()
        self.saveprocessor = saveprocessor

    def on_created(self, event):
        self.handle_event(event)

    def on_modified(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        if event.is_directory:
            return
        try:
            file_path = Path(event.src_path).resolve()
            logging.info(f"Handle file: {file_path}")

            # Create the file object
            with open(file_path, "rb") as f:
                content = f.read()
            file_name = Path(file_path).name
            file = File(content, file_name, str(file_path))

            # Process the file using the saveprocessor
            new_path = (
                Path(path).resolve()
                if (path := self.saveprocessor.process_file(file))
                else None
            )

            # Move the file to the new folder if the path has changed
            if new_path is not None:
                shutil.move(file_path, new_path)
                logging.info(f"File moved to {new_path}")
        except Exception as e:
            logging.error(e)


class File:
    def __init__(self, bytes: bytes, basename: str, abs_path: str):
        self.content = bytes
        self.basename = basename
        self.path = abs_path
        ext = Path(basename).suffix
        self.extension = ext.lstrip(".") if ext else None
