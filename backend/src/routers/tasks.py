from fastapi import APIRouter
from src.schemas.task import Task, TaskCreate, TaskUpdate
from src.dependencies.auth import authDep_user, authDep_admin
from src.dependencies.db import sessionDep
from fastapi_cache.decorator import cache
from src.utils.tasks_methods import TaskMethods


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create_task", summary="Создать задачу")
async def create_task_router(task_data: TaskCreate, db: sessionDep, user: authDep_user) -> Task:
    created_task = await TaskMethods.create_task(task_data, db, user)
    return created_task


@router.get("/get_task_by_id/{task_id}", summary="Получить задачу по id")
@cache(expire=60)
async def get_task_by_id_router(task_id: int, db: sessionDep, user: authDep_user) -> Task:
    task = await TaskMethods.get_task_by_id(task_id, db)
    return task 


@router.delete("/delete_task/{task_id}", summary="Удалить задачу по id")
async def delete_task_router(task_id: int, db: sessionDep, user: authDep_user) -> Task:
    deleted_task = await TaskMethods.delete_task_by_id(task_id, db)
    return deleted_task


@router.post("/update_task/{task_id}", summary="Обновить задачу по id")
async def update_task_router(task_id: int, new_data: TaskUpdate, db: sessionDep, user: authDep_user) -> Task:
    updated_task = await TaskMethods.update_task_by_id(task_id, new_data, db)
    return updated_task


@router.get("/get_all_tasks", summary="Получить все задачи")
@cache(expire=60)
async def get_all_tasks_router(db: sessionDep) -> list[Task]: # user: authDep_user
    all_tasks = await TaskMethods.get_all_tasks(db)
    return all_tasks


@router.get("/get_user_tasks/{user_id}", summary="Получить все задачи у пользователя")
@cache(expire=60)
async def get_user_tasks_router(user_id: int, db: sessionDep, user: authDep_admin) -> list[Task]:
    user_tasks = await TaskMethods.get_user_tasks(user_id, db)
    return user_tasks


@router.post("/reset_tasks", summary="Сбросить все задачи")
async def reset_tasks_router(db: sessionDep, user: authDep_admin) -> dict[str, str]:
    await TaskMethods.reset_tasks(db)
    return {'status': 'Tasks was successfully reset'}

