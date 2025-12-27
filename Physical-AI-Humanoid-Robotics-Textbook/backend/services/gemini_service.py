"""
Google Gemini API Service

This service handles interactions with Google's Gemini API for generating
contextual responses based on retrieved textbook content.
"""

from typing import List, Dict, Any, Optional
import google.generativeai as genai
import logging

from config import settings
from models.user_profile import KnowledgeLevel

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service for generating responses using Google Gemini API.

    Handles prompt engineering, context formatting, and response generation
    for the RAG chatbot system.
    """

    def __init__(self):
        """Initialize Gemini API with configuration from environment."""
        try:
            genai.configure(api_key=settings.gemini_api_key)

            # Configure generation parameters
            self.generation_config = {
                "temperature": 0.7,  # Balanced creativity vs consistency
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }

            # Configure safety settings
            self.safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]

            # Initialize model
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
            )

            logger.info("Gemini API initialized with gemini-1.5-pro model")

        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {e}")
            raise

    async def generate_response(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        knowledge_level: KnowledgeLevel = KnowledgeLevel.BEGINNER
    ) -> str:
        """
        Generate a response using Gemini API with retrieved context.

        Args:
            question (str): User's question
            context_chunks (List[Dict]): Retrieved textbook chunks with metadata
            conversation_history (List[Dict]): Previous messages for context
            knowledge_level (KnowledgeLevel): User's knowledge level for adaptive responses

        Returns:
            str: Generated response

        Raises:
            Exception: If generation fails
        """
        try:
            # Build prompt with retrieved context and knowledge level
            prompt = self._build_prompt(question, context_chunks, conversation_history, knowledge_level)

            # Generate response
            response = self.model.generate_content(prompt)

            if response.text:
                logger.info(f"Generated response for question: {question[:50]}...")
                return response.text
            else:
                logger.warning("Gemini returned empty response")
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."

        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise

    def _build_prompt(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        knowledge_level: KnowledgeLevel = KnowledgeLevel.BEGINNER
    ) -> str:
        """
        Build a prompt for Gemini API with context and history.

        Args:
            question (str): User's question
            context_chunks (List[Dict]): Retrieved textbook chunks
            conversation_history (List[Dict]): Previous conversation messages
            knowledge_level (KnowledgeLevel): User's knowledge level

        Returns:
            str: Formatted prompt
        """
        # Adaptive instruction based on knowledge level
        level_instructions = {
            KnowledgeLevel.BEGINNER: """
- Explain concepts in simple, accessible terms
- Use analogies and real-world examples to clarify complex ideas
- Define technical terms when you use them
- Break down complex topics into smaller, digestible parts
- Encourage learning with a supportive tone""",
            KnowledgeLevel.INTERMEDIATE: """
- Balance technical accuracy with clear explanations
- Assume familiarity with basic concepts but explain advanced ones
- Include practical applications and implementation details
- Connect related concepts to build deeper understanding""",
            KnowledgeLevel.ADVANCED: """
- Provide detailed technical explanations with precise terminology
- Discuss implementation details, trade-offs, and edge cases
- Reference advanced concepts and related research areas
- Focus on depth and technical accuracy"""
        }

        # System instruction with adaptive complexity
        system_prompt = f"""You are a helpful AI assistant for the Physical AI & Humanoid Robotics textbook.

Your role:
1. Answer questions ONLY using information from the provided textbook content
2. Include specific citations in the format: [Chapter X, Section Y]
3. If the question cannot be answered from the textbook, politely say so
4. Be clear, educational, and provide examples when helpful
5. Maintain accuracy - do not make up information not in the textbook

Important:
- Always cite your sources using the format: [Chapter X, Section Y]
- If multiple sections are relevant, cite all of them
- Stay focused on Physical AI, humanoid robotics, and related topics

Response Style (User Knowledge Level: {knowledge_level.value.upper()}):
{level_instructions[knowledge_level]}
"""

        # Format retrieved context
        context_text = "\n\n".join([
            f"[Chapter {chunk['metadata']['chapter']}, Section {chunk['metadata']['section']}]\n{chunk['content']}"
            for chunk in context_chunks
        ])

        # Format conversation history
        history_text = ""
        if conversation_history and len(conversation_history) > 0:
            # Include last 5 exchanges for context
            recent_history = conversation_history[-10:]  # Last 5 Q&A pairs
            history_text = "\n\nPrevious conversation:\n"
            for msg in recent_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_text += f"{role}: {msg['content']}\n"

        # Build final prompt
        prompt = f"""{system_prompt}

Textbook Content:
{context_text}
{history_text}

User Question: {question}

Please provide a helpful answer based on the textbook content above. Remember to include citations in the format [Chapter X, Section Y]."""

        return prompt

    def health_check(self) -> bool:
        """
        Check if Gemini API is accessible.

        Returns:
            bool: True if API is healthy, False otherwise
        """
        try:
            # Simple test generation
            test_response = self.model.generate_content("Say 'OK' if you can respond.")
            return test_response.text is not None
        except Exception as e:
            logger.error(f"Gemini health check failed: {e}")
            return False


# Global service instance
gemini_service = GeminiService()
