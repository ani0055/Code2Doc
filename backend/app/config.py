from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str  
    
    class Config:
        env_file = ".env"
        case_sensitive = False 
        extra = "allow"  # Change from "forbid" to "allow" or remove this line

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()