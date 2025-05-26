import pytest_asyncio
from sqlalchemy import text
from src.schemas.task import TaskCreate


# @pytest_asyncio.fixture
# async def tasks(client, test_token, db):
#     tasks = [
#         TaskCreate(
#             title="Task 1",
#             description="string",
#             priority=0,
#             is_completed=False,
#             date="2025-12-12",
#         ),
#         # TaskCreate(title="Task 2", description="Task description", date="2025-12-12"),
#     ]
#     for task in tasks:
#         await client.post(
#             "/api/tasks/create_task",
#             data=task.model_dump_json(),
#             headers={"Authorization": f"Bearer {test_token}"},
#         )

#     yield tasks

#     # Очистка после использования фикстуры
#     async with db.begin() as transaction:
#         await db.execute(text("DELETE FROM tasks"))
#         await transaction.commit()
