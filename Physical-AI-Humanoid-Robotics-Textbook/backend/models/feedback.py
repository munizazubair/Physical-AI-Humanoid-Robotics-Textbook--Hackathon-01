"""
Feedback Model

Stores user feedback (thumbs up/down ratings) for assistant messages
to help improve the RAG chatbot's responses.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Feedback(Base):
    """
    User feedback model for assistant messages.

    Tracks thumbs up (+1) and thumbs down (-1) ratings with optional comments
    to help improve response quality.

    Attributes:
        id (UUID): Unique feedback identifier
        message_id (UUID): Foreign key to Message table
        rating (Integer): 1 for thumbs up, -1 for thumbs down
        comment (Text): Optional user comment (nullable)
        created_at (DateTime): Timestamp of feedback submission
        message (relationship): Related Message object
    """

    __tablename__ = "feedback"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique feedback identifier",
    )

    message_id = Column(
        UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Message this feedback is for",
    )

    rating = Column(
        Integer,
        nullable=False,
        comment="Rating: 1 for thumbs up, -1 for thumbs down",
    )

    comment = Column(
        Text,
        nullable=True,
        comment="Optional user comment",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Feedback submission timestamp",
    )

    # Relationships
    message = relationship(
        "Message",
        back_populates="feedback",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Feedback(id={self.id}, message_id={self.message_id}, rating={self.rating})>"

    @classmethod
    def create(cls, message_id: uuid.UUID, rating: int, comment: str = None):
        """
        Create a new Feedback instance.

        Args:
            message_id (UUID): ID of the message being rated
            rating (int): 1 for thumbs up, -1 for thumbs down
            comment (str, optional): User's optional comment

        Returns:
            Feedback: New feedback instance

        Raises:
            ValueError: If rating is not 1 or -1
        """
        if rating not in (1, -1):
            raise ValueError("Rating must be 1 (thumbs up) or -1 (thumbs down)")

        return cls(
            message_id=message_id,
            rating=rating,
            comment=comment,
        )

    def is_positive(self) -> bool:
        """Check if feedback is positive (thumbs up)."""
        return self.rating == 1

    def is_negative(self) -> bool:
        """Check if feedback is negative (thumbs down)."""
        return self.rating == -1
