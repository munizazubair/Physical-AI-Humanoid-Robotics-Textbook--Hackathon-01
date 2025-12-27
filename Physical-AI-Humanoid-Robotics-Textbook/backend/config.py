"""
Configuration Management

This module handles loading and validating environment variables using
Pydantic Settings for type safety and validation.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are validated using Pydantic for type safety.
    Missing required variables will raise a validation error.
    """

    # Google Gemini API Configuration
    gemini_api_key: str

    # Qdrant Vector Database Configuration
    qdrant_url: str
    qdrant_api_key: str

    # Neon PostgreSQL Database Configuration
    database_url: str

    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:8000"

    # Application Configuration
    environment: str = "development"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS origins from comma-separated string to list.

        Returns:
            List[str]: List of allowed CORS origins
        """
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        """
        Check if running in development mode.

        Returns:
            bool: True if environment is development
        """
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """
        Check if running in production mode.

        Returns:
            bool: True if environment is production
        """
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()
