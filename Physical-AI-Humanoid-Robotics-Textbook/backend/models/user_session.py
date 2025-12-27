"""
UserSession Model

Represents anonymous user sessions for the RAG chatbot.
Each session is identified by a UUID and tracks session activity.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class UserSession(Base):
    """
    Anonymous user session model.

    Sessions are created on first interaction and persist across page reloads
    using localStorage in the frontend. No authentication is required.

    Attributes:
        id (UUID): Unique session identifier (primary key)
        created_at (DateTime): Session creation timestamp
        last_active_at (DateTime): Last activity timestamp
        conversations (relationship): All conversations for this session
    """

    __tablename__ = "user_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique session identifier",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Session creation timestamp",
    )

    last_active_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Last activity timestamp",
    )

    # Relationships
    conversations = relationship(
        "Conversation",
        back_populates="session",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    profile = relationship(
        "UserProfile",
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<UserSession(id={self.id}, created_at={self.created_at})>"

    def update_activity(self) -> None:
        """Update last_active_at to current timestamp."""
        self.last_active_at = datetime.utcnow()
