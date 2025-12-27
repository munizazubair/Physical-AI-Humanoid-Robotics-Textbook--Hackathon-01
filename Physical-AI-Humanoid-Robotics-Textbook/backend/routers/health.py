"""
Health Check Router

This module provides health check endpoints to monitor API and database status.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

router = APIRouter(
    prefix="",
    tags=["health"],
)


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API and database are healthy and responding",
)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint that verifies API and database connectivity.

    Returns:
        dict: Health status including API and database status

    Raises:
        HTTPException: 503 if database is unreachable
    """
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        # Return 503 Service Unavailable if database is down
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "api": "healthy",
                "database": db_status,
            }
        )

    return {
        "status": "healthy",
        "api": "healthy",
        "database": db_status,
    }


@router.get(
    "/",
    summary="Root Endpoint",
    description="Get API information and available endpoints",
)
async def root():
    """
    Root endpoint providing API metadata.

    Returns:
        dict: API information including title, version, and documentation links
    """
    return {
        "title": "RAG Chatbot API",
        "version": "0.1.0",
        "status": "active",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }
