# Task List: RAG Chatbot for Physical AI Textbook

**Feature**: RAG Chatbot with Gemini Integration
**Branch**: `002-rag-chatbot`
**Total Tasks**: 65 | **MVP**: 18 tasks (P1) | **Parallel**: 42 tasks [P]

---

## Phase 1: Project Setup & Infrastructure (7 tasks)

### T001: Initialize FastAPI Project Structure

- [X] T001 Initialize FastAPI project structure in backend/ directory

**Scope**:
- Create backend/ directory with proper Python project structure
- Create subdirectories: routers/, services/, models/, tests/
- Create __init__.py files in each subdirectory
- Create main.py as application entry point

**Deliverables**:
- backend/main.py (FastAPI app initialization)
- backend/routers/__init__.py
- backend/services/__init__.py
- backend/models/__init__.py
- backend/tests/__init__.py
- backend/requirements.txt (empty, to be populated)

**Acceptance Criteria**:
- [ ] backend/ directory exists with proper structure
- [ ] All subdirectories have __init__.py files
- [ ] main.py contains basic FastAPI app = FastAPI() initialization
- [ ] Project structure follows Python best practices

---

### T002: Create Environment Configuration Files

- [X] T002 [P] Create environment configuration files (.env, .env.example)

**Scope**:
- Create .env.example template with all required environment variables
- Add .env to .gitignore
- Document each environment variable with comments

**Deliverables**:
- backend/.env.example (template with placeholders)
- .gitignore update (ensure .env is excluded)
- backend/config.py (environment variable loader using pydantic-settings)

**Acceptance Criteria**:
- [ ] .env.example contains all required variables: GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL, CORS_ORIGINS
- [ ] .env is in .gitignore
- [ ] config.py loads variables using pydantic BaseSettings
- [ ] No secrets committed to repository

---

### T003: Setup Neon PostgreSQL Connection

- [X] T003 [P] Setup Neon PostgreSQL connection with SQLAlchemy async

**Scope**:
- Install SQLAlchemy with async support (asyncpg driver)
- Create database connection module with async session management
- Configure connection pooling and timeouts

**Deliverables**:
- backend/database.py (SQLAlchemy async engine and session factory)
- requirements.txt updated (sqlalchemy[asyncio], asyncpg, psycopg2-binary)

**Acceptance Criteria**:
- [ ] AsyncEngine configured with Neon DATABASE_URL
- [ ] async_sessionmaker created for dependency injection
- [ ] Connection pool configured (pool_size=10, max_overflow=20)
- [ ] Database connection tested successfully

---

### T004: Configure CORS Middleware

- [X] T004 [P] Configure CORS middleware for GitHub Pages origin

**Scope**:
- Add CORS middleware to FastAPI app
- Configure allowed origins from environment variable
- Set appropriate CORS headers for chat widget

**Deliverables**:
- backend/main.py updated (CORSMiddleware configuration)

**Acceptance Criteria**:
- [ ] CORSMiddleware added to app
- [ ] allow_origins set from CORS_ORIGINS environment variable
- [ ] allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
- [ ] CORS tested with browser fetch from localhost

---

### T005: Implement Health Check Endpoint

- [X] T005 Implement health check endpoint GET /health

**Scope**:
- Create health check router
- Implement endpoint to verify API is running
- Include database connectivity check

**Deliverables**:
- backend/routers/health.py (health check router)
- backend/main.py updated (include health router)

**Acceptance Criteria**:
- [ ] GET /health returns 200 with {"status": "healthy"}
- [ ] Endpoint checks database connection
- [ ] Returns 503 if database unreachable
- [ ] Endpoint accessible via curl/browser

---

### T006: Setup Alembic for Database Migrations

- [X] T006 [P] Setup Alembic for database migrations

**Scope**:
- Initialize Alembic in backend directory
- Configure alembic.ini with Neon DATABASE_URL
- Create initial migration scaffold

**Deliverables**:
- backend/alembic/ (Alembic directory structure)
- backend/alembic.ini (Alembic configuration)
- backend/alembic/env.py (migration environment)

**Acceptance Criteria**:
- [ ] alembic init alembic executed successfully
- [ ] alembic.ini configured with DATABASE_URL from environment
- [ ] alembic/env.py imports Base from models
- [ ] alembic revision --autogenerate works

---

### T007: Install Core Dependencies

- [X] T007 [P] Install core dependencies in requirements.txt

**Scope**:
- Add all required Python packages to requirements.txt
- Pin versions for reproducibility
- Group dependencies by category (web, database, AI services)

**Deliverables**:
- backend/requirements.txt (complete dependency list)

**Acceptance Criteria**:
- [ ] FastAPI, uvicorn[standard] included
- [ ] SQLAlchemy[asyncio], asyncpg, alembic included
- [ ] qdrant-client, google-generativeai included
- [ ] pydantic-settings, python-dotenv included
- [ ] All dependencies install successfully with pip install -r requirements.txt

---

## Phase 2: User Story 1 (P1) - Basic Question Answering (18 tasks - MVP)

### T008: Create UserSession Model

- [X] T008 [P] [US1] Create UserSession database model in backend/models/user_session.py

**Scope**:
- Define SQLAlchemy model for anonymous user sessions
- Include fields: id (UUID), created_at, last_active_at
- Add relationship to Conversation model

**Deliverables**:
- backend/models/user_session.py (UserSession model)

**Acceptance Criteria**:
- [ ] Model inherits from Base
- [ ] id field is UUID primary key with default uuid.uuid4
- [ ] created_at and last_active_at are DateTime with defaults
- [ ] __tablename__ = "user_sessions"
- [ ] Model validates successfully

