from fastapi import APIRouter,Request
from infra.db import conn

router = APIRouter()

@router.get("/summary")
def billing_summary(request: Request):
    """
    Get summary of all agents
    """
    rows = conn.execute("""
      SELECT * FROM usage_monthly
      WHERE tenant_id=?
      ORDER BY month DESC
      LIMIT 6
    """,(request.state.tenant_id,)).fetchall()

    if not rows:
        return {
            "code": "200",
            "data": [],
            "msg": "Success",
        }

    return {
        "code": "200",
        "data": [dict(r) for r in rows],
        "msg": "Success",
    }

@router.get("/events")
def billing_events(request: Request):
    """
    Get events of all agents
    """
    rows = conn.execute("""
      SELECT * FROM usage_event
      WHERE tenant_id=?
      ORDER BY created_at DESC
      LIMIT 100
    """,(request.state.tenant_id,)).fetchall()

    return {
        "code": "200",
        "data": [dict(r) for r in rows],
        "msg": "Success",
    }