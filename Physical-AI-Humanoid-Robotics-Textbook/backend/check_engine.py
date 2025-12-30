"""Check database engine settings"""
import asyncio
from database import engine

async def check():
    print("=== Engine Configuration ===")
    print(f"URL: {engine.url}")
    print(f"Pool class: {engine.pool.__class__.__name__}")
    print(f"Echo: {engine.echo}")

    # Check connect_args
    print(f"\nConnect args:")
    if hasattr(engine, 'dialect'):
        print(f"  Dialect: {engine.dialect.name}")
        if hasattr(engine.dialect, 'create_connect_args'):
            # Try to see what connect_args were passed
            print(f"  Engine._connect: {dir(engine)}")

    # Try to get a connection and check its settings
    async with engine.connect() as conn:
        print(f"\nConnection class: {conn.__class__.__name__}")

        # Check if we can access the raw connection
        raw_conn = await conn.get_raw_connection()
        print(f"Raw connection: {raw_conn.__class__.__name__}")

        if hasattr(raw_conn, '_holder'):
            holder = raw_conn._holder
            if hasattr(holder, '_con'):
                asyncpg_conn = holder._con
                print(f"AsyncPG connection: {asyncpg_conn}")

asyncio.run(check())
