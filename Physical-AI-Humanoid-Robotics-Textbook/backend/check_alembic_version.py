"""Check alembic version"""
import asyncio
from sqlalchemy import text
from database import AsyncSessionLocal

async def check():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text('SELECT version_num FROM alembic_version'))
        version = r.scalar()
        print(f"Alembic version in DB: {version}")

asyncio.run(check())