---

### T009: Create Conversation Model

- [X] T009 [P] [US1] Create Conversation database model in backend/models/conversation.py

**Scope**:
- Define SQLAlchemy model for conversations
- Include fields: id (UUID), session_id (FK), title, created_at
- Add relationships to UserSession and Message

**Deliverables**:
- backend/models/conversation.py (Conversation model)

**Acceptance Criteria**:
- [ ] Model inherits from Base
- [ ] id field is UUID primary key
- [ ] session_id is ForeignKey to user_sessions.id
- [ ] title is String(255), nullable
- [ ] created_at is DateTime with default
- [ ] Relationships defined for session and messages

---

### T010: Create Message Model

- [X] T010 [P] [US1] Create Message database model in backend/models/message.py

**Scope**:
- Define SQLAlchemy model for chat messages
- Include fields: id, conversation_id (FK), role (user/assistant), content, citations, created_at
- Support both user and assistant messages

**Deliverables**:
- backend/models/message.py (Message model)

**Acceptance Criteria**:
- [ ] Model inherits from Base
- [ ] id is UUID primary key
- [ ] conversation_id is ForeignKey to conversations.id
- [ ] role is String with check constraint (user/assistant)
- [ ] content is Text
- [ ] citations is JSONB (nullable)
- [ ] created_at is DateTime with default

---

### T011: Generate Initial Database Migration

- [X] T011 [US1] Generate initial database migration for UserSession, Conversation, Message

**Scope**:
- Create Alembic migration for US1 models
- Review autogenerated migration
- Apply migration to Neon database

**Deliverables**:
- backend/alembic/versions/001_initial_schema.py (migration file)

**Acceptance Criteria**:
- [ ] alembic revision --autogenerate -m "Initial schema" executes
- [ ] Migration creates user_sessions, conversations, messages tables
- [ ] All constraints, indexes, foreign keys correct
- [ ] alembic upgrade head succeeds on Neon database
- [ ] Tables visible in Neon dashboard

---

### T012: Implement Qdrant Client Service

- [X] T012 [P] [US1] Implement Qdrant client in backend/services/qdrant_service.py

**Scope**:
- Create QdrantService class for semantic search
- Implement search method to query textbook embeddings
- Configure connection to Qdrant Cloud
- Return top-k relevant chunks with metadata

**Deliverables**:
- backend/services/qdrant_service.py (QdrantService class)

**Acceptance Criteria**:
- [ ] QdrantClient initialized with QDRANT_URL and QDRANT_API_KEY
- [ ] search(query: str, top_k: int = 5) method implemented
- [ ] Returns list of chunks with metadata (chapter, section, page)
- [ ] Connection tested with sample query
- [ ] Error handling for Qdrant API failures

---

### T013: Implement Gemini API Integration

- [X] T013 [P] [US1] Implement Gemini API service in backend/services/gemini_service.py

**Scope**:
- Create GeminiService class for response generation
- Configure Gemini 1.5 Pro model with API key
- Implement generate_response method with prompt templating
- Handle conversation context in prompts

**Deliverables**:
- backend/services/gemini_service.py (GeminiService class)

**Acceptance Criteria**:
- [ ] google.generativeai configured with GEMINI_API_KEY
- [ ] Model = genai.GenerativeModel('gemini-1.5-pro')
- [ ] generate_response(prompt: str, context: list) method implemented
- [ ] Safety settings configured (block none/low harmful content)
- [ ] Temperature set to 0.7 for balanced responses
- [ ] Error handling for API rate limits and failures

---

### T014: Implement RAG Orchestration Service

- [X] T014 [US1] Implement RAG orchestration in backend/services/rag_service.py

**Scope**:
- Create RAGService class to orchestrate retrieval + generation
- Implement process_question method: retrieve chunks → generate response → extract citations
- Format citations as [Chapter X, Section Y]
- Combine Qdrant and Gemini services

**Deliverables**:
- backend/services/rag_service.py (RAGService class)

**Acceptance Criteria**:
- [ ] process_question(question: str, session_id: UUID) method implemented
- [ ] Calls QdrantService.search(question, top_k=5)
- [ ] Builds prompt with retrieved chunks
- [ ] Calls GeminiService.generate_response(prompt, context=[])
- [ ] Extracts citations from metadata
- [ ] Returns {"response": str, "citations": list[dict]}
- [ ] End-to-end flow tested with sample question

---

### T015: Create POST /api/chat Endpoint

- [X] T015 [US1] Create POST /api/chat endpoint in backend/routers/chat.py

**Scope**:
- Create chat router with POST /api/chat endpoint
- Accept request body: {session_id, question}
- Call RAGService to process question
- Save user message and assistant response to database
- Return response with citations

**Deliverables**:
- backend/routers/chat.py (chat router)
- backend/main.py updated (include chat router)

**Acceptance Criteria**:
- [ ] POST /api/chat accepts {session_id: UUID, question: str}
- [ ] Creates UserSession if session_id is new
- [ ] Calls RAGService.process_question(question, session_id)
- [ ] Saves user message and assistant response to database
- [ ] Returns 200 with {response: str, citations: list, message_id: UUID}
- [ ] Returns 400 for invalid input
- [ ] Returns 500 for internal errors with user-friendly message
- [ ] Response time <5 seconds for typical questions

---

### T016: Setup React Chat UI Library

- [X] T016 [P] [US1] Setup ChatKit or @chatscope/chat-ui-kit-react in frontend

**Scope**:
- Install chat UI library (ChatKit or chatscope)
- Create ChatWidget component skeleton
- Configure basic styling

**Deliverables**:
- frontend/src/components/ChatWidget.jsx (React component)
- frontend/package.json updated (chat UI library dependency)

