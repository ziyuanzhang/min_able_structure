import json
from fastapi import APIRouter,Request,Depends,HTTPException
from infra.db import conn
from agent.runtime.supervisor_runner import build_supervisor
from infra.middleware.rbac import require_role
from infra.delete_state import delete_state_by_id
from pydantic import BaseModel

supervisor = build_supervisor()

router = APIRouter()

@router.get("/pending",dependencies=[Depends(require_role(["admin","operator"]))])
def pending(request:Request):
    # require_role("admin","operator")(request)
    rows = conn.execute("SELECT request_id, state FROM agent_state WHERE status='waiting'").fetchall()
    return {
        "code":"200",
        "data": [{**dict(row), "state": json.loads(row["state"])} for row in rows],
        "msg": "Success",
    }

# 1. 定义请求体模型（推荐），比用 dict 更安全、文档更清晰
class HumanActionBody(BaseModel):
    action: str
    input: str = ""
@router.post("/human/{request_id}")
async def human_action(request_id:str,body:dict):
    """
    Human resume an agent run
    """
    row = conn.execute(
        "SELECT state FROM agent_state WHERE request_id=?",
        (request_id,)
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Task not found or already processed")
    try:
        state = json.loads(row["state"])
        state["human_action"] = body["action"]
        state["human_input"] = body.get("input","")

        result = await supervisor.ainvoke(state)
        delete_state_by_id(request_id)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Stored state is corrupted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))