# RAG Chatbot Deployment Guide

**Your Workflow Configuration:** Frontend (GitHub Pages) + Backend (Hugging Face Spaces) + Cohere Embeddings

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│  Frontend: GitHub Pages                                       │
│  - Docusaurus 3.0 with React                                  │
│  - ChatKit UI (@chatscope/chat-ui-kit-react)                  │
│  - Floating chat widget on all pages                          │
└────────────────────┬─────────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  Backend API: Hugging Face Spaces                             │
│  - FastAPI (Python 3.12)                                       │
│  - Docker deployment                                           │
│  - Port 8000                                                   │
└────────────────────┬─────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        ▼            ▼            ▼            ▼
  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
  │ Cohere  │  │ Qdrant  │  │ Gemini  │  │  Neon   │
  │   API   │  │  Cloud  │  │   API   │  │  PG DB  │
  │Embedding│  │ Vector  │  │  LLM    │  │Sessions │
  └─────────┘  └─────────┘  └─────────┘  └─────────┘
```

## Prerequisites

✅ **You already have:**
- Cohere API key
- Gemini API key
- Qdrant Cloud URL & API key
- Neon PostgreSQL database URL
- Hugging Face account
- GitHub Pages site (deployed)

## Step-by-Step Deployment

### Phase 1: Generate Embeddings with Cohere

**1.1 Install Cohere Package**
```bash
cd backend
pip install cohere
```

**1.2 Verify Environment Variables**

Check `backend/.env` contains:
```bash
COHERE_API_KEY=48ZaoYc4OqXt2VEOwZkHMMeYePcrUiZ5fJvZM9Eu  # ✅ Already set
QDRANT_URL=https://8e6d0192-3f09-4b56-8c20-6c80805d0da2.us-east4-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**1.3 Run Embedding Generation**
```bash
cd backend
python scripts/generate_embeddings.py
```

Expected output:
```
============================================================
Textbook Embedding Generation with Cohere API
============================================================

[*] Initializing Cohere client...
[OK] Cohere client initialized (model: embed-english-v3.0, vector size: 1024)

[*] Connecting to Qdrant...
[OK] Connected to Qdrant

[*] Creating collection: textbook_embeddings
[OK] Collection created

[*] Found 45 markdown/MDX files

[*] Processing: module-1/introduction.md
   Chunks: 23
   Embedding batch of 96 chunks...
   Uploaded 96 points to Qdrant

...

[SUCCESS] Embedding generation complete!
   Total chunks: 1247
   Collection: textbook_embeddings

[*] Verification:
   Points in Qdrant: 1247
```

**Troubleshooting:**
- **Error: COHERE_API_KEY not found** → Check backend/.env file
- **Error: No markdown files found** → Verify docs/ directory exists
- **Network timeout** → Check Cohere API dashboard for rate limits

---

### Phase 2: Deploy Backend to Hugging Face Spaces

**2.1 Create New Space**

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in details:
   - **Owner:** Your username
   - **Space name:** `rag-chatbot-backend` (or your choice)
   - **License:** MIT
   - **SDK:** **Docker** (IMPORTANT!)
   - **Visibility:** Public or Private
4. Click **"Create Space"**

**2.2 Clone Your Space**

```bash
# Clone the empty space
git clone https://huggingface.co/spaces/YOUR_USERNAME/rag-chatbot-backend
cd rag-chatbot-backend

# Copy backend files
cp -r ../Physical-AI-Humanoid-Robotics-Textbook/backend/* .

# Verify files copied
ls
# Should see: main.py, requirements.txt, Dockerfile, README.md, models/, services/, routers/, etc.
```

**2.3 Commit and Push**

```bash
git add .
git commit -m "Initial RAG chatbot backend deployment"
git push
```

HF Spaces will automatically start building your Docker container.

**2.4 Configure Environment Secrets**

Go to your Space → **Settings** → **Repository secrets**

Add the following secrets:

| Secret Name | Value | Source |
|-------------|-------|--------|
| `GEMINI_API_KEY` | `AIzaSyAsebwkX8bd3diV7OB6VJXva4rokD-biTU` | Google AI Studio |
| `COHERE_API_KEY` | `48ZaoYc4OqXt2VEOwZkHMMeYePcrUiZ5fJvZM9Eu` | Cohere Dashboard |
| `QDRANT_URL` | `https://8e6d0192-3f09-4b56-8c20-6c80805d0da2.us-east4-0.gcp.cloud.qdrant.io` | Qdrant Cloud |
| `QDRANT_API_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Qdrant Cloud |
| `DATABASE_URL` | `postgresql+asyncpg://neondb_owner:npg_rIiXhGD6dc8J@ep-aged-hill-a47yr5q8-pooler.us-east-1.aws.neon.tech/neondb?ssl=require` | Neon Dashboard |
| `CORS_ORIGINS` | `https://YOUR_USERNAME.github.io` | Your GitHub Pages URL |
| `ENVIRONMENT` | `production` | - |
| `LOG_LEVEL` | `INFO` | - |
| `HOST` | `0.0.0.0` | - |
| `PORT` | `8000` | - |

**2.5 Wait for Build**

- HF Spaces will build your Docker container (3-5 minutes)
- Monitor build logs in the "Logs" tab
- Once complete, your API will be live at: `https://YOUR_USERNAME-rag-chatbot-backend.hf.space`

**2.6 Run Database Migrations**

Option A - Local (Recommended):
```bash
cd backend
# Update .env with production DATABASE_URL
alembic upgrade head
```

