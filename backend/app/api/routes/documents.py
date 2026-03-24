from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.dependencies.auth import require_current_user
from app.schemas.auth import AuthenticatedUser
from app.services.firestore_service import FirestoreService
from app.services.storage_service import FirebaseStorageService

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    project_id: str | None = Form(default=None),
    context_type: str | None = Form(default=None),
    user: AuthenticatedUser = Depends(require_current_user),
) -> dict[str, object]:
    storage_service = FirebaseStorageService()
    firestore_service = FirestoreService()

    upload_result = await storage_service.upload_document(
        user=user,
        upload=file,
        project_id=project_id,
        context_type=context_type,
    )
    record = firestore_service.create_document_record(
        user=user,
        filename=file.filename or "document",
        content_type=upload_result["content_type"],
        size_bytes=upload_result["size_bytes"],
        storage_path=upload_result["storage_path"],
        access_url=upload_result["signed_url"],
        project_id=project_id,
        context_type=context_type,
        metadata={"url_expires_at": upload_result["url_expires_at"]},
    )
    return {
        "message": "Document uploaded successfully",
        "document": record,
    }
