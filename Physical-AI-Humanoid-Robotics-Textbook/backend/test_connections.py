#!/usr/bin/env python3
"""
Connection Test Script for RAG Chatbot
Tests all external service connections and reports status
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_qdrant():
    """Test Qdrant Cloud connection"""
    print("\n[*] Testing Qdrant Cloud Connection...")
    try:
        from qdrant_client import QdrantClient

        client = QdrantClient(
            url=os.getenv('QDRANT_URL'),
            api_key=os.getenv('QDRANT_API_KEY')
        )

        # Get collections
        collections = client.get_collections()
        print(f"[OK] Qdrant connected successfully!")
        print(f"   URL: {os.getenv('QDRANT_URL')[:50]}...")
        print(f"   Collections: {len(collections.collections)}")

        if len(collections.collections) == 0:
            print("   [WARNING] No collections found in Qdrant")
            print("   [NOTE] You need to populate Qdrant with textbook embeddings")
            print("   [ACTION] Run: python scripts/generate_embeddings.py")
            return True  # Connection works, just empty

        for col in collections.collections:
            info = client.get_collection(col.name)
            print(f"   - Collection: {col.name}")
            print(f"     Points: {info.points_count}")
            print(f"     Vector size: {info.config.params.vectors.size}")

        return True

    except Exception as e:
        print(f"[FAIL] Qdrant connection failed: {e}")
        return False


def test_gemini():
    """Test Google Gemini API"""
    print("\n[*] Testing Google Gemini API...")
    try:
        import google.generativeai as genai

        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content("Say 'Hello' in one word")

        print(f"[OK] Gemini API connected successfully!")
        print(f"   Model: gemini-1.5-pro")
        print(f"   Test response: {response.text[:50]}")

        return True

    except Exception as e:
        print(f"[FAIL] Gemini API connection failed: {e}")
        return False


def test_neon():
    """Test Neon PostgreSQL connection"""
    print("\n[*] Testing Neon PostgreSQL Connection...")
    try:
        import asyncio
        from sqlalchemy.ext.asyncio import create_async_engine

        engine = create_async_engine(os.getenv('DATABASE_URL'))

        async def test_connection():
            from sqlalchemy import text
            async with engine.connect() as conn:
                result = await conn.execute(text("SELECT version()"))
                version = result.scalar()
            await engine.dispose()
            return version

        version = asyncio.run(test_connection())

        print(f"[OK] Neon PostgreSQL connected successfully!")
        print(f"   Database: {os.getenv('DATABASE_URL').split('@')[1].split('/')[1]}")
        print(f"   Version: PostgreSQL {version.split()[1]}")

        return True

    except Exception as e:
        print(f"[FAIL] Neon connection failed: {e}")
        return False


def test_huggingface():
    """Test Hugging Face token (optional)"""
    print("\n[*] Testing Hugging Face Token...")

    hf_token = os.getenv('HF_TOKEN')
    if not hf_token or hf_token == 'your_hf_token_here':
        print("[SKIP] Hugging Face token not configured (optional)")
        return True

    try:
        from huggingface_hub import HfApi

        api = HfApi(token=hf_token)
        user = api.whoami()

        print(f"[OK] Hugging Face authenticated!")
        print(f"   User: {user.get('name', 'Unknown')}")

        return True

    except Exception as e:
        print(f"[WARN] Hugging Face token validation failed: {e}")
        print("   (This is optional for the RAG chatbot)")
        return True  # Non-critical


def main():
    """Run all connection tests"""
    print("=" * 60)
    print("RAG Chatbot Connection Test")
    print("=" * 60)

    # Check environment variables
    required_vars = ['GEMINI_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY', 'DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"\n[FAIL] Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n[NOTE] Make sure backend/.env file exists and contains all credentials")
        sys.exit(1)

    print("\n[OK] All required environment variables found")

    # Run tests
    results = {
        'Qdrant': test_qdrant(),
        'Gemini': test_gemini(),
        'Neon': test_neon(),
        'HuggingFace': test_huggingface()
    }

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for service, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{service:20} {status}")

    all_critical_passed = results['Qdrant'] and results['Gemini'] and results['Neon']

    if all_critical_passed:
        print("\n[SUCCESS] All critical services connected successfully!")
        print("\nNext steps:")

        if not results.get('Qdrant', False):
            print("   1. Populate Qdrant with textbook embeddings")
            print("      Run: python scripts/generate_embeddings.py")

        print("   2. Run database migrations:")
        print("      cd backend && alembic upgrade head")
        print("   3. Start the backend server:")
        print("      uvicorn main:app --reload")

        return 0
    else:
        print("\n[FAIL] Some critical services failed to connect")
        print("   Please check your credentials in backend/.env")
        return 1


if __name__ == "__main__":
    sys.exit(main())
