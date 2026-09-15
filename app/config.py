from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Cycle Timer App"
    database_url: str = "sqlite:///cycle_timer.db"

    class Config:
        env_file = ".env"

settings = Settings()