**Acceptance Criteria**:
- [ ] npm install @chatscope/chat-ui-kit-react or alternative
- [ ] ChatWidget component created with basic structure
- [ ] Renders in development environment
- [ ] Basic chat UI displays (message list, input box)

---

### T017: Implement Frontend API Client

- [X] T017 [P] [US1] Implement API client in frontend/src/services/chatApi.js

**Scope**:
- Create chatApi module for backend communication
- Implement sendMessage function with fetch
- Handle CORS and authentication headers
- Implement error handling and retries

**Deliverables**:
- frontend/src/services/chatApi.js (API client module)

**Acceptance Criteria**:
- [ ] sendMessage(sessionId, question) function implemented
- [ ] Uses fetch with POST to REACT_APP_CHAT_API_URL/api/chat
- [ ] Includes headers: Content-Type: application/json
- [ ] Handles network errors with user-friendly messages
- [ ] Returns parsed JSON response
- [ ] Retry logic for transient failures (max 2 retries)

---

### T018: Implement Session Management

- [X] T018 [P] [US1] Implement session management in frontend/src/services/sessionManager.js

**Scope**:
- Create session manager to handle anonymous session IDs
- Generate UUID on first visit, store in localStorage
- Provide getSessionId() function for components

**Deliverables**:
- frontend/src/services/sessionManager.js (session manager module)

**Acceptance Criteria**:
- [ ] Generates UUID v4 on first visit
- [ ] Stores session ID in localStorage
- [ ] getSessionId() retrieves existing or creates new session ID
- [ ] clearSession() removes session ID (for "New Conversation")
- [ ] Session persists across page reloads

---

### T019: Integrate Chat Widget with Docusaurus

- [X] T019 [US1] Integrate ChatWidget into Docusaurus layout

**Scope**:
- Add ChatWidget to Docusaurus theme components
- Position as floating button (bottom-right corner)
- Implement toggle show/hide functionality
- Ensure widget appears on all textbook pages

**Deliverables**:
- frontend/src/theme/Root.js (Docusaurus swizzled component)
- frontend/src/components/ChatWidget.jsx updated

**Acceptance Criteria**:
- [ ] ChatWidget component added to Root.js
- [ ] Floating button positioned fixed bottom-right (24px from edges)
- [ ] Click toggles chat window expand/collapse
- [ ] Widget appears on all documentation pages
- [ ] Does not interfere with page content or navigation
- [ ] Z-index ensures widget stays on top

---

### T020: Display Citations in Chat UI

- [X] T020 [P] [US1] Display citations as clickable links in chat messages

**Scope**:
- Parse citations from API response
- Render citations below assistant messages
- Format as [Chapter X, Section Y] with links to textbook sections
- Handle multiple citations per message

**Deliverables**:
- frontend/src/components/Citation.jsx (citation display component)
- frontend/src/components/ChatWidget.jsx updated

**Acceptance Criteria**:
- [ ] Citations displayed below assistant messages
- [ ] Each citation is a clickable link
- [ ] Links navigate to correct textbook section (anchor links)
- [ ] Citations styled distinctly (smaller font, gray color)
- [ ] Multiple citations displayed in comma-separated list
- [ ] Handles messages with no citations gracefully

---

### T021: Implement Loading States

- [X] T021 [P] [US1] Implement loading states ("typing..." indicator) in chat UI

**Scope**:
- Add loading indicator while waiting for API response
- Display "Claude is typing..." message
- Disable input box during loading
- Handle loading errors with retry option

**Deliverables**:
- frontend/src/components/ChatWidget.jsx updated (loading state)

**Acceptance Criteria**:
- [ ] Loading indicator appears after user sends message
- [ ] "Typing..." animation displays
- [ ] Input box disabled during loading
- [ ] Loading indicator removed when response received
- [ ] Error message displayed if request fails
- [ ] Retry button appears on error

---

### T022: Implement Off-Topic Detection

- [X] T022 [P] [US1] Implement off-topic detection in RAG service

**Scope**:
- Add relevance scoring to Qdrant retrieval results
- Implement threshold check (minimum relevance score)
- Return polite decline message for off-topic questions
- Log off-topic attempts for analysis

**Deliverables**:
- backend/services/rag_service.py updated (off-topic detection)

**Acceptance Criteria**:
- [ ] Qdrant search returns relevance scores
- [ ] Threshold set at 0.5 (configurable)
- [ ] Questions below threshold return predefined message
- [ ] Message: "I can only answer questions about the Physical AI textbook content."
- [ ] Off-topic questions logged to database or file
- [ ] 95% off-topic detection accuracy on test set

---

### T023: End-to-End Integration Test for US1

- [X] T023 [US1] Create end-to-end integration test for basic Q&A flow

**Scope**:
- Write integration test covering full RAG pipeline
- Test: user sends question → backend processes → response returned
- Verify database records created
- Test citations included in response

**Deliverables**:
- backend/tests/test_integration_chat.py (integration test)

**Acceptance Criteria**:
- [ ] Test sends POST /api/chat with sample question
- [ ] Verifies 200 response with response and citations
- [ ] Checks UserSession, Conversation, Message created in database
- [ ] Verifies citations format correct
- [ ] Test passes with real Qdrant and Gemini (or mocked)
- [ ] Test runs in CI pipeline

---

### T024: Unit Tests for US1 Services

- [X] T024 [P] [US1] Write unit tests for QdrantService, GeminiService, RAGService

**Scope**:
- Create unit tests for each service class
- Mock external API calls (Qdrant, Gemini)
- Test error handling and edge cases
- Aim for 80% code coverage

