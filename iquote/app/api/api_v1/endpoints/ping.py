# from project/app/api/ping.py

from core.config import settings
from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def pong():
    return {"ping": "pong!", "environment": settings.ENVIRONMENT}
