# RAG Chatbot Backend

FastAPI-based backend for the Physical AI & Humanoid Robotics Textbook chatbot.

## Architecture

**RAG (Retrieval-Augmented Generation) Pipeline**:
1. **Retrieval**: Qdrant vector database for semantic search
2. **Generation**: Google Gemini API for contextual responses
3. **Storage**: Neon PostgreSQL for conversations and history

## Project Structure

```
backend/
├── main.py                  # FastAPI application entry point
├── config.py                # Environment configuration (Pydantic Settings)
├── database.py              # Async PostgreSQL connection
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── alembic/                 # Database migrations
│   ├── env.py               # Migration environment (async)
│   ├── versions/            # Migration files
│   └── alembic.ini          # Alembic configuration
├── models/                  # SQLAlchemy ORM models
│   ├── user_session.py      # Anonymous user sessions
│   ├── conversation.py      # Conversation threads
│   └── message.py           # Chat messages (user + assistant)
├── services/                # Business logic
│   ├── qdrant_service.py    # Vector database client
│   ├── gemini_service.py    # Gemini API integration
│   └── rag_service.py       # RAG orchestration
├── routers/                 # API endpoints
│   ├── health.py            # Health check endpoints
│   └── chat.py              # Chat API endpoints
└── tests/                   # Test suite
```

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required variables:
- `GEMINI_API_KEY` - Get from https://ai.google.dev/
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `DATABASE_URL` - Neon PostgreSQL connection string
- `CORS_ORIGINS` - Allowed frontend origins (comma-separated)

Example `.env`:
```
GEMINI_API_KEY=AIzaSy...
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
CORS_ORIGINS=http://localhost:3000,https://yourusername.github.io
```

### 3. Run Database Migrations

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 4. Run Development Server

```bash
# Start server with auto-reload
uvicorn main:app --reload

# Or use Python directly
python main.py
```

Server runs at: http://localhost:8000

## API Endpoints

### Health Check
- **GET** `/health` - Check API and database status
- **GET** `/` - API information

### Chat
- **POST** `/api/chat` - Send a message to the chatbot

Request:
```json
{
  "session_id": "uuid-optional",
  "conversation_id": "uuid-optional",
  "question": "What is ROS 2?"
}
```

Response:
```json
{
  "response": "ROS 2 is...",
  "citations": [
    {
      "chapter": "3",
      "section": "2.1",
      "page": "45",
      "text": "[Chapter 3, Section 2.1]",
      "content_type": "text"
    }
  ],
  "message_id": "uuid",
  "conversation_id": "uuid",
  "session_id": "uuid",
  "is_off_topic": false
}
```

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

```sql
-- User Sessions (anonymous)
user_sessions (
  id UUID PRIMARY KEY,
  created_at TIMESTAMP,
  last_active_at TIMESTAMP
)

-- Conversation Threads
conversations (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES user_sessions(id),
  title VARCHAR(255),
  created_at TIMESTAMP
)

-- Chat Messages
messages (
  id UUID PRIMARY KEY,
  conversation_id UUID REFERENCES conversations(id),
  role VARCHAR(20) CHECK (role IN ('user', 'assistant')),
  content TEXT,
  citations JSONB,
  created_at TIMESTAMP
)
```

## Development

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .

# Sort imports
isort .
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_rag_service.py
```

## Deployment

### Environment Variables for Production

- `ENVIRONMENT=production`
- `LOG_LEVEL=INFO`
- All API keys (Gemini, Qdrant, Database)
- `CORS_ORIGINS` with production frontend URL

### Deployment Platforms

**Recommended**: Render or Railway

1. Connect GitHub repository
2. Set environment variables in dashboard
3. Deploy automatically on push to main branch

See `render.yaml` or `railway.json` for configuration.

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is correct
- Check Neon dashboard for connection limits
- Ensure SSL is enabled: `?ssl=require`

### Qdrant Connection Issues
- Verify `QDRANT_URL` and `QDRANT_API_KEY`
- Check Qdrant Cloud dashboard for cluster status
- Verify collection name is `textbook_chunks`

### Gemini API Issues
- Verify `GEMINI_API_KEY` is valid
- Check quota limits on Google AI Studio
- Review rate limiting settings

### CORS Issues
- Add frontend URL to `CORS_ORIGINS`
- Restart server after changing .env
- Check browser console for specific errors

## Architecture Decisions

See `specs/002-rag-chatbot/plan.md` for detailed architecture decisions and rationale.

## License

See main repository LICENSE file.
