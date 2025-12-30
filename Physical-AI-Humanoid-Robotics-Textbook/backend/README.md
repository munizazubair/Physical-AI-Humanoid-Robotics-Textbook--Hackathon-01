---
title: RAG Chatbot Backend API
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 8000
---

# RAG Chatbot Backend - Physical AI Textbook

FastAPI backend service for the RAG chatbot integrated with the Physical AI & Humanoid Robotics textbook.

## Features

- **RAG Pipeline**: Retrieval-Augmented Generation using Qdrant + Gemini
- **Conversation History**: Multi-turn conversations with context
- **Personalization**: Interest detection and adaptive responses
- **Multi-Modal Support**: Text, code, and diagram citations
- **Error Handling**: Graceful degradation and rate limiting
- **Feedback System**: Thumbs up/down ratings

## Tech Stack

- **Framework**: FastAPI (Python 3.12)
- **Database**: Neon PostgreSQL (serverless)
- **Vector DB**: Qdrant Cloud
- **LLM**: Google Gemini 2.5 Pro
- **Embeddings**: Cohere API (embed-english-v3.0)

## Environment Variables

Configure these secrets in Hugging Face Spaces settings:

```bash
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
CORS_ORIGINS=https://yourusername.github.io
ENVIRONMENT=production
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

## API Endpoints

### Chat & Conversation
- `POST /api/chat` - Send question, receive response with citations
- `GET /api/conversation/history` - Retrieve conversation history
- `POST /api/conversation/new` - Start new conversation
- `DELETE /api/conversation/{id}` - Delete conversation

### Feedback
- `POST /api/feedback` - Submit thumbs up/down rating

### Health
- `GET /health` - Health check endpoint

## Deployment on Hugging Face Spaces

This app is configured for Hugging Face Spaces with Docker SDK.

### 1. Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **Owner**: Your username or organization
   - **Space name**: `rag-chatbot-backend` (or your choice)
   - **License**: MIT
   - **SDK**: Docker
   - **Visibility**: Public or Private

### 2. Upload Files

Push this backend directory to your Space:

```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
cd SPACE_NAME

# Copy backend files
cp -r ../Physical-AI-Humanoid-Robotics-Textbook/backend/* .

# Commit and push
git add .
git commit -m "Initial backend deployment"
git push
```

### 3. Configure Secrets

In your Space's Settings → Repository secrets, add:

- `GEMINI_API_KEY`
- `COHERE_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `DATABASE_URL`
- `CORS_ORIGINS` (your GitHub Pages URL)

### 4. Auto-Deploy

Hugging Face Spaces will automatically build and deploy your Docker container.

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Generate Embeddings

Populate Qdrant with textbook embeddings:

```bash
python scripts/generate_embeddings.py
```

This will:
- Read all .md and .mdx files from docs/
- Generate embeddings using Cohere API (embed-english-v3.0)
- Upload to Qdrant vector database

## Testing

```bash
# Health check
curl https://YOUR_USERNAME-SPACE_NAME.hf.space/health

# Test chat endpoint
curl -X POST https://YOUR_USERNAME-SPACE_NAME.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a VLA model?"}'
```

## Architecture

```
Frontend (GitHub Pages)
    ↓
Backend API (Hugging Face Spaces)
    ↓
├── Qdrant Cloud (vector search)
├── Gemini API (response generation)
├── Cohere API (embeddings)
└── Neon PostgreSQL (conversation history)
```

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
  is_deleted BOOLEAN DEFAULT FALSE,
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

-- Feedback
feedback (
  id UUID PRIMARY KEY,
  message_id UUID REFERENCES messages(id),
  rating INTEGER CHECK (rating IN (1, -1)),
  comment TEXT,
  created_at TIMESTAMP
)

-- Rate Limiting
rate_limits (
  session_id UUID REFERENCES user_sessions(id),
  request_count INTEGER,
  window_start TIMESTAMP
)
```

## Interactive API Documentation

Once deployed, visit:
- **Swagger UI**: https://YOUR_USERNAME-SPACE_NAME.hf.space/docs
- **ReDoc**: https://YOUR_USERNAME-SPACE_NAME.hf.space/redoc

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` in Secrets
- Check Neon dashboard for connection limits
- Ensure SSL is enabled: `?ssl=require`

### Qdrant Connection Issues
- Verify `QDRANT_URL` and `QDRANT_API_KEY` in Secrets
- Check Qdrant Cloud dashboard for cluster status
- Verify collection name is `textbook_embeddings`

### Gemini API Issues
- Verify `GEMINI_API_KEY` in Secrets
- Check quota limits on Google AI Studio
- Review rate limiting settings

### Cohere API Issues
- Verify `COHERE_API_KEY` in Secrets
- Check usage limits on Cohere dashboard
- Ensure model `embed-english-v3.0` is available

### CORS Issues
- Add your GitHub Pages URL to `CORS_ORIGINS` in Secrets
- Format: `https://username.github.io`
- Restart Space after changing secrets

## License

MIT
