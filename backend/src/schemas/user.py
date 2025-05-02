from pydantic import BaseModel, EmailStr

from src.schemas.task import Task


class UserBase(BaseModel):
    username: str
    email: EmailStr
    roles: str | None = None

class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Схема Пользователя в БД
class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool


class UserRelInDB(UserInDB):
    tasks: list["Task"]
