import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database - must be provided via environment
    database_url: str = ""
    
    # Use SQLite if no DATABASE_URL provided
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.database_url:
            self.database_url = "sqlite:///./agenda.db"
            print("⚠️ No DATABASE_URL - using SQLite")
        elif self.database_url.startswith('postgres://'):
            self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
    
    # Ollama
    ollama_host: str = ""
    ollama_model: str = "llama3.2"
    
    # App
    app_name: str = "Assistente Intelligente API"
    debug: bool = False
    cors_origins: str = "http://localhost:4200,https://agenda-angular-livid.vercel.app"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()
