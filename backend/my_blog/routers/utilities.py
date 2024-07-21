from fastapi import APIRouter


router = APIRouter()


@router.get("/api/v1/ping")
async def ping() -> dict[str, str]:
    return {"status": "ok"}