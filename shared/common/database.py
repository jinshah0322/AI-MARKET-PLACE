"""
Database connection and session management.

This module provides:
- Async PostgreSQL connection using SQLAlchemy
- Session management with dependency injection
- Connection pooling for performance
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv(
    "POSTGRES_DB_URL",
    "postgresql+asyncpg://postgres:postgres123@localhost:5432/ai_marketplace"
)

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Create async engine
# echo=True logs all SQL queries (useful for debugging)
# pool_pre_ping=True checks connection health before using
engine = create_async_engine(
    DATABASE_URL,
    # echo=SQL_ECHO,  # Set to False in production
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Additional connections when pool is full
    pool_pre_ping=True,  # Test connections before using
    future=True,
)

# Session factory
# expire_on_commit=False keeps objects usable after commit
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all database models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function for FastAPI routes.
    
    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            # Use db here
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database - create all tables.
    
    Call this once when your service starts.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections gracefully.
    
    Call this when shutting down your service.
    """
    await engine.dispose()