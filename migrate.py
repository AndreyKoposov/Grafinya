import asyncio

from src.app.db.engine import engine, base
from src.app.models import *


async def migrate():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(migrate())
