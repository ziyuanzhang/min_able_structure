from fastapi import APIRouter,Request
from infra.db import conn
import json

router = APIRouter()

@router.get("/run/{request_id}")
async def run(request: Request, request_id: str):
    rows = conn.execute("""
            SELECT request_id,node,status,id
            FROM agent_event
            WHERE request_id=?
        """, (request_id,)).fetchall()
    return {
        "code": "200",
        "data": [row for row in rows],
        "msg": "Success",
    }