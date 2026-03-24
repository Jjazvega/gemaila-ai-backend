from datetime import datetime, timezone

from google.cloud.firestore import Client

from app.domain.user import User


class UserRepository:
    def __init__(self, db: Client):
        self.db = db

    async def upsert(self, uid: str, email: str, tenant_id: str) -> User:
        doc_ref = self.db.collection("users").document(uid)
        now = datetime.now(timezone.utc)

        current = doc_ref.get()
        if not current.exists:
            payload = {
                "uid": uid,
                "email": email,
                "tenant_id": tenant_id,
                "created_at": now,
                "updated_at": now,
            }
            doc_ref.set(payload)
            return User(uid=uid, email=email, tenant_id=tenant_id, created_at=now)

        doc_ref.set({"email": email, "tenant_id": tenant_id, "updated_at": now}, merge=True)
        current_data = current.to_dict() or {}
        return User(
            uid=uid,
            email=email,
            tenant_id=tenant_id,
            created_at=current_data.get("created_at"),
        )

    async def get_by_uid(self, uid: str) -> User | None:
        doc = self.db.collection("users").document(uid).get()
        if not doc.exists:
            return None
        data = doc.to_dict() or {}
        return User(
            uid=data.get("uid", uid),
            email=data.get("email", ""),
            tenant_id=data.get("tenant_id", ""),
            created_at=data.get("created_at"),
        )
