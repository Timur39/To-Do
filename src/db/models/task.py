from sqlalchemy import Column, Integer, String, Boolean, Date
from src.db.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, default=None)
    priority = Column(Integer)
    date = Column(Date)