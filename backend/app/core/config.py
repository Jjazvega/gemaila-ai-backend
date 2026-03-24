from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Gemailla Backend"
    app_env: str = "development"
    firebase_project_id: str = Field(..., alias="FIREBASE_PROJECT_ID")
    firebase_storage_bucket: str = Field(..., alias="FIREBASE_STORAGE_BUCKET")
    firebase_service_account_path: str | None = Field(default=None, alias="FIREBASE_SERVICE_ACCOUNT_PATH")
    firebase_service_account_json: str | None = Field(default=None, alias="FIREBASE_SERVICE_ACCOUNT_JSON")
    firestore_documents_collection: str = Field(default="documents", alias="FIRESTORE_DOCUMENTS_COLLECTION")
    firestore_users_collection: str = Field(default="users", alias="FIRESTORE_USERS_COLLECTION")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
