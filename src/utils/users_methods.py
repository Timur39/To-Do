from sqlalchemy import select
from src.db.models.user import User
from src.schemas.user import UserInDB
from src.dependencies.db import sessionDep

# Получаем пользователя из БД
async def get_user_by_email(db: sessionDep, email: str) -> UserInDB:
    user = await db.execute(
        select(User).where(User.email == email)
    )
    user_dict = user.scalar()
    if user_dict is None:
        return False
    
    return UserInDB.model_validate(user_dict, from_attributes=True)


# Получаем всех пользователей из БД
async def get_all_users(db: sessionDep) -> UserInDB:
    # Создаем запрос для выборки всех пользователей
    query = select(User)

    # Выполняем запрос и получаем результат
    result = await db.execute(query)

    records = result.scalars().all()

    if records is None:
        return {"Пользователей не найдено!"}

    result = [UserInDB.model_validate(i, from_attributes=True) for i in records]

    return result