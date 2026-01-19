import os
from dotenv import load_dotenv
load_dotenv(override=True)  # 加载 .env 文件中的变量到 os.environ


RAGFLOW_API_KEY = os.environ.get("RAGFLOW_API_KEY")
RAGFLOW_URL = os.environ.get("RAGFLOW_URL")
RAGFLOW_KNOWLEDGE_BASE_ID = os.environ.get("RAGFLOW_KNOWLEDGE_BASE_ID")

MCP_ENDPOINT = os.environ.get("MCP_ENDPOINT")

AUDIT_FILE = os.environ.get("AUDIT_FILE")

DB_FILE = os.environ.get("DB_FILE")