import pytest


@pytest.mark.asyncio
async def test_create_task(client, test_token):
    task = {
        "title": "Task",
        "description": "",
        "priority": 0,
        "is_completed": False,
        "date": "2025-05-21",
    }
    response = await client.post(
        "/api/tasks/create_task",
        json=task,
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 200
    data = response.json()

    assert (
        data["title"] == task["title"]
        and data["priority"] == data["priority"]
        and data["date"] == data["date"]
        and data["is_completed"] == data["is_completed"]
    )


@pytest.mark.asyncio
@pytest.mark.skipif("config.getoption('--run-slow') == 'false'", reason="Slow test")
async def test_get_all_tasks(client, test_token):
    response = await client.get("/api/tasks/get_all_tasks")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.skipif("config.getoption('--run-slow') == 'false'", reason="Slow test")
async def test_get_task_by_id(client):
    response = await client.get("/api/tasks/get_task_by_id/1")
    data = response.json()

    assert response.status_code == 200
    assert data.get("id") == 1


@pytest.mark.asyncio
@pytest.mark.skipif("config.getoption('--run-slow') == 'false'", reason="Slow test")
async def test_get_user_tasks(client):
    response = await client.get("/api/tasks/get_user_tasks/1")
    assert response.status_code == 200
