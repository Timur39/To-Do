from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, delete
from src.schemas.task import Task, TaskCreate, TaskUpdate
from src.db.models.task import TaskModel
from src.dependencies.auth import authDep_user, authDep_admin
from src.dependencies.db import sessionDep
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create_task", summary="Создать задачу")
async def create_task(task_data: TaskCreate, db: sessionDep, user: authDep_user):
    task = TaskModel(title=task_data.title,
                    description=task_data.description or None,
                    priority=task_data.priority or 0,
                    date=task_data.date,
                    user_id=user.id
                    )
    db.add(task)
    await db.commit()

    return {"Task is successfully created!"}


@router.get("/get_task_by_id/{task_id}", summary="Получить задачу по id")
@cache(expire=60)
async def get_task_by_id(task_id: int, db: sessionDep, user: authDep_user) -> Task:

    request = await db.execute(select(TaskModel).where(TaskModel.id == task_id))

    request = request.scalar()
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователя с таким id не существует")

    return request


@router.delete("/delete_task/{task_id}", summary="Удалить задачу по id")
async def delete_task_by_id(task_id: int, db: sessionDep, user: authDep_user) -> Task:

    if not await db.scalar(select(TaskModel).where(TaskModel.id == task_id)):
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Задача не найдена'
                    )

    task = await db.get(TaskModel, task_id)

    await db.delete(task)
    await db.commit()

    return task


@router.post("/update_task/{task_id}", summary="Обновить задачу по id")
async def update_task_by_id(task_id: int, new_data: TaskUpdate, db: sessionDep, user: authDep_user) -> Task:

    if not await db.scalar(select(TaskModel).where(TaskModel.id == task_id)):
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Пользователь не найден'
                    )

    task = await db.get(TaskModel, task_id)

    task.title = new_data.title
    task.description = new_data.description
    task.priority = new_data.priority
    task.is_completed = new_data.is_completed

    await db.commit()

    return task


@router.get("/get_all_tasks", summary="Получить все задачи")
@cache(expire=60)
async def get_all_tasks(db: sessionDep, user: authDep_user) -> list[Task]:

    if not await db.scalar(select(TaskModel)):
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Задач нет'
                    )

    tasks = await db.execute(select(TaskModel))

    tasks = tasks.scalars().all()   

    return tasks


@router.get("/get_user_tasks/{user_id}", summary="Получить все задачи у пользователя")
@cache(expire=60)
async def get_user_tasks(user_id: int, db: sessionDep, user: authDep_admin) -> list[Task]:
    if not await db.scalar(select(TaskModel).where(TaskModel.user_id == user_id)):
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Задач нет'
                    )

    tasks = await db.execute(select(TaskModel).where(TaskModel.user_id == user_id))

    tasks = tasks.scalars().all()

    return tasks

@router.post("/reset_tasks", summary="Сбросить все задачи")
async def reset_tasks(db: sessionDep, user: authDep_admin):
    await db.execute(delete(TaskModel.__table__))
    await db.commit()

    return {'status': 'Tasks was successfully reset'}
