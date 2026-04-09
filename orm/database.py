from global_variables.token import SQLALCHEMY_DATABASE_URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import select, insert, update, delete, and_, create_engine, desc, asc, text

# fix — Base объявляем ДО engine
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL)
Async_Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
async_session = Async_Session()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Лёгкая миграция схемы (без Alembic) для существующих БД
        # Добавляем поле роли Белбина, если таблица уже была создана раньше.
        await conn.execute(
            text('ALTER TABLE "AlmostCurator" ADD COLUMN IF NOT EXISTS belbin_role VARCHAR(64)')
        )
    await engine.dispose()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
