from fastapi import APIRouter

from .endpoints import config, health, profanity

v1_router = APIRouter()

# Include all endpoint routers with the common "v1" tag plus specific tags
v1_router.include_router(health.router, prefix="/health", tags=["v1"])
v1_router.include_router(profanity.router, tags=["v1"])
v1_router.include_router(config.router, prefix="/config", tags=["v1"])
