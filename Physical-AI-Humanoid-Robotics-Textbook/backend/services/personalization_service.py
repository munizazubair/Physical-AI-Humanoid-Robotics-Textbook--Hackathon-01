"""
Personalization Service

Provides personalized learning assistance including interest detection,
knowledge level tracking, and chapter recommendations.
"""

from typing import Dict, List, Optional, Any
import uuid
import logging
from collections import Counter
import re

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.user_session import UserSession
from models.user_profile import UserProfile, KnowledgeLevel
from models.message import Message
from models.conversation import Conversation
from services.gemini_service import gemini_service

logger = logging.getLogger(__name__)


class PersonalizationService:
    """
    Service for user personalization and adaptive learning.

    Tracks user interests, knowledge level, and provides personalized
    recommendations and greetings.
    """

    def __init__(self):
        """Initialize personalization service."""
        self.gemini = gemini_service

    async def get_or_create_profile(
        self,
        session_id: uuid.UUID,
        db: AsyncSession
    ) -> UserProfile:
        """
        Get existing user profile or create a new one.

        Args:
            session_id: User session UUID
            db: Database session

        Returns:
            UserProfile instance
        """
        # Check if profile exists
        query = select(UserProfile).where(UserProfile.session_id == session_id)
        result = await db.execute(query)
        profile = result.scalar_one_or_none()

        if profile:
            return profile

        # Create new profile
        profile = UserProfile.create_for_session(session_id)
        db.add(profile)
        await db.flush()

        logger.info(f"Created new user profile for session {session_id}")
        return profile

    async def analyze_interests(
        self,
        session_id: uuid.UUID,
        db: AsyncSession
    ) -> List[str]:
        """
        Analyze user interests from recent conversation history.

        Extracts topics and keywords from the last 10 user messages.

        Args:
            session_id: User session UUID
            db: Database session

        Returns:
            List of detected interest topics
        """
        # Get last 10 user messages
        query = (
            select(Message)
            .join(Conversation)
            .where(
                Conversation.session_id == session_id,
                Message.role == "user"
            )
            .order_by(Message.created_at.desc())
            .limit(10)
        )

        result = await db.execute(query)
        messages = result.scalars().all()

        if not messages:
            return []

        # Extract keywords from messages
        all_text = " ".join([msg.content for msg in messages])
        interests = self._extract_keywords(all_text)

        # Update user profile
        profile = await self.get_or_create_profile(session_id, db)
        for interest in interests:
            profile.add_interest(interest)

        await db.commit()

        logger.info(f"Detected {len(interests)} interests for session {session_id}")
        return interests

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords and topics from text.

        Uses pattern matching to identify robotics-related topics.

        Args:
            text: Input text to analyze

        Returns:
            List of extracted keywords/topics
        """
        # Common robotics topics to look for
        topic_patterns = {
            "ros": r"\b(ros\s*2?|robot\s*operating\s*system)\b",
            "digital-twin": r"\b(digital\s*twin|simulation|gazebo)\b",
            "isaac": r"\b(nvidia\s*)?isaac\b",
            "vla": r"\b(vla|vision\s*language\s*action)\b",
            "humanoid": r"\b(humanoid|bipedal|anthropomorphic)\b",
            "slam": r"\b(slam|simultaneous\s*localization)\b",
            "navigation": r"\b(navigation|path\s*planning|obstacle\s*avoidance)\b",
            "perception": r"\b(perception|computer\s*vision|object\s*detection)\b",
            "control": r"\b(control|motion\s*planning|trajectory)\b",
            "learning": r"\b(machine\s*learning|deep\s*learning|reinforcement)\b",
        }

        detected_topics = []
        text_lower = text.lower()

        for topic, pattern in topic_patterns.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected_topics.append(topic)

        return detected_topics[:5]  # Return top 5

    async def get_greeting(
        self,
        session_id: uuid.UUID,
        db: AsyncSession
    ) -> str:
        """
        Generate a personalized greeting for the user.

        Returns a generic greeting for new users or a personalized one
        mentioning recent topics for returning users.

        Args:
            session_id: User session UUID
            db: AsyncSession

        Returns:
            Greeting string
        """
        profile = await self.get_or_create_profile(session_id, db)

        # Check if user has previous conversations
        query = (
            select(Conversation)
            .where(Conversation.session_id == session_id)
        )
        result = await db.execute(query)
        conversations = result.scalars().all()

        # New user - generic greeting
        if not conversations or len(conversations) == 0:
            return "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics Textbook. Ask me anything!"

        # Returning user - personalized greeting
        interests_summary = profile.get_interests_summary()

        greetings = [
            f"Welcome back! I see you've been exploring {interests_summary}. How can I help you today?",
            f"Great to see you again! Last time we discussed {interests_summary}. What would you like to learn about now?",
            f"Hello again! You've shown interest in {interests_summary}. Ready to continue learning?",
        ]

        # Use first greeting for simplicity
        return greetings[0]

    async def infer_knowledge_level(
        self,
        session_id: uuid.UUID,
        db: AsyncSession
    ) -> KnowledgeLevel:
        """
        Infer user knowledge level from question patterns.

        Analyzes question complexity, length, and terminology to determine
        if user is beginner, intermediate, or advanced.

        Args:
            session_id: User session UUID
            db: Database session

        Returns:
            Inferred KnowledgeLevel
        """
        # Get last 5 user messages
        query = (
            select(Message)
            .join(Conversation)
            .where(
                Conversation.session_id == session_id,
                Message.role == "user"
            )
            .order_by(Message.created_at.desc())
            .limit(5)
        )

        result = await db.execute(query)
        messages = result.scalars().all()

        if not messages or len(messages) < 2:
            return KnowledgeLevel.BEGINNER

        # Analyze complexity
        avg_length = sum(len(msg.content.split()) for msg in messages) / len(messages)
        technical_terms = 0

        # Technical terminology indicators
        advanced_terms = [
            "architecture", "algorithm", "implementation", "optimization",
            "configuration", "deployment", "integration", "framework",
            "parameter", "latency", "throughput", "scalability"
        ]

        all_text = " ".join([msg.content for msg in messages]).lower()
        technical_terms = sum(1 for term in advanced_terms if term in all_text)

        # Determine level
        if avg_length > 20 and technical_terms >= 3:
            level = KnowledgeLevel.ADVANCED
        elif avg_length > 10 or technical_terms >= 1:
            level = KnowledgeLevel.INTERMEDIATE
        else:
            level = KnowledgeLevel.BEGINNER

        # Update profile
        profile = await self.get_or_create_profile(session_id, db)
        profile.set_knowledge_level(level)
        await db.commit()

        logger.info(f"Inferred knowledge level {level} for session {session_id}")
        return level

    async def get_recommendations(
        self,
        session_id: uuid.UUID,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """
        Get personalized chapter recommendations based on interests and history.

        Args:
            session_id: User session UUID
            db: Database session

        Returns:
            List of recommendation dictionaries with chapter and reason
        """
        profile = await self.get_or_create_profile(session_id, db)

        # Map interests to recommended chapters
        interest_to_chapters = {
            "ros": {
                "chapter": 1,
                "title": "Introduction to ROS 2",
                "reason": "Learn the fundamentals of the Robot Operating System"
            },
            "digital-twin": {
                "chapter": 3,
                "title": "Digital Twins and Simulation",
                "reason": "Explore virtual representations and simulation techniques"
            },
            "isaac": {
                "chapter": 4,
                "title": "NVIDIA Isaac Platform",
                "reason": "Discover NVIDIA's robotics simulation and development tools"
            },
            "vla": {
                "chapter": 5,
                "title": "Vision-Language-Action Models",
                "reason": "Master cutting-edge multimodal AI for robotics"
            },
            "humanoid": {
                "chapter": 2,
                "title": "Humanoid Robot Design",
                "reason": "Understand the principles of humanoid robot architecture"
            },
        }

        recommendations = []

        # Add recommendations based on interests
        if profile.interests:
            for interest in profile.interests[:3]:  # Top 3 interests
                if interest in interest_to_chapters:
                    chapter_info = interest_to_chapters[interest]
                    # Skip if already visited
                    if chapter_info["chapter"] not in (profile.visited_chapters or []):
                        recommendations.append(chapter_info)

        # Add default recommendations if not enough
        if len(recommendations) < 3:
            default_chapters = [
                {
                    "chapter": 1,
                    "title": "Introduction to ROS 2",
                    "reason": "Start with the fundamentals of robot programming"
                },
                {
                    "chapter": 5,
                    "title": "Vision-Language-Action Models",
                    "reason": "Explore the latest in AI-powered robotics"
                },
            ]

            for chapter in default_chapters:
                if chapter not in recommendations and len(recommendations) < 5:
                    if chapter["chapter"] not in (profile.visited_chapters or []):
                        recommendations.append(chapter)

        return recommendations[:5]  # Return max 5


# Global instance
personalization_service = PersonalizationService()
