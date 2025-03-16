from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from authx import AuthX, AuthXConfig
from src.config.settings import settings
from src.db.models.user import User

config = AuthXConfig()
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ['cookies']
config.JWT_SECRET_KEY = settings.SECRET_KEY

security = AuthX(config=config)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user: User) -> str:
        
        token = security.create_access_token(uid=str(user.id),
                                            expiry=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                                            data={"email": user.email,
                                                  "roles": user.roles.split(","),
                                                  })
        return token
    