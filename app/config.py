"""Application configuration using Pydantic Settings."""
import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Entrepreneur Mitra Backend"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    SECRET_KEY: str = "sih26092-dev-secret-key-for-local-evaluation"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = "sqlite:///./entrepreneur_mitra.db"
    SUPABASE_DATABASE_URL: str = ""
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    
    # Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]

    # AI & Service Mock Switches
    MOCK_AI: bool = True
    MOCK_VOICE: bool = True
    MOCK_OCR: bool = True
    
    # DigiLocker Requester Integration
    DIGILOCKER_CLIENT_ID: str = ""
    DIGILOCKER_CLIENT_SECRET: str = ""
    DIGILOCKER_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/documents/digilocker/callback"
    DIGILOCKER_ENVIRONMENT: str = "sandbox"  # 'sandbox' or 'production'
    DIGILOCKER_SCOPES: str = "read:income read:caste read:aadhaar"

    # AI Engine Settings
    LLM_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "llama3"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    BHASHINI_API_KEY: str = ""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()
