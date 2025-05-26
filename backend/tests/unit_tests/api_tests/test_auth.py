import pytest
from src.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_register(client):
    user = UserCreate(
        username="Timur", email="user@example2.com", roles="admin", password="123"
    )
    await client.post(
        "/api/auth/register",
        content=user.model_dump_json(),
    )


@pytest.mark.asyncio
async def test_login(client):
    user = {"username": "user@example2.com", "password": "123"}

    response = await client.post(
        "/api/auth/login",
        data=user,
    )
    assert response.status_code == 200
