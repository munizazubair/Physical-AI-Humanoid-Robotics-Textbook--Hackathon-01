import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_rag():
    print("Testing RAG Pipeline...")

    try:
        # Test 1: Import services
        print("\n1. Importing services...")
        from services.rag_service import rag_service
        print("   OK - Services imported")

        # Test 2: Process a simple question
        print("\n2. Processing test question...")
        from database import AsyncSessionLocal

        async with AsyncSessionLocal() as db:
            result = await rag_service.process_question(
                question="What is ROS2?",
                session_id=None,
                conversation_history=[],
                db=db
            )

            print(f"   OK - Got response: {result['response'][:100]}...")
            print(f"   Citations: {len(result['citations'])}")

        print("\nSUCCESS - RAG pipeline working!")

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_rag())
