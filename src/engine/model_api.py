import requests

from settings import settings


class ModelAPI:
    def __init__(self, model_name: str, temperature: float = 0.0):
        self.model_name = model_name  # e.g., "gemini-2.0-flash"
        self.temperature = temperature
        self.api_key = settings.get_gemini_api_key()
        self.endpoint_base = "https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    def call(self, system_prompt: str) -> str:
        url = (
            self.endpoint_base.format(model_name=self.model_name)
            + f"?key={self.api_key}"
        )
        headers = {
            "Content-Type": "application/json",
        }
        body = {
            "contents": [{"role": "user", "parts": [{"text": system_prompt}]}],
            "generationConfig": {
                "temperature": self.temperature,
                "topK": 40,
                "topP": 0.95,
            },
        }
        response = requests.post(url, headers=headers, json=body)
        if response.status_code != 200:
            raise RuntimeError(f"API call failed: {response.text}")

        result = response.json()
        try:
            text_response = result["candidates"][0]["content"]["parts"][0]["text"]
            return text_response
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected API response format: {result}") from e
