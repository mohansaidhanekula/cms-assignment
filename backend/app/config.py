from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://cms_user:cms_password@db:5432/cms_db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    WORKER_INTERVAL: int = int(os.getenv("WORKER_INTERVAL", "60"))
    
    class Config:
        env_file = ".env"

settings = Settings()
