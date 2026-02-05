
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: Optional[str] = "paste neon db string key"
    
    # Authentication settings
    SECRET_KEY: str = "paste your secret key here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Better Auth settings
    BETTER_AUTH_SECRET: Optional[str] = None
    DATABASE_URL_BETTER_AUTH: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()
