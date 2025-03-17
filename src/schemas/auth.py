from pydantic import BaseModel, EmailStr


# Схема Токена
class Token(BaseModel):
    access_token: str
    token_type: str

# Схема Данных токена
class TokenData(BaseModel):
    email: EmailStr | None = None
