import logging
from pathlib import Path
from typing import Optional

from classifier.model_api import ModelAPI
from classifier.prompt_builder import (
    build_classification_prompt,
    build_summarization_prompt,
    prepare_folder_info,
)
from models.file import File
from settings import settings
from utilities.preprocessor import Preprocessor


class Classifier:
    def __init__(self, token_threshold: int = None):
        self.preprocessor = Preprocessor(token_threshold)
        self.summarization_model = ModelAPI(
            model_name="gemini-2.0-flash", temperature=0.3
        )
        self.classification_model = ModelAPI(
            model_name="gemini-2.0-flash", temperature=0.0
        )

    def classify(self, file: File) -> Optional[str]:
        """
        Choose a destination folder to put the file in, or return none if none of them are suitable.
        The path returned is guaranteed to exist in the system.
        """
        file_content = self.preprocessor.preprocess(file)
        file_name = file.name

        summary = self._summarize_content(file_content, file_name)

        file.add_summary(summary)

        folder_paths, folder_descriptions = prepare_folder_info(
            settings.get_folder_paths().items()
        )

        classification_response = self._classify_file(
            summary, file_name, folder_paths, folder_descriptions
        )

        validated_path = self._validate_response(classification_response, folder_paths)

        return validated_path

    def _summarize_content(self, content: str, file_name: str) -> str:
        prompt = build_summarization_prompt(content, file_name)
        summary = self.summarization_model.call(prompt)
        return summary.strip()

    def _classify_file(
        self,
        summary: str,
        file_name: str,
        folder_paths: list[str],
        folder_descriptions: list[str],
    ) -> str:
        classification_prompt = build_classification_prompt(
            summary, file_name, folder_paths, folder_descriptions
        )
        logging.info(f"classification prompt is: {classification_prompt}")
        response = self.classification_model.call(classification_prompt)
        logging.info(f"Classification is: {response}")
        return response

    def _validate_response(
        self, response: str, folder_paths: list[str]
    ) -> Optional[str]:
        response = response.strip()
        if response in folder_paths and Path(response).exists():
            return response
        return None
