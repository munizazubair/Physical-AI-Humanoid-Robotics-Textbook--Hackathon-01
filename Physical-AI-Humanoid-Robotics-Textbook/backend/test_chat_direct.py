"""
Direct test of chat endpoint to see real errors
"""
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat():
    response = client.post(
        "/api/chat",
        json={"question": "What is ROS2?"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code != 200:
        print(f"Headers: {response.headers}")

if __name__ == "__main__":
    test_chat()
