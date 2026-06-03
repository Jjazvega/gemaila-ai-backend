from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto import MeResponse
from app.application.use_cases import AuthUseCases
from app.core.firebase import get_firestore_client
from app.core.security import verify_firebase_token
from app.core.tenant import get_tenant_id
from app.infrastructure.user_repository import UserRepository


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=MeResponse)
async def me(
    token_payload: dict = Depends(verify_firebase_token),
    tenant_id: str = Depends(get_tenant_id),
) -> MeResponse:
    uid = token_payload.get("uid")
    email = token_payload.get("email")

    if not uid or not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing required claims")

    effective_tenant_id = str(token_payload.get("tenant_id") or tenant_id)

    use_cases = AuthUseCases(UserRepository(get_firestore_client()))
    user = await use_cases.me(uid=uid, email=email, tenant_id=effective_tenant_id)
    return MeResponse(uid=user.uid, email=user.email, tenant_id=user.tenant_id)
