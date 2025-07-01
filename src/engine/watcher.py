import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from settings import MONGO_URI


class WatcherHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        from db.database import VectorDatabase
        from engine.saveprocessor import SaveProcessor
        from engine.encoder import Encoder
        from classifier.classifier import Classifier

        logging.info(f"Importing dependencies for watcher handler finished")
        try:
            self.db = VectorDatabase(MONGO_URI)
            self.saveprocessor = SaveProcessor(
                encoder=Encoder(), classifier=Classifier(), db=self.db
            )
        except Exception as e:
            logging.error(e)

    def on_created(self, event):
        try:
            if not event.is_directory:
                logging.info(f"File created: {event.src_path}")
                path = self.saveprocessor.process_file(str(event.src_path))
                logging.info(f"File moved to {path}")
        except Exception as e:
            logging.error(e)

    def on_modified(self, event):
        return self.on_created(event)
