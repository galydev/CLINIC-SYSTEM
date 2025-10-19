"""Pytest configuration and fixtures"""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config.database import get_db_session
from config.settings import Settings, get_settings
from infrastructure.database.models import Base
from main import app

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_identity_db"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Create test settings"""
    settings = Settings(
        DATABASE_URL=TEST_DATABASE_URL,
        ENVIRONMENT="test",
        DEBUG=True,
        SECRET_KEY="test-secret-key",
        ACCESS_TOKEN_EXPIRE_MINUTES=30,
        REFRESH_TOKEN_EXPIRE_DAYS=7
    )
    return settings


@pytest.fixture(scope="session")
async def test_engine(test_settings: Settings):
    """Create test database engine"""
    engine = create_async_engine(
        test_settings.DATABASE_URL,
        echo=False,
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client(db_session: AsyncSession, test_settings: Settings) -> TestClient:
    """Create test client with overridden dependencies"""

    async def override_get_db():
        yield db_session

    def override_get_settings():
        return test_settings

    app.dependency_overrides[get_db_session] = override_get_db
    app.dependency_overrides[get_settings] = override_get_settings

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def password_context() -> CryptContext:
    """Create password hashing context"""
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "is_superuser": False
    }


@pytest.fixture
def sample_superuser_data() -> dict:
    """Sample superuser data for testing"""
    return {
        "email": "admin@example.com",
        "username": "adminuser",
        "password": "AdminPassword123!",
        "full_name": "Admin User",
        "is_superuser": True
    }
