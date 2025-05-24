from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session


sessionDep = Annotated[AsyncSession, Depends(get_async_session)]
