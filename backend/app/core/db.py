from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import event
from sqlalchemy.engine import Engine

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     """Bật Foreign Key trong Sqlite"""
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()
    
# URI = "sqlite+aiosqlite:///data.db"
URI = "postgresql+asyncpg://postgres:ledinhlam@localhost:5432/devwebdata"

Base = declarative_base()

engine = create_async_engine(
    url=URI,
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

