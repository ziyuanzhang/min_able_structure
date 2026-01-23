import os
from dotenv import load_dotenv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # langchain_app/
load_dotenv(ROOT / ".env")
class Settings:
    METAPHOR_API_KEY = os.getenv("METAPHOR_API_KEY")

setting = Settings();
