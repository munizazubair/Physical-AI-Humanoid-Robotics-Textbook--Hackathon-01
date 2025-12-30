"""
Rate Limiting Middleware

Enforces rate limits on API requests to prevent abuse.
Limits each session to 20 requests per hour.
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
import uuid

from models.rate_limit import RateLimit
from database import AsyncSessionLocal

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    Middleware to enforce rate limits on API requests.

    Tracks requests per session per hour and returns 429 when limit exceeded.
    """

    def __init__(self, app, limit: int = 20):
        """
        Initialize rate limiting middleware.

        Args:
            app: FastAPI application
            limit (int): Maximum requests per hour (default: 20)
        """
        self.app = app
        self.limit = limit

    async def __call__(self, request: Request, call_next):
        """
        Process request and enforce rate limits.

        Args:
            request (Request): Incoming HTTP request
            call_next: Next middleware in chain

        Returns:
            Response: HTTP response or 429 if rate limited
        """
        # Only apply rate limiting to /api/chat endpoint
        if not request.url.path.startswith("/api/chat"):
            return await call_next(request)

        # Extract session_id from request body (for POST) or query params (for GET)
        session_id = await self._extract_session_id(request)

        if not session_id:
            # No session_id, skip rate limiting (will fail later in handler)
            return await call_next(request)

        # Check rate limit
        try:
            async with AsyncSessionLocal() as db:
                is_limited, retry_after = await self._check_rate_limit(
                    session_id, db
                )

                if is_limited:
                    logger.warning(
                        f"Rate limit exceeded for session {session_id}. "
                        f"Retry after {retry_after} seconds."
                    )
                    return JSONResponse(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        content={
                            "detail": "Rate limit exceeded. Please try again later.",
                            "retry_after": retry_after
                        },
                        headers={"Retry-After": str(retry_after)}
                    )

                # Increment request count
                await self._increment_request_count(session_id, db)

        except Exception as e:
            logger.error(f"Rate limiting error: {e}", exc_info=True)
            # On error, allow request through (fail open)

        # Process request
        response = await call_next(request)
        return response

    async def _extract_session_id(self, request: Request) -> str:
        """
        Extract session_id from request.

        Args:
            request (Request): HTTP request

        Returns:
            str: Session ID or None
        """
        # Try query parameters first
        session_id = request.query_params.get("session_id")
        if session_id:
            return session_id

        # Try request body for POST requests
        if request.method == "POST":
            try:
                body = await request.json()
                session_id = body.get("session_id")
                if session_id:
                    return session_id
            except Exception:
                pass

        return None

    async def _check_rate_limit(
        self,
        session_id: str,
        db: AsyncSession
    ) -> tuple[bool, int]:
        """
        Check if session has exceeded rate limit.

        Args:
            session_id (str): Session UUID
            db (AsyncSession): Database session

        Returns:
            tuple: (is_limited: bool, retry_after: int)
        """
        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            return False, 0

        # Get current window start
        window_start = RateLimit.get_current_window_start()

        # Find existing rate limit record for current window
        result = await db.execute(
            select(RateLimit).where(
                RateLimit.session_id == session_uuid,
                RateLimit.window_start == window_start
            )
        )
        rate_limit = result.scalar_one_or_none()

        if not rate_limit:
            # No record exists, create one
            return False, 0

        # Check if limit exceeded
        if rate_limit.is_limit_exceeded(self.limit):
            retry_after = rate_limit.get_retry_after_seconds()
            return True, retry_after

        return False, 0

    async def _increment_request_count(
        self,
        session_id: str,
        db: AsyncSession
    ):
        """
        Increment request count for session.

        Args:
            session_id (str): Session UUID
            db (AsyncSession): Database session
        """
        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            return

        window_start = RateLimit.get_current_window_start()

        # Find or create rate limit record
        result = await db.execute(
            select(RateLimit).where(
                RateLimit.session_id == session_uuid,
                RateLimit.window_start == window_start
            )
        )
        rate_limit = result.scalar_one_or_none()

        if not rate_limit:
            # Create new record
            rate_limit = RateLimit.create_for_session(session_uuid)
            db.add(rate_limit)

        # Increment count
        rate_limit.increment()
        await db.commit()

        logger.info(
            f"Request count for session {session_id}: "
            f"{rate_limit.request_count}/{self.limit}"
        )
