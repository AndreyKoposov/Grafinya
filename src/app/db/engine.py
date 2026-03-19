from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.app.config import DB_USER, DB_PSWRD, DB_HOST, DB_PORT, DB_NAME


engine = create_async_engine(f"postgresql+asyncpg://"
                             f"{DB_USER}:{DB_PSWRD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
maker = async_sessionmaker(bind=engine)

def get_session() -> AsyncSession:
    return maker()
