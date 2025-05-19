from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from src.db.models.user import UserModel
from src.schemas.user import UserBase, UserCreate, UserRelInDB
from src.dependencies.db import sessionDep
from src.utils.security import hash_password
from src.db.models.task import TaskModel
from fastapi import HTTPException, status


user_not_found_exeption = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User not found'
)

class UserService: 
    # Получаем пользователя по email из БД
    @staticmethod
    async def get_user_by_email(db: sessionDep, email: str) -> UserRelInDB:
        query = (
            select(UserModel).where(UserModel.email == email)
        )

        user = await db.execute(query)
        user = user.scalar()

        return user

    # Получаем пользователя по id из БД
    @staticmethod
    async def get_user_by_id(db: sessionDep, user_id: int) -> UserRelInDB:
        query = (
            select(UserModel).where(UserModel.id == user_id)
            .join(UserModel.tasks)
            .options(selectinload(UserModel.tasks).load_only(TaskModel.id, TaskModel.title, TaskModel.is_completed, TaskModel.date))
        )
        user = await db.execute(query)
        user = user.scalar()

        return user

    # Получаем всех пользователей из БД
    @staticmethod
    async def get_all_users(db: sessionDep) -> dict[str, list[UserRelInDB]]:
        # Создаем запрос для выборки всех пользователей
        query = (
            select(UserModel)
            .join(UserModel.tasks)
            .options(selectinload(UserModel.tasks))
        )
        # Выполняем запрос и получаем результат
        result = await db.execute(query)
        records = result.unique().scalars().all()

        if records is None:
            raise user_not_found_exeption
        return {"users": [UserRelInDB.model_validate(i, from_attributes=True) for i in records]}

    # Создаем пользователя
    @staticmethod
    async def create_user(user_data: UserCreate, db: sessionDep) -> UserCreate:
        hashed_password = hash_password(user_data.password)
        user = UserModel(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            roles=user_data.roles or "user"
        )
        db.add(user)
        await db.commit()
        return UserCreate.model_validate(user, from_attributes=True)

    # Обновляем данные о пользователе
    @staticmethod
    async def update_user(db: sessionDep, user_id: int, new_username: str = '', new_roles: str = '') -> UserBase:
        user = await db.get(UserModel, user_id)
        if not user:
            raise user_not_found_exeption
        
        user.username = new_username if new_username else user.username
        user.roles = new_roles if new_roles else user.roles
        await db.commit()
        return UserBase.model_validate(user, from_attributes=True)

    # Удаляем пользователя
    @staticmethod
    async def delete_user(user_id: int, db: sessionDep) -> HTTPException:
        user = await db.get(UserModel, user_id)
        if user:
            await db.delete(user)
            await db.commit()
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                                detail="User deleted")
        else:
            raise user_not_found_exeption

    # Удаляем всех пользователей из БД
    @staticmethod
    async def reset_users(db: sessionDep) -> None:
        await db.execute(delete(UserModel.__table__))
        await db.commit()
