---
id: 003
title: RAG Chatbot Implementation Plan
stage: plan
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-rag-chatbot
branch: 002-rag-chatbot
user: SIBGHAT
command: /sp.plan
labels: ["plan", "rag", "chatbot", "gemini", "fastapi", "architecture"]
links:
  spec: specs/002-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-rag-chatbot/plan.md
tests:
  - Constitution Check: PASSED (all 5 principles aligned)
---

## Prompt

User executed `/sp.plan` command with comprehensive argument:

"I have a completed feature specification for a Retrieval-Augmented Generation (RAG) chatbot to be embedded in a Docusaurus textbook on Physical AI & Humanoid Robotics.

The system uses:
- FastAPI backend
- Qdrant Cloud vector database for textbook embeddings
- Google Gemini API for response generation
- Neon PostgreSQL for conversation history and personalization
- ChatKit or React-based chat UI on the frontend
- Deployment on GitHub Pages (frontend) and Render/Railway/Vercel (backend)

I want you to create a **step-by-step development plan** for building this chatbot MVP.

Requirements for the plan:
1. Break down the work into **phases or milestones** (e.g., backend setup, retrieval integration, frontend chat UI, personalization, testing, deployment).
2. Include specific **tasks under each phase**, such as setting up FastAPI endpoints, integrating Qdrant retrieval, connecting Gemini API, storing messages in Neon, embedding the chat widget in Docusaurus, adding feedback buttons, and implementing sliding window context.
3. Include **priority order** based on feature importance (P1 to P5).
4. Include any **critical considerations**, such as API token limits, CORS setup, environment variables, error handling, and performance constraints.
5. Suggest **testing and validation steps** for each phase.
6. Suggest a **timeline or sequence** for a hackathon MVP.

Output should be a **clear, actionable development plan** that I or a developer can follow to implement the chatbot from scratch, starting with backend setup."

## Response snapshot

### Implementation Plan Created

**Feature**: RAG Chatbot for Physical AI Textbook
**Branch**: `002-rag-chatbot`
**Status**: Draft - Ready for task generation

### Key Decisions

**1. System Architecture**
- **Frontend**: React + ChatKit UI library embedded in Docusaurus (GitHub Pages)
- **Backend**: FastAPI (Python 3.10+) deployed on Render/Railway
- **Vector DB**: Qdrant Cloud Free Tier (pre-populated with textbook embeddings)
- **LLM**: Google Gemini API (Gemini 1.5 Pro - 1M token context window)
- **Database**: Neon Serverless PostgreSQL for conversation history and personalization

**2. Development Phases**

**Phase 0: Research & Discovery**
- Resolve critical unknowns (Gemini model selection, ChatKit vs alternatives, Qdrant schema verification)
- Research backend hosting options (Render vs Railway vs Vercel)
- Design citation format for responses
- **Output**: `research.md` with all decisions documented

**Phase 1: Design & Contracts**
- Design database schema (6 tables: user_sessions, conversations, messages, feedback, user_profiles, rate_limits)
- Generate API contracts (OpenAPI 3.0 specification for 4 endpoints)
- Create quickstart guide for local development
- Update agent context with new technologies
- **Output**: `data-model.md`, `contracts/api-spec.yaml`, `quickstart.md`

**Phase 2: Implementation Roadmap (8 Milestones)**

**Milestone 1: Core Backend Setup** (P1 Foundation)
- Initialize FastAPI project structure
- Setup Neon PostgreSQL connection (SQLAlchemy async)
- Implement health check endpoint
- Configure CORS middleware (allow GitHub Pages origin)
- Setup environment variables

**Milestone 2: RAG Pipeline Integration** (P1 Core Functionality)
- Integrate Qdrant Client (semantic search retrieval)
- Integrate Gemini API (response generation)
- Implement RAG orchestration (retrieve → generate → cite)
- Create `/api/chat` endpoint
- Implement session management (UUID-based anonymous sessions)

**Milestone 3: Frontend Chat Widget** (P1 User-Facing Deliverable)
- Setup React Chat UI library
- Implement API client (fetch with error handling)
- Integrate chat widget with Docusaurus (floating button, bottom-right corner)
- Display citations as clickable links
- Implement loading states ("typing..." indicator)

**Milestone 4: Conversation History** (P2)
- Implement message persistence (save to Neon)
- Implement conversation retrieval (`GET /api/conversation/history`)
- Update RAG service for context (last 20 messages sliding window)
- Implement "New Conversation" feature
- Update frontend for history display

**Milestone 5: Personalization Layer** (P3)
- Implement user profile tracking (topics, chapters, knowledge level)
- Implement interest detection (analyze last 10 questions)
- Implement personalized greetings ("Welcome back! I see you've been exploring VLA...")
- Implement adaptive response complexity (beginner vs advanced)
- Implement recommendation system (suggest next chapters)

**Milestone 6: Multi-Modal Content Integration** (P4)
- Enhance Qdrant metadata (verify content type: text, code, diagram)
- Implement content type detection
- Update response generation for visual content references
- Enhance citation display (different styles for code vs diagrams)

**Milestone 7: Error Handling & Feedback** (P5)
- Implement feedback endpoint (`POST /api/feedback` for thumbs up/down)
- Add feedback UI to chat widget
- Implement graceful degradation (Qdrant/Gemini unavailable)
- Implement rate limiting (max 20 questions/hour per session)
- Implement error logging

