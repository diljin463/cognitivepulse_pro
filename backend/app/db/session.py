from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from backend.app.core.config import settings

# Create async database engine for SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True if you want raw SQL queries printed in the terminal
    future=True
)

# Factory for creating async database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class from which all database ORM models inherit
class Base(DeclarativeBase):
    pass

# Helper dependency to inject database sessions into FastAPI endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session