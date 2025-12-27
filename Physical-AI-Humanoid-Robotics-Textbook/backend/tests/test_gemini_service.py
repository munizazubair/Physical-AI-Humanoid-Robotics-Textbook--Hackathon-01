"""
Unit Tests for Gemini Service

Tests the GeminiService class for LLM response generation.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from services.gemini_service import GeminiService


@pytest.fixture
def gemini_service():
    """Create a GeminiService instance for testing."""
    with patch('services.gemini_service.genai'):
        service = GeminiService(api_key="test_api_key")
        return service


@pytest.mark.asyncio
async def test_generate_response_with_context(gemini_service):
    """Test response generation with context chunks."""
    context_chunks = [
        {
            "text": "ROS 2 is a robot operating system.",
            "reference": "[Chapter 1, Section 1.2]",
            "score": 0.85
        },
        {
            "text": "ROS 2 uses DDS for communication.",
            "reference": "[Chapter 1, Section 1.3]",
            "score": 0.78
        }
    ]

    mock_response = MagicMock()
    mock_response.text = "ROS 2 is a robot operating system that uses DDS for communication. [Chapter 1, Section 1.2][Chapter 1, Section 1.3]"

    gemini_service.model = MagicMock()
    gemini_service.model.generate_content = AsyncMock(return_value=mock_response)

    response = await gemini_service.generate_response(
        question="What is ROS 2?",
        context_chunks=context_chunks
    )

    assert "ROS 2 is a robot operating system" in response
    assert "[Chapter 1, Section 1.2]" in response
    gemini_service.model.generate_content.assert_called_once()


@pytest.mark.asyncio
async def test_generate_response_with_conversation_history(gemini_service):
    """Test that conversation history is included in the prompt."""
    context_chunks = [{"text": "ROS 2 info", "reference": "[Ch 1]", "score": 0.8}]
    conversation_history = [
        {"role": "user", "content": "What is ROS?"},
        {"role": "assistant", "content": "ROS is a robotics middleware."}
    ]

    mock_response = MagicMock()
    mock_response.text = "ROS 2 builds upon ROS with better features."

    gemini_service.model = MagicMock()
    gemini_service.model.generate_content = AsyncMock(return_value=mock_response)

    response = await gemini_service.generate_response(
        question="Tell me about ROS 2",
        context_chunks=context_chunks,
        conversation_history=conversation_history
    )

    assert response == "ROS 2 builds upon ROS with better features."

    # Verify prompt includes conversation history
    call_args = gemini_service.model.generate_content.call_args
    prompt = call_args[0][0]
    assert "What is ROS?" in prompt
    assert "ROS is a robotics middleware" in prompt


@pytest.mark.asyncio
async def test_generate_response_without_context(gemini_service):
    """Test response generation when no context chunks are provided."""
    mock_response = MagicMock()
    mock_response.text = "I don't have enough information to answer that."

    gemini_service.model = MagicMock()
    gemini_service.model.generate_content = AsyncMock(return_value=mock_response)

    response = await gemini_service.generate_response(
        question="Random question",
        context_chunks=[]
    )

    assert "don't have enough information" in response


@pytest.mark.asyncio
async def test_generate_response_handles_api_error(gemini_service):
    """Test that API errors are handled gracefully."""
    gemini_service.model = MagicMock()
    gemini_service.model.generate_content = AsyncMock(
        side_effect=Exception("API rate limit exceeded")
    )

    with pytest.raises(Exception) as exc_info:
        await gemini_service.generate_response(
            question="Test question",
            context_chunks=[]
        )

    assert "API rate limit exceeded" in str(exc_info.value)


@pytest.mark.asyncio
async def test_generate_response_with_long_context(gemini_service):
    """Test that long context is handled properly."""
    # Create many context chunks
    context_chunks = [
        {
            "text": f"Text chunk {i}" * 50,
            "reference": f"[Chapter {i}]",
            "score": 0.8
        }
        for i in range(20)
    ]

    mock_response = MagicMock()
    mock_response.text = "Summary of all chunks."

    gemini_service.model = MagicMock()
    gemini_service.model.generate_content = AsyncMock(return_value=mock_response)

    response = await gemini_service.generate_response(
        question="Summarize",
        context_chunks=context_chunks
    )

    assert response == "Summary of all chunks."


def test_format_context_chunks(gemini_service):
    """Test that context chunks are formatted correctly for the prompt."""
    chunks = [
        {"text": "Chunk 1", "reference": "[Ch 1]", "score": 0.9},
        {"text": "Chunk 2", "reference": "[Ch 2]", "score": 0.7}
    ]

    formatted = gemini_service.format_context_chunks(chunks)

    assert "[Ch 1]" in formatted
    assert "Chunk 1" in formatted
    assert "[Ch 2]" in formatted
    assert "Chunk 2" in formatted


@pytest.mark.asyncio
async def test_generate_response_validates_empty_question(gemini_service):
    """Test that empty questions are rejected."""
    with pytest.raises(ValueError) as exc_info:
        await gemini_service.generate_response(
            question="",
            context_chunks=[]
        )

    assert "Question cannot be empty" in str(exc_info.value)
