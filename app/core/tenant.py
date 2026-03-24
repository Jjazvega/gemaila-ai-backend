from contextvars import ContextVar

from fastapi import Header

from app.core.config import settings


tenant_context: ContextVar[str] = ContextVar("tenant_id", default=settings.DEFAULT_TENANT_ID)


async def get_tenant_id(x_tenant_id: str | None = Header(default=None, alias="X-Tenant-Id")) -> str:
    tenant_id = (x_tenant_id or settings.DEFAULT_TENANT_ID).strip()
    token = tenant_context.set(tenant_id)
    try:
        return tenant_id
    finally:
        tenant_context.reset(token)
