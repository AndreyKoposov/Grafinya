import asyncio

from src.app.db.engine import engine, base
from src.app.models import user


async def migrate():
    print("Trying connect...")

    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(base.metadata.create_all)
        print(f"Created <{user.User.__tablename__}>")

        print("Closing connection...")

    print("Connection closed")
    await engine.dispose()
    print("Migration completed!")


if __name__ == '__main__':
    print("Starting migration...")
    asyncio.run(migrate())
