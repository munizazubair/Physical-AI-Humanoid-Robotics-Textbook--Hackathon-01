"""
Qdrant Vector Database Service

This service handles semantic search operations against the Qdrant vector database
containing embedded textbook content chunks.
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest, Filter, FieldCondition, MatchValue
import logging
import cohere
import asyncio
from functools import partial

from config import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """
    Service for interacting with Qdrant vector database.

    Performs semantic search over textbook content to retrieve relevant
    chunks for RAG (Retrieval-Augmented Generation).
    """

    def __init__(self):
        """Initialize Qdrant client with configuration from environment."""
        try:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                timeout=60.0,  # Increased from 10s to 60s to accommodate Cohere API
            )
            self.collection_name = "textbook_embeddings"  # Updated collection name

            # Initialize Cohere client for embeddings
            self.cohere_client = cohere.Client(
                api_key=settings.cohere_api_key,
                timeout=120.0  # 120-second timeout for embedding generation (first call can be slow)
            )

            logger.info(f"Qdrant client initialized for {settings.qdrant_url}")
            logger.info("Cohere embeddings client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant/Cohere client: {e}")
            raise

    async def search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search for relevant textbook chunks.

        Args:
            query (str): User's search query
            top_k (int): Number of results to return (default: 5)
            score_threshold (float): Minimum relevance score (default: 0.5)
            filters (dict): Optional metadata filters (e.g., {"chapter": "2"})

        Returns:
            List[Dict]: List of search results with metadata
                Each result contains:
                - content (str): Chunk text
                - metadata (dict): Chapter, section, page info
                - score (float): Relevance score

        Raises:
            Exception: If search fails or Qdrant is unavailable
        """
        try:
            # Generate embedding for the query using Cohere (run in thread pool to avoid blocking)
            logger.info(f"Generating embedding for query: {query[:50]}...")

            # Run synchronous Cohere call in thread pool
            loop = asyncio.get_event_loop()
            embedding_response = await loop.run_in_executor(
                None,
                partial(
                    self.cohere_client.embed,
                    texts=[query],
                    model="embed-english-v3.0",
                    input_type="search_query"
                )
            )

            query_vector = embedding_response.embeddings[0]
            logger.info(f"Query embedding generated: {len(query_vector)} dimensions")

            # Build filter conditions if provided
            filter_conditions = None
            if filters:
                filter_conditions = Filter(
                    must=[
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                        for key, value in filters.items()
                    ]
                )

            # Perform search with the query vector
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                score_threshold=score_threshold,
                query_filter=filter_conditions,
            )

            # Format results
            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    "content": result.payload.get("text", ""),
                    "metadata": {
                        "chapter": result.payload.get("chapter", ""),
                        "section": result.payload.get("section", ""),
                        "page": result.payload.get("page", ""),
                        "content_type": result.payload.get("content_type", "text"),
                    },
                    "score": result.score,
                })

            logger.info(f"Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results

        except Exception as e:
            logger.error(f"Qdrant search failed: {e}", exc_info=True)
            logger.warning(
                "Qdrant service unavailable - returning empty results for graceful degradation. "
                "RAG service will return error message to user."
            )
            # Return empty results instead of raising to allow graceful degradation
            return []

    async def search_with_embedding(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        score_threshold: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search using pre-computed embedding vector.

        Args:
            query_embedding (List[float]): Query embedding vector
            top_k (int): Number of results to return
            score_threshold (float): Minimum relevance score

        Returns:
            List[Dict]: Search results with metadata
        """
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=score_threshold,
            )

            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    "content": result.payload.get("text", ""),
                    "metadata": {
                        "chapter": result.payload.get("chapter", ""),
                        "section": result.payload.get("section", ""),
                        "page": result.payload.get("page", ""),
                        "content_type": result.payload.get("content_type", "text"),
                    },
                    "score": result.score,
                })

            return formatted_results

        except Exception as e:
            logger.error(f"Qdrant embedding search failed: {e}")
            return []

    def health_check(self) -> bool:
        """
        Check if Qdrant service is accessible.

        Returns:
            bool: True if Qdrant is healthy, False otherwise
        """
        try:
            collections = self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False


# Global service instance
qdrant_service = QdrantService()
