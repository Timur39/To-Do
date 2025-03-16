from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from src.services.auth import security
from src.db.session import get_async_session
from src.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from src.config.settings import settings

async def get_current_user(
    token: str = Depends(security.access_token_required),
    db: AsyncSession = Depends(get_async_session),
    ) -> User:
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")

        user = await db.get(User, int(user_id))
 
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
