from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, Depends
from src.dependencies.auth import get_current_user
from src.db.models.user import User


router = APIRouter(tags=['Users'])


router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/me")
async def read_current_user(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "roles": user.roles
    }

@router.get("/admin")
async def admin_route(user: User = Depends(get_current_user)):
    if "admin" not in user.roles.split(","):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"message": "Admin access granted"}
