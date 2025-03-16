from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from src.schemas.user import UserCreate, UserLogin
from src.services.auth import AuthService
from src.db.models.user import User
from src.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth import config


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(
    user_data: UserCreate,
    db_session: AsyncSession = Depends(get_async_session)
):
    # Проверка существования пользователя
    existing_user = await db_session.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Создание пользователя
    hashed_password = AuthService.hash_password(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        roles=user_data.roles or "user"
    )
    db_session.add(user)
    await db_session.commit()
    return {"message": "User created"}

@router.post("/login")
async def login(
    user_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_async_session)
):
    user = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    user = user.scalar()
    if not user or not AuthService.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = AuthService.create_access_token(user)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    
    return {"access_token": token, "token_type": "bearer"}
