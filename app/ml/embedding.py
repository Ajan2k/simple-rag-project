import asyncio
from typing import Sequence

from sentence_transformers import SentenceTransformer

from app.core.config import settings


_model : SentenceTransformer | None = None

def get_embedding_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )
    return _model

async def preload_embedding_model() -> SentenceTransformer :
    return await asyncio.to_thread(get_embedding_model)

async def encode_text(texts:Sequence[str]) -> list[list[float]]:
    model = get_embedding_model()
    result =await asyncio.to_thread(
        model.encode,
        list(texts),
        normalize_embeddings=True,
        convert_to_numpy=True,
        batch_size=32,
        show_progress_bar=False,
    )
    return result.astype(float).tolist()

async def encode_prompt(prompt:str) ->  list[float]:
    vectors =await encode_text(prompt)
    return vectors[0] if vectors else []