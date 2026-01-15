from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "University Intranet API"
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        case_sensitive = True

settings = Settings()
