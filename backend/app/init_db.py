import app.models as Database # Dont remove!
from app.core.db import engine , Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def clode_db():
    await engine.dispose()