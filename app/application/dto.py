from pydantic import BaseModel, EmailStr


class MeResponse(BaseModel):
    uid: str
    email: EmailStr
    tenant_id: str
