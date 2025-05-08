from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routers import auth, users, tasks, db
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
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
              version='0.4.0',
              openapi_prefix='/api',
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost", 
                   "http://127.0.0.1:3000", "http://127.0.0.1",
                   "http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"]
)
