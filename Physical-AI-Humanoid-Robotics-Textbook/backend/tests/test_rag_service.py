"""
Unit Tests for RAG Service

Tests the RAGService class for end-to-end RAG pipeline orchestration.
"""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from services.rag_service import RAGService


@pytest.fixture
def rag_service():
    """Create a RAGService instance for testing."""
    with patch('services.rag_service.QdrantService'), \
         patch('services.rag_service.GeminiService'):
        service = RAGService(
            qdrant_url="https://test.qdrant.io",
            qdrant_api_key="test_key",
            gemini_api_key="test_key"
        )
        return service


@pytest.mark.asyncio
async def test_process_question_on_topic(rag_service):
    """Test processing an on-topic question with successful retrieval."""
    # Mock Qdrant retrieval
    rag_service.qdrant_service.search = AsyncMock(return_value=[
        {
            "id": "chunk_1",
            "text": "ROS 2 is a robot operating system.",
            "reference": "[Chapter 1, Section 1.2]",
            "score": 0.85
        },
        {
            "id": "chunk_2",
            "text": "ROS 2 uses DDS for communication.",
            "reference": "[Chapter 1, Section 1.3]",
            "score": 0.78
        }
    ])

    # Mock Gemini generation
    rag_service.gemini_service.generate_response = AsyncMock(
        return_value="ROS 2 is a robot operating system that uses DDS. [Chapter 1, Section 1.2][Chapter 1, Section 1.3]"
    )

    session_id = uuid.uuid4()
    result = await rag_service.process_question(
        question="What is ROS 2?",
        session_id=session_id
    )

    assert result["is_off_topic"] is False
    assert "ROS 2 is a robot operating system" in result["response"]
    assert len(result["citations"]) == 2
    assert result["citations"][0] == "[Chapter 1, Section 1.2]"
    assert result["citations"][1] == "[Chapter 1, Section 1.3]"


@pytest.mark.asyncio
async def test_process_question_off_topic_no_chunks(rag_service):
    """Test processing an off-topic question (no relevant chunks found)."""
    # Mock Qdrant retrieval - no results
    rag_service.qdrant_service.search = AsyncMock(return_value=[])

    session_id = uuid.uuid4()
    result = await rag_service.process_question(
        question="What is the weather today?",
        session_id=session_id
    )

    assert result["is_off_topic"] is True
    assert "outside the scope" in result["response"].lower() or \
           "not related to" in result["response"].lower()
    assert result["citations"] == []


@pytest.mark.asyncio
async def test_process_question_off_topic_low_scores(rag_service):
    """Test processing an off-topic question (low relevance scores)."""
    # Mock Qdrant retrieval - low scores
    rag_service.qdrant_service.search = AsyncMock(return_value=[
        {
            "id": "chunk_1",
            "text": "Some unrelated text.",
            "reference": "[Chapter 5]",
            "score": 0.35  # Below threshold
        }
    ])

    session_id = uuid.uuid4()
    result = await rag_service.process_question(
        question="Random question",
        session_id=session_id,
        relevance_threshold=0.5
    )

    assert result["is_off_topic"] is True


@pytest.mark.asyncio
async def test_process_question_with_conversation_history(rag_service):
    """Test processing a question with conversation context."""
    rag_service.qdrant_service.search = AsyncMock(return_value=[
        {
            "id": "chunk_1",
            "text": "ROS 2 features.",
            "reference": "[Chapter 2]",
            "score": 0.88
        }
    ])

    rag_service.gemini_service.generate_response = AsyncMock(
        return_value="Based on our previous discussion, ROS 2 has improved features. [Chapter 2]"
    )

    conversation_history = [
        {"role": "user", "content": "What is ROS?"},
        {"role": "assistant", "content": "ROS is a robotics middleware."}
    ]

    session_id = uuid.uuid4()
    result = await rag_service.process_question(
        question="What about ROS 2?",
        session_id=session_id,
        conversation_history=conversation_history
    )

    # Verify Gemini was called with conversation history
    rag_service.gemini_service.generate_response.assert_called_once_with(
        question="What about ROS 2?",
        context_chunks=[{
            "id": "chunk_1",
            "text": "ROS 2 features.",
            "reference": "[Chapter 2]",
            "score": 0.88
        }],
        conversation_history=conversation_history
    )


@pytest.mark.asyncio
async def test_extract_citations(rag_service):
    """Test citation extraction from response text."""
    retrieved_chunks = [
        {"reference": "[Chapter 1, Section 1.2]"},
        {"reference": "[Chapter 2, Section 2.1]"},
        {"reference": "[Chapter 3]"}
    ]

    response_text = "Information from [Chapter 1, Section 1.2] and [Chapter 2, Section 2.1]."

    citations = rag_service._extract_citations(retrieved_chunks, response_text)

    assert len(citations) == 2
    assert "[Chapter 1, Section 1.2]" in citations
    assert "[Chapter 2, Section 2.1]" in citations
    assert "[Chapter 3]" not in citations  # Not mentioned in response


@pytest.mark.asyncio
async def test_extract_citations_deduplicate(rag_service):
    """Test that duplicate citations are removed."""
    retrieved_chunks = [
        {"reference": "[Chapter 1]"},
        {"reference": "[Chapter 1]"}  # Duplicate
    ]

    response_text = "Information from [Chapter 1]."

    citations = rag_service._extract_citations(retrieved_chunks, response_text)

    assert len(citations) == 1
    assert citations[0] == "[Chapter 1]"


@pytest.mark.asyncio
async def test_process_question_handles_retrieval_error(rag_service):
    """Test error handling when Qdrant retrieval fails."""
    rag_service.qdrant_service.search = AsyncMock(
        side_effect=Exception("Qdrant connection error")
    )

    session_id = uuid.uuid4()

    with pytest.raises(Exception) as exc_info:
        await rag_service.process_question(
            question="Test question",
            session_id=session_id
        )

    assert "Qdrant connection error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_process_question_handles_generation_error(rag_service):
    """Test error handling when Gemini generation fails."""
    rag_service.qdrant_service.search = AsyncMock(return_value=[
        {"text": "Some text", "reference": "[Ch 1]", "score": 0.9}
    ])

    rag_service.gemini_service.generate_response = AsyncMock(
        side_effect=Exception("Gemini API error")
    )

    session_id = uuid.uuid4()

    with pytest.raises(Exception) as exc_info:
        await rag_service.process_question(
            question="Test question",
            session_id=session_id
        )

    assert "Gemini API error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_off_topic_response(rag_service):
    """Test off-topic response generation."""
    response = rag_service._get_off_topic_response()

    assert "outside the scope" in response.lower() or \
           "not related to" in response.lower() or \
           "textbook" in response.lower()


@pytest.mark.asyncio
async def test_process_question_validates_empty_question(rag_service):
    """Test that empty questions are rejected."""
    session_id = uuid.uuid4()

    with pytest.raises(ValueError) as exc_info:
        await rag_service.process_question(
            question="",
            session_id=session_id
        )

    assert "Question cannot be empty" in str(exc_info.value)
