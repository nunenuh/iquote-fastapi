# from project/app/api/ping.py

from core.config import Settings, settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/ping")
async def pong():
    return {
        "ping": "pong!",
        "environment": settings.ENVIRONMENT
    }
