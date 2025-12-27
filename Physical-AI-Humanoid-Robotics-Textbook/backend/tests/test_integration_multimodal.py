"""
Integration Tests for Multi-Modal Content Retrieval

Tests that the RAG pipeline correctly handles different content types
(text, code, diagrams) and includes appropriate references in responses.
"""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

from services.rag_service import rag_service
from models.user_profile import KnowledgeLevel


@pytest.fixture
def mock_qdrant_search_with_code():
    """Mock Qdrant search that returns code chunks."""
    return [
        {
            "content": "import rclpy\nfrom rclpy.node import Node\n\nclass MinimalPublisher(Node):\n    def __init__(self):\n        super().__init__('minimal_publisher')",
            "metadata": {
                "chapter": "1",
                "section": "1.4",
                "page": "12",
                "content_type": "code"
            },
            "score": 0.92
        },
        {
            "content": "ROS 2 provides a powerful publish-subscribe messaging system for inter-node communication.",
            "metadata": {
                "chapter": "1",
                "section": "1.3",
                "page": "10",
                "content_type": "text"
            },
            "score": 0.85
        }
    ]


@pytest.fixture
def mock_qdrant_search_with_diagram():
    """Mock Qdrant search that returns diagram chunks."""
    return [
        {
            "content": "Figure 2.1: ROS 2 Communication Architecture - This diagram shows the publisher-subscriber pattern with nodes, topics, and messages.",
            "metadata": {
                "chapter": "2",
                "section": "2.1",
                "page": "18",
                "content_type": "diagram"
            },
            "score": 0.95
        },
        {
            "content": "The ROS 2 architecture consists of multiple layers including the middleware, transport, and application layers.",
            "metadata": {
                "chapter": "2",
                "section": "2.1",
                "page": "17",
                "content_type": "text"
            },
            "score": 0.88
        }
    ]


@pytest.fixture
def mock_qdrant_search_mixed_types():
    """Mock Qdrant search that returns mixed content types."""
    return [
        {
            "content": "Digital twins provide virtual representations of physical robots for simulation and testing.",
            "metadata": {
                "chapter": "3",
                "section": "3.1",
                "page": "35",
                "content_type": "text"
            },
            "score": 0.90
        },
        {
            "content": "Figure 3.2: Digital Twin Architecture - Shows the connection between physical robot and virtual model.",
            "metadata": {
                "chapter": "3",
                "section": "3.2",
                "page": "38",
                "content_type": "diagram"
            },
            "score": 0.87
        },
        {
            "content": "// URDF example for robot description\n<robot name='my_robot'>\n  <link name='base_link'/>\n</robot>",
            "metadata": {
                "chapter": "3",
                "section": "3.3",
                "page": "40",
                "content_type": "code"
            },
            "score": 0.85
        }
    ]


@pytest.mark.asyncio
async def test_content_type_grouping_code_and_text(mock_qdrant_search_with_code):
    """Test that content is correctly grouped by type (code + text)."""
    groups = rag_service._group_chunks_by_type(mock_qdrant_search_with_code)

    assert "text" in groups
    assert "code" in groups
    assert "diagram" in groups

    assert len(groups["code"]) == 1
    assert len(groups["text"]) == 1
    assert len(groups["diagram"]) == 0

    # Verify code chunk is in code group
    assert groups["code"][0]["metadata"]["content_type"] == "code"
    assert "import rclpy" in groups["code"][0]["content"]


@pytest.mark.asyncio
async def test_content_type_grouping_diagram_and_text(mock_qdrant_search_with_diagram):
    """Test that content is correctly grouped by type (diagram + text)."""
    groups = rag_service._group_chunks_by_type(mock_qdrant_search_with_diagram)

    assert len(groups["diagram"]) == 1
    assert len(groups["text"]) == 1
    assert len(groups["code"]) == 0

    # Verify diagram chunk
    assert groups["diagram"][0]["metadata"]["content_type"] == "diagram"
    assert "Figure 2.1" in groups["diagram"][0]["content"]


@pytest.mark.asyncio
async def test_content_type_grouping_mixed_types(mock_qdrant_search_mixed_types):
    """Test grouping with all content types present."""
    groups = rag_service._group_chunks_by_type(mock_qdrant_search_mixed_types)

    assert len(groups["text"]) == 1
    assert len(groups["diagram"]) == 1
    assert len(groups["code"]) == 1

    # Verify each type
    assert "Digital twins" in groups["text"][0]["content"]
    assert "Figure 3.2" in groups["diagram"][0]["content"]
    assert "URDF" in groups["code"][0]["content"]


@pytest.mark.asyncio
@patch('services.rag_service.qdrant_service.search')
@patch('services.rag_service.gemini_service.generate_response')
async def test_code_example_question_includes_code_content_type(
    mock_gemini,
    mock_qdrant,
    mock_qdrant_search_with_code
):
    """Test that questions about code examples retrieve and cite code chunks."""
    mock_qdrant.return_value = mock_qdrant_search_with_code
    mock_gemini.return_value = "Here's a ROS 2 publisher example. See code example in [Chapter 1, Section 1.4]."

    session_id = uuid.uuid4()
    question = "Show me a code example of a ROS 2 publisher"

    result = await rag_service.process_question(
        question=question,
        session_id=session_id
    )

    # Verify response was generated
    assert result["response"]
    assert not result["is_off_topic"]

    # Verify citations include content type
    assert len(result["citations"]) > 0
    code_citation = next(
        (c for c in result["citations"] if c.get("content_type") == "code"),
        None
    )
    assert code_citation is not None
    assert code_citation["chapter"] == "1"
    assert code_citation["section"] == "1.4"

    # Verify Gemini was called with content type groups
    mock_gemini.assert_called_once()
    call_kwargs = mock_gemini.call_args.kwargs
    assert "content_type_groups" in call_kwargs
    groups = call_kwargs["content_type_groups"]
    assert len(groups["code"]) > 0


