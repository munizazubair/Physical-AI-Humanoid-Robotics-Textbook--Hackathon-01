# Backend Testing Guide

## Environment Setup Status

✅ **Environment File**: `.env` configured with API keys
⏳ **Dependencies**: Installing (in progress)
⏸️ **Database**: Migration pending
⏸️ **Server**: Not started yet

---

## Quick Start Checklist

Once dependency installation completes:

- [ ] Run Alembic migration
- [ ] Start FastAPI server
- [ ] Test health endpoint
- [ ] Test chat endpoint
- [ ] Access API documentation

---

## Step 1: Run Database Migration

**Purpose**: Create database tables from SQLAlchemy models

```bash
cd backend
python -m alembic upgrade head
```

**Expected Output**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> <revision>, Initial schema
```

**Troubleshooting**:
- **Error**: `No module named 'alembic'` → Dependencies not installed yet
- **Error**: `(psycopg2.OperationalError) connection to server failed` → Check DATABASE_URL in .env
- **Error**: `sqlalchemy.exc.ProgrammingError` → Database doesn't exist, create it in Neon dashboard

---

## Step 2: Start FastAPI Development Server

**Purpose**: Run the backend API server with auto-reload

```bash
# From backend/ directory
python main.py

# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Will watch for changes in these directories: ['C:\\...\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [PID]
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Server should be accessible at**: http://localhost:8000

---

## Step 3: Test Health Check Endpoint

**Purpose**: Verify API and database connectivity

### Using curl (Command Line)

```bash
curl http://localhost:8000/health
```

### Using Python

```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())
```

### Using PowerShell

```powershell
Invoke-WebRequest -Uri http://localhost:8000/health | Select-Object -Expand Content
```

**Expected Response (Success)**:
```json
{
  "status": "healthy",
  "api": "healthy",
  "database": "healthy"
}
```

**Expected Response (Database Issue)**:
```json
{
  "status": "unhealthy",
  "api": "healthy",
  "database": "unhealthy: connection error"
}
```

---

## Step 4: Test Chat Endpoint

**Purpose**: Verify full RAG pipeline (Qdrant → Gemini → Citations)

###Option 1: curl (Minimal)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -D '{\"question\": \"What is ROS 2?\"}'
```

### Option 2: curl (With Session)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": null,
    "conversation_id": null,
    "question": "What is ROS 2?"
  }'
```

### Option 3: Python Script

```python
import requests
import json

url = "http://localhost:8000/api/chat"
headers = {"Content-Type": "application/json"}
data = {
    "question": "What is ROS 2?"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

print("Response:", result["response"])
print("\nCitations:")
for citation in result["citations"]:
    print(f"  - {citation['text']}")
print(f"\nMessage ID: {result['message_id']}")
print(f"Session ID: {result['session_id']}")
print(f"Is Off-Topic: {result['is_off_topic']}")
```

### Option 4: PowerShell

```powershell
$body = @{
    question = "What is ROS 2?"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/api/chat `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body | Select-Object -Expand Content
```

**Expected Response**:
```json
{
  "response": "ROS 2 (Robot Operating System 2) is...",
  "citations": [
    {
      "chapter": "3",
      "section": "2.1",
      "page": "45",
      "text": "[Chapter 3, Section 2.1]",
      "content_type": "text"
    }
  ],
  "message_id": "uuid-here",
  "conversation_id": "uuid-here",
  "session_id": "uuid-here",
  "is_off_topic": false
}
```

---

## Step 5: Test Off-Topic Detection

**Purpose**: Verify chatbot declines non-textbook questions

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{\"question\": \"What is the weather today?\"}'
```

**Expected Response**:
```json
{
  "response": "I apologize, but I can only answer questions related to the Physical AI & Humanoid Robotics textbook...",
  "citations": [],
  "message_id": "uuid",
  "conversation_id": "uuid",
  "session_id": "uuid",
  "is_off_topic": true
}
```

---

## Step 6: Test Conversation Continuity

**Purpose**: Verify session management and conversation threading

```python
import requests

url = "http://localhost:8000/api/chat"

# First message
response1 = requests.post(url, json={"question": "What is ROS 2?"})
data1 = response1.json()
session_id = data1["session_id"]
conversation_id = data1["conversation_id"]

print(f"First Response: {data1['response'][:100]}...")

# Second message in same conversation
response2 = requests.post(url, json={
    "session_id": session_id,
    "conversation_id": conversation_id,
    "question": "What are its main components?"
})
data2 = response2.json()

print(f"\nSecond Response: {data2['response'][:100]}...")
print(f"Same Session: {data2['session_id'] == session_id}")
print(f"Same Conversation: {data2['conversation_id'] == conversation_id}")
```

---

## Step 7: Access API Documentation

**Purpose**: Explore interactive API documentation

### Swagger UI
Open in browser: **http://localhost:8000/docs**

Features:
- Interactive API exploration
- "Try it out" functionality
- Request/response schemas
- Authentication testing (if added)

### ReDoc
Open in browser: **http://localhost:8000/redoc**

Features:
- Clean, readable documentation
- Code examples
- Schema definitions
- Search functionality

---

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
pip install -r requirements.txt --user
# OR
python -m pip install -r requirements.txt
```

### Issue 2: Database Connection Failed

**Error**: `sqlalchemy.exc.OperationalError: (asyncpg.exceptions.InvalidCatalogNameError)`

**Solution**:
1. Verify DATABASE_URL in `.env`
2. Ensure Neon database exists
3. Check database name is correct
4. Verify connection string format: `postgresql+asyncpg://user:pass@host/db?ssl=require`

