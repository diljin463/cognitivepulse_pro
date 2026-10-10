from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CognitivePulse Pro"
    # Local SQLite database path using asynchronous driver (aiosqlite)
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/cognitivepulse.db"

settings = Settings()