**Deliverables**:
- backend/tests/test_qdrant_service.py
- backend/tests/test_gemini_service.py
- backend/tests/test_rag_service.py

**Acceptance Criteria**:
- [ ] QdrantService.search tested with mock responses
- [ ] GeminiService.generate_response tested with mock API
- [ ] RAGService.process_question tested end-to-end with mocks
- [ ] Error cases tested (API failures, invalid input)
- [ ] All tests pass
- [ ] Code coverage ≥80% for services/

---

## Phase 3: User Story 2 (P2) - Conversation History & Context (10 tasks)

### T025: Implement Conversation Retrieval Endpoint

- [X] T025 [P] [US2] Create GET /api/conversation/history endpoint

**Scope**:
- Create endpoint to retrieve conversation history for a session
- Return list of messages with timestamps
- Support pagination (optional)

**Deliverables**:
- backend/routers/conversation.py (conversation router)
- backend/main.py updated (include conversation router)

**Acceptance Criteria**:
- [ ] GET /api/conversation/history?session_id={uuid} implemented
- [ ] Returns list of messages ordered by created_at
- [ ] Each message includes: id, role, content, citations, created_at
- [ ] Returns 200 with empty list for new sessions
- [ ] Returns 400 for invalid session_id

---

### T026: Update RAG Service for Context Window

- [X] T026 [US2] Update RAGService to include conversation context in prompts

**Scope**:
- Modify process_question to retrieve last 20 messages
- Include conversation history in Gemini prompt
- Implement sliding window (limit to 10K tokens)
- Format context for Gemini API

**Deliverables**:
- backend/services/rag_service.py updated (context retrieval)

**Acceptance Criteria**:
- [ ] Retrieves last 20 messages from database for session
- [ ] Formats as conversation history in prompt
- [ ] Includes role (user/assistant) and content
- [ ] Estimates token count, truncates if >10K tokens
- [ ] Gemini responses reference previous questions
- [ ] Context improves answer relevance

---

### T027: Implement New Conversation Feature

- [X] T027 [P] [US2] Create POST /api/conversation/new endpoint

**Scope**:
- Create endpoint to start a new conversation
- Generate new conversation ID
- Reset context for session
- Return new conversation ID

**Deliverables**:
- backend/routers/conversation.py updated (new conversation endpoint)

**Acceptance Criteria**:
- [ ] POST /api/conversation/new accepts {session_id: UUID}
- [ ] Creates new Conversation record in database
- [ ] Returns 200 with {conversation_id: UUID}
- [ ] Frontend can call to reset chat
- [ ] Previous conversations preserved

---

### T028: Update Frontend for History Display

- [X] T028 [P] [US2] Update ChatWidget to load and display conversation history

**Scope**:
- Call GET /api/conversation/history on widget load
- Display historical messages in chat UI
- Maintain scroll position
- Show timestamps for older messages

**Deliverables**:
- frontend/src/components/ChatWidget.jsx updated (history loading)

**Acceptance Criteria**:
- [ ] Calls API to fetch history when widget opens
- [ ] Displays all historical messages in order
- [ ] Distinguishes user vs assistant messages
- [ ] Scrolls to bottom (most recent message)
- [ ] Handles empty history gracefully

---

### T029: Implement Conversation Titles

- [X] T029 [P] [US2] Auto-generate conversation titles from first user question

**Scope**:
- Extract first 50 characters of first question as title
- Update Conversation.title in database
- Display title in conversation list (future enhancement)

**Deliverables**:
- backend/services/conversation_service.py (new service)

**Acceptance Criteria**:
- [ ] First message in conversation sets title
- [ ] Title = first 50 chars + "..." if longer
- [ ] Stored in conversations.title column
- [ ] Endpoint returns title with conversation data

---

### T030: Frontend "New Conversation" Button

- [X] T030 [P] [US2] Add "New Conversation" button to chat widget

**Scope**:
- Add button to chat widget header
- Call POST /api/conversation/new on click
- Clear chat UI and start fresh conversation
- Preserve session ID

**Deliverables**:
- frontend/src/components/ChatWidget.jsx updated (new conversation button)

**Acceptance Criteria**:
- [ ] Button labeled "New Conversation" in widget header
- [ ] Calls API to create new conversation
- [ ] Clears message list in UI
- [ ] Session ID remains same
- [ ] User can start asking questions immediately

---

### T031: Integration Test for Conversation History

- [X] T031 [US2] Create integration test for conversation history flow

**Scope**:
- Test multi-turn conversation with context
- Verify history retrieval
- Test new conversation creation
- Verify context improves responses

**Deliverables**:
- backend/tests/test_integration_conversation.py

**Acceptance Criteria**:
- [ ] Test sends 3 messages in sequence
- [ ] Retrieves history via GET endpoint
- [ ] Verifies all messages returned
- [ ] Creates new conversation
- [ ] Verifies new conversation ID different
- [ ] All tests pass

---

## Phase 4: User Story 3 (P3) - Personalized Learning Assistance (8 tasks)

### T032: Create UserProfile Model

- [ ] T032 [P] [US3] Create UserProfile database model

**Scope**:
- Define SQLAlchemy model for user profiles
- Track interests, knowledge level, visited chapters
- Link to UserSession

**Deliverables**:
- backend/models/user_profile.py (UserProfile model)
- backend/alembic/versions/002_user_profiles.py (migration)

**Acceptance Criteria**:
- [ ] Model includes: session_id (FK), interests (JSONB), knowledge_level (String), visited_chapters (JSONB)
- [ ] Migration creates user_profiles table
- [ ] Relationship to UserSession defined
- [ ] alembic upgrade head succeeds

