from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from src.dependencies.auth import get_current_user
from src.services.db import DBService
from src.config.settings import settings
from src.main import app as main_app
from src.db.session import async_session_maker, engine, get_async_session
from src.schemas.user import UserCreate


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    assert settings.MODE == "TEST"
    await DBService.setup_database()


@pytest_asyncio.fixture(scope="function")
async def db():
    async with async_session_maker() as session:
        async with session.begin():
            yield session
            await session.rollback()
    await engine.dispose()


@pytest_asyncio.fixture
async def app():
    async with LifespanManager(main_app) as manager:
        print("We're in!")
        yield manager.app


@pytest_asyncio.fixture
async def client(app, db):
    main_app.dependency_overrides[get_async_session] = lambda: db

    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        print("Client is ready")
        yield client

    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_token(client):
    await client.post(
        "/api/auth/register",
        json={
            "username": "Timur",
            "email": "user@example.com",
            "roles": "admin",
            "password": "123",
        },
    )

    login = await client.post(
        "/api/auth/login", data={"username": "user@example.com", "password": "123"}
    )
    token = login.json().get("access_token")
    return token


# @pytest_asyncio.fixture
# async def test_user(test_token, db):
#     user = await get_current_user(test_token, db)
    
#     return UserCreate.model_validate(user, from_attributes=True)


def pytest_addoption(parser):
    parser.addoption("--run-slow", default="false", choices=("true", "false"))
