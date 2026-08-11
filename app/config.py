from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    BOT_TOKEN: str
    OPENAI_API_KEY: str = ""

    DATABASE_URL: str = "sqlite+aiosqlite:///./archon.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    OWNER_ID: int = 0
    LOGGER_GROUP_ID: int = 0

    MAINTENANCE: bool = False
    DEFAULT_LANGUAGE: str = "auto"


settings = Settings()
