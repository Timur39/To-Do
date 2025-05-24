from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.session import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    description: Mapped[str | None]
    priority: Mapped[int] = mapped_column(default=0)
    is_completed: Mapped[bool] = mapped_column(default=False)
    date: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["UserModel"] = relationship(
        back_populates="tasks",
    )

    repr_cols_num = 5
