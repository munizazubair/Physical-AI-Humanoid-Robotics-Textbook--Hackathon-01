"""
Google Gemini API Service

This service handles interactions with Google's Gemini API for generating
contextual responses based on retrieved textbook content.
"""

from typing import List, Dict, Any, Optional
import google.generativeai as genai
import logging
import time

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
                model_name="gemini-2.5-flash",  # Free tier model with good performance
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
            )

            logger.info("Gemini API initialized with gemini-2.5-flash model")

        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {e}")
            raise

    async def generate_response(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        knowledge_level: KnowledgeLevel = KnowledgeLevel.BEGINNER,
        content_type_groups: Optional[Dict[str, List[Dict[str, Any]]]] = None
    ) -> str:
        """
        Generate a response using Gemini API with retrieved context.

        Args:
            question (str): User's question
            context_chunks (List[Dict]): Retrieved textbook chunks with metadata
            conversation_history (List[Dict]): Previous messages for context
            knowledge_level (KnowledgeLevel): User's knowledge level for adaptive responses
            content_type_groups (Dict): Chunks grouped by content type

        Returns:
            str: Generated response

        Raises:
            Exception: If generation fails
        """
        # Retry with exponential backoff
        max_retries = 2
        base_delay = 1  # seconds

        for attempt in range(max_retries + 1):
            try:
                # Build prompt with retrieved context, knowledge level, and content types
                prompt = self._build_prompt(
                    question,
                    context_chunks,
                    conversation_history,
                    knowledge_level,
                    content_type_groups
                )

                # Generate response
                response = self.model.generate_content(prompt)

                if response.text:
                    logger.info(f"Generated response for question: {question[:50]}... (attempt {attempt + 1})")
                    return response.text
                else:
                    logger.warning("Gemini returned empty response")
                    return "I apologize, but I couldn't generate a response. Please try rephrasing your question."

            except Exception as e:
                logger.error(f"Gemini generation failed (attempt {attempt + 1}/{max_retries + 1}): {e}")

                # Check if this was the last attempt
                if attempt == max_retries:
                    logger.error("All Gemini retry attempts exhausted", exc_info=True)
                    return "Response generation is temporarily unavailable. Please try again in a moment."

                # Exponential backoff: wait before retrying
                delay = base_delay * (2 ** attempt)
                logger.info(f"Retrying after {delay} seconds...")
                time.sleep(delay)

    def _build_prompt(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        knowledge_level: KnowledgeLevel = KnowledgeLevel.BEGINNER,
        content_type_groups: Optional[Dict[str, List[Dict[str, Any]]]] = None
    ) -> str:
        """
        Build a prompt for Gemini API with context and history.

        Args:
            question (str): User's question
            context_chunks (List[Dict]): Retrieved textbook chunks
            conversation_history (List[Dict]): Previous conversation messages
            knowledge_level (KnowledgeLevel): User's knowledge level
            content_type_groups (Dict): Chunks grouped by content type

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

        # Multi-modal content instructions
        content_type_instructions = ""
        if content_type_groups:
            has_code = len(content_type_groups.get("code", [])) > 0
            has_diagrams = len(content_type_groups.get("diagram", [])) > 0

            if has_code or has_diagrams:
                content_type_instructions = "\n\nMulti-Modal Content Guidelines:\n"
                if has_diagrams:
                    content_type_instructions += "- When referencing diagrams, use: 'Refer to Figure X in [Chapter Y, Section Z]'\n"
                    content_type_instructions += "- Explicitly mention diagram relevance in your explanation\n"
                if has_code:
                    content_type_instructions += "- When referencing code examples, use: 'See code example in [Chapter Y, Section Z]'\n"
                    content_type_instructions += "- Explain what the code does in context of the question\n"

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
- Stay focused on Physical AI, humanoid robotics, and related topics{content_type_instructions}

Response Style (User Knowledge Level: {knowledge_level.value.upper()}):
{level_instructions[knowledge_level]}
"""

        # Format retrieved context with content type labels
        context_parts = []
        for chunk in context_chunks:
            metadata = chunk['metadata']
            content_type = metadata.get('content_type', 'text')

            # Add content type label
            type_label = ""
            if content_type == "code":
                type_label = " [CODE EXAMPLE]"
            elif content_type == "diagram":
                type_label = " [DIAGRAM/FIGURE]"

            context_parts.append(
                f"[Chapter {metadata['chapter']}, Section {metadata['section']}]{type_label}\n{chunk['content']}"
            )

        context_text = "\n\n".join(context_parts)

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
