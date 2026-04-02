from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./agenda.db"
    
    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    
    # App
    app_name: str = "Assistente Intelligente API"
    debug: bool = False
    cors_origins: str = "http://localhost:4200,https://agenda-angular-livid.vercel.app"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
