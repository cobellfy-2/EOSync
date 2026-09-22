"""EOSync - FastAPI Entry Point.

Starten:  uvicorn backend.app.main:app --reload
Docs:     http://localhost:8000/docs
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import search
from backend.app.config import get_settings

settings = get_settings()
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)-8s %(name)s | %(message)s",
)
logger = logging.getLogger("eosync")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/Shutdown - hier gehoeren geteilte Ressourcen hin.

    TODO (Phase 1): Einen einzigen httpx.AsyncClient anlegen und in
    app.state.http ablegen. Ein Client pro Request ist ein klassischer
    Performance-Fehler: du verlierst Connection-Pooling und Keep-Alive.

    TODO (Phase 3): Cache-Backend verbinden (core/cache.py) und beim
    Shutdown sauber schliessen.
    """
    logger.info("EOSync startet (env=%s)", settings.app_env)
    yield
    logger.info("EOSync faehrt herunter")


app = FastAPI(
    title="EOSync",
    description="Aggregiert biomedizinische Datenquellen zu einem Gen in einem Request.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/v1")


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Liveness-Probe. Haelt Docker/Railway am Leben."""
    return {"status": "ok", "version": app.version}
