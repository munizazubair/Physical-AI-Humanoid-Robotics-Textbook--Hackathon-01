#!/usr/bin/env python3
"""
Textbook Embedding Generation Script with Cohere API
Generates embeddings for Physical AI textbook and uploads to Qdrant
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Generate and upload textbook embeddings to Qdrant using Cohere API"""

    print("="*60)
    print("Textbook Embedding Generation with Cohere API")
    print("="*60)

    # Check required environment variables
    required_vars = ['QDRANT_URL', 'QDRANT_API_KEY', 'COHERE_API_KEY']
    missing = [v for v in required_vars if not os.getenv(v)]

    if missing:
        print(f"\n[FAIL] Missing environment variables: {', '.join(missing)}")
        print("\nRequired environment variables:")
        print("  - QDRANT_URL: Your Qdrant Cloud URL")
        print("  - QDRANT_API_KEY: Your Qdrant API key")
        print("  - COHERE_API_KEY: Your Cohere API key")
        print("\nAdd these to backend/.env file")
        return 1

    try:
        import cohere
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams, PointStruct
        import hashlib

        print("\n[*] Initializing Cohere client...")
        # Initialize Cohere client
        co = cohere.Client(os.getenv('COHERE_API_KEY'))

        # Get embedding dimension from Cohere
        # Using embed-english-v3.0 model (1024 dimensions)
        vector_size = 1024
        print(f"[OK] Cohere client initialized (model: embed-english-v3.0, vector size: {vector_size})")

        print("\n[*] Connecting to Qdrant...")
        client = QdrantClient(
            url=os.getenv('QDRANT_URL'),
            api_key=os.getenv('QDRANT_API_KEY')
        )
        print("[OK] Connected to Qdrant")

        # Create collection
        collection_name = "textbook_embeddings"
        print(f"\n[*] Creating collection: {collection_name}")

        try:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            print(f"[OK] Collection created")
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"[NOTE] Collection already exists, will update it")
            else:
                raise

        # Find all markdown files in docs directory
        docs_dir = Path(__file__).parent.parent.parent / "docs"
        md_files = list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx"))

        if not md_files:
            print(f"\n[FAIL] No markdown files found in {docs_dir}")
            return 1

        print(f"\n[*] Found {len(md_files)} markdown/MDX files")

        # Process each file
        total_chunks = 0
        points = []
        texts_to_embed = []
        text_metadata = []

        for md_file in md_files:
            print(f"\n[*] Processing: {md_file.relative_to(docs_dir)}")

            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split into chunks (simple approach: by paragraphs)
            chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]

            # Filter out very short chunks
            chunks = [c for c in chunks if len(c) > 100]

            print(f"   Chunks: {len(chunks)}")

            # Extract metadata
            relative_path = md_file.relative_to(docs_dir)
            parts = relative_path.parts

            module = parts[0] if len(parts) > 0 else "unknown"
            chapter = parts[1] if len(parts) > 1 else md_file.stem

            # Collect chunks for batch embedding
            for idx, chunk in enumerate(chunks):
                # Generate unique ID
                chunk_id = hashlib.md5(f"{md_file}_{idx}".encode()).hexdigest()

                texts_to_embed.append(chunk)
                text_metadata.append({
                    "chunk_id": chunk_id,
                    "file_path": str(relative_path),
                    "module": module,
                    "chapter": chapter,
                    "chunk_index": idx,
                    "content": chunk
                })

                # Process in batches of 96 (Cohere's max batch size)
                if len(texts_to_embed) >= 96:
                    print(f"   Embedding batch of {len(texts_to_embed)} chunks...")

                    # Generate embeddings using Cohere
                    response = co.embed(
                        texts=texts_to_embed,
                        model="embed-english-v3.0",
                        input_type="search_document"
                    )

                    embeddings = response.embeddings

                    # Create points
                    for i, embedding in enumerate(embeddings):
                        metadata = text_metadata[i]
                        point = PointStruct(
                            id=metadata["chunk_id"],
                            vector=embedding,
                            payload={
                                "content": metadata["content"],
                                "file_path": metadata["file_path"],
                                "module": metadata["module"],
                                "chapter": metadata["chapter"],
                                "chunk_index": metadata["chunk_index"],
                                "content_type": "text"
                            }
                        )
                        points.append(point)

                    # Upload to Qdrant
                    client.upsert(collection_name=collection_name, points=points)
                    print(f"   Uploaded {len(points)} points to Qdrant")

                    total_chunks += len(points)

                    # Reset batches
                    texts_to_embed = []
                    text_metadata = []
                    points = []

        # Process remaining chunks
        if texts_to_embed:
            print(f"\n[*] Embedding final batch of {len(texts_to_embed)} chunks...")

            response = co.embed(
                texts=texts_to_embed,
                model="embed-english-v3.0",
                input_type="search_document"
            )

            embeddings = response.embeddings

            for i, embedding in enumerate(embeddings):
                metadata = text_metadata[i]
                point = PointStruct(
                    id=metadata["chunk_id"],
                    vector=embedding,
                    payload={
                        "content": metadata["content"],
                        "file_path": metadata["file_path"],
                        "module": metadata["module"],
                        "chapter": metadata["chapter"],
                        "chunk_index": metadata["chunk_index"],
                        "content_type": "text"
                    }
                )
                points.append(point)

            client.upsert(collection_name=collection_name, points=points)
            print(f"   Uploaded final {len(points)} points")
            total_chunks += len(points)

        print(f"\n[SUCCESS] Embedding generation complete!")
        print(f"   Total chunks: {total_chunks}")
        print(f"   Collection: {collection_name}")

        # Verify
        collection_info = client.get_collection(collection_name)
        print(f"\n[*] Verification:")
        print(f"   Points in Qdrant: {collection_info.points_count}")

        return 0

    except ImportError as e:
        print(f"\n[FAIL] Missing required package: {e}")
        print("\nInstall missing packages:")
        print("   pip install cohere qdrant-client")
        return 1
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
