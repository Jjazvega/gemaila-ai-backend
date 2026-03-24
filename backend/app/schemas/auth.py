from pydantic import BaseModel, Field


class AuthenticatedUser(BaseModel):
    uid: str
    email: str | None = None
    name: str | None = None
    picture: str | None = None
    tenant_id: str | None = None
    role: str | None = None
    provider: str | None = None
    claims: dict[str, object] = Field(default_factory=dict)
