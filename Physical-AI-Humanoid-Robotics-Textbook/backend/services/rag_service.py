"""
RAG (Retrieval-Augmented Generation) Orchestration Service

This service coordinates the RAG pipeline:
1. Retrieve relevant textbook chunks from Qdrant
2. Generate contextual response using Gemini
3. Extract and format citations
"""

from typing import Dict, Any, List, Optional
import uuid
import logging
import re

from sqlalchemy.ext.asyncio import AsyncSession
from services.qdrant_service import qdrant_service
from services.gemini_service import gemini_service
from services.personalization_service import personalization_service
from models.user_profile import KnowledgeLevel

logger = logging.getLogger(__name__)


class RAGService:
    """
    RAG orchestration service that combines retrieval and generation.

    Coordinates the flow: User Question → Qdrant Retrieval → Gemini Generation → Response with Citations
    """

    def __init__(self):
        """Initialize RAG service with Qdrant and Gemini services."""
        self.qdrant = qdrant_service
        self.gemini = gemini_service
        self.min_relevance_score = 0.5  # Threshold for off-topic detection

    async def process_question(
        self,
        question: str,
        session_id: uuid.UUID,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        db: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """
        Process a user question through the complete RAG pipeline.

        Args:
            question (str): User's question
            session_id (UUID): User session identifier
            conversation_history (List[Dict]): Previous conversation messages
            db (AsyncSession): Database session for personalization

        Returns:
            Dict: Response with text and citations
                {
                    "response": str,
                    "citations": List[Dict],
                    "is_off_topic": bool
                }
        """
        try:
            # Step 1: Get user knowledge level for adaptive responses
            knowledge_level = KnowledgeLevel.BEGINNER  # Default
            if db:
                try:
                    profile = await personalization_service.get_or_create_profile(session_id, db)
                    knowledge_level = profile.knowledge_level
                    logger.info(f"Using knowledge level {knowledge_level} for session {session_id}")
                except Exception as e:
                    logger.warning(f"Could not retrieve knowledge level: {e}")

            # Step 2: Retrieve relevant chunks from Qdrant
            logger.info(f"Processing question for session {session_id}: {question[:50]}...")

            retrieved_chunks = await self.qdrant.search(
                query=question,
                top_k=5,
                score_threshold=self.min_relevance_score
            )

            # Step 2: Check if question is off-topic or search service failed
            if not retrieved_chunks or len(retrieved_chunks) == 0:
                logger.warning(f"No relevant chunks found for question: {question[:50]}...")
                # Could be off-topic OR Qdrant service failure
                # Return generic error message that covers both cases
                return {
                    "response": "I apologize, but I'm having trouble finding relevant information. This could be because the question is outside the textbook scope, or the search service is temporarily unavailable. Please try again in a moment.",
                    "citations": [],
                    "is_off_topic": True
                }

            # Check maximum relevance score
            max_score = max(chunk["score"] for chunk in retrieved_chunks)
            if max_score < self.min_relevance_score:
                logger.warning(f"Low relevance score ({max_score}) for question: {question[:50]}...")
                return {
                    "response": self._get_off_topic_response(),
                    "citations": [],
                    "is_off_topic": True
                }

            # Step 3: Categorize chunks by content type
            content_type_groups = self._group_chunks_by_type(retrieved_chunks)

            # Step 4: Generate response using Gemini with knowledge level and content types
            response_text = await self.gemini.generate_response(
                question=question,
                context_chunks=retrieved_chunks,
                conversation_history=conversation_history,
                knowledge_level=knowledge_level,
                content_type_groups=content_type_groups
            )

            # Step 4: Extract and format citations
            citations = self._extract_citations(retrieved_chunks, response_text)

            logger.info(f"Successfully processed question with {len(citations)} citations")

            return {
                "response": response_text,
                "citations": citations,
                "is_off_topic": False
            }

        except Exception as e:
            logger.error(f"RAG processing failed: {e}")
            return {
                "response": self._get_error_response(),
                "citations": [],
                "is_off_topic": False
            }

    def _group_chunks_by_type(
        self,
        retrieved_chunks: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group retrieved chunks by content type.

        Args:
            retrieved_chunks (List[Dict]): Chunks from Qdrant

        Returns:
            Dict[str, List[Dict]]: Chunks grouped by content type
                {
                    "text": [chunk1, chunk2, ...],
                    "code": [chunk3, ...],
                    "diagram": [chunk4, ...]
                }
        """
        groups = {
            "text": [],
            "code": [],
            "diagram": []
        }

        for chunk in retrieved_chunks:
            content_type = chunk["metadata"].get("content_type", "text")
            if content_type in groups:
                groups[content_type].append(chunk)
            else:
                # Default unknown types to text
                groups["text"].append(chunk)

        logger.info(
            f"Grouped chunks: {len(groups['text'])} text, "
            f"{len(groups['code'])} code, {len(groups['diagram'])} diagrams"
        )

        return groups

    def _extract_citations(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        response_text: str
    ) -> List[Dict[str, str]]:
        """
        Extract citations from retrieved chunks and response text.

        Args:
            retrieved_chunks (List[Dict]): Chunks from Qdrant
            response_text (str): Generated response text

        Returns:
            List[Dict]: Formatted citations
                [{
                    "chapter": str,
                    "section": str,
                    "page": str,
                    "text": str (formatted citation)
                }]
        """
        citations = []

        # Pattern to match citations in response: [Chapter X, Section Y]
        citation_pattern = r'\[Chapter\s+(\d+),\s*Section\s+([^\]]+)\]'
        found_citations = re.findall(citation_pattern, response_text)

        # Create set of cited chapters and sections
        cited_sources = {(chapter, section) for chapter, section in found_citations}

        # Match with retrieved chunks
        for chunk in retrieved_chunks:
            metadata = chunk["metadata"]
            chapter = str(metadata.get("chapter", ""))
            section = str(metadata.get("section", ""))

            # Check if this chunk was cited in the response
            # If explicit citations found, only include those
            # Otherwise, include all retrieved chunks
            if cited_sources:
                if (chapter, section) not in cited_sources:
                    continue

            citation = {
                "chapter": chapter,
                "section": section,
                "page": str(metadata.get("page", "")),
                "text": f"[Chapter {chapter}, Section {section}]",
                "content_type": metadata.get("content_type", "text")
            }

            # Avoid duplicates
            if citation not in citations:
                citations.append(citation)

        # If no specific citations were found in response, include all retrieved chunks
        if not citations:
            for chunk in retrieved_chunks:
                metadata = chunk["metadata"]
                citations.append({
                    "chapter": str(metadata.get("chapter", "")),
                    "section": str(metadata.get("section", "")),
                    "page": str(metadata.get("page", "")),
                    "text": f"[Chapter {metadata.get('chapter', '')}, Section {metadata.get('section', '')}]",
                    "content_type": metadata.get("content_type", "text")
                })

        return citations

    def _get_off_topic_response(self) -> str:
        """
        Get standard response for off-topic questions.

        Returns:
            str: Polite off-topic message
        """
        return (
            "I'm sorry, but I can only answer questions about the Physical AI & Humanoid Robotics textbook content. "
            "Your question seems to be outside the scope of the textbook topics. "
            "Please ask questions related to physical AI, humanoid robotics, vision-language-action models, "
            "or other topics covered in the textbook."
        )

    def _get_error_response(self) -> str:
        """
        Get standard response for processing errors.

        Returns:
            str: User-friendly error message
        """
        return (
            "I apologize, but I encountered an error while processing your question. "
            "Please try again in a moment. If the problem persists, try rephrasing your question."
        )


# Global service instance
rag_service = RAGService()
