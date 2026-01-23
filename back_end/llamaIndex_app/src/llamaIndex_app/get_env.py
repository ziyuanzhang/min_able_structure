import os
from dotenv import load_dotenv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # langchain_app/
load_dotenv(ROOT / ".env")

class Settings:
    METAPHOR_API_KEY = os.getenv("METAPHOR_API_KEY")
    QDRANT_URL = "http://localhost:6333"
    COLLECTION_NAME = "python_faq_collection"  # Using a new collection for the Python data
    HOST = "127.0.0.1"
    PORT = 8080

setting = Settings()
