from fastapi import APIRouter
from app.api.routes import (
    login , users , products,
    categories
)
import sys, asyncio

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)


api_routers = APIRouter()
api_routers.include_router(login.router)
api_routers.include_router(users.router)
api_routers.include_router(products.router)
api_routers.include_router(categories.router)
