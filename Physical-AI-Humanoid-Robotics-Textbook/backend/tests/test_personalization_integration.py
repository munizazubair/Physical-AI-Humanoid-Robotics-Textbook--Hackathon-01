"""
Integration Tests for Personalization Features

Tests the complete personalization workflow including:
- Interest detection from conversation history
- Knowledge level inference
- Personalized greetings
- Chapter recommendations
- Adaptive response complexity
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from models.user_session import UserSession
from models.user_profile import UserProfile, KnowledgeLevel
from models.conversation import Conversation
from models.message import Message
from services.personalization_service import personalization_service


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_session():
    """Create a test database session."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_session(db_session: AsyncSession):
    """Create a test user session."""
    session = UserSession(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        last_active_at=datetime.utcnow()
    )
    db_session.add(session)
    await db_session.commit()
    await db_session.refresh(session)
    return session


@pytest.fixture
async def test_conversation(db_session: AsyncSession, test_session: UserSession):
    """Create a test conversation."""
    conversation = Conversation(
        id=uuid.uuid4(),
        session_id=test_session.id,
        title="Test Conversation",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(conversation)
    await db_session.commit()
    await db_session.refresh(conversation)
    return conversation


@pytest.mark.asyncio
async def test_create_user_profile(db_session: AsyncSession, test_session: UserSession):
    """Test creating a new user profile."""
    profile = await personalization_service.get_or_create_profile(
        test_session.id, db_session
    )

    assert profile is not None
    assert profile.session_id == test_session.id
    assert profile.knowledge_level == KnowledgeLevel.BEGINNER
    assert profile.interests == []
    assert profile.visited_chapters == []
    assert profile.total_questions == "0"


@pytest.mark.asyncio
async def test_analyze_interests_ros(
    db_session: AsyncSession,
    test_session: UserSession,
    test_conversation: Conversation
):
    """Test interest detection for ROS-related questions."""
    # Add messages about ROS
    messages = [
        "What is ROS 2?",
        "How do I install the Robot Operating System?",
        "Explain ROS nodes and topics",
    ]

    for msg_content in messages:
        msg = Message.create_user_message(
            conversation_id=test_conversation.id,
            content=msg_content
        )
        db_session.add(msg)

    await db_session.commit()

    # Analyze interests
    interests = await personalization_service.analyze_interests(
        test_session.id, db_session
    )

    assert "ros" in interests
    assert len(interests) > 0


@pytest.mark.asyncio
async def test_analyze_interests_multiple_topics(
    db_session: AsyncSession,
    test_session: UserSession,
    test_conversation: Conversation
):
    """Test interest detection for multiple topics."""
    # Add messages about various topics
    messages = [
        "What is a digital twin in robotics?",
        "How does NVIDIA Isaac work?",
        "Explain vision-language-action models",
        "What is SLAM and how does it work?",
        "Tell me about humanoid robot design",
    ]

    for msg_content in messages:
        msg = Message.create_user_message(
            conversation_id=test_conversation.id,
            content=msg_content
        )
        db_session.add(msg)

    await db_session.commit()

    # Analyze interests
    interests = await personalization_service.analyze_interests(
        test_session.id, db_session
    )

    # Should detect multiple topics
    assert len(interests) >= 3
    assert any(topic in interests for topic in ["digital-twin", "isaac", "vla", "slam", "humanoid"])


@pytest.mark.asyncio
async def test_knowledge_level_beginner(
    db_session: AsyncSession,
    test_session: UserSession,
    test_conversation: Conversation
):
    """Test knowledge level inference for beginner users."""
    # Add simple, short questions
    messages = [
        "What is ROS?",
        "How do robots work?",
        "Tell me about AI",
    ]

    for msg_content in messages:
        msg = Message.create_user_message(
            conversation_id=test_conversation.id,
            content=msg_content
        )
        db_session.add(msg)

    await db_session.commit()

    # Infer knowledge level
    level = await personalization_service.infer_knowledge_level(
        test_session.id, db_session
    )

    assert level == KnowledgeLevel.BEGINNER


@pytest.mark.asyncio
async def test_knowledge_level_intermediate(
    db_session: AsyncSession,
    test_session: UserSession,
    test_conversation: Conversation
):
    """Test knowledge level inference for intermediate users."""
    # Add moderately complex questions
    messages = [
        "How does the ROS 2 middleware architecture enable inter-process communication?",
        "What are the key differences between Gazebo and Isaac Sim for robot simulation?",
        "Explain the implementation of SLAM algorithms in mobile robotics",
    ]

    for msg_content in messages:
        msg = Message.create_user_message(
            conversation_id=test_conversation.id,
            content=msg_content
        )
        db_session.add(msg)

    await db_session.commit()

    # Infer knowledge level
    level = await personalization_service.infer_knowledge_level(
        test_session.id, db_session
    )

    assert level in [KnowledgeLevel.INTERMEDIATE, KnowledgeLevel.ADVANCED]


@pytest.mark.asyncio
async def test_knowledge_level_advanced(
    db_session: AsyncSession,
    test_session: UserSession,
    test_conversation: Conversation
):
    """Test knowledge level inference for advanced users."""
    # Add complex, technical questions
    messages = [
        "What are the performance optimization strategies for real-time trajectory planning in high-DOF manipulators considering kinematic constraints and collision avoidance?",
        "How do transformer-based vision-language-action models handle temporal dependencies in multimodal action sequences, and what are the architectural trade-offs between latency and accuracy?",
        "Discuss the implementation challenges of deploying graph-based SLAM algorithms on resource-constrained embedded systems with considerations for loop closure detection and map optimization",
    ]

    for msg_content in messages:
        msg = Message.create_user_message(
            conversation_id=test_conversation.id,
            content=msg_content
        )
        db_session.add(msg)

    await db_session.commit()

    # Infer knowledge level
    level = await personalization_service.infer_knowledge_level(
        test_session.id, db_session
    )

    assert level == KnowledgeLevel.ADVANCED


@pytest.mark.asyncio
async def test_personalized_greeting_new_user(
    db_session: AsyncSession,
    test_session: UserSession
):
    """Test greeting for new users."""
    greeting = await personalization_service.get_greeting(
        test_session.id, db_session
    )

    # Should be a generic greeting for new users
    assert "AI assistant" in greeting or "Physical AI" in greeting
    assert len(greeting) > 0


@pytest.mark.asyncio
async def test_personalized_greeting_returning_user(
    db_session: AsyncSession,
    test_session: UserSession,
    test_conversation: Conversation
):
    """Test greeting for returning users with interests."""
    # Add messages to create history
    msg = Message.create_user_message(
        conversation_id=test_conversation.id,
        content="Tell me about ROS 2"
    )
    db_session.add(msg)
    await db_session.commit()

    # Analyze interests first
    await personalization_service.analyze_interests(test_session.id, db_session)

    # Get personalized greeting
    greeting = await personalization_service.get_greeting(
        test_session.id, db_session
    )

    # Should mention interests or be personalized
    assert "Welcome back" in greeting or "see you" in greeting or "again" in greeting
    assert len(greeting) > 0


@pytest.mark.asyncio
async def test_chapter_recommendations_based_on_interests(
    db_session: AsyncSession,
    test_session: UserSession,
    test_conversation: Conversation
):
    """Test chapter recommendations based on user interests."""
    # Create profile with specific interests
    profile = await personalization_service.get_or_create_profile(
        test_session.id, db_session
    )
    profile.add_interest("ros")
    profile.add_interest("isaac")
    profile.add_interest("vla")
    await db_session.commit()

    # Get recommendations
    recommendations = await personalization_service.get_recommendations(
        test_session.id, db_session
    )

    assert len(recommendations) > 0
    assert len(recommendations) <= 5

    # Check recommendation structure
    for rec in recommendations:
        assert "chapter" in rec
        assert "title" in rec
        assert "reason" in rec
        assert isinstance(rec["chapter"], int)
        assert isinstance(rec["title"], str)
        assert isinstance(rec["reason"], str)


@pytest.mark.asyncio
async def test_recommendations_exclude_visited_chapters(
    db_session: AsyncSession,
    test_session: UserSession
):
    """Test that recommendations exclude already visited chapters."""
    # Create profile with interests and visited chapters
    profile = await personalization_service.get_or_create_profile(
        test_session.id, db_session
    )
    profile.add_interest("ros")
    profile.add_visited_chapter(1)  # Mark chapter 1 as visited
    await db_session.commit()

    # Get recommendations
    recommendations = await personalization_service.get_recommendations(
        test_session.id, db_session
    )

    # Should not recommend chapter 1
    recommended_chapters = [rec["chapter"] for rec in recommendations]
    assert 1 not in recommended_chapters


@pytest.mark.asyncio
async def test_profile_persistence(
    db_session: AsyncSession,
    test_session: UserSession
):
    """Test that user profile persists correctly."""
    # Create and update profile
    profile1 = await personalization_service.get_or_create_profile(
        test_session.id, db_session
    )
    profile1.add_interest("ros")
    profile1.add_interest("isaac")
    profile1.set_knowledge_level(KnowledgeLevel.INTERMEDIATE)
    profile1.add_visited_chapter(1)
    profile1.increment_question_count()
    await db_session.commit()

    # Retrieve profile again
    profile2 = await personalization_service.get_or_create_profile(
        test_session.id, db_session
    )

    # Should have same data
    assert profile2.id == profile1.id
    assert "ros" in profile2.interests
    assert "isaac" in profile2.interests
    assert profile2.knowledge_level == KnowledgeLevel.INTERMEDIATE
    assert 1 in profile2.visited_chapters
    assert profile2.total_questions == "1"


@pytest.mark.asyncio
async def test_interests_summary(db_session: AsyncSession, test_session: UserSession):
    """Test interests summary generation."""
    profile = await personalization_service.get_or_create_profile(
        test_session.id, db_session
    )
    profile.add_interest("ros")
    profile.add_interest("slam")
    profile.add_interest("perception")
    await db_session.commit()

    summary = profile.get_interests_summary()

    assert isinstance(summary, str)
    assert "ros" in summary or "slam" in summary or "perception" in summary


@pytest.mark.asyncio
async def test_empty_interests_summary(
    db_session: AsyncSession,
    test_session: UserSession
):
    """Test interests summary with no interests."""
    profile = await personalization_service.get_or_create_profile(
        test_session.id, db_session
    )

    summary = profile.get_interests_summary()

    assert isinstance(summary, str)
    assert "general" in summary.lower() or "robotics" in summary.lower()
