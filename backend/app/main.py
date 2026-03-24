from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.documents import router as documents_router
from app.api.routes.health import router as health_router
from app.api.routes.me import router as me_router
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)
settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.exception_handler(AppError)
async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
    logger.warning(
        "Handled application error",
        extra={"event": "app_error", "context": {"code": exc.code, "status_code": exc.status_code}},
    )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message, "code": exc.code})


@app.exception_handler(Exception)
async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled server error",
        extra={"event": "unhandled_exception", "context": {}},
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "code": "internal_error"})


app.include_router(health_router)
app.include_router(me_router)
app.include_router(documents_router)
