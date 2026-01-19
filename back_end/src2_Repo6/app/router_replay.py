from fastapi import APIRouter
from infra.db import conn
import json
from agent.graphs.graph import build_graph

graph = build_graph()
router = APIRouter()


@router.post("/replay/{request_id}")
async def replay (request_id:str):
    """
    Replay an agent run
    """
    row = conn.execute(
        "SELECT input_data FROM agent_event WHERE request_id=? AND input_data IS NOT NULL ORDER BY id ASC LIMIT 1",
        (request_id,)
    ).fetchone()
    if not row:
        return {"error":"request_id not found"}
    print("row:",dict(row))
    state = json.loads(row["input_data"])
    print("state:",state)
    result  = await graph.ainvoke(state)
    return {
        "replay_result":result,
        "request_id":request_id
    }