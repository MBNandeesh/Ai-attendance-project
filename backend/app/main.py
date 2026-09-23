from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    # Hide interactive docs in production to reduce surface area.
    show_docs = not settings.is_production()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        openapi_url="/api/v1/openapi.json" if show_docs else None,
        docs_url="/api/docs" if show_docs else None,
        redoc_url=None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/api/health")
    def health():
        return {"status": "ok", "environment": settings.environment}

    return app


app = create_app()
