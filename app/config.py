"""
Configuration module for the TODO FastAPI application.
Centralizes all configuration settings and environment variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Follows the Single Responsibility Principle by handling only configuration.
    """
    # Application settings
    app_name: str = "TODO FastAPI Application"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # Database settings
    database_url: str = "sqlite:///./tasks.db"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS settings - use string for simple parsing
    cors_origins: str = "*"
    
    # Monitoring settings
    enable_metrics: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    def get_cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list."""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses LRU cache to ensure settings are loaded only once.
    """
    return Settings()
