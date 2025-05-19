from fastapi import HTTPException, status
from sqlalchemy import delete, select
from src.db.models.task import TaskModel
from src.db.models.user import UserModel
from src.schemas.task import Task, TaskCreate, TaskUpdate
from src.dependencies.db import sessionDep


task_not_found_exeption = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, 
    detail='Задач(а) не найдено(а)'
)

class TaskService:
    # Создать задачу 
    @staticmethod
    async def create_task(task_data: TaskCreate, db: sessionDep, user: UserModel) -> Task:
        task = TaskModel(title=task_data.title,
                        description=task_data.description or None,
                        priority=task_data.priority or 0,
                        is_completed=task_data.is_completed,
                        date=task_data.date,
                        user_id=user.id
                        )
        db.add(task)
        await db.commit()
        return task

    # Получить задачу по id
    @staticmethod
    async def get_task_by_id(task_id: int, db: sessionDep) -> Task:
        task = await db.get(TaskModel, task_id)
        if not task:
            raise task_not_found_exeption
        return task
    
    # Удалить задачу по id
    @staticmethod
    async def delete_task_by_id(task_id: int, db: sessionDep) -> Task:
        try:
            task = await db.get(TaskModel, task_id)
            if not task:
                raise task_not_found_exeption
            await db.delete(task)
            await db.commit()

            return task
        except Exception as e:
            print(f'Delete Task error: {e}')
            return

    # Обновить задачу по id
    @staticmethod
    async def update_task_by_id(task_id: int, new_data: TaskUpdate, db: sessionDep) -> Task:
        task = await db.get(TaskModel, task_id)
        if not task:
            raise task_not_found_exeption
        task.title = new_data.title
        task.description = new_data.description
        task.priority = new_data.priority
        task.is_completed = new_data.is_completed

        await db.commit()
        return task

    # Получить все задачи
    @staticmethod
    async def get_all_tasks(db: sessionDep) -> dict[str, list[Task]]:
        query = (
                select(TaskModel)
                )
        if not await db.scalar(select(TaskModel)):
            raise task_not_found_exeption
        tasks = await db.execute(query)
        tasks = tasks.unique().scalars().all()   

        return {"tasks": tasks}

    # Получить все задачи конкретного пользователя
    @staticmethod
    async def get_user_tasks(user_id: int, db: sessionDep) -> dict[str, list[Task]]:
        query = (
            select(TaskModel).where(TaskModel.user_id == user_id)
        )
        res = await db.execute(query)
        result = res.unique().scalars().all()
        if not result:
            raise task_not_found_exeption
        
        return {"tasks": [Task.model_validate(task, from_attributes=True) for task in result]}

    # Сбросить все задачи
    @staticmethod
    async def reset_tasks(db: sessionDep) -> dict[str, str]:
        await db.execute(delete(TaskModel.__table__))
        await db.commit()
        return {'status': 'Tasks was successfully reset'}
    