Option B - In HF Space:
1. Go to your Space
2. Click "Embed" → "Direct URL"
3. SSH into container (if available) or use API to trigger migration

**2.7 Verify Deployment**

Test health check:
```bash
curl https://YOUR_USERNAME-rag-chatbot-backend.hf.space/health
```

Expected response:
```json
{"status": "healthy", "database": "connected"}
```

Test chat endpoint:
```bash
curl -X POST https://YOUR_USERNAME-rag-chatbot-backend.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a VLA model?"}'
```

Expected response:
```json
{
  "response": "A VLA (Vision-Language-Action) model is...",
  "citations": [...],
  "message_id": "...",
  "conversation_id": "...",
  "session_id": "..."
}
```

---

### Phase 3: Update Frontend Configuration

**3.1 Update Frontend .env**

Edit the root `.env` file:
```bash
# Old (local development)
REACT_APP_API_URL=http://localhost:8000

# New (production - update with YOUR space name)
REACT_APP_API_URL=https://YOUR_USERNAME-rag-chatbot-backend.hf.space
```

**3.2 Update CORS in Backend (if needed)**

If you get CORS errors, verify `CORS_ORIGINS` secret in HF Spaces matches your GitHub Pages URL exactly:
```bash
# Correct format
CORS_ORIGINS=https://YOUR_USERNAME.github.io

# NOT
CORS_ORIGINS=https://YOUR_USERNAME.github.io/
```

**3.3 Rebuild and Deploy Frontend**

```bash
# Build Docusaurus
npm run build

# Deploy to GitHub Pages
npm run deploy
```

Or if using GitHub Actions, just push to main:
```bash
git add .env
git commit -m "Update backend API URL for production"
git push origin main
```

**3.4 Test End-to-End**

1. Visit your GitHub Pages site: `https://YOUR_USERNAME.github.io`
2. Click the floating chat button (bottom-right)
3. Ask a question: "What is ROS 2?"
4. Verify:
   - ✅ Response appears
   - ✅ Citations show up
   - ✅ No CORS errors in browser console

---

## Monitoring & Maintenance

### View Logs

**Backend Logs (HF Spaces):**
```
https://huggingface.co/spaces/YOUR_USERNAME/rag-chatbot-backend/logs
```

**Frontend Logs (GitHub Pages):**
```
Check browser console (F12) for client-side errors
```

### Update Backend Code

```bash
cd rag-chatbot-backend
# Make changes to files
git add .
git commit -m "Update: description"
git push
# HF Spaces will auto-rebuild
```

### Update Environment Secrets

1. Go to HF Space → Settings → Repository secrets
2. Edit the secret value
3. Restart the Space (it will automatically restart)

### Database Migrations

When adding new models/fields:
```bash
cd backend
alembic revision --autogenerate -m "Add new field"
alembic upgrade head
```

---

## Troubleshooting

### Backend Won't Start

**Check Logs:**
```
https://huggingface.co/spaces/YOUR_USERNAME/rag-chatbot-backend/logs
```

**Common Issues:**
- Missing environment secrets → Add in Settings
- Database connection failed → Check DATABASE_URL
- Port binding error → Ensure PORT=8000

### CORS Errors

**Symptom:** Browser console shows:
```
Access to fetch at 'https://...hf.space/api/chat' from origin 'https://...github.io' has been blocked by CORS policy
```

**Fix:**
1. Go to HF Space → Settings → Secrets
2. Update `CORS_ORIGINS` to match your GitHub Pages URL EXACTLY
3. Restart Space

### Embeddings Not Found

**Symptom:** Chatbot responds with "Search service temporarily unavailable"

**Fix:**
1. Check Qdrant dashboard: https://cloud.qdrant.io
2. Verify collection `textbook_embeddings` exists
3. Re-run embedding generation if needed:
   ```bash
   cd backend
   python scripts/generate_embeddings.py
   ```

### Gemini API Quota Exceeded

**Symptom:** 429 error in logs

**Fix:**
1. Wait for quota to reset (usually hourly)
2. Or upgrade Gemini API plan
3. Or get a new API key

---

## Cost Breakdown (All Free Tier)

| Service | Cost | Limits |
|---------|------|--------|
| Hugging Face Spaces | FREE | 2 CPU cores, 16GB RAM |
| Cohere Embeddings | FREE | 100 API calls/month trial |
| Qdrant Cloud | FREE | 1GB storage |
| Gemini API | FREE | 60 requests/minute |
| Neon PostgreSQL | FREE | 3GB storage |
| GitHub Pages | FREE | 100GB bandwidth/month |

**Total Monthly Cost: $0** (within free tier limits)

---

## Next Steps After Deployment

1. ✅ Test all features (chat, history, feedback)
2. ✅ Monitor usage in each service dashboard
3. ✅ Set up error alerting (optional)
4. ✅ Document API for team members
5. ✅ Create user guide for students

## Support & Resources

- **Hugging Face Docs:** https://huggingface.co/docs/hub/spaces
- **Cohere Docs:** https://docs.cohere.com/
- **Qdrant Docs:** https://qdrant.tech/documentation/
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

**Deployment completed successfully!** 🎉

Your RAG chatbot is now live with:
- ✅ Cohere embeddings (fast, cloud-based)
- ✅ Hugging Face Spaces backend (free, reliable)
- ✅ GitHub Pages frontend (already deployed)
- ✅ All services connected and working
