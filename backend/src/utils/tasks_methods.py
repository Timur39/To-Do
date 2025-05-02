from fastapi import HTTPException, status
from sqlalchemy import delete, select
from src.db.models.task import TaskModel
from src.db.models.user import UserModel
from src.schemas.task import Task, TaskCreate, TaskUpdate
from src.dependencies.db import sessionDep
from sqlalchemy.orm import joinedload, selectinload, contains_eager


class TaskMethods:
    # Создать задачу 
    @staticmethod
    async def create_task(task_data: TaskCreate, db: sessionDep, user: UserModel) -> None:
        task = TaskModel(title=task_data.title,
                        description=task_data.description or None,
                        priority=task_data.priority or 0,
                        date=task_data.date,
                        user_id=user.id
                        )
        db.add(task)
        await db.commit()


    # Получить задачу по id
    @staticmethod
    async def get_task_by_id(task_id: int, db: sessionDep) -> Task:
        request = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = request.scalar()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Задачи с таким id не существует")
        return task
    
    # Удалить задачу по id
    @staticmethod
    async def delete_task_by_id(task_id: int, db: sessionDep) -> Task:
        task = await db.get(TaskModel, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Задача не найдена'
                )
        
        await db.delete(task)
        await db.commit()

        return task

    # Обновить задачу по id
    @staticmethod
    async def update_task_by_id(task_id: int, new_data: TaskUpdate, db: sessionDep) -> Task:
        task = await db.get(TaskModel, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Задача не найдена'
                )
        task.title = new_data.title
        task.description = new_data.description
        task.priority = new_data.priority
        task.is_completed = new_data.is_completed

        await db.commit()

        return task

    # Получить все задачи
    @staticmethod
    async def get_all_tasks(db: sessionDep) -> list[Task]:
        query = (
                select(TaskModel)
                .join(TaskModel.user)
                .options(joinedload(TaskModel.user).load_only(UserModel.id, UserModel.username))
                )
        if not await db.scalar(select(TaskModel)):
            raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='Задач нет'
                        )
        tasks = await db.execute(query)
        tasks = tasks.unique().scalars().all()   

        return tasks

    # Получить все задачи конкретного пользователя
    @staticmethod
    async def get_user_tasks(user_id: int, db: sessionDep) -> list[Task]:
        query = (
            select(UserModel).where(UserModel.id == user_id)
            .join(UserModel.tasks)
            .options(selectinload(UserModel.tasks))
            # .filter(TaskModel.priority >= 2)
            # .limit(10)
        )

        res = await db.execute(query)
        result = res.unique().scalars().all()

        if result:
            user_tasks = result[0].tasks

            return [Task.model_validate(task, from_attributes=True) for task in user_tasks]
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Задач нет')

    
    # Сбросить все задачи
    @staticmethod
    async def reset_tasks(db: sessionDep) -> None:
        await db.execute(delete(TaskModel.__table__))
        await db.commit()

        return {'status': 'Tasks was successfully reset'}

    