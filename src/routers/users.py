from fastapi import APIRouter
from src.schemas.user import UserInDB, UserBase
from src.dependencies.auth import authDep_user, authDep_admin
from src.dependencies.db import sessionDep
from src.utils.users_methods import get_all_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", summary="Получить данные о себе")
async def get_current_user(user: authDep_user) -> UserBase:
    return UserBase(username=user.username, email=user.email, roles=user.roles)

@router.get("/all_users", summary="Получить всех пользователей")
async def get_all_users_route(user: authDep_admin, db: sessionDep) -> list[UserInDB]:
    users = await get_all_users(db) 
    return users
