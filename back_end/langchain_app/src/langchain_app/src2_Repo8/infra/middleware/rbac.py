from fastapi import Request, HTTPException, status

def require_role(allowed_roles: list):
    def dependency(request: Request):
        # 1. 安全获取 role
        # 如果中间件没跑，或者中间件没设置 role，这里的 user_role 就是 None
        user_role = getattr(request.state, "role", None)

        # 2. 如果没有角色信息 -> 报 401 未认证
        if user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required (Role not found)"
            )
        # 3. 如果有角色但不在允许列表中 -> 报 403 禁止访问
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return user_role  # 可以选择返回角色，以便在视图函数里使用

        # if not hasattr(request.state,"role"):
        #     raise Exception("Role not found")
        # if not request.state.role in allowed_roles:
        #     raise Exception("Permission denied")
    return  dependency