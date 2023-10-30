from fastapi import APIRouter

__all__ = [
    "router"
]

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/health")
async def health():
    return {"message": "Hello World"}
