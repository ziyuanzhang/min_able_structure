import json

from fastapi import APIRouter
from infra.db import conn
from agent.runtime.supervisor_runner import build_supervisor
supervisor = build_supervisor()

router = APIRouter()

@router.get("/pending")
def pending():
    rows = conn.execute("SELECT request_id, state FROM agent_state WHERE status='waiting'").fetchall()
    return [{**dict(row), "state": json.loads(row["state"])} for row in rows]

@router.post("/human/{request_id}")
async def human_action(request_id:str,body:dict):
    """
    Human resume an agent run
    """
    row = conn.execute(
        "SELECT state FROM agent_state WHERE request_id=?",
        (request_id,)
    ).fetchone()

    state = json.loads(row["state"])
    state["human_action"] = body["action"]
    state["human_input"] = body.get("input","")

    result = await supervisor.ainvoke(state)
    return result