---

### T033: Implement Interest Detection

- [ ] T033 [P] [US3] Implement interest detection in backend/services/personalization_service.py

**Scope**:
- Analyze last 10 user questions
- Extract topics/keywords using keyword extraction
- Update UserProfile.interests
- Use for personalized recommendations

**Deliverables**:
- backend/services/personalization_service.py (PersonalizationService class)

**Acceptance Criteria**:
- [ ] analyze_interests(session_id: UUID) method implemented
- [ ] Retrieves last 10 messages for session
- [ ] Extracts keywords using TF-IDF or Gemini summarization
- [ ] Updates user_profiles.interests as JSON array
- [ ] Returns list of detected topics

---

### T034: Implement Personalized Greetings

- [ ] T034 [P] [US3] Implement personalized greetings for returning users

**Scope**:
- Check if user has previous conversations
- Generate greeting mentioning recent topics
- Display in chat widget on load

**Deliverables**:
- backend/services/personalization_service.py updated
- GET /api/personalization/greeting endpoint

**Acceptance Criteria**:
- [ ] get_greeting(session_id: UUID) method implemented
- [ ] Returns generic greeting for new users
- [ ] Returns personalized greeting for returning users
- [ ] Example: "Welcome back! I see you've been exploring Vision-Language-Action models."
- [ ] Frontend displays greeting on widget open

---

### T035: Implement Knowledge Level Tracking

- [ ] T035 [P] [US3] Track user knowledge level (beginner/intermediate/advanced)

**Scope**:
- Infer knowledge level from question complexity
- Store in UserProfile.knowledge_level
- Use to adjust response complexity

**Deliverables**:
- backend/services/personalization_service.py updated

**Acceptance Criteria**:
- [ ] infer_knowledge_level(session_id: UUID) method implemented
- [ ] Analyzes question patterns (length, terminology)
- [ ] Sets knowledge_level to beginner/intermediate/advanced
- [ ] Stored in user_profiles table
- [ ] Used in RAG prompt engineering

---

### T036: Implement Adaptive Response Complexity

- [ ] T036 [US3] Adjust Gemini response complexity based on user knowledge level

**Scope**:
- Modify RAGService to include knowledge level in prompt
- Prompt engineering for different levels
- Test with sample questions at each level

**Deliverables**:
- backend/services/rag_service.py updated (adaptive prompts)

**Acceptance Criteria**:
- [ ] Retrieves knowledge_level from UserProfile
- [ ] Adds instruction to Gemini prompt based on level
- [ ] Beginner: "Explain in simple terms with examples"
- [ ] Advanced: "Provide detailed technical explanation"
- [ ] Responses appropriate for knowledge level
- [ ] Tested with sample questions

---

### T037: Implement Chapter Recommendations

- [ ] T037 [P] [US3] Implement chapter recommendations based on interests

**Scope**:
- Analyze user interests and visited chapters
- Recommend next chapters to explore
- Create GET /api/personalization/recommendations endpoint

**Deliverables**:
- backend/services/personalization_service.py updated
- backend/routers/personalization.py (new router)

**Acceptance Criteria**:
- [ ] get_recommendations(session_id: UUID) method implemented
- [ ] Returns list of recommended chapters with reasons
- [ ] Based on interests and reading history
- [ ] Returns 3-5 recommendations
- [ ] Endpoint returns 200 with recommendations array

---

### T038: Integration Test for Personalization

- [ ] T038 [US3] Create integration test for personalization features

**Scope**:
- Test interest detection with sample conversations
- Test personalized greetings
- Test adaptive responses
- Verify UserProfile updates

**Deliverables**:
- backend/tests/test_integration_personalization.py

**Acceptance Criteria**:
- [ ] Test sends questions on specific topics
- [ ] Verifies interests detected and stored
- [ ] Retrieves personalized greeting
- [ ] Verifies knowledge level inferred correctly
- [ ] All tests pass

---

## Phase 5: User Story 4 (P4) - Multi-Modal Content Integration (6 tasks)

### T039: Enhance Qdrant Metadata for Content Types

- [ ] T039 [P] [US4] Verify and enhance Qdrant metadata to include content_type

**Scope**:
- Check existing Qdrant schema for content_type field
- If missing, add metadata to distinguish text/code/diagram
- Update embedding pipeline to include content_type

**Deliverables**:
- Documentation of Qdrant schema (specs/002-rag-chatbot/qdrant-schema.md)
- Script to update metadata if needed

**Acceptance Criteria**:
- [ ] Qdrant chunks have content_type metadata (text/code/diagram)
- [ ] Metadata accessible in search results
- [ ] Can filter searches by content type
- [ ] Documentation updated

---

### T040: Implement Content Type Detection

- [ ] T040 [P] [US4] Implement content type detection in RAG service

**Scope**:
- Parse content_type from Qdrant metadata
- Categorize retrieved chunks as text/code/diagram
- Pass content type information to response generation

**Deliverables**:
- backend/services/rag_service.py updated (content type handling)

**Acceptance Criteria**:
- [ ] Extracts content_type from each retrieved chunk
- [ ] Groups chunks by type
- [ ] Passes type information to Gemini prompt
- [ ] Returns content_type in citations

---

### T041: Update Gemini Prompts for Visual Content

- [ ] T041 [US4] Update Gemini prompts to reference diagrams and code

**Scope**:
- Modify prompt engineering to handle visual content
- Instruct Gemini to reference diagrams explicitly
- Format code examples with syntax highlighting hints

**Deliverables**:
- backend/services/gemini_service.py updated (prompt templates)

