"""
Unit Tests for Qdrant Service

Tests the QdrantService class for semantic search functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from services.qdrant_service import QdrantService


@pytest.fixture
def qdrant_service():
    """Create a QdrantService instance for testing."""
    with patch('services.qdrant_service.QdrantClient'):
        service = QdrantService(
            url="https://test-qdrant.example.com",
            api_key="test_api_key",
            collection_name="test_collection"
        )
        return service


@pytest.mark.asyncio
async def test_search_returns_relevant_chunks(qdrant_service):
    """Test that search returns relevant chunks with scores."""
    # Mock Qdrant search response
    mock_result = MagicMock()
    mock_result.id = "chunk_123"
    mock_result.score = 0.85
    mock_result.payload = {
        "text": "ROS 2 is a robot operating system.",
        "chapter": "1",
        "section": "1.2",
        "reference": "[Chapter 1, Section 1.2]"
    }

    qdrant_service.client.search = AsyncMock(return_value=[mock_result])

    results = await qdrant_service.search(query="What is ROS 2?", top_k=5)

    assert len(results) == 1
    assert results[0]["id"] == "chunk_123"
    assert results[0]["score"] == 0.85
    assert results[0]["text"] == "ROS 2 is a robot operating system."
    assert results[0]["reference"] == "[Chapter 1, Section 1.2]"

    # Verify search was called with correct parameters
    qdrant_service.client.search.assert_called_once()


@pytest.mark.asyncio
async def test_search_filters_low_scores(qdrant_service):
    """Test that search filters out chunks with low relevance scores."""
    # Mock Qdrant search response with mixed scores
    mock_results = [
        MagicMock(
            id="chunk_high",
            score=0.75,
            payload={"text": "High relevance", "reference": "[Chapter 1]"}
        ),
        MagicMock(
            id="chunk_low",
            score=0.3,
            payload={"text": "Low relevance", "reference": "[Chapter 2]"}
        ),
    ]

    qdrant_service.client.search = AsyncMock(return_value=mock_results)

    results = await qdrant_service.search(
        query="Test query",
        top_k=5,
        score_threshold=0.5
    )

    # Only high score result should be returned
    assert len(results) == 1
    assert results[0]["id"] == "chunk_high"


@pytest.mark.asyncio
async def test_search_handles_empty_results(qdrant_service):
    """Test that search handles empty results gracefully."""
    qdrant_service.client.search = AsyncMock(return_value=[])

    results = await qdrant_service.search(query="Unknown topic", top_k=5)

    assert results == []


@pytest.mark.asyncio
async def test_search_with_custom_top_k(qdrant_service):
    """Test that search respects top_k parameter."""
    mock_results = [
        MagicMock(id=f"chunk_{i}", score=0.9 - i * 0.1, payload={"text": f"Text {i}"})
        for i in range(10)
    ]

    qdrant_service.client.search = AsyncMock(return_value=mock_results[:3])

    results = await qdrant_service.search(query="Test", top_k=3)

    assert len(results) == 3
    qdrant_service.client.search.assert_called_once()


@pytest.mark.asyncio
async def test_search_handles_connection_error(qdrant_service):
    """Test that search handles Qdrant connection errors."""
    qdrant_service.client.search = AsyncMock(
        side_effect=Exception("Connection timeout")
    )

    with pytest.raises(Exception) as exc_info:
        await qdrant_service.search(query="Test", top_k=5)

    assert "Connection timeout" in str(exc_info.value)


def test_format_chunk_for_context(qdrant_service):
    """Test that chunks are formatted correctly for LLM context."""
    chunk = {
        "text": "ROS 2 uses DDS for communication.",
        "reference": "[Chapter 1, Section 1.3]",
        "score": 0.88
    }

    formatted = qdrant_service.format_chunk_for_context(chunk)

    assert "[Chapter 1, Section 1.3]" in formatted
    assert "ROS 2 uses DDS for communication." in formatted


@pytest.mark.asyncio
async def test_search_validates_query(qdrant_service):
    """Test that search validates empty or whitespace queries."""
    with pytest.raises(ValueError) as exc_info:
        await qdrant_service.search(query="", top_k=5)

    assert "Query cannot be empty" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        await qdrant_service.search(query="   ", top_k=5)

    assert "Query cannot be empty" in str(exc_info.value)
