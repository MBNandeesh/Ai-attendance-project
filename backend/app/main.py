from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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

    if settings.allow_localhost_origins:
        # Dev mode: allow any localhost/127.0.0.1 port (dev servers drift ports).
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
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

    @app.get("/api/health/db")
    def health_db():
        from sqlalchemy import text

        from app.db.session import engine

        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return {"status": "ok", "database": "reachable"}
        except Exception as exc:
            return JSONResponse(
                status_code=503,
                content={"status": "degraded", "database": str(exc)},
            )

    return app


app = create_app()
