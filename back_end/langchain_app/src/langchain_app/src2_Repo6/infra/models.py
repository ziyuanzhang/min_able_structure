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
    conn.execute("""
    CREATE TABLE IF NOT EXISTS agent_state (
      request_id TEXT PRIMARY KEY,
      state TEXT,
      status TEXT,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tenant (
      id TEXT PRIMARY KEY,
      name TEXT,
      status TEXT
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS user (
      id TEXT PRIMARY KEY,
      tenant_id TEXT,
      name TEXT,
      role TEXT,
      FOREIGN KEY (tenant_id) REFERENCES tenant(id)
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS api_key (
      key TEXT PRIMARY KEY,
      tenant_id TEXT,
      user_id TEXT,
      enabled BOOLEAN
    );
    """)
    # Quota（配额）
    conn.execute("""
    CREATE TABLE IF NOT EXISTS quota (
      tenant_id TEXT PRIMARY KEY,
      max_requests INTEGER,
      used_requests INTEGER,
      reset_at DATETIME
    );
     """)

    conn.commit()