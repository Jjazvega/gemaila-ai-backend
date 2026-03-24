import json
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore, storage

from app.core.config import get_settings


@lru_cache
def get_firebase_app() -> firebase_admin.App:
    settings = get_settings()

    if settings.firebase_service_account_json:
        certificate = credentials.Certificate(json.loads(settings.firebase_service_account_json))
    elif settings.firebase_service_account_path:
        certificate = credentials.Certificate(settings.firebase_service_account_path)
    else:
        certificate = credentials.ApplicationDefault()

    return firebase_admin.initialize_app(
        certificate,
        {
            "projectId": settings.firebase_project_id,
            "storageBucket": settings.firebase_storage_bucket,
        },
    )


@lru_cache
def get_firestore_client() -> firestore.Client:
    app = get_firebase_app()
    return firestore.client(app=app)


@lru_cache
def get_storage_bucket():
    app = get_firebase_app()
    return storage.bucket(app=app)
