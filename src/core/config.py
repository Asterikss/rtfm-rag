from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  PROJECT_NAME: str = "RTFM RAG"
  API_VERSION: str = "0.1.0"
  API_V1_STR: str = "/api/v1"

  SERVER_HOST: str = "0.0.0.0"
  SERVER_PORT: int = 8032
  SERVER_DEBUG_MODE: bool = False

  LOG_LEVEL: str = "INFO"
  LOG_FILE: str | None = None
  LOG_FORMAT: str = "console"  # "json" or "console"

  model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
