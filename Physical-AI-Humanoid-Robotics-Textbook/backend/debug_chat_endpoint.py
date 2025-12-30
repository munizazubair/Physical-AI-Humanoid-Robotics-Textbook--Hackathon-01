"""
Debug script for chat endpoint 500 errors
Tests each component of the RAG pipeline individually
"""
import asyncio
import sys
import traceback
from sqlalchemy import text
from database import AsyncSessionLocal
from services.rag_service import rag_service
from services.gemini_service import gemini_service
from services.qdrant_service import qdrant_service
from config import settings

async def test_database():
    """Test database connection"""
    print("\n=== Testing Database Connection ===")
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(text("SELECT 1"))
            print("[PASS] Database connection successful")
            return True
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        traceback.print_exc()
        return False

async def test_qdrant():
    """Test Qdrant service"""
    print("\n=== Testing Qdrant Service ===")
    try:
        print(f"Qdrant URL: {settings.qdrant_url}")
        print(f"Qdrant API Key configured: {bool(settings.qdrant_api_key)}")

        # Test search
        results = await qdrant_service.search(
            query="What is ROS2?",
            top_k=3,
            score_threshold=0.3
        )
        print(f"[PASS] Qdrant search successful: {len(results)} results")
        for i, result in enumerate(results[:2]):
            print(f"  Result {i+1}: score={result['score']:.3f}, chapter={result['metadata'].get('chapter', 'N/A')}")
        return True
    except Exception as e:
        print(f"[FAIL] Qdrant search failed: {e}")
        traceback.print_exc()
        return False

async def test_gemini():
    """Test Gemini service"""
    print("\n=== Testing Gemini Service ===")
    try:
        print(f"Gemini API Key configured: {bool(settings.gemini_api_key)}")

        # Test simple generation
        context_chunks = [{
            "content": "ROS 2 (Robot Operating System 2) is a robotics middleware framework.",
            "metadata": {"chapter": "test", "section": "test"}
        }]
        response = await gemini_service.generate_response(
            question="What is ROS2?",
            context_chunks=context_chunks,
            conversation_history=[]
        )
        print(f"[PASS] Gemini generation successful")
        print(f"  Response preview: {response[:100]}...")
        return True
    except Exception as e:
        print(f"[FAIL] Gemini generation failed: {e}")
        traceback.print_exc()
        return False

async def test_rag_pipeline():
    """Test full RAG pipeline"""
    print("\n=== Testing Full RAG Pipeline ===")
    try:
        async with AsyncSessionLocal() as db:
            result = await rag_service.process_question(
                question="What is ROS2?",
                session_id=None,
                conversation_history=[],
                db=db
            )
            print("[PASS] RAG pipeline successful")
            print(f"  Response: {result['response'][:150]}...")
            print(f"  Citations: {len(result['citations'])}")
            print(f"  Off-topic: {result.get('is_off_topic', False)}")
            return True
    except Exception as e:
        print(f"[FAIL] RAG pipeline failed: {e}")
        traceback.print_exc()
        return False

async def main():
    """Run all diagnostic tests"""
    print("=" * 60)
    print("CHAT ENDPOINT DIAGNOSTIC TESTS")
    print("=" * 60)

    # Test 1: Database
    db_ok = await test_database()

    # Test 2: Qdrant (may be slow due to embedding generation)
    print("\n[INFO] This may take 10-30 seconds due to Cohere API embedding generation...")
    qdrant_ok = await test_qdrant()

    # Test 3: Gemini
    gemini_ok = await test_gemini()

    # Test 4: Full RAG pipeline
    if db_ok and qdrant_ok and gemini_ok:
        print("\n[INFO] Testing full pipeline (may take 30-60 seconds)...")
        rag_ok = await test_rag_pipeline()
    else:
        print("\n[WARN] Skipping full RAG test due to component failures")
        rag_ok = False

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Database:     {'[PASS]' if db_ok else '[FAIL]'}")
    print(f"Qdrant:       {'[PASS]' if qdrant_ok else '[FAIL]'}")
    print(f"Gemini:       {'[PASS]' if gemini_ok else '[FAIL]'}")
    print(f"RAG Pipeline: {'[PASS]' if rag_ok else '[FAIL]'}")

    if not all([db_ok, qdrant_ok, gemini_ok, rag_ok]):
        print("\n[FAIL] FAILURES DETECTED - Review errors above")
        sys.exit(1)
    else:
        print("\n[PASS] ALL TESTS PASSED")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
