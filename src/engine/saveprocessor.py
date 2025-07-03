from typing import Optional

from engine.classifier import Classifier, Summarizer
from engine.db.database import VectorDatabase
from engine.watcher import File
from engine.preprocessor import Preprocessor


class SaveProcessor:
    def __init__(
        self,
        db: VectorDatabase,
        token_threshold: Optional[int] = None,
    ) -> None:
        self.classifier = Classifier()
        self.summarizer = Summarizer()
        self.db = db
        self.preprocessor = Preprocessor(token_threshold)

    def process_file(self, file: File) -> str | None:
        # Preprocess the file into a string
        contents = self.preprocessor.preprocess(file)

        # Summarize its content
        summary = self.summarizer.summarize(contents)

        # Save embedding + new file path into database
        self.db.create_entry(file, summary)

        # Classify file to determine target folder
        # TODO: run in parallel with storing the embedding, possibly using multiprocessing
        return self.classifier.classify(file.basename, summary)
