import logging

from watchdog.events import FileSystemEventHandler

from settings import MONGO_URI


class WatcherHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        from engine.classifier import Classifier
        from engine.database import VectorDatabase
        from engine.encoder import Encoder
        from engine.saveprocessor import SaveProcessor

        logging.info("Importing dependencies for watcher handler finished")
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
