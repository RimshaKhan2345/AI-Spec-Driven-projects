
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: Optional[str] = "postgresql://neondb_owner:npg_P46QVlmBqxDj@ep-wispy-fire-ahgr18i5-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    # Authentication settings
    SECRET_KEY: str = "napi_3ggx0n6twt43yz9km4dphptemhrgvbp25d100cc807fnajmnf1pi6vl1rr7u5nzt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Better Auth settings
    BETTER_AUTH_SECRET: Optional[str] = None
    DATABASE_URL_BETTER_AUTH: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()