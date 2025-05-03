from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload, contains_eager
from src.schemas.task import Task
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

class UserMethods: 
    # Получаем пользователя по email из БД
    @staticmethod
    async def get_user_by_email(db: sessionDep, email: str) -> UserRelInDB:
        query = (
            select(UserModel).where(UserModel.email == email)
            .join(UserModel.tasks)
            .options(selectinload(UserModel.tasks).load_only(TaskModel.id, TaskModel.title, TaskModel.is_completed, TaskModel.date))
        )
        user = await db.execute(query)
        user = user.scalar()

        if user is None:
            raise user_not_found_exeption
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

        if user is None:
            raise user_not_found_exeption
        return user

    # Получаем всех пользователей из БД
    @staticmethod
    async def get_all_users(db: sessionDep) -> UserRelInDB:
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
        result = [UserRelInDB.model_validate(i, from_attributes=True) for i in records]
        return result

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
    async def update_user(user_id: int, new_username: str, db: sessionDep) -> UserBase:
        user = await db.get(UserModel, user_id)
        if not user:
            raise user_not_found_exeption
        user.username = new_username
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

    # Получаем все задачи пользователя
    @staticmethod
    async def get_users_tasks(user_id: int, db: sessionDep) -> list[Task]:
        query = (
            select(UserModel).where(UserModel.id == user_id)
            .options(selectinload(UserModel.tasks))
        )
        res = await db.execute(query)
        result = res.unique().scalars().all()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Users tasks not found")
        user_tasks = result[0].tasks

        return [Task.model_validate(task, from_attributes=True) for task in user_tasks]
