# Feature Specification: RAG Chatbot for Physical AI Textbook

**Feature Branch**: `002-rag-chatbot`
**Created**: 2025-12-26
**Status**: Draft
**Input**: User description: "Create a separate specification file specifically for the RAG chatbot, FastAPI backend, ChatKit integration, and Neon personalization layer. This spec is independent from the book ingestion/Qdrant spec file. Design a complete architecture for a RAG chatbot to be embedded inside a deployed Docusaurus textbook on Physical AI & Humanoid Robotics."

## Executive Summary

This specification defines a RAG (Retrieval-Augmented Generation) chatbot system embedded within the deployed Physical AI & Humanoid Robotics textbook on GitHub Pages. The chatbot provides intelligent, context-aware assistance to learners by retrieving relevant content from the book (stored in Qdrant vector database) and generating helpful responses using Google's Gemini language models. The system includes user personalization, conversation history, and seamless integration with the Docusaurus documentation interface.

## User Scenarios & Testing

### User Story 1 - Basic Question Answering (Priority: P1)

A student reading Chapter 5 on ROS 2 Services encounters an unfamiliar concept and asks the chatbot for clarification. The chatbot retrieves relevant context from the textbook and provides a concise, accurate explanation with references to specific chapters.

**Why this priority**: This is the core value proposition - instant, contextual help while studying. Without this, the chatbot has no purpose.

**Independent Test**: Can be fully tested by opening the textbook, clicking the chat widget, asking "What is a ROS 2 service?" and verifying the response includes relevant book content with chapter references.

**Acceptance Scenarios**:

1. **Given** a user is viewing any page in the textbook, **When** they click the chat widget icon, **Then** a chat interface opens with a welcome message
2. **Given** the chat interface is open, **When** the user types "Explain ROS 2 topics" and presses send, **Then** the chatbot responds within 5 seconds with an explanation drawn from the textbook content
3. **Given** the chatbot has answered a question, **When** the response is displayed, **Then** it includes citations showing which chapters/sections the information came from
4. **Given** the user asks a question outside the textbook's scope (e.g., "What's the weather?"), **When** the chatbot responds, **Then** it politely indicates the question is outside its knowledge domain and suggests textbook-related topics

---

### User Story 2 - Conversation History & Context (Priority: P2)

A learner has an ongoing conversation with the chatbot across multiple sessions, asking follow-up questions about digital twins. The system remembers previous questions from the same user and provides contextually relevant answers that build on earlier discussions.

**Why this priority**: Enhances learning by enabling deeper, multi-turn conversations. However, basic Q&A (P1) must work first.

**Independent Test**: Can be tested by asking an initial question ("What is a digital twin?"), closing the chat, reopening it, and asking a follow-up ("How is it different from a simulator?"). The chatbot should reference the prior question.

**Acceptance Scenarios**:

1. **Given** a user has asked a question in a previous session, **When** they return to the textbook and open the chat, **Then** their conversation history is loaded and visible
2. **Given** a user asked "What is Isaac Sim?" in a previous message, **When** they ask "How does it compare to Gazebo?", **Then** the chatbot understands the context and compares Isaac Sim to Gazebo without re-explaining Isaac Sim
3. **Given** a user has 10+ messages in their history, **When** they scroll the chat interface, **Then** all historical messages are accessible and properly formatted
4. **Given** a user wants to start fresh, **When** they click "New Conversation" or similar option, **Then** the chat history is cleared and a new conversation begins

---

### User Story 3 - Personalized Learning Assistance (Priority: P3)

A student who frequently asks questions about VLA (Vision-Language-Action) systems receives personalized suggestions and content recommendations based on their interaction patterns and learning progress.

**Why this priority**: Adds significant value but requires P1 and P2 to be functional. This is an enhancement that improves long-term engagement.

**Independent Test**: Can be tested by simulating multiple user sessions asking questions clustered around specific topics (e.g., VLA), then verifying the chatbot proactively suggests related content or identifies knowledge gaps.

**Acceptance Scenarios**:

1. **Given** a user has asked 5+ questions about VLA systems, **When** they open the chat, **Then** the chatbot greets them with a message acknowledging their interest in VLA and suggests related chapters
2. **Given** a user has read Chapter 15 (VLA intro) but not Chapter 16-18, **When** they finish a conversation about VLA basics, **Then** the chatbot suggests "Next, you might want to explore Chapter 16 on Vision Systems"
3. **Given** a user struggles with a concept (asks 3+ similar questions), **When** the chatbot detects this pattern, **Then** it offers alternative explanations or suggests prerequisite chapters
4. **Given** a user has completed reading all ROS 2 chapters, **When** they ask about advanced topics, **Then** the chatbot adjusts its response complexity to match their demonstrated knowledge level

