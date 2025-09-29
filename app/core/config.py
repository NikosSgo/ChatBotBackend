from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    name: str = Field(default="app_db")
    user: str = Field(default="postgres")
    password: str = Field(default="password")
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=25)
    echo: bool = Field(default=False)
    echo_pool: bool = Field(default=False)

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="API_")

    bearer_token_url: str = Field(default="auth/login")
    title: str = Field(default="My FastAPI App")
    version: str = Field(default="1.0.0")
    description: str = Field(default="FastAPI application")
    debug: bool = Field(default=False)
    allowed_hosts: List[str] = Field(default=["*"])


class GPTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GPT_")

    folder_id: str = Field(default="")
    api_key: str = Field(default="")


class AccessTokenSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ACCESS_TOKEN_")

    lifetime_seconds: int = Field(default=3600)
    reset_password_token_secret: str = Field(default="")
    verification_token_secret: str = Field(default="")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    db: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()
    gpt: GPTSettings = GPTSettings()
    access_token: AccessTokenSettings = AccessTokenSettings()
    environment: str = Field(default="development")
    secret_key: str = Field(default="your-secret-key-here")


settings = Settings()
