import app.models as Database #TODO: !!!DONT'T REMOVE!!!
from app.core.db import engine , Base
from asyncpg.exceptions import InvalidCatalogNameError

"""
NOT USE
"""
async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except InvalidCatalogNameError as e:
        print(f"ERROR: {e}")
        
        
async def clode_db():
    await engine.dispose()