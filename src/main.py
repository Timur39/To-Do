from fastapi import FastAPI
from src.routers import auth, users

app = FastAPI()

# Подключение роутеров
app.include_router(auth.router)
app.include_router(users.router)

