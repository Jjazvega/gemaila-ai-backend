from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    uid: str
    email: str
    tenant_id: str
    created_at: datetime | None = None
