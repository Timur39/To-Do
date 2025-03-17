from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from src.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


async def get_async_session():
    async with async_session_maker() as session:
        yield session

# TODO: Убрать в utils
async def setup_database() -> dict[str, str]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'status': 'Database was successfully reset'}


