"""
Personalization Router

Handles personalized learning assistance endpoints including greetings,
interest analysis, and chapter recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
import uuid

from database import get_db
from services.personalization_service import personalization_service
from pydantic import BaseModel


router = APIRouter(prefix="/api/personalization", tags=["personalization"])


# Response Models
class GreetingResponse(BaseModel):
    """Response model for personalized greeting."""
    greeting: str
    session_id: str


class InterestsResponse(BaseModel):
    """Response model for detected interests."""
    interests: List[str]
    session_id: str


class RecommendationItem(BaseModel):
    """Single chapter recommendation."""
    chapter: int
    title: str
    reason: str


class RecommendationsResponse(BaseModel):
    """Response model for chapter recommendations."""
    recommendations: List[RecommendationItem]
    session_id: str


@router.get("/greeting", response_model=GreetingResponse)
async def get_personalized_greeting(
    session_id: str = Query(..., description="Session ID to get greeting for"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a personalized greeting for the user.

    Returns a generic greeting for new users or a personalized greeting
    mentioning recent topics for returning users.

    Args:
        session_id: UUID of the user session
        db: Database session

    Returns:
        GreetingResponse with personalized greeting

    Raises:
        HTTPException: 400 if session_id is invalid
    """
    # Validate session_id format
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session_id format")

    try:
        greeting = await personalization_service.get_greeting(session_uuid, db)

        return GreetingResponse(
            greeting=greeting,
            session_id=session_id
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting greeting: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate greeting")


@router.get("/interests", response_model=InterestsResponse)
async def get_user_interests(
    session_id: str = Query(..., description="Session ID to analyze interests for"),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze and return user interests from conversation history.

    Extracts topics and keywords from the user's recent messages.

    Args:
        session_id: UUID of the user session
        db: Database session

    Returns:
        InterestsResponse with list of detected interests

    Raises:
        HTTPException: 400 if session_id is invalid
    """
    # Validate session_id format
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session_id format")

    try:
        interests = await personalization_service.analyze_interests(session_uuid, db)

        return InterestsResponse(
            interests=interests,
            session_id=session_id
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error analyzing interests: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to analyze interests")


@router.get("/recommendations", response_model=RecommendationsResponse)
async def get_chapter_recommendations(
    session_id: str = Query(..., description="Session ID to get recommendations for"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized chapter recommendations based on user interests and history.

    Returns 3-5 recommended chapters with reasons for the recommendation.

    Args:
        session_id: UUID of the user session
        db: Database session

    Returns:
        RecommendationsResponse with list of recommendations

    Raises:
        HTTPException: 400 if session_id is invalid
    """
    # Validate session_id format
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session_id format")

    try:
        recommendations_data = await personalization_service.get_recommendations(
            session_uuid, db
        )

        recommendations = [
            RecommendationItem(**rec) for rec in recommendations_data
        ]

        return RecommendationsResponse(
            recommendations=recommendations,
            session_id=session_id
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting recommendations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get recommendations")


@router.post("/analyze")
async def analyze_user_profile(
    session_id: str = Query(..., description="Session ID to analyze"),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze user profile including interests and knowledge level.

    This endpoint triggers a comprehensive analysis of the user's conversation
    history to update their profile.

    Args:
        session_id: UUID of the user session
        db: Database session

    Returns:
        Analysis results including interests and knowledge level

    Raises:
        HTTPException: 400 if session_id is invalid
    """
    # Validate session_id format
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session_id format")

    try:
        # Analyze interests
        interests = await personalization_service.analyze_interests(session_uuid, db)

        # Infer knowledge level
        knowledge_level = await personalization_service.infer_knowledge_level(
            session_uuid, db
        )

        return {
            "session_id": session_id,
            "interests": interests,
            "knowledge_level": knowledge_level.value,
            "status": "analysis_complete"
        }
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error analyzing profile: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to analyze user profile")
