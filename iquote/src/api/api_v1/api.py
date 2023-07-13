from fastapi import APIRouter

from api.api_v1.endpoints import (
    author,
    category,
    health,
    login,
    ping,
    quote,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(ping.router, tags=["ping"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(author.router, prefix="/author", tags=["author"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(quote.router, prefix="/quote", tags=["quote"])

# api_router.include_router(items.router, prefix="/items", tags=["items"])
