from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from pfsw_gestao.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
