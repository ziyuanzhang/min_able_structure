from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from infra.db import conn

async def auth_middleware(request: Request, call_next):
    """
    认证中间件
    """
    # print("auth-request:",request)
    # 1. 白名单机制：允许访问文档和 openapi，不需要 API Key
    if request.url.path in ["/docs", "/openapi.json", "/favicon.ico"]:
        return await call_next(request)
    # 2. 获取 Header
    api_key = request.headers.get("x-api-key")
    # print("api_key:",type(api_key),api_key)

    # 3. 校验失败直接返回 JSONResponse，而不是 raise Exception
    if not api_key:
        # raise HTTPException(status_code=401, detail="Missing API key")
        return JSONResponse(status_code=401, content={"detail": "Missing API key"})

    # 4. 查询数据库 (注意：conn 应该是线程安全的，或者在这里创建新的 cursor)
    # 假设你在 infra.db 里设置了 conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            "SELECT tenant_id, user_id FROM api_key WHERE key=? AND enabled=1",
            (api_key,)
        ).fetchone()
    except Exception as e:
        print(f"DB Error: {e}")
        return JSONResponse(status_code=500, content={"detail": "Database error"})

    # print("auth-row:",row)
    if not row:
       # raise HTTPException(status_code=403, detail="Invalid API key")
       return JSONResponse(status_code=403, content={"detail": "Invalid API key"})

    try:
        arr = conn.execute(
            "SELECT role FROM user WHERE tenant_id=?",
            (row["tenant_id"],)
        ).fetchone()
    except Exception as e:
        print(f"DB Error: {e}")
        return JSONResponse(status_code=500, content={"detail": "Database error"})
    print("auth-arr:",arr)
    if not arr:
        return JSONResponse(status_code=403, content={"detail": "用户不存在"})
    # 5. 赋值给 state (前提是 row 是支持字典访问的对象)
    request.state.tenant_id = row["tenant_id"]
    request.state.user_id = row["user_id"]
    request.state.role = arr["role"]



    return  await call_next(request)