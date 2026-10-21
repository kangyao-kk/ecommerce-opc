
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ecommerce_opc.infrastructure.database.engine import engine


AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """提供一个具有独立事务边界的异步数据库 Session。"""
    async with AsyncSessionFactory() as session:
        async with session.begin():
            yield session
