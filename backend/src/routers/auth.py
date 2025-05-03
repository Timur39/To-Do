from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.user import UserCreate
from src.schemas.auth import Token
from src.services.auth import AuthService
from src.dependencies.db import sessionDep
from src.config.settings import settings
from src.utils.users_methods import UserMethods

router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post("/register", summary="Зарегистрироваться")
async def register(
    user_data: UserCreate,
    db: sessionDep
):
    # Проверка существования пользователя
    existing_user = await UserMethods.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Создание пользователя
    user = await UserMethods.create_user(user_data, db)
    
    raise HTTPException(status_code=status.HTTP_201_CREATED,
                        detail=user)


@router.post("/login", summary="Войти")
async def login(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: sessionDep
) -> Token:
    user = await AuthService.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await AuthService.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    ) # Создаем jwt токен
    
    return Token(access_token=access_token, token_type="bearer")  # Возвращаем Токен в виде pydatic схемы
