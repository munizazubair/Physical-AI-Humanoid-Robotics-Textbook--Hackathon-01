import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_API_KEY')

print(f"Qdrant URL: {qdrant_url}")
print(f"API Key (first 10 chars): {qdrant_api_key[:10] if qdrant_api_key else 'NOT FOUND'}")

try:
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    # Test connection
    collections = client.get_collections()
    print(f"\n✅ Successfully connected to Qdrant!")
    print(f"Collections: {[c.name for c in collections.collections]}")

    # Check textbook_embeddings collection
    collection_info = client.get_collection("textbook_embeddings")
    print(f"\n✅ textbook_embeddings collection found!")
    print(f"   Points: {collection_info.points_count}")
    print(f"   Vectors: {collection_info.vectors_count}")

    # Test search
    test_vector = [0.1] * 1024  # Dummy vector for testing
    results = client.search(
        collection_name="textbook_embeddings",
        query_vector=test_vector,
        limit=1
    )
    print(f"\n✅ Search test successful! Found {len(results)} results")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
