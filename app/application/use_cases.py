from app.infrastructure.user_repository import UserRepository


class AuthUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def me(self, uid: str, email: str, tenant_id: str):
        user = await self.user_repository.upsert(uid=uid, email=email, tenant_id=tenant_id)
        return user
