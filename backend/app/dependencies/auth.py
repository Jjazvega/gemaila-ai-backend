from fastapi import Depends, Header, HTTPException, status

from app.core.exceptions import AppError
from app.core.logging import get_logger
from app.schemas.auth import AuthenticatedUser
from app.services.firebase_auth_service import FirebaseAuthService
from app.services.firestore_service import FirestoreService

logger = get_logger(__name__)


def get_current_user(authorization: str | None = Header(default=None)) -> AuthenticatedUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Empty Bearer token")

    try:
        auth_service = FirebaseAuthService()
        firestore_service = FirestoreService()
        user = auth_service.verify_id_token(token)
        firestore_service.upsert_user_profile(user)
        return user
    except AppError:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception(
            "Unhandled authentication dependency failure",
            extra={"event": "auth_dependency_failure", "context": {}},
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token") from exc


def require_current_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    return user
