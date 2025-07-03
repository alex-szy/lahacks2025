from pathlib import Path

from engine.model_api import ModelAPI
from engine.prompt_builder import (
    build_classification_prompt,
    build_summarization_prompt,
)
from settings import settings


class Summarizer:
    def __init__(self):
        self.summarization_model = ModelAPI(
            model_name="gemini-2.0-flash", temperature=0.3
        )

    def summarize(self, contents: str):
        prompt = build_summarization_prompt(contents)
        summary = self.summarization_model.call(prompt)
        return summary.strip()


class Classifier:
    def __init__(self):
        self.classification_model = ModelAPI(
            model_name="gemini-2.0-flash", temperature=0.0
        )

    def classify(self, file_name: str, summary: str) -> str | None:
        """
        Choose a destination folder to put the file in, or return none if none of them are suitable.
        The path returned is guaranteed to exist in the system.
        """
        folder_paths = settings.get_folder_paths()

        classification_response = self._classify_file(summary, file_name, folder_paths)

        validated_path = self._validate_response(classification_response, folder_paths)

        return validated_path

    def _classify_file(
        self, summary: str, file_name: str, folder_paths: dict[str, str]
    ) -> str:
        classification_prompt = build_classification_prompt(
            summary, file_name, folder_paths
        )
        # logging.info(f"classification prompt is: {classification_prompt}")
        response = self.classification_model.call(classification_prompt)
        # logging.info(f"Classification is: {response}")
        return response

    def _validate_response(
        self, response: str, folder_paths: dict[str, str]
    ) -> str | None:
        response = response.strip()
        if response in folder_paths and Path(response).exists():
            return response
        return None