**Acceptance Criteria**:
- [ ] Prompts distinguish between text, code, and diagrams
- [ ] For diagrams: "Refer to Figure X in Chapter Y"
- [ ] For code: "See code example in Chapter Y, Section Z"
- [ ] Responses appropriately reference visual content

---

### T042: Enhanced Citation Display for Multi-Modal

- [ ] T042 [P] [US4] Enhance citation display to show content type icons

**Scope**:
- Update Citation component to show icons for content types
- Use different icons for text/code/diagram
- Link to correct page section or figure

**Deliverables**:
- frontend/src/components/Citation.jsx updated (content type icons)

**Acceptance Criteria**:
- [ ] Citations show icon based on content_type
- [ ] Icons: 📄 (text), 💻 (code), 📊 (diagram)
- [ ] Links navigate to correct section or figure
- [ ] Tooltip shows content type on hover

---

### T043: Integration Test for Multi-Modal Content

- [ ] T043 [US4] Create integration test for multi-modal content retrieval

**Scope**:
- Test questions that should return diagrams or code
- Verify content_type in citations
- Verify Gemini references visual content correctly

**Deliverables**:
- backend/tests/test_integration_multimodal.py

**Acceptance Criteria**:
- [ ] Test asks question requiring diagram reference
- [ ] Verifies response mentions diagram/figure
- [ ] Citations include content_type
- [ ] Test asks question requiring code example
- [ ] Verifies code cited correctly
- [ ] All tests pass

---

## Phase 6: User Story 5 (P5) - Error Handling & Feedback (8 tasks)

### T044: Create Feedback Model

- [ ] T044 [P] [US5] Create Feedback database model

**Scope**:
- Define SQLAlchemy model for user feedback
- Include fields: message_id (FK), rating (thumbs up/down), comment, created_at
- Link to Message model

**Deliverables**:
- backend/models/feedback.py (Feedback model)
- backend/alembic/versions/003_feedback_ratelimits.py (migration)

**Acceptance Criteria**:
- [ ] Model includes: id, message_id (FK), rating (Integer: 1=up, -1=down), comment (Text), created_at
- [ ] Migration creates feedback table
- [ ] Relationship to Message defined
- [ ] alembic upgrade head succeeds

---

### T045: Implement Feedback Endpoint

- [ ] T045 [P] [US5] Create POST /api/feedback endpoint

**Scope**:
- Create endpoint to submit feedback for a message
- Accept rating and optional comment
- Store in database

**Deliverables**:
- backend/routers/feedback.py (feedback router)
- backend/main.py updated (include feedback router)

**Acceptance Criteria**:
- [ ] POST /api/feedback accepts {message_id: UUID, rating: int, comment: str}
- [ ] Validates rating is 1 or -1
- [ ] Creates Feedback record in database
- [ ] Returns 200 with {feedback_id: UUID}
- [ ] Returns 400 for invalid input

---

### T046: Add Feedback Buttons to Chat UI

- [ ] T046 [P] [US5] Add thumbs up/down buttons to assistant messages

**Scope**:
- Add feedback buttons below each assistant message
- Call POST /api/feedback on click
- Disable buttons after feedback submitted
- Show confirmation message

**Deliverables**:
- frontend/src/components/FeedbackButtons.jsx (new component)
- frontend/src/components/ChatWidget.jsx updated

**Acceptance Criteria**:
- [ ] Thumbs up/down buttons displayed below assistant messages
- [ ] Calls API on button click
- [ ] Buttons disabled after submission
- [ ] Shows "Thank you for your feedback!" message
- [ ] Handles API errors gracefully

---

### T047: Create RateLimit Model

- [ ] T047 [P] [US5] Create RateLimit database model

**Scope**:
- Define SQLAlchemy model for rate limiting
- Track request counts per session per hour
- Include fields: session_id, request_count, window_start

**Deliverables**:
- backend/models/rate_limit.py (RateLimit model)
- Migration already created in T044

**Acceptance Criteria**:
- [ ] Model includes: session_id (FK), request_count (Integer), window_start (DateTime)
- [ ] Unique constraint on session_id + window_start
- [ ] Model validates successfully

---

### T048: Implement Rate Limiting Middleware

- [ ] T048 [US5] Implement rate limiting in backend/middleware/rate_limiter.py

**Scope**:
- Create middleware to enforce 20 questions/hour per session
- Check request count before processing
- Return 429 status if limit exceeded
- Include retry-after header

**Deliverables**:
- backend/middleware/rate_limiter.py (rate limiting middleware)
- backend/main.py updated (include middleware)

**Acceptance Criteria**:
- [ ] Middleware checks rate_limits table for session
- [ ] Increments request_count for current hour window
- [ ] Returns 429 if count > 20
- [ ] Response includes Retry-After header with seconds
- [ ] Resets counter after 1 hour
- [ ] Applied to /api/chat endpoint

---

### T049: Implement Graceful Degradation for Qdrant

- [ ] T049 [P] [US5] Implement fallback when Qdrant unavailable

**Scope**:
- Wrap Qdrant calls in try-except
- Return error message if Qdrant fails
- Log error for monitoring
- Return user-friendly message within 3 seconds

**Deliverables**:
- backend/services/qdrant_service.py updated (error handling)

**Acceptance Criteria**:
- [ ] Catches QdrantException and RequestException
- [ ] Returns empty results on failure
- [ ] RAGService detects empty results
- [ ] Returns message: "Search service temporarily unavailable. Please try again."
- [ ] Error logged with details
- [ ] Response time <3 seconds

---

### T050: Implement Graceful Degradation for Gemini

- [ ] T050 [P] [US5] Implement fallback when Gemini API unavailable

