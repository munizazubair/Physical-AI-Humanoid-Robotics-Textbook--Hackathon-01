"""
Message Model

Represents individual chat messages (user questions and assistant responses).
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from database import Base


class Message(Base):
    """
    Chat message model for storing user questions and assistant responses.

    Messages are the core content of conversations, storing both user
    input and RAG-generated responses with citations.

    Attributes:
        id (UUID): Unique message identifier (primary key)
        conversation_id (UUID): Foreign key to conversations
        role (str): Message role - 'user' or 'assistant'
        content (str): Message text content
        citations (dict): Citations for assistant responses (chapter, section, page)
        created_at (DateTime): Message timestamp
        conversation (relationship): Parent conversation
    """

    __tablename__ = "messages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique message identifier",
    )

    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to conversations",
    )

    role = Column(
        String(20),
        nullable=False,
        comment="Message role: 'user' or 'assistant'",
    )

    content = Column(
        Text,
        nullable=False,
        comment="Message text content",
    )

    citations = Column(
        JSONB,
        nullable=True,
        comment="Citations for assistant responses (JSON array of {chapter, section, page})",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
        comment="Message timestamp",
    )

    # Relationships
    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )

    feedback = relationship(
        "Feedback",
        back_populates="message",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'assistant')",
            name="check_message_role",
        ),
    )

    def __repr__(self) -> str:
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message(id={self.id}, role={self.role}, content='{preview}')>"

    @classmethod
    def create_user_message(cls, conversation_id: uuid.UUID, content: str) -> "Message":
        """
        Factory method to create a user message.

        Args:
            conversation_id (UUID): Parent conversation ID
            content (str): User's question

        Returns:
            Message: New user message instance
        """
        return cls(
            conversation_id=conversation_id,
            role="user",
            content=content,
            citations=None,
        )

    @classmethod
    def create_assistant_message(
        cls,
        conversation_id: uuid.UUID,
        content: str,
        citations: list[dict] = None,
    ) -> "Message":
        """
        Factory method to create an assistant message with citations.

        Args:
            conversation_id (UUID): Parent conversation ID
            content (str): Assistant's response
            citations (list[dict]): List of citation objects with chapter/section/page

        Returns:
            Message: New assistant message instance
        """
        return cls(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            citations=citations or [],
        )