---

### User Story 4 - Multi-Modal Content Integration (Priority: P4)

A student asks about a diagram from Chapter 8 (Gazebo Simulation), and the chatbot not only explains the concept but also references the specific ASCII diagram or image from the textbook, helping the user locate visual aids.

**Why this priority**: Enhances the learning experience by connecting text explanations to visual content. This is valuable but not essential for MVP.

**Independent Test**: Can be tested by asking "Explain the ROS 2 architecture diagram" and verifying the response includes references to the specific diagram location and explanation.

**Acceptance Scenarios**:

1. **Given** a chapter contains a diagram or code example, **When** a user asks about that visual content, **Then** the chatbot references the specific diagram/example and its location in the textbook
2. **Given** a user asks "Show me an example of a ROS 2 node", **When** the chatbot responds, **Then** it references the relevant code example from the textbook and provides the chapter/section number
3. **Given** a diagram has multiple components, **When** the user asks about a specific part, **Then** the chatbot explains that component and how it relates to the overall diagram
4. **Given** the textbook contains both ASCII diagrams and text descriptions, **When** the chatbot retrieves content, **Then** it includes both the visual representation and the textual explanation

---

### User Story 5 - Error Recovery & Feedback (Priority: P5)

When the chatbot provides an incorrect or unhelpful answer, the user can provide feedback (thumbs up/down), and the system logs this for improvement. Additionally, if the RAG system fails to retrieve relevant content, the chatbot gracefully handles the error.

**Why this priority**: Improves system reliability and provides data for continuous improvement. This is a polish feature that enhances quality but isn't blocking for launch.

**Independent Test**: Can be tested by asking a deliberately obscure question, receiving a "I don't have enough information" response, and verifying the graceful degradation. Then test the feedback mechanism by clicking thumbs down.

**Acceptance Scenarios**:

1. **Given** the chatbot provides a response, **When** the user clicks thumbs up/down, **Then** the feedback is recorded with the question, response, and timestamp
2. **Given** the Qdrant vector database is unavailable, **When** a user asks a question, **Then** the chatbot displays an error message: "I'm having trouble accessing the textbook content right now. Please try again in a moment."
3. **Given** the Gemini API times out, **When** a user's question is pending, **Then** the chatbot shows a loading indicator and retries up to 2 times before displaying an error
4. **Given** a user reports a bug via feedback, **When** the feedback is submitted, **Then** it's logged to the personalization database with user context for review
5. **Given** the chatbot receives multiple thumbs-down for a specific topic, **When** the system is reviewed, **Then** that topic is flagged for content improvement in the textbook

---

### Edge Cases

