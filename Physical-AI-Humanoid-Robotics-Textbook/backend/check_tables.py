"""
Check what tables exist in the database
"""
import asyncio
from sqlalchemy import text
from database import AsyncSessionLocal

async def check_tables():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = result.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")

asyncio.run(check_tables())
