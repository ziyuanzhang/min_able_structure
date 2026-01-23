import os
from dotenv import load_dotenv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # langchain_app/

load_dotenv(ROOT / ".env")

class Get_env:
    RAGFLOW_API_KEY = os.environ.get("RAGFLOW_API_KEY")
    RAGFLOW_URL = os.environ.get("RAGFLOW_URL")
    RAGFLOW_KNOWLEDGE_BASE_ID = os.environ.get("RAGFLOW_KNOWLEDGE_BASE_ID")

    MCP_ENDPOINT = os.environ.get("MCP_ENDPOINT")

    AUDIT_FILE = os.environ.get("AUDIT_FILE")

    DB_FILE = os.environ.get("DB_FILE")

get_env = Get_env()