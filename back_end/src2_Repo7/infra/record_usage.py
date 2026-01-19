from infra.db import conn

def record_usage(
    tenant_id, request_id, user_id,
    prompt_tokens, completion_tokens, duration_ms
):
    conn.execute("""
      INSERT INTO usage_event
      (tenant_id, request_id, user_id,
       agent_run, prompt_tokens, completion_tokens, agent_duration_ms)
      VALUES (?, ?, ?, 1, ?, ?, ?)
    """, (
        tenant_id, request_id, user_id,
        prompt_tokens, completion_tokens, duration_ms
    ))
    conn.commit()
