from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.db import init_models,dispose_engine
from app.api.routers import health,chat
from app.ml.embedding import preload_embedding_model

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.embedder = await preload_embedding_model()
    app.state.vector_index  = None
    await init_models()
    yield
    app.state.embedder = None
    app.state.vector_index  = None
    await dispose_engine()

def create_app() -> FastAPI :
    app = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
        lifespan=lifespan,
        version=settings.version
    )
    app.include_router(health.router)
    app.include_router(chat.router)
    return app 

app = create_app()

