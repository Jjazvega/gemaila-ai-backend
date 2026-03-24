from datetime import datetime, timezone
from uuid import uuid4

from app.core.config import get_settings
from app.core.exceptions import PersistenceError
from app.core.firebase import get_firestore_client
from app.core.logging import get_logger
from app.schemas.auth import AuthenticatedUser

logger = get_logger(__name__)


class FirestoreService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = get_firestore_client()

    def upsert_user_profile(self, user: AuthenticatedUser) -> dict[str, object]:
        payload = {
            "uid": user.uid,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
            "tenant_id": user.tenant_id,
            "role": user.role,
            "provider": user.provider,
            "last_login_at": datetime.now(timezone.utc),
        }
        try:
            ref = self.client.collection(self.settings.firestore_users_collection).document(user.uid)
            ref.set(payload, merge=True)
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "Failed to upsert Firestore user profile",
                extra={"event": "firestore_user_upsert_failed", "context": {"uid": user.uid}},
            )
            raise PersistenceError("Unable to persist authenticated user profile") from exc

        logger.info(
            "Firestore user profile synced",
            extra={"event": "firestore_user_upserted", "context": {"uid": user.uid}},
        )
        return {"id": ref.id, **payload}

    def create_document_record(self, *, user: AuthenticatedUser, filename: str, content_type: str | None, size_bytes: int, storage_path: str, access_url: str, project_id: str | None, context_type: str | None, metadata: dict[str, object] | None = None) -> dict[str, object]:
        record_id = str(uuid4())
        created_at = datetime.now(timezone.utc)
        payload = {
            "owner_uid": user.uid,
            "tenant_id": user.tenant_id,
            "project_id": project_id,
            "context_type": context_type,
            "filename": filename,
            "content_type": content_type,
            "size_bytes": size_bytes,
            "storage_path": storage_path,
            "access_url": access_url,
            "created_at": created_at,
            "metadata": metadata or {},
        }
        try:
            self.client.collection(self.settings.firestore_documents_collection).document(record_id).set(payload)
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "Failed to persist document metadata in Firestore",
                extra={"event": "firestore_document_create_failed", "context": {"uid": user.uid, "record_id": record_id}},
            )
            raise PersistenceError("Unable to persist document metadata") from exc

        logger.info(
            "Firestore document metadata stored",
            extra={"event": "firestore_document_created", "context": {"uid": user.uid, "record_id": record_id}},
        )
        return {"id": record_id, **payload}
