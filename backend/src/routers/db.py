from fastapi import APIRouter
from src.db.session import setup_database
from src.dependencies.auth import authDep_admin

router = APIRouter(prefix='/db', tags=['Data base'])

@router.post("/reset_db", summary="Перезагрузить базу данных")
async def reset_db(user: authDep_admin):
    res = await setup_database()
    return res
