from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./agenda.db"
    
    # Fix Render PostgreSQL SSL
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.database_url and 'render.com' in self.database_url:
            if '?' in self.database_url:
                if 'sslmode' not in self.database_url:
                    self.database_url += '&sslmode=require'
            else:
                self.database_url += '?sslmode=require'
            # Fix postgres:// -> postgresql://
            if self.database_url.startswith('postgres://'):
                self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
    
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