### Issue 3: Qdrant Connection Failed

**Error**: `qdrant_client.http.exceptions.ResponseHandlingException`

**Solution**:
1. Verify QDRANT_URL and QDRANT_API_KEY in `.env`
2. Check Qdrant Cloud dashboard for cluster status
3. Ensure collection `textbook_chunks` exists
4. Verify API key permissions

### Issue 4: Gemini API Error

**Error**: `google.api_core.exceptions.PermissionDenied: 403 API key not valid`

**Solution**:
1. Verify GEMINI_API_KEY in `.env`
2. Check API key at https://ai.google.dev/
3. Ensure API is enabled for your project
4. Check quota limits

### Issue 5: CORS Errors (Frontend)

**Error**: `Access to fetch at 'http://localhost:8000/api/chat' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**:
1. Add frontend origin to `CORS_ORIGINS` in `.env`:
   ```
   CORS_ORIGINS=http://localhost:3000,http://localhost:8000
   ```
2. Restart FastAPI server

### Issue 6: Port Already in Use

**Error**: `OSError: [WinError 10048] Only one usage of each socket address`

**Solution**:
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# OR use a different port
uvicorn main:app --reload --port 8001
```

---

## Testing Checklist

### Basic Functionality
- [ ] Health check returns 200 OK
- [ ] Database connection healthy
- [ ] Chat endpoint accepts POST requests
- [ ] Response includes citations
- [ ] Session ID generated correctly
- [ ] Conversation ID generated correctly

### RAG Pipeline
- [ ] Qdrant retrieves relevant chunks
- [ ] Gemini generates contextual responses
- [ ] Citations extracted correctly
- [ ] Off-topic questions declined
- [ ] Response time < 5 seconds

### Session Management
- [ ] New session created automatically
- [ ] Session persists across requests
- [ ] Conversation threading works
- [ ] Conversation history maintained
- [ ] Conversation title auto-generated

### Error Handling
- [ ] Invalid JSON returns 400
- [ ] Non-existent conversation returns 400
- [ ] Database errors handled gracefully
- [ ] Qdrant errors handled gracefully
- [ ] Gemini errors handled gracefully

### API Documentation
- [ ] Swagger UI accessible at /docs
- [ ] ReDoc accessible at /redoc
- [ ] API schemas documented
- [ ] Examples provided

---

## Performance Testing

### Response Time Test

```python
import requests
import time

url = "http://localhost:8000/api/chat"
question = "What is ROS 2?"

times = []
for i in range(10):
    start = time.time()
    response = requests.post(url, json={"question": question})
    elapsed = time.time() - start
    times.append(elapsed)
    print(f"Request {i+1}: {elapsed:.2f}s")

print(f"\nAverage: {sum(times)/len(times):.2f}s")
print(f"Min: {min(times):.2f}s")
print(f"Max: {max(times):.2f}s")
```

**Target**: < 5 seconds p95 (SC-001)

### Concurrent Requests Test

```python
import requests
import concurrent.futures
import time

url = "http://localhost:8000/api/chat"

def send_request(i):
    start = time.time()
    response = requests.post(url, json={"question": f"What is ROS 2? (request {i})"})
    elapsed = time.time() - start
    return elapsed, response.status_code

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(send_request, i) for i in range(10)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

for i, (elapsed, status) in enumerate(results):
    print(f"Request {i+1}: {elapsed:.2f}s - Status {status}")
```

**Target**: 100 concurrent users

---

## Database Verification

### Check Tables Created

```python
import asyncio
from sqlalchemy import text
from database import engine

async def check_tables():
    async with engine.begin() as conn:
        result = await conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
        """))
        tables = [row[0] for row in result]
        print("Tables created:")
        for table in tables:
            print(f"  - {table}")

asyncio.run(check_tables())
```

**Expected Tables**:
- `user_sessions`
- `conversations`
- `messages`
- `alembic_version`

### Check Data

```python
import asyncio
from database import AsyncSessionLocal
from sqlalchemy import select, func
from models.user_session import UserSession
from models.conversation import Conversation
from models.message import Message

async def check_data():
    async with AsyncSessionLocal() as session:
        # Count sessions
        result = await session.execute(select(func.count()).select_from(UserSession))
        print(f"Total Sessions: {result.scalar()}")

        # Count conversations
        result = await session.execute(select(func.count()).select_from(Conversation))
        print(f"Total Conversations: {result.scalar()}")

        # Count messages
        result = await session.execute(select(func.count()).select_from(Message))
        print(f"Total Messages: {result.scalar()}")

asyncio.run(check_data())
```

---

## Next Steps After Testing

1. **Frontend Integration** (T016-T024):
   - Implement React chat widget
   - Connect to backend API
   - Display citations with links
   - Add loading states

2. **Enhanced Features** (Phase 3-6):
   - Conversation history UI
   - User personalization
   - Multi-modal content
   - Feedback system

3. **Deployment** (Phase 7):
   - Deploy backend to Render/Railway
   - Deploy frontend to GitHub Pages
   - Configure production environment

---

**Last Updated**: 2025-12-27
**Backend Version**: 0.1.0
**Status**: Awaiting dependency installation completion
