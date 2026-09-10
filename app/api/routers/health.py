from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    ml_status = "loaded" if hasattr(request.app.state,"vector_index") else "missing"
    return {
        "status" : "healthy",
        "ml_status" : ml_status
    }