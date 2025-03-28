from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routers import auth, users, tasks, db

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis:///6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi_cache")

    # Подключение роутеров
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(tasks.router)
    app.include_router(db.router)

    yield


app = FastAPI(lifespan=lifespan, 
              title="To-do app", 
              summary="To-do application's API",
              version='0.4.0'
              )
