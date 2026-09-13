from fastapi import APIRouter

from app.schemas.payload import ChatRequest, ChatResponse ,SourceChunk

router = APIRouter(prefix="/chat",tags=["chat"])

@router.post("",response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:

    return ChatResponse(
        answer=f"stub answer for {payload.query}",
        sources=[SourceChunk(chunk_id="c1",text="placeholder",score="0.0")]
    )
