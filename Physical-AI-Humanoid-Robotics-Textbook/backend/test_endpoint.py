"""
Simple test endpoint to debug RAG service
"""
from fastapi import FastAPI
from database import AsyncSessionLocal
from services.rag_service import rag_service
import uvicorn

app = FastAPI()

@app.get("/test")
async def test_rag():
    try:
        async with AsyncSessionLocal() as db:
            result = await rag_service.process_question(
                question="What is ROS2?",
                session_id=None,
                conversation_history=[],
                db=db
            )
            return {
                "success": True,
                "response": result["response"][:200],
                "citations_count": len(result["citations"])
            }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