**Milestone 8: Testing & Deployment** (Final MVP)
- Backend deployment (Render/Railway with HTTPS and CORS)
- Frontend integration (update `REACT_APP_CHAT_API_URL`)
- End-to-end testing (all user stories P1-P5)
- Performance testing (100 concurrent users, response time <5s)
- User acceptance testing (target: 70% thumbs-up rating)
- Bug fixes & refinements

**3. Hackathon Timeline (5 Days)**

**Day 1**: Phase 0 Research + Milestone 1 (Core Backend Setup)
**Day 2**: Milestone 2 (RAG Pipeline Integration)
**Day 3**: Milestone 3 (Frontend Chat Widget)
**Day 4**: Milestone 4 (Conversation History) + Milestone 5 (Personalization)
**Day 5**: Milestone 6, 7, 8 (Multi-Modal, Error Handling, Testing, Deployment)

**4. Critical Considerations**

**API Token Limits**
- Gemini 1.5 Pro: 1M token context window (supports long conversations)
- Implement sliding window (last 20 messages, ~10K tokens)
- Monitor token usage in logs, summarize older messages if needed

**CORS Configuration**
- FastAPI CORS middleware with explicit allowed origins (GitHub Pages URL)
- Test early in Milestone 1 (manual fetch from browser console)
- Require HTTPS for backend (Render/Railway provide by default)

**Environment Variables**
- Backend: `GEMINI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `DATABASE_URL`, `CORS_ORIGINS`
- Frontend: `REACT_APP_CHAT_API_URL`
- Use `.env` files locally, platform dashboards for production

**Error Handling**
- Wrap Qdrant and Gemini API calls in try-except blocks
- Implement retries with exponential backoff (up to 2 attempts)
- Return user-friendly error messages within 3 seconds (FR-025, SC-011)

**Performance Constraints**
- RAG pipeline must complete within 5 seconds (SC-001)
- Use async/await for parallel operations (Qdrant query + Neon history fetch)
- Optimize Qdrant query (limit top-k to 5 chunks, use metadata filters)
- Monitor latency for each component

**Rate Limiting**
- FR-027: Max 20 questions per user per hour
- Store counters in Neon `rate_limits` table
- Return 429 status with retry-after header

**Data Privacy**
- Anonymous session IDs (UUIDs), no user authentication
- Implement conversation deletion endpoint (FR-032)
- Encrypt data at rest in Neon
- Display privacy notice in chat widget

**5. Constitution Check**

**All 5 Core Principles Aligned:**

✅ **I. Accuracy & Faithfulness**: System enforces "Single Source of Truth" - answers ONLY from textbook content (FR-007, SC-005: 95% off-topic detection)

✅ **II. Clarity & Accessibility**: Responses include citations (FR-005) and educational explanations (SC-003: 70% thumbs-up rating)

✅ **III. Spec-Driven Development**: All requirements trace to spec.md (FR-001 to FR-037), no features outside scope

✅ **IV. Single Source of Truth**: Chatbot answers ONLY from Qdrant-stored textbook content, no external knowledge sources

✅ **V. Transparency**: System displays error messages (FR-025), logs feedback (FR-023), allows conversation deletion (FR-032)

**Gate Evaluation**: ✅ **PASS** - No constitutional violations

**6. Risks & Mitigations**

**High Priority Risks:**
1. **Gemini API Rate Limits** (Medium likelihood, High impact) → Mitigation: caching, usage monitoring, rate limiting
2. **Qdrant Retrieval Quality** (Medium likelihood, High impact) → Mitigation: test in Phase 0, implement fallback for low-confidence retrievals
3. **CORS Configuration Issues** (Medium likelihood, High impact) → Mitigation: test early in Milestone 1

**Medium Priority Risks:**
4. **Backend Deployment Complexity** (Medium likelihood, Medium impact) → Mitigation: use simple platform (Render/Railway)
5. **Conversation Context Overflow** (Low likelihood, Medium impact) → Mitigation: sliding window context
6. **Performance Under Load** (Low likelihood, Medium impact) → Mitigation: async operations, rate limiting

**7. Success Metrics**

**MVP Completion Criteria:**
- [ ] All P1 features implemented (User Story 1)
- [ ] Backend deployed with HTTPS and CORS
- [ ] Frontend chat widget embedded in textbook
- [ ] All 12 success criteria (SC-001 to SC-012) validated
- [ ] All acceptance scenarios for P1-P3 pass
- [ ] User acceptance testing: 70%+ thumbs-up rating

**Stretch Goals:**
- [ ] P4: Multi-modal content integration
- [ ] P5: Error handling and feedback
- [ ] Performance: Response time <3 seconds
- [ ] Advanced personalization

## Outcome

- ✅ Impact: Comprehensive implementation plan created with 8 milestones, 5-day hackathon timeline, and complete risk analysis
- 🧪 Tests: Constitution Check PASSED (all 5 principles aligned)
- 📁 Files: 1 file created (specs/002-rag-chatbot/plan.md)
- 🔁 Next prompts: `/sp.tasks` to generate actionable task list from plan.md, then `/sp.implement` to begin Milestone 1 (Core Backend Setup)
- 🧠 Reflection: Plan successfully breaks down complex RAG chatbot system into incremental, testable milestones. Follows spec-driven development workflow (spec → plan → tasks → implementation). All critical considerations addressed (CORS, environment variables, token limits, error handling, performance). Ready for task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan creation successful
- Graders run and results (PASS/FAIL): Constitution Check PASSED (all 5 principles aligned)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - plan is complete and ready for `/sp.tasks`
