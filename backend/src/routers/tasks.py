from fastapi import APIRouter
from src.schemas.task import Task, TaskCreate, TaskInBD, TaskUpdate
from src.dependencies.auth import authDep_user, authDep_admin
from src.dependencies.db import sessionDep
from fastapi_cache.decorator import cache
from src.services.tasks import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])
expire_time = 360


@router.post("/create_task", summary="Создать задачу")
async def create_task_router(
    task_data: TaskCreate, db: sessionDep, user: authDep_user
) -> Task:
    created_task = await TaskService.create_task(task_data, db, user)
    return created_task


@router.get("/get_task_by_id/{task_id}", summary="Получить задачу по id")
@cache(expire=expire_time)
async def get_task_by_id_router(task_id: int, db: sessionDep) -> TaskInBD:
    task = await TaskService.get_task_by_id(task_id, db)
    return task


@router.get("/get_all_tasks", summary="Получить все задачи")
@cache(expire=expire_time)
async def get_all_tasks_router(db: sessionDep) -> dict[str, list[Task]]:
    all_tasks = await TaskService.get_all_tasks(db)
    return all_tasks


@router.get("/get_user_tasks/{user_id}", summary="Получить все задачи у пользователя")
@cache(expire=expire_time)
async def get_user_tasks_router(user_id: int, db: sessionDep) -> dict[str, list[Task]]:
    user_tasks = await TaskService.get_user_tasks(user_id, db)

    return user_tasks


@router.delete("/delete_task/{task_id}", summary="Удалить задачу по id")
async def delete_task_router(task_id: int, db: sessionDep, user: authDep_user) -> Task:
    deleted_task = await TaskService.delete_task_by_id(task_id, db)
    return deleted_task


@router.put("/update_task/{task_id}", summary="Обновить задачу по id")
async def update_task_router(
    task_id: int, new_data: TaskUpdate, db: sessionDep
) -> Task:
    updated_task = await TaskService.update_task_by_id(task_id, new_data, db)
    return updated_task


@router.post("/reset_tasks", summary="Сбросить все задачи")
async def reset_tasks_router(db: sessionDep, user: authDep_admin) -> dict[str, str]:
    await TaskService.reset_tasks(db)
    return {"status": "Tasks was successfully reset"}
