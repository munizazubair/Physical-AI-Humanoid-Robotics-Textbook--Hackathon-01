# Add this after line 78 (before embedding generation)
import time
start_time = time.time()

# Add this after line 90 (after embedding generation)
elapsed = time.time() - start_time
logger.info(f"Cohere embedding generated in {elapsed:.2f}s")
