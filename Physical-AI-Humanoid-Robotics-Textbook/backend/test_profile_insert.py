"""Test UserProfile insertion"""
import asyncio
import uuid
from database import AsyncSessionLocal
from models.user_profile import UserProfile, KnowledgeLevel
from models.user_session import UserSession

async def test():
    async with AsyncSessionLocal() as db:
        try:
            # Create session first
            session = UserSession()
            db.add(session)
            await db.flush()

            # Create profile
            profile = UserProfile(
                session_id=session.id,
                interests=[],
                knowledge_level=KnowledgeLevel.BEGINNER,
                visited_chapters=[],
                total_questions=0  # Integer!
            )
            db.add(profile)
            await db.flush()
            await db.commit()

            print(f"✅ SUCCESS! Created profile: {profile.id}")
            print(f"   total_questions = {profile.total_questions} (type: {type(profile.total_questions)})")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            await db.rollback()

asyncio.run(test())
