from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class DocumentRecord(BaseModel):
    id: str
    owner_uid: str
    tenant_id: str | None = None
    project_id: str | None = None
    context_type: str | None = None
    filename: str
    content_type: str | None = None
    size_bytes: int
    storage_path: str
    access_url: HttpUrl
    created_at: datetime
    metadata: dict[str, object] = Field(default_factory=dict)
