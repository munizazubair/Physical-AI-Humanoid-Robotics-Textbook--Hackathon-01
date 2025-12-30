# Implementation Plan: RAG Chatbot for Physical AI Textbook

**Feature**: RAG Chatbot with Gemini Integration
**Branch**: `002-rag-chatbot`
**Created**: 2025-12-26
**Status**: Draft
**Spec**: [spec.md](./spec.md)

---

## Executive Summary

This plan outlines the implementation strategy for a Retrieval-Augmented Generation (RAG) chatbot system embedded in the Physical AI & Humanoid Robotics Docusaurus textbook. The system retrieves relevant content from a Qdrant vector database and generates contextual responses using Google Gemini API, with conversation history and personalization powered by Neon PostgreSQL.

**Architecture**: FastAPI backend (deployed on Render/Railway) + ChatKit/React frontend (embedded in Docusaurus/GitHub Pages) + Qdrant (vector DB) + Neon (PostgreSQL) + Gemini API (LLM)

**Delivery Strategy**: Incremental MVP delivery following user story priorities (P1 → P5), enabling independent testing at each phase.

---

## Plan Status

✅ **Complete** - Ready for task generation (`/sp.tasks`)

**Author**: Claude Sonnet 4.5 (Spec-Driven Development Agent)  
**Date**: 2025-12-26

---

## System Architecture

### Directory Structure

```
Physical-AI-Humanoid-Robotics-Textbook/
├── backend/                    # FastAPI backend service
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Environment configuration
│   ├── database.py             # SQLAlchemy async setup
│   ├── models/                 # Database models
│   │   ├── user_session.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── feedback.py
│   │   └── rate_limit.py
│   ├── routers/                # API endpoints
│   │   ├── chat.py             # POST /api/chat
│   │   ├── conversation.py     # GET/POST conversation endpoints
│   │   ├── feedback.py         # POST /api/feedback
│   │   └── health.py           # GET /health
│   ├── services/               # Business logic
│   │   ├── qdrant_service.py   # Vector search
│   │   ├── gemini_service.py   # LLM generation
│   │   ├── rag_service.py      # RAG orchestration
│   │   └── personalization_service.py
│   ├── middleware/
│   │   └── rate_limiter.py     # Rate limiting middleware
│   ├── alembic/                # Database migrations
│   ├── tests/                  # Backend tests
│   ├── .env                    # Backend secrets (gitignored)
│   └── requirements.txt
│
├── src/                        # Docusaurus frontend integration
│   ├── components/
│   │   ├── ChatWidget/         # Main chat UI (@chatscope/chat-ui-kit-react)
│   │   └── FloatingChatWidget/ # Floating button wrapper
│   ├── services/
│   │   ├── chatApi.js          # Fetch API client for backend
│   │   └── sessionManager.js   # localStorage session management
│   ├── theme/
│   │   └── Root.js             # Global wrapper (injects FloatingChatWidget)
│   └── css/                    # Styles
│
├── docs/                       # Docusaurus textbook content
├── .env                        # Frontend environment vars (REACT_APP_API_URL)
├── docusaurus.config.js
├── package.json
└── specs/002-rag-chatbot/      # Feature documentation
```

### Technology Stack

**Frontend (Docusaurus Integration)**
- **Framework**: Docusaurus 3.0 (React-based static site generator)
- **Chat UI**: @chatscope/chat-ui-kit-react v2.1.1
- **State Management**: React hooks (useState, useEffect)
- **API Client**: Native Fetch API
- **Session Persistence**: localStorage
- **Deployment**: GitHub Pages

**Backend (FastAPI Service)**
- **Framework**: FastAPI (Python 3.10+)
- **Database**: Neon PostgreSQL (serverless)
- **ORM**: SQLAlchemy with asyncpg driver
- **Migrations**: Alembic
- **Vector DB**: Qdrant Cloud Free Tier
- **LLM**: Google Gemini 1.5 Pro API
- **Input Sanitization**: Python's built-in `html.escape()` for HTML/JS escaping, Pydantic models for validation
- **Logging**: Python logging module with rotation
- **Deployment**: Render (primary choice) or Railway (fallback) - see deployment decision below

