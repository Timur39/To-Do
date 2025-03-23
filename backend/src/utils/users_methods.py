from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from src.db.models.user import UserModel
from src.schemas.user import UserInDB, UserBase, UserCreate
from src.dependencies.db import sessionDep
from src.utils.security import hash_password
from src.db.models.task import TaskModel
from fastapi import HTTPException, status


class UserMethods: 
    # Получаем пользователя по email из БД
    @staticmethod
    async def get_user_by_email(db: sessionDep, email: str) -> UserInDB:
        user = await db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_dict = user.scalar()
        if user_dict is None:
            return False
        
        return UserInDB.model_validate(user_dict, from_attributes=True)


    # Получаем пользователя по id из БД
    @staticmethod
    async def get_user_by_id(db: sessionDep, user_id: int) -> UserBase:
        user = await db.get(UserModel, user_id)

        if user is None:
            return False
        
        return UserBase.model_validate(user, from_attributes=True)


    # Получаем всех пользователей из БД
    @staticmethod
    async def get_all_users(db: sessionDep) -> UserInDB:
        # Создаем запрос для выборки всех пользователей
        query = select(UserModel)

        # Выполняем запрос и получаем результат
        result = await db.execute(query)
        records = result.scalars().all()

        if records is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Users not found")
        
        result = [UserInDB.model_validate(i, from_attributes=True) for i in records]

        return result


    # Создаем пользователя
    @staticmethod
    async def create_user(user_data: UserCreate, db: sessionDep) -> HTTPException:
        hashed_password = hash_password(user_data.password)
        user = UserModel(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            roles=user_data.roles or "user"
        )
        db.add(user)
        await db.commit()

        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail="User created")


    # Обновляем данные о пользователе
    @staticmethod
    async def update_user(user_id: int, new_username: str, db: sessionDep) -> UserBase:
        user = await db.get(UserModel, user_id)
        if user:
            user.username = new_username
            await db.commit()
            return UserBase.model_validate(user, from_attributes=True)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")


    # Удаляем пользователя
    @staticmethod
    async def delete_user(user_id: int, db: sessionDep) -> bool:
        user = await db.get(UserModel, user_id)
        if user:
            await db.delete(user)
            await db.commit()
            return True
        return False


    # Удаляем всех пользователей из БД
    @staticmethod
    async def reset_users(db: sessionDep) -> None:
        await db.execute(delete(UserModel.__table__))
        await db.commit()

    
    @staticmethod
    async def select_users_with_selectin_relationship(user_id: int, db: sessionDep) -> list[TaskModel]:
        query = (
            select(UserModel).where(UserModel.id == user_id)
            .options(selectinload(UserModel.tasks))
        )

        res = await db.execute(query)
        result = res.unique().scalars().all()

        user_tasks = result[0].tasks

        return user_tasks
    
    
    # @staticmethod
    # async def select_users_with_condition_relationship(user_id: int, db: sessionDep) -> list[TaskModel]:
    #     query = (
    #         select(UserModel).where(UserModel.id == user_id)
    #         .options(selectinload(UserModel.tasks_high_priotity))
    #     )

    #     res = await db.execute(query)
    #     result = res.unique().scalars().all()

    #     user_tasks = result[0].tasks_high_priotity

    #     return user_tasks
    

    @staticmethod
    async def select_users_with_condition_relationship_contais_eager(user_id: int, db: sessionDep) -> list[TaskModel]:
        # subq = (
        #     select(TaskModel.id.label("high_priority_task_id"))
        #     .filter(TaskModel.user_id == UserModel.id)
        #     .order_by(UserModel.id.desc())
        #     .limit(1)
        #     .scalar_subquery()
        #     .correlate(UserModel)
        # )   
        query = (
            select(UserModel).where(UserModel.id == user_id)
            .join(UserModel.tasks)
            .options(contains_eager(UserModel.tasks))
            .filter(TaskModel.priority >= 2)
        )

        res = await db.execute(query)
        result = res.unique().scalars().all()
        if result:
            user_tasks = result[0].tasks

            return user_tasks
    