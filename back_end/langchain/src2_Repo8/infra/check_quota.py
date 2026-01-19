from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from infra.db import conn

def check_quota(tenant_id):
    row = conn.execute(
        "SELECT max_requests, used_requests FROM quota WHERE tenant_id=?",
        (tenant_id,)
    ).fetchone()

    if row["used_requests"] >=row["max_requests"]:
        raise HTTPException(status_code=403, detail="请求次数用完")