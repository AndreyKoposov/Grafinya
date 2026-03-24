from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.app.config import DB_USER, DB_PSWRD, DB_HOST, DB_PORT, DB_NAME


db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PSWRD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(db_url)
maker = async_sessionmaker(bind=engine)
base = declarative_base()

async def get_session():
    async with maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
