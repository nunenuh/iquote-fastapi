# from project/app/api/ping.py

from fastapi import APIRouter

from core.config import settings

router = APIRouter()


@router.get("/ping")
async def pong():
    return {"ping": "pong!", "environment": settings.ENVIRONMENT}
