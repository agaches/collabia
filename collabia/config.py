from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    gcp_project_id: str
    gcp_region: str = "us-central1"
    gemini_model: str = "gemini-2.5-pro"
    gemini_flash_model: str = "gemini-2.5-flash"
    gemini_lite_model: str = "gemini-3.1-flash-lite-preview"
    max_rounds: int = 5


settings = Settings()
