from infra.db import conn
import json

def save_state(request_id,state):
    conn.execute(
        "REPLACE INTO agent_state (request_id, state, status)  VALUES (?, ?, ?)",
        (request_id, json.dumps(state), state["status"])
    )
    conn.commit()