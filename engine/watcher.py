import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"Created: {event.src_path}")
            # TODO: call the processor with the file path
