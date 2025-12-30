"""
Conversation Model

Represents a conversation thread within a user session.
Each conversation can contain multiple messages.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Conversation(Base):
    """
    Conversation model for organizing chat messages.

    Each user session can have multiple conversations. Conversations
    allow users to start fresh topics while preserving history.

    Attributes:
        id (UUID): Unique conversation identifier (primary key)
        session_id (UUID): Foreign key to user_sessions
        title (str): Auto-generated conversation title (first 50 chars of first message)
        created_at (DateTime): Conversation creation timestamp
        session (relationship): Parent user session
        messages (relationship): All messages in this conversation
    """

    __tablename__ = "conversations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique conversation identifier",
    )

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to user_sessions",
    )

    title = Column(
        String(255),
        nullable=True,
        comment="Auto-generated conversation title",
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Soft delete flag",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Conversation creation timestamp",
    )

    # Relationships
    session = relationship(
        "UserSession",
        back_populates="conversations",
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Message.created_at",
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, title={self.title}, created_at={self.created_at})>"

    def set_title_from_first_message(self, message_content: str) -> None:
        """
        Set conversation title from the first user message.

        Args:
            message_content (str): Content of the first message
        """
        if not self.title and message_content:
            self.title = message_content[:50] + ("..." if len(message_content) > 50 else "")
