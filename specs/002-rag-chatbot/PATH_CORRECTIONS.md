# Path Corrections for RAG Chatbot Tasks

**Issue**: Tasks T016-T030 reference `frontend/src/` paths that don't exist.
**Root Cause**: The project uses Docusaurus with integrated React components in `src/`, not a separate `frontend/` directory.

## Correct Directory Structure

```
Physical-AI-Humanoid-Robotics-Textbook/
├── src/                        ✅ Actual location (Docusaurus convention)
│   ├── components/
│   ├── services/
│   ├── theme/
│   └── css/
├── backend/                    ✅ Backend FastAPI service
├── docs/                       ✅ Docusaurus content
├── .env                        ✅ Frontend environment vars
└── package.json                ✅ Docusaurus package.json
```

## Path Mapping (Incorrect → Correct)

| Incorrect Path (in tasks) | Correct Path | Tasks Affected |
|---------------------------|--------------|----------------|
| `frontend/src/components/ChatWidget.jsx` | `src/components/ChatWidget/` | T016, T020, T021, T028, T030, T031a |
| `frontend/src/services/chatApi.js` | `src/services/chatApi.js` | T017 |
| `frontend/src/services/sessionManager.js` | `src/services/sessionManager.js` | T018 |
| `frontend/src/theme/Root.js` | `src/theme/Root.js` | T019 |
| `frontend/src/components/Citation.jsx` | `src/components/ChatWidget/Citation.jsx` | T020, T042 |
| `frontend/src/components/FeedbackButtons.jsx` | `src/components/ChatWidget/FeedbackButtons.jsx` | T046 |
| `frontend/package.json` | `package.json` (root) | T016 |
| `frontend/.env.production` | `.env` (root, update for production) | T055 |

## Implementation Status

**Already Correct in Codebase:**
- ✅ `src/theme/Root.js` exists and imports FloatingChatWidget
- ✅ `src/components/ChatWidget/` directory exists
- ✅ `src/components/FloatingChatWidget/` directory exists
- ✅ `src/services/` directory exists
- ✅ Root `.env` file exists with `REACT_APP_API_URL`

**Tasks Already Completed (with correct paths):**
- T016, T017, T018, T019, T020, T021, T028, T030, T031 (marked [X] in tasks.md)

## Action Items

1. ✅ **DONE**: Created `src/README.md` documenting the structure
2. ✅ **DONE**: Updated `plan.md` with correct directory structure
3. ✅ **DONE**: Updated `spec.md` FR-036 to clarify frontend integration
4. ⚠️ **PARTIAL**: Tasks.md still contains incorrect paths in descriptions (but implementation used correct paths)
5. 📋 **RECOMMENDED**: Update all task descriptions to reflect actual paths (cosmetic fix)

## Notes for Future Tasks

When working on tasks T053-T065 (deployment and documentation):
- Use `src/` for all frontend component references
- Environment variables for frontend go in root `.env` (not `frontend/.env`)
- Docusaurus build command: `npm run build` (builds to `build/`)
- Frontend deployment: `npm run deploy` (deploys to GitHub Pages)

---

**Created**: 2025-12-28
**Purpose**: Document path inconsistency resolution for critical issue E2 and C1
