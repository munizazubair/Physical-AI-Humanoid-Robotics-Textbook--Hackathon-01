"""
Input Validation Middleware

Provides input sanitization and validation to prevent injection attacks
and malicious content in API requests.
"""

import re
import html
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class InputValidator:
    """
    Input validation and sanitization utility class.

    Prevents:
    - SQL injection
    - XSS attacks (HTML/JS injection)
    - Oversized inputs
    - Malformed UUIDs
    """

    # Maximum allowed length for question input
    MAX_QUESTION_LENGTH = 500

    # SQL injection patterns to detect
    SQL_INJECTION_PATTERNS = [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bINSERT\b.*\bINTO\b)",
        r"(\bDELETE\b.*\bFROM\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(;\s*--)",
        r"('\s*OR\s*'1'\s*=\s*'1)",
        r"(--\s*$)",
        r"(/\*.*\*/)",
    ]

    @staticmethod
    def validate_uuid(value: str, field_name: str = "ID") -> UUID:
        """
        Validate and convert string to UUID.

        Args:
            value (str): String representation of UUID
            field_name (str): Name of the field for error messages

        Returns:
            UUID: Validated UUID object

        Raises:
            HTTPException: If UUID is invalid
        """
        try:
            return UUID(value)
        except (ValueError, AttributeError, TypeError):
            logger.warning(f"Invalid UUID provided for {field_name}: {value}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid {field_name} format. Must be a valid UUID."
            )

    @staticmethod
    def sanitize_question(question: str) -> str:
        """
        Sanitize user question input.

        Steps:
        1. Escape HTML entities
        2. Remove malicious patterns
        3. Trim whitespace
        4. Validate length

        Args:
            question (str): User's question input

        Returns:
            str: Sanitized question

        Raises:
            HTTPException: If input is invalid or malicious
        """
        if not question or not question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )

        # Trim whitespace
        sanitized = question.strip()

        # Check length
        if len(sanitized) > InputValidator.MAX_QUESTION_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question too long. Maximum length is {InputValidator.MAX_QUESTION_LENGTH} characters."
            )

        # Escape HTML entities to prevent XSS
        sanitized = html.escape(sanitized)

        # Check for SQL injection patterns
        for pattern in InputValidator.SQL_INJECTION_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                logger.warning(f"SQL injection attempt detected: {sanitized[:100]}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid input detected. Please rephrase your question."
                )

        # Remove any remaining potentially dangerous characters
        # Allow: letters, numbers, spaces, common punctuation
        allowed_pattern = r"[^a-zA-Z0-9\s\.,!?;:()\-\'\"\n]"
        if re.search(allowed_pattern, sanitized):
            # Replace disallowed characters with spaces
            sanitized = re.sub(allowed_pattern, " ", sanitized)
            sanitized = re.sub(r"\s+", " ", sanitized).strip()  # Collapse multiple spaces

        return sanitized

    @staticmethod
    def validate_session_id(session_id: Optional[str]) -> Optional[UUID]:
        """
        Validate session ID if provided.

        Args:
            session_id (Optional[str]): Session ID string or None

        Returns:
            Optional[UUID]: Validated UUID or None

        Raises:
            HTTPException: If session ID is provided but invalid
        """
        if session_id is None or session_id == "":
            return None

        return InputValidator.validate_uuid(session_id, "session_id")

    @staticmethod
    def validate_conversation_id(conversation_id: str) -> UUID:
        """
        Validate conversation ID.

        Args:
            conversation_id (str): Conversation ID string

        Returns:
            UUID: Validated UUID

        Raises:
            HTTPException: If conversation ID is invalid
        """
        return InputValidator.validate_uuid(conversation_id, "conversation_id")

    @staticmethod
    def validate_message_id(message_id: str) -> UUID:
        """
        Validate message ID.

        Args:
            message_id (str): Message ID string

        Returns:
            UUID: Validated UUID

        Raises:
            HTTPException: If message ID is invalid
        """
        return InputValidator.validate_uuid(message_id, "message_id")

    @staticmethod
    def sanitize_feedback_comment(comment: Optional[str]) -> Optional[str]:
        """
        Sanitize optional feedback comment.

        Args:
            comment (Optional[str]): User feedback comment

        Returns:
            Optional[str]: Sanitized comment or None
        """
        if not comment or not comment.strip():
            return None

        # Limit comment length
        max_length = 1000
        sanitized = comment.strip()[:max_length]

        # Escape HTML
        sanitized = html.escape(sanitized)

        return sanitized