@pytest.mark.asyncio
@patch('services.rag_service.qdrant_service.search')
@patch('services.rag_service.gemini_service.generate_response')
async def test_diagram_question_includes_diagram_content_type(
    mock_gemini,
    mock_qdrant,
    mock_qdrant_search_with_diagram
):
    """Test that questions about diagrams retrieve and cite diagram chunks."""
    mock_qdrant.return_value = mock_qdrant_search_with_diagram
    mock_gemini.return_value = "Refer to Figure 2.1 in [Chapter 2, Section 2.1] which shows the ROS 2 architecture."

    session_id = uuid.uuid4()
    question = "Show me the ROS 2 architecture diagram"

    result = await rag_service.process_question(
        question=question,
        session_id=session_id
    )

    # Verify citations include diagram
    diagram_citation = next(
        (c for c in result["citations"] if c.get("content_type") == "diagram"),
        None
    )
    assert diagram_citation is not None
    assert "Figure" in result["response"] or "figure" in result["response"].lower()


@pytest.mark.asyncio
@patch('services.rag_service.qdrant_service.search')
@patch('services.rag_service.gemini_service.generate_response')
async def test_gemini_receives_content_type_labels(
    mock_gemini,
    mock_qdrant,
    mock_qdrant_search_mixed_types
):
    """Test that Gemini receives content with proper type labels."""
    mock_qdrant.return_value = mock_qdrant_search_mixed_types
    mock_gemini.return_value = "Digital twins are virtual models. Refer to Figure 3.2 in [Chapter 3, Section 3.2]."

    session_id = uuid.uuid4()
    question = "What are digital twins in robotics?"

    await rag_service.process_question(
        question=question,
        session_id=session_id
    )

    # Verify Gemini was called
    mock_gemini.assert_called_once()
    call_kwargs = mock_gemini.call_args.kwargs

    # Verify content type groups were passed
    assert "content_type_groups" in call_kwargs
    groups = call_kwargs["content_type_groups"]
    assert groups["text"]
    assert groups["diagram"]
    assert groups["code"]


@pytest.mark.asyncio
async def test_citation_extraction_preserves_content_type():
    """Test that content type is preserved in extracted citations."""
    retrieved_chunks = [
        {
            "content": "Sample text content",
            "metadata": {
                "chapter": "1",
                "section": "1.1",
                "page": "5",
                "content_type": "text"
            },
            "score": 0.9
        },
        {
            "content": "Sample code content",
            "metadata": {
                "chapter": "1",
                "section": "1.2",
                "page": "6",
                "content_type": "code"
            },
            "score": 0.85
        }
    ]

    response_text = "Here is the answer. [Chapter 1, Section 1.1] and [Chapter 1, Section 1.2]"

    citations = rag_service._extract_citations(retrieved_chunks, response_text)

    assert len(citations) == 2

    # Find text citation
    text_citation = next(c for c in citations if c["section"] == "1.1")
    assert text_citation["content_type"] == "text"

    # Find code citation
    code_citation = next(c for c in citations if c["section"] == "1.2")
    assert code_citation["content_type"] == "code"


@pytest.mark.asyncio
async def test_default_content_type_for_missing_metadata():
    """Test that missing content_type defaults to 'text'."""
    chunks_without_type = [
        {
            "content": "Content without type metadata",
            "metadata": {
                "chapter": "1",
                "section": "1.1",
                "page": "5"
                # content_type is missing
            },
            "score": 0.9
        }
    ]

    groups = rag_service._group_chunks_by_type(chunks_without_type)

    # Should default to text group
    assert len(groups["text"]) == 1
    assert len(groups["code"]) == 0
    assert len(groups["diagram"]) == 0


@pytest.mark.asyncio
@patch('services.rag_service.qdrant_service.search')
@patch('services.rag_service.gemini_service.generate_response')
async def test_multimodal_response_quality(
    mock_gemini,
    mock_qdrant,
    mock_qdrant_search_mixed_types
):
    """Test that responses appropriately reference different content types."""
    mock_qdrant.return_value = mock_qdrant_search_mixed_types
    mock_gemini.return_value = (
        "Digital twins provide virtual representations of physical robots. "
        "Refer to Figure 3.2 in [Chapter 3, Section 3.2] for the architecture. "
        "See code example in [Chapter 3, Section 3.3] for URDF implementation."
    )

    session_id = uuid.uuid4()
    question = "Explain digital twins with examples"

    result = await rag_service.process_question(
        question=question,
        session_id=session_id
    )

    # Verify response mentions multiple content types
    response = result["response"]
    assert "Figure" in response or "diagram" in response.lower()
    assert "code example" in response.lower() or "urdf" in response.lower()

    # Verify multiple citations with different types
    citations = result["citations"]
    assert len(citations) >= 2

    content_types_cited = {c.get("content_type") for c in citations}
    assert "diagram" in content_types_cited or "code" in content_types_cited
