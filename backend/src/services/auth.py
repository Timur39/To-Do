from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
import jwt
from src.config.settings import settings
from src.utils.security import verify_password
from src.utils.users_methods import UserMethods


AUTH_SECRET_KEY = settings.AUTH_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class AuthService:
    # Создаем access_token 
    @staticmethod
    async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(payload=to_encode, key=AUTH_SECRET_KEY, algorithm=ALGORITHM) # Кодируем данные

        return encoded_jwt
    
    # Аунтефицируем пользователя
    @staticmethod
    async def authenticate_user(db, email: str, password: str):
        user = await UserMethods.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return False
        return user
