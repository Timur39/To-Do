from fastapi import APIRouter, HTTPException, status
from src.schemas.user import UserBase, UserRelInDB
from src.dependencies.auth import authDep_user, authDep_admin
from src.dependencies.db import sessionDep
from src.utils.users_methods import UserMethods
from fastapi_cache.decorator import cache


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", summary="Получить данные о себе")
@cache(expire=60)
async def get_current_user_router(db: sessionDep, user: authDep_user) -> UserBase:
    user = await UserMethods.get_user_by_id(db, user.id)
    return user


@router.get("/get_user/{user_id}", summary="Получить пользователя по id")
@cache(expire=60)
async def get_user_router(user_id: int, db: sessionDep) -> UserBase:
    user = await UserMethods.get_user_by_id(db, user_id)
    return user


@router.get("/all_users", summary="Получить всех пользователей")
@cache(expire=60)
async def get_all_users_router(db: sessionDep) -> dict[str, list[UserRelInDB]]:
    all_users = await UserMethods.get_all_users(db)
    return all_users


@router.patch("/update_user/{user_id}", summary="Изменить данные о пользователе")
async def update_user_router(db: sessionDep, user: authDep_admin, user_id: int, new_roles: str = '', new_username: str = '') -> UserBase:
    updated_user = await UserMethods.update_user(db, user_id, new_username, new_roles)
    return updated_user


@router.delete("/delete_user/{user_id}", summary="Удалить пользователя")
async def delete_user_router(user_id: int, db: sessionDep, user: authDep_admin):
    deleted_user = await UserMethods.delete_user(user_id, db) 
    return deleted_user


@router.post("/reset_users", summary="Сбросить всех пользователей")
async def reset_users_router(db: sessionDep, user: authDep_admin):
    await UserMethods.reset_users(db)
    raise HTTPException(status_code=status.HTTP_205_RESET_CONTENT,
                        detail="Reset users in DB")

