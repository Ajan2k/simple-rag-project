from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.api.routers import health,chat


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.embedder = None
    app.state.vector_index  = None
    yield
    app.state.embedder = None
    app.state.vector_index  = None

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

