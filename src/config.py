from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    debug: bool = Field(False, env="DEBUG")
    api_port: int = Field(8000, env="API_PORT")
    api_key: str = Field(..., env="API_KEY")
    folder_id: str = Field(..., env="FOLDER_ID")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
