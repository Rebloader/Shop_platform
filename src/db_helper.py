from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.config import settings

engine = create_async_engine(
    settings.DB_URL,
    echo=True)

AsyncSession = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_async_session() -> AsyncSession:
    async with AsyncSession() as async_session:
        yield async_session