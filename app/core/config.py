from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Simple-Ufro"
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        case_sensitive = True

settings = Settings()
