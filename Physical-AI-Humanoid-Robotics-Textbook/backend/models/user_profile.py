"""
UserProfile Model

Stores user personalization data including interests, knowledge level, and reading history.
"""

from sqlalchemy import Column, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from database import Base


class KnowledgeLevel(str, enum.Enum):
    """Enumeration for user knowledge levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class UserProfile(Base):
    """
    User profile model for personalization.

    Tracks user interests, knowledge level, and visited chapters to provide
    personalized learning assistance and recommendations.
    """

    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_sessions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )

    # User interests extracted from conversation topics
    interests = Column(
        JSONB,
        nullable=False,
        default=list,
        comment="List of detected user interests/topics"
    )

    # User knowledge level inferred from question complexity
    knowledge_level = Column(
        SQLEnum(KnowledgeLevel),
        nullable=False,
        default=KnowledgeLevel.BEGINNER,
        comment="User's inferred knowledge level"
    )

    # Chapters the user has asked about
    visited_chapters = Column(
        JSONB,
        nullable=False,
        default=list,
        comment="List of chapter numbers visited by user"
    )

    # Additional metadata
    total_questions = Column(
        String,
        default="0",
        nullable=False,
        comment="Total questions asked by user"
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship("UserSession", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(session_id={self.session_id}, level={self.knowledge_level}, interests={len(self.interests)})>"

    def add_interest(self, interest: str):
        """Add a new interest to the user's profile."""
        if not self.interests:
            self.interests = []

        # Avoid duplicates and limit to top 10 interests
        if interest not in self.interests:
            self.interests.append(interest)
            # Keep only most recent 10 interests
            if len(self.interests) > 10:
                self.interests = self.interests[-10:]
            self.updated_at = datetime.utcnow()

    def add_visited_chapter(self, chapter_number: int):
        """Add a chapter to the visited chapters list."""
        if not self.visited_chapters:
            self.visited_chapters = []

        # Avoid duplicates
        if chapter_number not in self.visited_chapters:
            self.visited_chapters.append(chapter_number)
            self.updated_at = datetime.utcnow()

    def set_knowledge_level(self, level: KnowledgeLevel):
        """Update the user's knowledge level."""
        if level != self.knowledge_level:
            self.knowledge_level = level
            self.updated_at = datetime.utcnow()

    def increment_question_count(self):
        """Increment the total question count."""
        try:
            count = int(self.total_questions)
            self.total_questions = str(count + 1)
        except ValueError:
            self.total_questions = "1"
        self.updated_at = datetime.utcnow()

    @classmethod
    def create_for_session(cls, session_id: uuid.UUID):
        """
        Create a new user profile for a session.

        Args:
            session_id: UUID of the user session

        Returns:
            UserProfile instance
        """
        return cls(
            session_id=session_id,
            interests=[],
            knowledge_level=KnowledgeLevel.BEGINNER,
            visited_chapters=[],
            total_questions="0"
        )

    def get_interests_summary(self) -> str:
        """
        Get a human-readable summary of user interests.

        Returns:
            Comma-separated string of interests
        """
        if not self.interests or len(self.interests) == 0:
            return "general robotics topics"

        return ", ".join(self.interests[:5])  # Top 5 interests

    def get_visited_chapters_summary(self) -> str:
        """
        Get a human-readable summary of visited chapters.

        Returns:
            Comma-separated string of chapter numbers
        """
        if not self.visited_chapters or len(self.visited_chapters) == 0:
            return "no chapters yet"

        sorted_chapters = sorted(self.visited_chapters)
        return ", ".join([f"Chapter {ch}" for ch in sorted_chapters[:5]])  # Top 5 chapters
