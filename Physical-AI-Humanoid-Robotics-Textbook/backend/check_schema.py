"""Check database schema"""
import asyncio
from database import engine
from sqlalchemy import text

async def check():
    async with engine.connect() as conn:
        result = await conn.execute(text("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_name = 'user_profiles' AND column_name = 'total_questions'
        """))
        row = result.fetchone()
        if row:
            print(f"Column: {row[0]}, Type: {row[1]}, Default: {row[2]}")
        else:
            print("Column not found")

asyncio.run(check())
