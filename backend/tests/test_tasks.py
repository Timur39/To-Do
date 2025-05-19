import pytest

from src.schemas.task import Task
from src.services.tasks import TaskMethods
from src.dependencies.db import get_async_session
from src.schemas.user import UserBase
from src.utils.db import setup_database


@pytest.fixture(scope="function", autouse=True)
def db():
    get_async_session()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    setup_database()

@pytest.fixture
def tasks():
    tasks = [
        Task(title="Task 1", priority=5),
        Task(title="Task 2", description="Task description")
    ]
    return tasks

@pytest.fixture
def delete_tasks(db):
    TaskMethods.reset_tasks(db)


@pytest.mark.usefixtures("delete_tasks")
class TestTasks:
    def test_get_all_tasks(self, tasks, db):
        for task in tasks:
            print(TaskMethods.create_task(db, task, UserBase(username='Timur', email='user@example.com')))
        
        all_tasks = TaskMethods.get_all_tasks(db)
        print(all_tasks)
        for added_task in all_tasks:
            assert added_task in tasks


