from sqlalchemy.orm import Mapped, mapped_column
from src.db.session import Base


class UserModel(Base):
    __tablename__ = "users"

    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    roles: Mapped[str] = mapped_column(server_default="user")


    