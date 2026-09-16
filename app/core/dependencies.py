from typing import Annotated

from fastapi import Depends, Request, HTTPException, status

from app.core.config import settings, Settings
from app.core.db import get_db_session

from sqlalchemy.ext.asyncio import AsyncSession
def get_settings() -> Settings :
    return settings

def get_vector_store(request: Request):
    store = getattr(request.app.state, "vector_index", None)
    if store is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = "vector store not ready"
        )
    return store

def get_embedder(request: Request):
    embedder =getattr(request.app.state, "embedder", None)
    if embedder is None:
        raise HTTPException(503,"Embedding Model is not ready")
    return embedder


SettingDep = Annotated[Settings,Depends(get_settings)]
VectorDep = Annotated[object , Depends(get_vector_store)]
EmbedderDep = Annotated[object, Depends(get_embedder)]
DbSession = Annotated[AsyncSession,Depends(get_db_session)]