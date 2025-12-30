"""
RateLimit Model

Tracks API request counts per session per time window for rate limiting.
"""

import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class RateLimit(Base):
    """
    Rate limit tracking model.

    Tracks the number of requests per session per hour to enforce
    rate limits and prevent abuse.

    Attributes:
        id (UUID): Unique rate limit record identifier
        session_id (UUID): Foreign key to UserSession table
        request_count (Integer): Number of requests in current window
        window_start (DateTime): Start of the current time window
        session (relationship): Related UserSession object
    """

    __tablename__ = "rate_limits"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique rate limit record identifier",
    )

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="User session being rate limited",
    )

    request_count = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of requests in current window",
    )

    window_start = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="Start of the current time window (hourly)",
    )

    # Relationships
    session = relationship(
        "UserSession",
        back_populates="rate_limits",
        lazy="selectin",
    )

    # Unique constraint: one record per session per window
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "window_start",
            name="uq_session_window",
        ),
    )

    def __repr__(self) -> str:
        return f"<RateLimit(session_id={self.session_id}, count={self.request_count}, window={self.window_start})>"

    @classmethod
    def get_current_window_start(cls) -> datetime:
        """
        Get the start of the current hour window.

        Returns:
            datetime: Start of current hour (minutes/seconds/microseconds set to 0)
        """
        now = datetime.utcnow()
        return now.replace(minute=0, second=0, microsecond=0)

    @classmethod
    def create_for_session(cls, session_id: uuid.UUID):
        """
        Create a new rate limit record for a session.

        Args:
            session_id (UUID): ID of the user session

        Returns:
            RateLimit: New rate limit instance
        """
        return cls(
            session_id=session_id,
            request_count=0,
            window_start=cls.get_current_window_start(),
        )

    def increment(self) -> None:
        """Increment the request count for this window."""
        self.request_count += 1

    def is_limit_exceeded(self, limit: int = 20) -> bool:
        """
        Check if the rate limit has been exceeded.

        Args:
            limit (int): Maximum requests allowed per window (default: 20)

        Returns:
            bool: True if limit exceeded, False otherwise
        """
        return self.request_count >= limit

    def is_window_expired(self) -> bool:
        """
        Check if the current window has expired.

        Returns:
            bool: True if window has expired, False otherwise
        """
        now = datetime.utcnow()
        window_end = self.window_start + timedelta(hours=1)
        return now >= window_end

    def get_retry_after_seconds(self) -> int:
        """
        Get the number of seconds until the window resets.

        Returns:
            int: Seconds until window reset
        """
        now = datetime.utcnow()
        window_end = self.window_start + timedelta(hours=1)
        delta = window_end - now
        return max(0, int(delta.total_seconds()))
