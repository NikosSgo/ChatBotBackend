from app.core.config import settings
from yandex_cloud_ml_sdk import YCloudML
import asyncio


MODEL_NAME = "yandexgpt-lite"
MODEL_VERSION = "rc"


class YandexAgent:
    def __init__(self) -> None:
        self.settings = settings
        self.sdk = YCloudML(
            folder_id=self.settings.gpt.folder_id, auth=self.settings.gpt.api_key
        )
        self.model = self.sdk.models.completions(
            MODEL_NAME, model_version=MODEL_VERSION
        )
        self.thread = None

    def __get_thread(self):
        if self.thread is None:
            self.thread = self.sdk.threads.create(
                ttl_days=1, expiration_policy="static"
            )
        return self.thread

    def __call__(self, message: str):
        response = self.model.run(message)
        assistant_response = response.text
        return assistant_response

    async def async_call(self, message: str):
        """Асинхронная версия вызова нейросети"""
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self.model.run, message)
        return response.text
