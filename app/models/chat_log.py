from datetime import datetime,UTC
from typing import Any
from enum import StrEnum
from uuid import UUID,uuid4

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SAEnum,
    Identity,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB,UUID as PG_UUID
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase

class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str,Any]: JSONB,
        list[dict[str,Any]]: JSONB,
        datetime : DateTime(timezone=True),
        UUID : PG_UUID(as_uuid=True)
    }

class TurnStatus(StrEnum):
    OK = "ok"
    ERROR =  "error"
    TIMEOUT = "timeout"

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id:Mapped[int] = mapped_column(BigInteger,Identity(),primary_key=True)

    conversation_id : Mapped[UUID] = mapped_column(default=uuid4,nullable=False)

    turn_index: Mapped[int] = mapped_column(Integer,nullable=False,default=0)
    user_id : Mapped[str | None] = mapped_column(String(64))

    query : Mapped[str] = mapped_column(Text,nullable=False)
    answer : Mapped[str | None] = mapped_column(Text)

    sources : Mapped[list[dict[str,Any]] | None] = mapped_column(JSONB)   

    status : Mapped[TurnStatus] = mapped_column(SAEnum(TurnStatus,native_enum=False, length = 16,
                                                        validate_strings = True),
                                                        default = TurnStatus.OK,
                                                        nullable=False)
    error_detail: Mapped[str | None] = mapped_column(Text)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    prompt_tokens: Mapped[int | None] = mapped_column(Integer)
    completion_tokens: Mapped[int | None] = mapped_column(Integer)
    model_name: Mapped[str | None] = mapped_column(String(128))

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "uq_chat_logs_conv_turn",
            "conversation_id",
            "turn_index",
            unique=True,
        ),
        Index("ix_chat_logs_created_at", text("created_at DESC")),
        Index(
            "ix_chat_logs_errors",
            "created_at",
            postgresql_where=text("status <> 'ok'"),
        ),
        # GIN lets you query INTO the JSON: sources @> '[{"chunk_id":"c1"}]'
        Index("ix_chat_logs_sources_gin", "sources", postgresql_using="gin"),
        {"comment": "One row per conversation turn. Append-then-update."},
    )

    def __repr__(self):
        return (
            f"<ChatLog id={self.id} conv={self.conversation_id}"
            f"turn={self.turn_index} status=e{self.status}"
        )