**Scope**:
- Wrap Gemini calls in try-except
- Handle rate limit errors (429)
- Implement exponential backoff retry
- Return fallback message if all retries fail

**Deliverables**:
- backend/services/gemini_service.py updated (error handling)

**Acceptance Criteria**:
- [ ] Catches API exceptions (429, 500, network errors)
- [ ] Implements retry with exponential backoff (max 2 retries)
- [ ] Returns fallback message on failure
- [ ] Message: "Response generation temporarily unavailable. Please try again in a moment."
- [ ] Error logged with details
- [ ] Total response time <10 seconds

---

### T051: Implement Error Logging

- [ ] T051 [P] [US5] Setup error logging with Python logging module

**Scope**:
- Configure logging for all services
- Log errors to file and console
- Include timestamp, service name, error details
- Rotate logs daily

**Deliverables**:
- backend/logging_config.py (logging configuration)
- backend/main.py updated (initialize logging)

**Acceptance Criteria**:
- [ ] Logging configured with rotating file handler
- [ ] Log level: INFO for production, DEBUG for development
- [ ] All errors logged with traceback
- [ ] Logs include session_id for debugging
- [ ] Log files rotated daily, kept for 7 days

---

### T052: Integration Test for Error Handling

- [ ] T052 [US5] Create integration test for error handling and feedback

**Scope**:
- Test rate limiting (send 21 requests)
- Test feedback submission
- Mock Qdrant/Gemini failures and verify graceful degradation

**Deliverables**:
- backend/tests/test_integration_errors.py

**Acceptance Criteria**:
- [ ] Test sends 21 requests, verifies 21st returns 429
- [ ] Test submits feedback, verifies stored in database
- [ ] Test mocks Qdrant failure, verifies error message
- [ ] Test mocks Gemini failure, verifies fallback message
- [ ] All tests pass

---

## Phase 7: Testing & Deployment (10 tasks)

### T053: Create Backend Deployment Configuration

- [ ] T053 [P] Create deployment configuration for Render/Railway

**Scope**:
- Create render.yaml or railway.json deployment config
- Configure environment variables
- Set build and start commands
- Configure health check endpoint

**Deliverables**:
- render.yaml or railway.json (deployment config)
- .env.production (environment variable template)

**Acceptance Criteria**:
- [ ] Config specifies Python 3.10+ runtime
- [ ] Build command: pip install -r requirements.txt
- [ ] Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
- [ ] Health check: GET /health
- [ ] Environment variables placeholder for all required keys

---

### T054: Deploy Backend to Render/Railway

- [ ] T054 Deploy FastAPI backend to Render or Railway

**Scope**:
- Connect GitHub repository to Render/Railway
- Configure environment variables in dashboard
- Deploy backend application
- Verify health check passes

**Deliverables**:
- Deployed backend with HTTPS URL

