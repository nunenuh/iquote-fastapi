from api.api_v1.endpoints import (
    health,
    login,
    ping,
    quote_author,
    users,
    utils,
)
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(ping.router, tags=["ping"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(
    quote_author.router, prefix="/quote/author", tags=["quote_author"]
)


# api_router.include_router(items.router, prefix="/items", tags=["items"])
