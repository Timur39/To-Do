from src.db.session import Base, engine


class DBService:
    # Удаляем все данные из БД
    @staticmethod
    async def setup_database() -> dict[str, str]:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        return {"status": "Database was successfully reset"}
