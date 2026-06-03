from threading import Lock

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client

from app.core.config import settings


_firebase_lock = Lock()
_firebase_app: firebase_admin.App | None = None


def initialize_firebase() -> firebase_admin.App:
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    with _firebase_lock:
        if _firebase_app is not None:
            return _firebase_app

        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        _firebase_app = firebase_admin.initialize_app(
            cred,
            {"projectId": settings.FIREBASE_PROJECT_ID},
        )
    return _firebase_app


def get_firestore_client() -> Client:
    app = initialize_firebase()
    return firestore.client(app=app)
