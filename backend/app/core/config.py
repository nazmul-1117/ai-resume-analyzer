from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

class Settings(BaseSettings):

    API_VERSION: str
    API_PREFIX: str

    API_KEY: str
    AI_MODEL: str
    BASE_URL: str

    model_config = SettingsConfigDict(
        title="setting config dict",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()