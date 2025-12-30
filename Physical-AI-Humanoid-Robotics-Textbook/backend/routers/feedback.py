"""
Feedback Router

Handles user feedback submission for assistant messages.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
import uuid
import logging

from database import get_db
from models.feedback import Feedback
from models.message import Message
from sqlalchemy import select

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


# Request/Response Models
class FeedbackRequest(BaseModel):
    """Request model for submitting feedback."""
    message_id: str = Field(..., description="UUID of the message being rated")
    rating: int = Field(..., description="1 for thumbs up, -1 for thumbs down")
    comment: str = Field(None, description="Optional user comment")


class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    feedback_id: str
    message: str = "Thank you for your feedback!"


@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_200_OK)
async def submit_feedback(
    request: FeedbackRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit feedback for an assistant message.

    Accepts thumbs up (+1) or thumbs down (-1) ratings with optional comments.

    Args:
        request (FeedbackRequest): Feedback data
        db (AsyncSession): Database session

    Returns:
        FeedbackResponse: Confirmation with feedback ID

    Raises:
        HTTPException: 400 if validation fails, 404 if message not found
    """
    try:
        # Validate rating
        if request.rating not in (1, -1):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be 1 (thumbs up) or -1 (thumbs down)"
            )

        # Validate message_id format
        try:
            message_uuid = uuid.UUID(request.message_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message_id format"
            )

        # Check if message exists
        result = await db.execute(
            select(Message).where(Message.id == message_uuid)
        )
        message = result.scalar_one_or_none()

        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )

        # Check if message is from assistant (only assistant messages can be rated)
        if message.role != "assistant":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only assistant messages can be rated"
            )

        # Check if feedback already exists for this message
        existing_feedback = await db.execute(
            select(Feedback).where(Feedback.message_id == message_uuid)
        )
        if existing_feedback.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback already submitted for this message"
            )

        # Create feedback
        feedback = Feedback.create(
            message_id=message_uuid,
            rating=request.rating,
            comment=request.comment
        )

        db.add(feedback)
        await db.commit()
        await db.refresh(feedback)

        logger.info(
            f"Feedback submitted: message_id={message_uuid}, "
            f"rating={request.rating}, feedback_id={feedback.id}"
        )

        return FeedbackResponse(
            feedback_id=str(feedback.id),
            message="Thank you for your feedback!"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit feedback"
        )
