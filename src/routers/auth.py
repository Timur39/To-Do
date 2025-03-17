from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.user import UserCreate
from src.schemas.auth import Token
from src.services.auth import AuthService, get_user_by_email
from src.db.models.user import User
from src.db.session import setup_database
from src.dependencies.db import sessionDep
from src.config.settings import settings
from src.utils.security import hash_password


router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post("/register", summary="Зарегистрироваться")
async def register(
    user_data: UserCreate,
    db: sessionDep
):
    # Проверка существования пользователя
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Создание пользователя
    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        roles=user_data.roles or "user"
    )
    db.add(user)
    await db.commit()
    return {"message": "User created"}


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


@router.post("/reset_db", summary="Перезагрузить базу данных")
async def reset_db():
    res = await setup_database()
    return res
