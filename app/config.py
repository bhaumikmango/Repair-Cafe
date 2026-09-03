from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central place for all config. Reads from environment variables / .env file.
    Add new settings here as the app grows instead of scattering os.getenv() calls.
    """

    database_url: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Import `settings` anywhere you need config, e.g. `from app.config import settings`
settings = Settings()
