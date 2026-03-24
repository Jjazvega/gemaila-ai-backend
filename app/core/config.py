from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Auth Base"
    ENVIRONMENT: str = "DEV"
    DEBUG: bool = True

    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_CREDENTIALS_PATH: str = "./serviceAccountKey.json"

    DEFAULT_TENANT_ID: str = "public"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        upper_value = value.upper()
        if upper_value not in {"DEV", "PROD"}:
            raise ValueError("ENVIRONMENT must be DEV or PROD")
        return upper_value


settings = Settings()