**Acceptance Criteria**:
- [ ] Backend deployed successfully
- [ ] HTTPS URL accessible (e.g., https://chatbot-api.onrender.com)
- [ ] GET /health returns 200
- [ ] Database migrations applied (alembic upgrade head)
- [ ] Environment variables set correctly
- [ ] CORS configured for GitHub Pages origin

---

### T055: Update Frontend Environment Variables

- [ ] T055 [P] Update frontend REACT_APP_CHAT_API_URL to production backend

**Scope**:
- Update .env.production with deployed backend URL
- Rebuild frontend for production
- Test API connection from frontend

**Deliverables**:
- frontend/.env.production updated
- Frontend production build

**Acceptance Criteria**:
- [ ] REACT_APP_CHAT_API_URL set to production backend URL
- [ ] npm run build succeeds
- [ ] Build output in build/ directory
- [ ] API calls from frontend reach backend

---

### T056: Deploy Frontend to GitHub Pages

- [ ] T056 Deploy Docusaurus frontend to GitHub Pages

**Scope**:
- Configure Docusaurus for GitHub Pages deployment
- Run npm run deploy
- Verify chat widget appears on live site

**Deliverables**:
- Frontend deployed to GitHub Pages

**Acceptance Criteria**:
- [ ] docusaurus.config.js configured with correct organizationName and projectName
- [ ] npm run deploy succeeds
- [ ] Site accessible at GitHub Pages URL
- [ ] Chat widget appears on all pages
- [ ] Widget connects to backend successfully

---

### T057: End-to-End Smoke Test

- [ ] T057 Perform end-to-end smoke test on production

**Scope**:
- Test all 5 user stories on production deployment
- Verify core functionality works
- Test on multiple browsers (Chrome, Firefox, Safari)

**Deliverables**:
- Test results document (specs/002-rag-chatbot/smoke-test-results.md)

**Acceptance Criteria**:
- [ ] US1: Ask question, receive response with citations
- [ ] US2: Load conversation history, create new conversation
- [ ] US3: Verify personalized greeting for returning user
- [ ] US4: Ask question requiring diagram, verify citation
- [ ] US5: Submit feedback, verify rate limiting
- [ ] All tests pass on Chrome, Firefox, Safari

---

### T058: Performance Testing

- [ ] T058 Perform performance testing with 100 concurrent users

**Scope**:
- Use load testing tool (Locust or k6)
- Simulate 100 concurrent users asking questions
- Measure response times (p50, p95, p99)
- Verify response time <5 seconds (SC-001)

**Deliverables**:
- Load testing script
- Performance test results (specs/002-rag-chatbot/performance-test-results.md)

**Acceptance Criteria**:
- [ ] Load test script created with 100 virtual users
- [ ] Test runs for 10 minutes
- [ ] p95 response time <5 seconds
- [ ] No errors or timeouts
- [ ] Backend scales appropriately

---

### T059: Validate Success Criteria

- [ ] T059 Validate all 12 success criteria (SC-001 to SC-012)

**Scope**:
- Test each success criterion from spec.md
- Document results with evidence
- Fix any failures

**Deliverables**:
- Validation report (specs/002-rag-chatbot/success-criteria-validation.md)

**Acceptance Criteria**:
- [ ] SC-001: RAG pipeline completes within 5 seconds (p95) ✅
- [ ] SC-002: Retrieves 5 relevant chunks from Qdrant ✅
- [ ] SC-003: 70%+ thumbs-up rating on test questions ✅
- [ ] SC-004: Responses include citations in [Chapter X, Section Y] format ✅
- [ ] SC-005: 95%+ off-topic detection accuracy ✅
- [ ] SC-006: Conversation history loads within 2 seconds ✅
- [ ] SC-007: Context window supports 20 messages ✅
- [ ] SC-008: Personalized greeting for returning users ✅
- [ ] SC-009: Interest detection accuracy >80% ✅
- [ ] SC-010: Multi-modal citations display correctly ✅
- [ ] SC-011: User-friendly error messages within 3 seconds ✅
- [ ] SC-012: Rate limiting enforced (20 questions/hour) ✅

---

### T060: User Acceptance Testing

- [ ] T060 Conduct user acceptance testing with 5 test users

**Scope**:
- Recruit 5 test users from target audience
- Have users test all P1-P3 features
- Collect feedback via survey
- Verify 70%+ satisfaction rate

**Deliverables**:
- UAT plan (specs/002-rag-chatbot/uat-plan.md)
- UAT results (specs/002-rag-chatbot/uat-results.md)

**Acceptance Criteria**:
- [ ] 5 users complete UAT sessions
- [ ] Users test all acceptance scenarios from spec.md
- [ ] Collect ratings for helpfulness, accuracy, ease of use
- [ ] 70%+ thumbs-up rating
- [ ] Document feedback and issues
- [ ] Prioritize bug fixes

---

### T061: Bug Fixes from UAT

- [ ] T061 Fix critical bugs discovered during UAT

**Scope**:
- Review UAT feedback
- Prioritize and fix critical bugs
- Retest affected functionality
- Document fixes

**Deliverables**:
- Bug fix commits
- Updated test results

**Acceptance Criteria**:
- [ ] All P0/P1 bugs fixed
- [ ] Fixes deployed to production
- [ ] Retested by original reporters
- [ ] No regressions introduced

---

### T062: Final Production Validation

- [ ] T062 Final validation of production deployment

**Scope**:
- Verify all features working on production
- Check monitoring and logging
- Verify environment variables secure
- Document deployment

**Deliverables**:
- Deployment documentation (specs/002-rag-chatbot/deployment.md)

**Acceptance Criteria**:
- [ ] All features functional on production
- [ ] No secrets in code or logs
- [ ] Error logging working
- [ ] Health check endpoint accessible
- [ ] CORS configured correctly
- [ ] Deployment documented

---

## Phase 8: Documentation & Polish (3 tasks)

### T063: Create User Documentation

- [ ] T063 [P] Create user documentation for chat widget

**Scope**:
- Write user guide for chat widget
- Include screenshots and examples
- Document features and limitations
- Add to textbook site

**Deliverables**:
- docs/chatbot-user-guide.md (user documentation)
- docs/assets/chatbot-screenshots/ (screenshots)

**Acceptance Criteria**:
- [ ] User guide explains how to use chat widget
- [ ] Includes screenshots of key features
- [ ] Documents limitations (textbook content only)
- [ ] Explains feedback mechanism
- [ ] Published on textbook site

---

### T064: Create Developer Documentation

- [ ] T064 [P] Create developer documentation for maintenance

**Scope**:
- Document architecture and components
- Document API endpoints with examples
- Create deployment runbook
- Document troubleshooting procedures

**Deliverables**:
- specs/002-rag-chatbot/developer-guide.md (developer documentation)

**Acceptance Criteria**:
- [ ] Architecture diagram included
- [ ] All API endpoints documented with request/response examples
- [ ] Environment variables documented
- [ ] Deployment steps documented
- [ ] Troubleshooting guide for common issues
- [ ] Database schema documented

---

### T065: Setup Monitoring and Alerting

- [ ] T065 [P] Setup monitoring and alerting for production

**Scope**:
- Configure monitoring for backend (Render/Railway dashboard)
- Setup error alerting (email or Slack)
- Create dashboard for key metrics
- Document monitoring setup

**Deliverables**:
- Monitoring configuration
- Alert rules
- Monitoring documentation

**Acceptance Criteria**:
- [ ] Backend uptime monitored
- [ ] Error rate tracked
- [ ] Response time metrics collected
- [ ] Alerts configured for errors and downtime
- [ ] Dashboard accessible to team
- [ ] Monitoring documented

---

## Next Steps

**Immediate Action**: Execute `/sp.implement` to begin Phase 1 (Project Setup & Infrastructure)

**MVP Scope**: Complete Phase 1 and Phase 2 (Tasks T001-T024) for working RAG chatbot

**Timeline**:
- **Days 1-2**: Phase 1 + Phase 2 (Setup + US1 Basic Q&A)
- **Day 3**: Phase 3 (US2 Conversation History)
- **Day 4**: Phase 4 (US3 Personalization) + Phase 5 (US4 Multi-Modal)
- **Day 5**: Phase 6 (US5 Error Handling) + Phase 7 (Deployment) + Phase 8 (Polish)

**Parallel Execution**: 42 tasks marked [P] can be executed in parallel within their phase

**Success Criteria**: All 12 success criteria (SC-001 to SC-012) validated in Phase 7
