from fastapi import APIRouter, Depends

from app.dependencies.auth import require_current_user
from app.schemas.auth import AuthenticatedUser

router = APIRouter(prefix="/api", tags=["auth"])


@router.get("/me")
def get_me(user: AuthenticatedUser = Depends(require_current_user)) -> dict[str, object]:
    return {
        "uid": user.uid,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
        "tenant_id": user.tenant_id,
        "role": user.role,
        "provider": user.provider,
    }
