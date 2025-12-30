# Frontend Source Directory

This directory contains the Docusaurus frontend integration for the RAG Chatbot.

## Directory Structure

```
src/
├── components/           # React components
│   ├── ChatWidget/      # Main chat UI component
│   ├── FloatingChatWidget/  # Floating chat button wrapper
│   ├── CTASection.js    # Call-to-action sections
│   ├── FeatureCards.js  # Feature display cards
│   └── Footer.js        # Custom footer
├── css/                 # Global styles
├── pages/              # Custom Docusaurus pages
├── services/           # API clients and utilities
│   ├── chatApi.js      # Backend API client
│   └── sessionManager.js  # Session management
└── theme/              # Docusaurus theme overrides
    └── Root.js         # Global app wrapper (includes FloatingChatWidget)
```

## Architecture

This is **NOT** a separate frontend application. It's a **Docusaurus integration** where:

- **Docusaurus** serves the static textbook (`docs/` directory)
- **React components** in `src/components/` provide the chat interface
- **Theme override** in `src/theme/Root.js` injects the chat widget globally
- **Services** in `src/services/` communicate with the FastAPI backend

## Environment Variables

Frontend environment variables are defined in the **root `.env` file** (not `src/.env`):

- `REACT_APP_API_URL` - Backend API endpoint

See `../.env.example` for the template.

## Tasks Reference

When tasks mention `frontend/src/`, they actually refer to `src/` (this directory).
The naming inconsistency has been identified and documented in the analysis report.

**Correct paths:**
- ✅ `src/components/ChatWidget.jsx`
- ✅ `src/services/chatApi.js`
- ✅ `src/theme/Root.js`

**Incorrect paths in tasks:**
- ❌ `frontend/src/components/ChatWidget.jsx` (should be `src/components/...`)
- ❌ `frontend/src/services/chatApi.js` (should be `src/services/...`)

## Related Documentation

- **Backend**: `../backend/README.md`
- **Deployment**: `../specs/002-rag-chatbot/deployment.md` (pending)
- **Architecture**: `../specs/002-rag-chatbot/plan.md`
