from collections.abc import AsyncGenerator
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine,
)

from app.core.config import settings
from app.models.chat_log import Base

engine : AsyncEngine = create_async_engine(
    str(settings.postgres_uri),
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=300,
)

async_session_factory : async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except:
                 await session.rollback()
                 raise


type session_type = AsyncGenerator[AsyncSession,None]

async def init_models():
     async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)


async def check_db_health() -> bool : 
     async with engine.connect() as conn:
        try:  
                await conn.execute(text("SELECT 1"))
                return True
        except Exception:
                return False

async def dispose_engine() -> None :
      await engine.dispose()