from datetime import datetime, UTC
from enum import StrEnum
from typing import Literal, Annotated
from uuid import UUID , uuid4

from pydantic import BaseModel, Field, ConfigDict


type ChunkId = str
type Score = Annotated[float,Field(ge=0.0, le=1.0)]
type Topk = Annotated[int, Field(ge=1, le=20)]
type QueryText = Annotated[str, Field(min_length=1,max_length=4_000)]
type MessageText = Annotated[str, Field(min_length=1, max_length=8_000)]


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Base(BaseModel):

    model_config = ConfigDict(
        extra = "forbid",
        frozen = True,
        str_strip_whitespace = True,
        validate_assignment = True,
    )

class Message(Base):
    role : Role
    content : MessageText

class ChatRequest(Base):
    query: QueryText
    conversation_id: UUID | None = None
    top_k : Topk = 4
    stream : bool = True

class SourceChunk(Base):
    chunk_id : ChunkId 
    text : str
    score : Score
    metadata : dict[str, str] = Field(default_factory=dict)

class ChatResponse(Base):
    conversation_id : UUID = Field(default_factory=uuid4)
    answer : str
    sources : list[SourceChunk] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class TokenFrame(Base):
    type: Literal["token"] = "token"
    delta: str

class SourcesFrame(Base):
    type: Literal["sources"] = "sources"
    sources: list[SourceChunk]

class DoneFrame(Base):
    type: Literal["done"] = "done"
    conversation_id: UUID

class ErrorFrame(Base):
    type: Literal["error"] = "error"
    detail: str

type StreamFrame = Annotated[
    TokenFrame | SourcesFrame | DoneFrame | ErrorFrame,
    Field(discriminator="type")
]