- **What happens when a user asks a question in a language other than English?** The chatbot should respond in English (the textbook's language) with a polite message: "I currently support questions in English. Please ask your question in English, and I'll be happy to help!"
- **How does the system handle very long questions (>500 words)?** The chatbot should truncate or summarize the question to stay within API token limits, responding with: "Your question is quite long. I'll focus on the key parts: [summarized question]"
- **What happens if a user pastes code or technical content?** The chatbot should recognize code blocks and technical jargon, treating them as valid inputs and responding with relevant technical content from the textbook.
- **How does the chatbot handle rapid-fire questions (multiple questions in <10 seconds)?** The system should queue requests and process them sequentially, displaying a "typing..." indicator for pending responses.
- **What happens if a user's conversation history exceeds 100 messages?** The system should implement sliding window context (keep last 20 messages in active context) while maintaining full history in the database for retrieval.
- **How does the system behave on mobile devices with limited screen space?** The chat widget should be responsive, collapsing to a minimal icon when closed and expanding to a mobile-optimized interface when opened.
- **What happens if the user's browser blocks third-party cookies (affecting session management)?** The system should fall back to local storage for conversation persistence, warning the user if neither is available.
- **How does the chatbot handle ambiguous questions (e.g., "What is ROS?" - could be ROS 1 or ROS 2)?** The chatbot should ask for clarification: "Are you asking about ROS 1 or ROS 2? This textbook focuses on ROS 2, which is covered in Module 1."

## Requirements

### Functional Requirements

**Core Chat Functionality**

- **FR-001**: System MUST provide a chat interface widget embedded on every page of the deployed Docusaurus textbook
- **FR-002**: System MUST accept natural language questions from users via text input
- **FR-003**: System MUST retrieve relevant context from the Qdrant vector database using semantic search
- **FR-004**: System MUST generate responses using Google Gemini API augmented with retrieved textbook content
- **FR-005**: System MUST include chapter/section citations in responses showing which parts of the textbook were referenced
- **FR-006**: System MUST respond to user questions within 5 seconds under normal load conditions
- **FR-007**: System MUST handle questions outside the textbook's scope by politely declining and suggesting relevant topics

**Conversation Management**

- **FR-008**: System MUST maintain conversation history for each user across multiple sessions
- **FR-009**: System MUST provide conversation context to the language model to enable coherent multi-turn dialogues
- **FR-010**: System MUST allow users to start a new conversation, clearing the current context
- **FR-011**: System MUST persist conversation history in the Neon PostgreSQL database
- **FR-012**: System MUST implement a sliding window context mechanism keeping the last 20 messages in active memory while maintaining full history in storage

**Personalization**

- **FR-013**: System MUST track user interaction patterns (topics asked about, chapters referenced, frequency of questions)
- **FR-014**: System MUST identify users via session identifiers or anonymous user IDs
- **FR-015**: System MUST store user preferences and learning progress in the Neon personalization layer
- **FR-016**: System MUST provide personalized greetings and content recommendations based on user history
- **FR-017**: System MUST detect when a user struggles with a concept (e.g., repeated similar questions) and adjust response complexity

**Content Integration**

- **FR-018**: System MUST reference specific textbook content including chapters, sections, and page-equivalent anchors
- **FR-019**: System MUST handle ASCII diagrams, code examples, and technical terminology from the textbook
- **FR-020**: System MUST provide direct links to relevant sections of the textbook when referencing content
- **FR-021**: System MUST differentiate between foundational concepts (Foundation module) and advanced topics (VLA module) in responses

**Error Handling & Feedback**

- **FR-022**: System MUST provide user feedback mechanisms (thumbs up/down or rating) for chatbot responses
- **FR-023**: System MUST log all user feedback with associated questions and responses for analysis
- **FR-024**: System MUST gracefully degrade when external dependencies (Qdrant, Gemini API) are unavailable
- **FR-025**: System MUST display clear error messages to users when failures occur
- **FR-026**: System MUST retry failed API calls up to 2 times before displaying an error
- **FR-027**: System MUST implement rate limiting to prevent abuse (max 20 questions per user per hour)

**Security & Privacy**

- **FR-028**: System MUST NOT collect personally identifiable information (PII) unless explicitly provided by the user
- **FR-029**: System MUST sanitize user inputs to prevent injection attacks or malicious content
- **FR-030**: System MUST implement CORS policies to restrict API access to the deployed textbook domain
- **FR-031**: System MUST encrypt conversation data at rest in the Neon database
- **FR-032**: System MUST provide users the option to delete their conversation history

**Integration Requirements**

- **FR-033**: System MUST integrate with the existing Qdrant Cloud Free Tier vector database containing book embeddings
- **FR-034**: System MUST expose a FastAPI backend with RESTful endpoints for chat interactions
- **FR-035**: System MUST use @chatscope/chat-ui-kit-react or equivalent UI library for the chat interface components
- **FR-036**: Backend service MUST be deployable independently from the static Docusaurus site. Frontend integration embeds chat components in Docusaurus `src/` directory (not a separate application).
- **FR-037**: System MUST support cross-origin requests from the GitHub Pages deployment
- **FR-037a**: System MUST expose backend API URL to frontend via Docusaurus customFields or build-time substitution to enable dynamic environment configuration (development vs production)

### Key Entities

- **User Session**: Represents an anonymous or identified user interacting with the chatbot. Attributes include session ID, user ID (optional), creation timestamp, last activity timestamp, and associated conversation ID.

- **Conversation**: Represents a dialogue thread between a user and the chatbot. Attributes include conversation ID, user session ID, creation timestamp, messages (list of Message entities), and status (active/archived).

- **Message**: Represents a single exchange in a conversation. Attributes include message ID, conversation ID, role (user/assistant), content (text), timestamp, retrieved chunks (references to textbook content), and feedback score (thumbs up/down).

- **Textbook Chunk**: Represents a retrievable segment of the textbook stored in Qdrant. Attributes include chunk ID, chapter number, section title, content text, vector embedding, and metadata (module, difficulty level, keywords).

- **User Profile**: Represents personalization data for a user. Attributes include user ID, topics of interest (inferred from questions), chapters completed, knowledge level (beginner/intermediate/advanced), and interaction statistics (total questions asked, favorite topics).

- **Feedback Event**: Represents user feedback on chatbot responses. Attributes include feedback ID, message ID, user session ID, rating (thumbs up/down or 1-5 stars), optional text comment, and timestamp.

- **RAG Context**: Represents the retrieved context used to generate a response. Attributes include context ID, message ID, retrieved chunks (list of Textbook Chunk IDs), relevance scores, and token count.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can ask a question and receive a relevant response within 5 seconds for 95% of queries
- **SC-002**: Chatbot responses include accurate citations to textbook chapters in 90% of answers
- **SC-003**: Users rate chatbot responses as helpful (thumbs up) in at least 70% of interactions
- **SC-004**: System maintains conversation context across sessions, with 90% of follow-up questions correctly understanding prior context
- **SC-005**: Chatbot correctly declines to answer off-topic questions (not in textbook scope) in 95% of cases
- **SC-006**: System handles 100 concurrent users without response time degradation beyond 10%
- **SC-007**: Personalization features detect user interests and provide relevant suggestions within 3 interactions
- **SC-008**: System uptime is at least 99% during the hackathon evaluation period
- **SC-009**: User conversation history is persisted and retrievable across browser sessions for 100% of users
- **SC-010**: Chat widget loads and becomes interactive within 2 seconds on the deployed textbook page
- **SC-011**: Error messages are displayed to users within 3 seconds when external services fail
- **SC-012**: System successfully retrieves relevant textbook content from Qdrant in 95% of queries

## Scope

### In Scope

- FastAPI backend service with REST endpoints for chat interactions
- Integration with existing Qdrant Cloud Free Tier vector database containing textbook embeddings
- Google Gemini API integration for response generation using Gemini Pro or Gemini 1.5 Pro
- ChatKit or equivalent React-based chat UI component library
- Neon PostgreSQL database for conversation history and user personalization
- Conversation management (multi-turn dialogues, context retention)
- User feedback mechanisms (thumbs up/down)
- Personalized content recommendations based on user interaction patterns
- Citation of textbook sources in chatbot responses
- Error handling and graceful degradation
- Deployment as a separate service accessible from the GitHub Pages static site
- CORS configuration for cross-origin requests
- Basic analytics (question counts, popular topics, user engagement metrics)

### Out of Scope

- User authentication and account creation (system uses anonymous sessions only)
- Real-time collaboration features (multiple users in the same chat)
- Voice or audio interaction capabilities
- Integration with external learning management systems (LMS)
- Automated grading or assessment of user knowledge
- Content creation or editing features (chatbot cannot modify the textbook)
- Advanced natural language understanding beyond Gemini's capabilities
- Custom machine learning model training for the chatbot
- Multi-language support (English only for MVP)
- Mobile native applications (web-based interface only)
- Payment or subscription features
- Integration with social media platforms
- Email notifications or alerts
- Admin dashboard for content moderation (basic logging only)

## Assumptions

1. **Textbook content is already embedded**: The Qdrant vector database already contains high-quality embeddings of the Physical AI & Humanoid Robotics textbook content, properly chunked and indexed.

2. **Gemini API access is available**: The hackathon setup provides Google Gemini API keys with sufficient quota for development and testing.

3. **Static site is deployed**: The Docusaurus textbook is already deployed to GitHub Pages and accessible at a public URL.

4. **CORS is configurable**: The deployment environment allows configuring CORS policies on the FastAPI backend to accept requests from the GitHub Pages domain.

5. **Neon Free Tier suffices**: The Neon PostgreSQL free tier provides adequate storage and performance for conversation history and user personalization during the hackathon period.

6. **ChatKit is available**: ChatKit or an equivalent open-source React chat component library is available and compatible with the Docusaurus/React environment.

7. **Users have modern browsers**: The target audience uses modern web browsers (Chrome, Firefox, Safari, Edge) with JavaScript enabled.

8. **No heavy traffic expected**: The hackathon deployment will not face production-scale traffic (hundreds of concurrent users), so infrastructure is optimized for demo purposes.

9. **Anonymous usage is acceptable**: Users do not require accounts or authentication to use the chatbot; anonymous sessions are sufficient for the MVP.

10. **English language only**: All user interactions and textbook content are in English, eliminating the need for multi-language support.

## Dependencies

### External Services

- **Qdrant Cloud Free Tier**: Vector database containing textbook embeddings. System requires API access and assumes the database is pre-populated.
- **Google Gemini API**: Language model service (Gemini Pro or Gemini Pro Vision) for generating chatbot responses. System requires valid API keys (GEMINI_API_KEY environment variable).
- **Neon PostgreSQL**: Serverless PostgreSQL database for storing conversation history and user personalization data. System requires connection string and sufficient storage quota.
- **GitHub Pages**: Hosting platform for the Docusaurus textbook. The chatbot widget must be embedded on this deployed site.

### Infrastructure

- **FastAPI Backend Deployment**: Requires a hosting platform for the FastAPI service (e.g., Render, Railway, Vercel, or local hosting for hackathon demo). System must be accessible via HTTPS for CORS compatibility.
- **Environment Variables**: System requires configuration for API keys (GEMINI_API_KEY, Qdrant, Neon) and CORS allowed origins (GitHub Pages URL).

### Libraries & Frameworks

- **ChatKit or React Chat UI**: Frontend chat component library compatible with React and Docusaurus.
- **FastAPI**: Python web framework for the backend API.
- **Qdrant Client**: Python library for interacting with the Qdrant vector database.
- **Google Gemini SDK**: Official Python library for Google Gemini API interactions.
- **Psycopg2 or SQLAlchemy**: PostgreSQL database adapter for Python.
- **CORS Middleware**: FastAPI middleware for handling cross-origin requests.

### Data

- **Textbook Embeddings**: Pre-existing vector embeddings of the Physical AI & Humanoid Robotics textbook stored in Qdrant. System assumes these are properly indexed with metadata (chapter numbers, section titles, module names).

## Technical Constraints

- **Gemini Token Limits**: Gemini models have context window limits (e.g., 32K tokens for Gemini Pro, 1M tokens for Gemini 1.5 Pro). System must manage conversation history to stay within limits.
- **Qdrant Free Tier Limits**: Free tier may have restrictions on storage size, query rate, or concurrent connections. System must operate within these limits.
- **Neon Free Tier Limits**: Free tier has storage limits (~10GB) and compute limits (e.g., 100 hours of active time per month). System must optimize database usage.
- **GitHub Pages Static Hosting**: Chatbot backend cannot run on GitHub Pages (static hosting only). Backend must be deployed separately.
- **CORS Restrictions**: Browser security policies require proper CORS configuration for the chatbot API to be accessible from the GitHub Pages domain.
- **Latency Considerations**: Round-trip time for RAG queries (Qdrant retrieval + Gemini generation) must be minimized to achieve <5 second response times.

## Risks

1. **Gemini API Rate Limits or Costs**: Risk of exceeding Gemini API quota during testing or demo, leading to service disruption. **Mitigation**: Implement caching for common questions and set up usage monitoring/alerts.

2. **Qdrant Retrieval Quality**: Risk that retrieved textbook chunks are not relevant to user questions, leading to poor chatbot responses. **Mitigation**: Test and refine embedding strategy, implement fallback responses for low-confidence retrievals.

3. **Conversation Context Overflow**: Risk that long conversations exceed Gemini token limits, breaking context retention. **Mitigation**: Implement sliding window context and summarization for older messages.

4. **CORS Configuration Issues**: Risk that cross-origin requests from GitHub Pages are blocked by backend CORS policies. **Mitigation**: Test CORS configuration early and ensure proper headers are set.

5. **Backend Deployment Complexity**: Risk that deploying the FastAPI backend to a separate hosting platform introduces delays or technical issues during the hackathon. **Mitigation**: Use a simple deployment platform (Render, Railway) and test deployment pipeline early.

6. **User Privacy Concerns**: Risk that storing conversation history raises privacy concerns, especially if users share sensitive information. **Mitigation**: Clearly communicate anonymous usage, implement conversation deletion feature, and avoid logging PII.

7. **Performance Under Load**: Risk that the system becomes slow or unresponsive if multiple users interact simultaneously. **Mitigation**: Implement basic rate limiting and optimize database queries; accept that the MVP is not production-scale.

8. **Dependency on External Services**: Risk that Qdrant, Gemini, or Neon experience downtime during the hackathon. **Mitigation**: Implement graceful error handling and fallback messages to maintain user experience during outages.

## Notes

- This specification is designed for a hackathon MVP and prioritizes rapid development and demonstration value over production-ready scalability.
- The system architecture assumes independent deployment of the chatbot backend from the static textbook site, allowing for iterative development without redeploying the Docusaurus site.
- User stories are prioritized to enable incremental delivery: P1 (basic Q&A) must work before P2 (conversation history), which must work before P3 (personalization), etc.
- The personalization layer (Neon database) is designed to be lightweight, storing only anonymous usage patterns and conversation history without requiring user accounts.
- The specification intentionally avoids implementation details (e.g., which React hooks to use, database schema specifics) to remain technology-agnostic and focused on user value.
