# Event 表
from infra.db import conn

def init_db():
    conn.execute("""
    CREATE TABLE IF NOT EXISTS agent_event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id TEXT,
        node TEXT,
        status TEXT CHECK(status IN ('start', 'success', 'error', 'skipped')) DEFAULT 'start',
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
    # =========计费 & 账单 UI（Usage / Token / Agent 分钟）=================
    # Usage 明细表（最重要）
    conn.execute("""
    CREATE TABLE IF NOT EXISTS usage_event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id TEXT NOT NULL,
        request_id TEXT,
        user_id TEXT,
        agent_run INTEGER NOT NULL CHECK(agent_run IN (0,1)),  -- SQLite 无 BOOLEAN
        prompt_tokens INTEGER NOT NULL DEFAULT 0,
        completion_tokens INTEGER NOT NULL DEFAULT 0,
        agent_duration_ms INTEGER NOT NULL DEFAULT 0,
        created_at DATETIME DEFAULT (datetime('now'))
    );
    """)
    # 月度汇总表（账单快）
    conn.execute("""
    CREATE TABLE IF NOT EXISTS usage_monthly (
        tenant_id TEXT,
        month TEXT, -- 2025-12
        agent_runs INTEGER,
        prompt_tokens INTEGER,
        completion_tokens INTEGER,
        agent_minutes FLOAT,
        cost FLOAT,
        PRIMARY KEY (tenant_id, month)
    );
    """)
    # Pricing 表（可配置）
    conn.execute("""
    CREATE TABLE IF NOT EXISTS pricing (
        tenant_id TEXT PRIMARY KEY, 
        price_per_run FLOAT,
        price_per_1k_prompt FLOAT,
        price_per_1k_completion FLOAT,
        price_per_agent_minute FLOAT
    );
    """)
    # 插入一些测试数据
    # conn.execute("DELETE FROM usage_event")
    # conn.execute("""
    # INSERT INTO usage_event (tenant_id, created_at, prompt_tokens, completion_tokens, agent_duration_ms, agent_run)
    # VALUES ('qwert', '2025-05-01 10:00:00', 1000, 500, 60000, 1)
    # """) # 1分钟
    # conn.execute("""
    # INSERT INTO usage_event (tenant_id, created_at, prompt_tokens, completion_tokens, agent_duration_ms, agent_run)
    # VALUES ('qwert', '2025-05-02 11:00:00', 2000, 500, 120000, 1)
    # """) # 2分钟

    # ============== Prompt / Policy 管理台 =======================================================================
    conn.execute("""
    CREATE TABLE IF NOT EXISTS prompt_template (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        content TEXT NOT NULL,   -- prompt 内容
        variables TEXT,          -- 存 JSON 字符串（用 json.dumps() 写入）
        version INTEGER NOT NULL DEFAULT 1,
        status TEXT NOT NULL DEFAULT 'active',   -- draft / active / archived
        created_by TEXT NOT NULL,
        created_at DATETIME DEFAULT (datetime('now'))
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS policy (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('input', 'output', 'tool', 'cost', 'safety')),  -- input / output / tool / cost / safety
        rule TEXT NOT NULL,      -- 存 JSON 字符串
        action TEXT NOT NULL CHECK(action IN ('block', 'warn', 'retry', 'escalate')),
        enabled INTEGER NOT NULL DEFAULT 1,  -- SQLite 用 1/0 表示布尔值
        created_at DATETIME DEFAULT (datetime('now'))
    );
    """)
    # ALTER TABLE agent_event ADD COLUMN prompt_version INTEGER;
    # ALTER TABLE agent_event ADD COLUMN policy_snapshot JSON;

    # =========Graph 可视化（DAG Viewer）=====================================
    # conn.execute("ALTER TABLE agent_event ADD COLUMN status TEXT CHECK(status IN ('start', 'success', 'error', 'skipped'));")
    conn.commit()