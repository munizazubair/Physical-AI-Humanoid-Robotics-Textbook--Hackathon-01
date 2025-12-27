"""
Conversation Router

Handles conversation management endpoints including history retrieval and new conversation creation.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import uuid

from database import get_db
from models.user_session import UserSession
from models.conversation import Conversation
from models.message import Message
from pydantic import BaseModel
from datetime import datetime


router = APIRouter(prefix="/api/conversation", tags=["conversation"])


# Response Models
class MessageResponse(BaseModel):
    """Response model for a single message."""
    id: str
    role: str
    content: str
    citations: Optional[List[dict]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history."""
    session_id: str
    conversation_id: Optional[str]
    messages: List[MessageResponse]
    total_messages: int


class NewConversationRequest(BaseModel):
    """Request model for creating a new conversation."""
    session_id: str


class NewConversationResponse(BaseModel):
    """Response model for new conversation creation."""
    conversation_id: str
    session_id: str
    created_at: datetime


@router.get("/history", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    session_id: str = Query(..., description="Session ID to retrieve history for"),
    conversation_id: Optional[str] = Query(None, description="Specific conversation ID (optional)"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of messages to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve conversation history for a session.

    Returns all messages for a session, optionally filtered by conversation_id.
    Messages are ordered chronologically (oldest first).

    Args:
        session_id: UUID of the user session
        conversation_id: Optional UUID to filter by specific conversation
        limit: Maximum number of messages to return (default: 100, max: 500)
        db: Database session

    Returns:
        ConversationHistoryResponse with list of messages

    Raises:
        HTTPException: 400 if session_id or conversation_id is invalid
    """
    # Validate session_id format
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session_id format")

    # Check if session exists
    session_query = select(UserSession).where(UserSession.id == session_uuid)
    session_result = await db.execute(session_query)
    session = session_result.scalar_one_or_none()

    if not session:
        # Return empty history for non-existent sessions
        return ConversationHistoryResponse(
            session_id=session_id,
            conversation_id=conversation_id,
            messages=[],
            total_messages=0
        )

    # Build query for messages
    query = (
        select(Message)
        .join(Conversation)
        .where(Conversation.session_id == session_uuid)
    )

    # Filter by conversation_id if provided
    if conversation_id:
        try:
            conversation_uuid = uuid.UUID(conversation_id)
            query = query.where(Message.conversation_id == conversation_uuid)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation_id format")

    # Order by created_at and limit
    query = query.order_by(Message.created_at.asc()).limit(limit)

    # Execute query
    result = await db.execute(query)
    messages = result.scalars().all()

    # Convert to response models
    message_responses = [
        MessageResponse(
            id=str(msg.id),
            role=msg.role,
            content=msg.content,
            citations=msg.citations if msg.citations else None,
            created_at=msg.created_at
        )
        for msg in messages
    ]

    # Get conversation_id from first message if not provided
    actual_conversation_id = conversation_id
    if not actual_conversation_id and messages:
        actual_conversation_id = str(messages[0].conversation_id)

    return ConversationHistoryResponse(
        session_id=session_id,
        conversation_id=actual_conversation_id,
        messages=message_responses,
        total_messages=len(message_responses)
    )


@router.post("/new", response_model=NewConversationResponse)
async def create_new_conversation(
    request: NewConversationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new conversation for a session.

    This endpoint allows users to start a fresh conversation while preserving
    previous conversation history.

    Args:
        request: NewConversationRequest with session_id
        db: Database session

    Returns:
        NewConversationResponse with new conversation_id

    Raises:
        HTTPException: 400 if session_id is invalid
        HTTPException: 404 if session does not exist
    """
    # Validate session_id format
    try:
        session_uuid = uuid.UUID(request.session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session_id format")

    # Check if session exists
    session_query = select(UserSession).where(UserSession.id == session_uuid)
    session_result = await db.execute(session_query)
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Create new conversation
    new_conversation = Conversation(
        session_id=session_uuid,
        title=None  # Will be set from first user message
    )

    db.add(new_conversation)
    await db.commit()
    await db.refresh(new_conversation)

    return NewConversationResponse(
        conversation_id=str(new_conversation.id),
        session_id=request.session_id,
        created_at=new_conversation.created_at
    )


@router.get("/list", response_model=List[dict])
async def list_conversations(
    session_id: str = Query(..., description="Session ID to list conversations for"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all conversations for a session.

    Returns a list of conversations with their titles and metadata.

    Args:
        session_id: UUID of the user session
        db: Database session

    Returns:
        List of conversation summaries

    Raises:
        HTTPException: 400 if session_id is invalid
    """
    # Validate session_id format
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session_id format")

    # Get all conversations for session
    query = (
        select(Conversation)
        .where(Conversation.session_id == session_uuid)
        .order_by(Conversation.created_at.desc())
    )

    result = await db.execute(query)
    conversations = result.scalars().all()

    # Format response
    conversation_list = []
    for conv in conversations:
        # Get message count
        message_count_query = (
            select(Message)
            .where(Message.conversation_id == conv.id)
        )
        message_count_result = await db.execute(message_count_query)
        message_count = len(message_count_result.scalars().all())

        conversation_list.append({
            "id": str(conv.id),
            "title": conv.title if conv.title else "New Conversation",
            "created_at": conv.created_at.isoformat(),
            "message_count": message_count
        })

    return conversation_list
