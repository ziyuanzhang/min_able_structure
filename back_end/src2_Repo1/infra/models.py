# Event 表
from infra.db import conn

def init_db():
    conn.execute("""
    CREATE TABLE IF NOT EXISTS agent_event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id TEXT,
        node TEXT,
        input_data TEXT,
        output_data TEXT,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()