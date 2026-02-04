from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.core.config import settings    

Base = declarative_base()
engine = create_async_engine(
    url=settings.DATABASE_URL,
    future=True,
    pool_size=100,
    max_overflow=200,
    pool_timeout=30
    )

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)