**External Services**
- **Qdrant Cloud**: Pre-populated with textbook embeddings
- **Neon PostgreSQL**: Conversation history, user profiles, feedback
- **Google Gemini API**: Response generation

### Data Flow

1. **User asks question** → Docusaurus page (src/components/FloatingChatWidget)
2. **Frontend sends POST /api/chat** → FastAPI backend (routers/chat.py)
3. **Backend retrieves context** → Qdrant vector search (services/qdrant_service.py)
4. **Backend generates response** → Gemini API (services/gemini_service.py)
5. **Backend saves to DB** → Neon PostgreSQL (models/message.py)
6. **Frontend displays response** → ChatWidget component with citations

### Environment Variables

**Root `.env` (Frontend - Docusaurus)**
```bash
REACT_APP_API_URL=http://localhost:8000  # Backend API endpoint
```

**`backend/.env` (Backend - FastAPI)**
```bash
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_key
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
CORS_ORIGINS=http://localhost:3000,https://munizazubair.github.io
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### API Endpoints

**Chat & Conversation**
- `POST /api/chat` - Send question, receive response with citations
- `GET /api/conversation/history?session_id={uuid}` - Retrieve conversation history
- `POST /api/conversation/new` - Start new conversation

**Feedback & Personalization**
- `POST /api/feedback` - Submit thumbs up/down rating
- `GET /api/personalization/greeting?session_id={uuid}` - Get personalized greeting
- `GET /api/personalization/recommendations?session_id={uuid}` - Get chapter recommendations

**Health & Monitoring**
- `GET /health` - Health check endpoint

### Deployment Architecture

**Production Setup:**
```
GitHub Pages (Frontend)
    ↓ HTTPS
FastAPI (Render/Railway)
    ↓
Neon PostgreSQL (Serverless)
Qdrant Cloud (Vector DB)
Google Gemini API
```

**CORS Configuration:**
- Backend allows: `https://munizazubair.github.io`
- Development allows: `http://localhost:3000`, `http://localhost:8000`

### Key Architectural Decisions

**Decision: Docusaurus Integration vs Separate Frontend**
- **Chosen**: Integrate chat widget into existing Docusaurus site via `src/theme/Root.js`
- **Rationale**: Simpler deployment (single GitHub Pages site), better UX (no separate frontend), consistent styling
- **Alternative Rejected**: Separate React app (more complex deployment, iframe integration issues)

**Decision: @chatscope/chat-ui-kit-react vs Custom UI**
- **Chosen**: @chatscope/chat-ui-kit-react
- **Rationale**: Production-ready components, TypeScript support, active maintenance, MIT license
- **Alternative Rejected**: ChatKit SDK (outdated), custom build (time-consuming)

**Decision: Render vs Railway for Backend**
- **Chosen**: Render (primary), Railway (fallback)
- **Rationale**:
  - Render offers 750 free hours/month for web services (sufficient for demo/hackathon)
  - Native PostgreSQL support (can connect to Neon via DATABASE_URL)
  - Automatic HTTPS with custom domains
  - Simple deployment from GitHub repository
  - Zero-config deployments with render.yaml
  - Railway is fallback if Render free tier exhausted
- **Evaluation Criteria Met**:
  - Free tier: ✅ 750hrs/month (enough for MVP testing)
  - Cold start: ~30-60s (acceptable for demo)
  - PostgreSQL: ✅ Native support via connection string
  - HTTPS: ✅ Automatic
  - Deployment: ✅ GitHub integration
- **Alternative Considered**: Railway (similar features, $5 free credit/month)

## Full Plan Details

See Phase 0, Phase 1, and Phase 2 sections below for complete implementation roadmap.
