from pydantic import BaseModel
from datetime import date

class Task(BaseModel):
    title: str | None = None
    description: str  | None = None
    priority: int = 0
    is_completed: bool | None = False


class TaskCreate(BaseModel):
    title: str
    description: str = None
    priority: int = 0
    date: date


class TaskDelete(BaseModel):
    id: int


class TaskUpdate(Task):
    pass


class TaskRel(Task):
    user: "UserInDB"
