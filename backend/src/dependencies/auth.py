import jwt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from src.schemas.auth import TokenData
from src.utils.users_methods import UserMethods
from src.db.session import get_async_session
from src.db.models.user import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.settings import settings
from src.services.auth import oauth2_scheme


# Получаем текущего пользователя
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], 
                           db: AsyncSession = Depends(get_async_session)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # Декодируем полученный токен
        email = payload.get("sub")  # Получаем id из декодируемых данных
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email) # Преобразуем даннык в pydantic схему 

    except jwt.InvalidTokenError:
        raise credentials_exception

    user = await UserMethods.get_user_by_email(db, email=token_data.email) # Получаем пользователя из БД

    if user is None:
        raise credentials_exception
    
    return user

# Получаем текущего активного пользователя
async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Получаем текущего администратора
async def get_current_admin(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:
    if "admin" not in current_user.roles.split(","):
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


authDep_user = Annotated[UserModel, Depends(get_current_active_user)]
authDep_admin = Annotated[UserModel, Depends(get_current_admin)]
