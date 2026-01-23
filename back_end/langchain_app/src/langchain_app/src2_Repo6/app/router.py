from fastapi import APIRouter,Request

from agent.runtime.supervisor_runner import run_supervisor
from infra.check_quota import check_quota
from infra.consume_quota import consume_quota
from infra.db import conn
import json

router = APIRouter()

@router.post("/run")
async def run (request:Request,bode:dict):
    # tenant_id = request.state.get("tenant_id")
    tenant_id = getattr(request.state, "tenant_id", None)

    check_quota(tenant_id)
    result =  await run_supervisor(bode["input"],tenant_id=tenant_id)
    consume_quota(tenant_id)

    return {
         "code":"200",
         "data": result,
         "msg": "Success",
     }

@router.get("/run/{request_id}")
async def run(request: Request, request_id: str):
    rows = conn.execute("""
        SELECT request_id,node,output_data,id
        FROM agent_event
        WHERE request_id=?
    """,(request_id,)).fetchall()
    return {
        "code": "200",
        "data": [{**dict(row), "output_data": json.loads(row["output_data"])} for row in rows],
        "msg": "Success",
    }

@router.get("/runs")
def runs(request: Request):
    rows = conn.execute("""
      SELECT request_id, MAX(ts) as ts
      FROM agent_event
      WHERE tenant_id=?
      GROUP BY request_id
      ORDER BY ts DESC
      LIMIT 50
    """, (request.state.tenant_id,)).fetchall()

    return {
        "code": "200",
        "data": [dict(r) for r in rows],
        "msg": "Success",
    }