"""
Create missing tables (feedback, rate_limits, user_profiles) manually
"""
import asyncio
from sqlalchemy import text
from database import AsyncSessionLocal

async def create_tables():
    async with AsyncSessionLocal() as db:
        # Create user_profiles table
        print("Creating user_profiles table...")
        await db.execute(text("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                session_id UUID NOT NULL REFERENCES user_sessions(id) ON DELETE CASCADE,
                interests JSONB,
                knowledge_level VARCHAR(50) NOT NULL DEFAULT 'beginner',
                visited_chapters JSONB,
                total_questions INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(session_id)
            );
        """))
        print("Created user_profiles")

        # Create feedback table
        print("Creating feedback table...")
        await db.execute(text("""
            CREATE TABLE IF NOT EXISTS feedback (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
                rating INTEGER NOT NULL CHECK (rating IN (-1, 1)),
                comment TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """))
        await db.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_feedback_message_id ON feedback(message_id);
        """))
        print("Created feedback")

        # Create rate_limits table
        print("Creating rate_limits table...")
        await db.execute(text("""
            CREATE TABLE IF NOT EXISTS rate_limits (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                session_id UUID NOT NULL REFERENCES user_sessions(id) ON DELETE CASCADE,
                request_count INTEGER NOT NULL DEFAULT 0,
                window_start TIMESTAMP NOT NULL,
                UNIQUE(session_id, window_start)
            );
        """))
        await db.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_rate_limits_session_id ON rate_limits(session_id);
        """))
        await db.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_rate_limits_window_start ON rate_limits(window_start);
        """))
        print("Created rate_limits")

        await db.commit()
        print("\nAll tables created successfully!")

asyncio.run(create_tables())
