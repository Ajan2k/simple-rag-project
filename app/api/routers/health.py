from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    ml_status = "loaded" if getattr(request.app.state,"vector_index") else "missing"
    return {
        "status" : "healthy",
        "ml_status" : ml_status
    }