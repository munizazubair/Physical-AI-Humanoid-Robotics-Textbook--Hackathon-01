"""
Chat API Router

Handles chat interactions between users and the RAG chatbot.
"""

from typing import Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user_session import UserSession
from models.conversation import Conversation
from models.message import Message
from services.rag_service import rag_service

router = APIRouter(
    prefix="/api",
    tags=["chat"],
)


# Request/Response Models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    session_id: Optional[uuid.UUID] = Field(
        None,
        description="Session ID (optional - will be created if not provided)"
    )
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's question"
    )
    conversation_id: Optional[uuid.UUID] = Field(
        None,
        description="Conversation ID (optional - will be created if not provided)"
    )


class Citation(BaseModel):
    """Citation metadata."""
    chapter: str
    section: str
    page: str
    text: str
    content_type: str = "text"


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Assistant's response")
    citations: list[Citation] = Field(..., description="Source citations")
    message_id: uuid.UUID = Field(..., description="Created message ID")
    conversation_id: uuid.UUID = Field(..., description="Conversation ID")
    session_id: uuid.UUID = Field(..., description="Session ID")
    is_off_topic: bool = Field(False, description="Whether question was off-topic")


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a chat message",
    description="Send a question to the RAG chatbot and receive a response with citations"
)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Process a chat message through the RAG pipeline.

    Flow:
    1. Get or create user session
    2. Get or create conversation
    3. Save user message
    4. Process question through RAG pipeline
    5. Save assistant response
    6. Return response with citations

    Args:
        request (ChatRequest): Chat request with question and optional session/conversation IDs
        db (AsyncSession): Database session

    Returns:
        ChatResponse: Response with answer and citations

    Raises:
        HTTPException: 400 for invalid input, 500 for processing errors
    """
    try:
        # Step 1: Get or create user session
        session_id = request.session_id
        if not session_id:
            # Create new session
            user_session = UserSession()
            db.add(user_session)
            await db.flush()  # Get the ID
            session_id = user_session.id
        else:
            # Verify session exists
            result = await db.execute(
                select(UserSession).where(UserSession.id == session_id)
            )
            user_session = result.scalar_one_or_none()

            if not user_session:
                # Create session with provided ID
                user_session = UserSession(id=session_id)
                db.add(user_session)
                await db.flush()

        # Update activity timestamp
        user_session.update_activity()

        # Step 2: Get or create conversation
        conversation_id = request.conversation_id
        if not conversation_id:
            # Create new conversation
            conversation = Conversation(session_id=session_id)
            db.add(conversation)
            await db.flush()
            conversation_id = conversation.id
        else:
            # Verify conversation exists and belongs to session
            result = await db.execute(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.session_id == session_id
                )
            )
            conversation = result.scalar_one_or_none()

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Conversation not found or does not belong to session"
                )

        # Step 3: Save user message
        user_message = Message.create_user_message(
            conversation_id=conversation_id,
            content=request.question
        )
        db.add(user_message)
        await db.flush()

        # Set conversation title from first message if not set
        if not conversation.title:
            conversation.set_title_from_first_message(request.question)

        # Step 4: Get conversation history for context
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(20)  # Last 20 messages for context
        )
        history_messages = result.scalars().all()

        # Format history for RAG service
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(history_messages)  # Reverse to chronological order
        ]

        # Step 5: Process question through RAG pipeline with personalization
        rag_result = await rag_service.process_question(
            question=request.question,
            session_id=session_id,
            conversation_history=conversation_history,
            db=db
        )

        # Step 6: Save assistant response
        assistant_message = Message.create_assistant_message(
            conversation_id=conversation_id,
            content=rag_result["response"],
            citations=rag_result["citations"]
        )
        db.add(assistant_message)

        # Commit all changes
        await db.commit()

        # Step 7: Format response
        return ChatResponse(
            response=rag_result["response"],
            citations=[Citation(**citation) for citation in rag_result["citations"]],
            message_id=assistant_message.id,
            conversation_id=conversation_id,
            session_id=session_id,
            is_off_topic=rag_result.get("is_off_topic", False)
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Log error and return 500
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Chat endpoint error: {e}", exc_info=True)

        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your question. Please try again."
        )
