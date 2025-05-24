import pytest_asyncio
from src.config.settings import settings
from src.schemas.task import TaskCreate
from src.services.tasks import TaskService


@pytest_asyncio.fixture
async def tasks():
    tasks = [
        TaskCreate(title="Task 1", priority=5, date="2025-12-12"),
        TaskCreate(title="Task 2", description="Task description", date="2025-12-12"),
    ]
    return tasks


@pytest_asyncio.fixture
async def delete_tasks(db):
    TaskService.reset_tasks(db)

# @pytest_asyncio.fixture(autouse=True)
# async def create_data(tasks, db, test_user):
#     print(tasks)
#     for task in tasks:
#         await TaskService.create_task(task, db, test_user)
