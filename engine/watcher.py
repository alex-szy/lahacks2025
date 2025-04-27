import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from settings import MONGO_URI


class WatcherHandler(FileSystemEventHandler):
    def __init__(self):
        from db.database import VectorDatabase
        from engine.saveprocessor import SaveProcessor
        from engine.encoder import Encoder
        from classifier.classifier import Classifier
        super().__init__()
        self.db = VectorDatabase(MONGO_URI)
        self.saveprocessor = SaveProcessor(
            encoder=Encoder(), classifier=Classifier(), db=self.db)

    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
            path = self.saveprocessor.process_file("path_to_file")
            logging.info(f"File moved to {path}")
