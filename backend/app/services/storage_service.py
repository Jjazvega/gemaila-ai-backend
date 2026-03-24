from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.exceptions import StorageError
from app.core.firebase import get_storage_bucket
from app.core.logging import get_logger
from app.schemas.auth import AuthenticatedUser

logger = get_logger(__name__)


class FirebaseStorageService:
    def __init__(self) -> None:
        self.bucket = get_storage_bucket()

    async def upload_document(self, *, user: AuthenticatedUser, upload: UploadFile, project_id: str | None, context_type: str | None) -> dict[str, object]:
        extension = Path(upload.filename or "document").suffix
        safe_name = f"{uuid4()}{extension}"
        tenant_prefix = user.tenant_id or "public"
        path = f"documents/{tenant_prefix}/{user.uid}/{project_id or 'general'}/{safe_name}"
        blob = self.bucket.blob(path)

        try:
            content = await upload.read()
            blob.cache_control = "private, max-age=0, no-transform"
            blob.upload_from_string(content, content_type=upload.content_type)
            expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
            signed_url = blob.generate_signed_url(version="v4", expiration=expires_at, method="GET")
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "Failed to upload document to Firebase Storage",
                extra={"event": "firebase_storage_upload_failed", "context": {"uid": user.uid, "filename": upload.filename}},
            )
            raise StorageError("Unable to upload document to Firebase Storage") from exc

        logger.info(
            "Document uploaded to Firebase Storage",
            extra={"event": "firebase_storage_uploaded", "context": {"uid": user.uid, "storage_path": path}},
        )
        return {
            "storage_path": path,
            "signed_url": signed_url,
            "url_expires_at": expires_at.isoformat(),
            "size_bytes": len(content),
            "content_type": upload.content_type,
            "context_type": context_type,
        }
