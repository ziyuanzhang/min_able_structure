def allow_rag(state) -> bool:

    # 最简单的策略：每次最多 1 次
    return  state['rag_calls']<1

# ==============================================================================
TOOL_POLICIES={
    "ragflow.search":{
        "max_calls":2,
        "roles":["user","admin"]
    }
}
def check_tool_policy(tool_name:str,state:dict):
    policy = TOOL_POLICIES.get(tool_name)
    if not policy:
        raise RuntimeError(f"No policy for tool{tool_name}")
    if state["role"] not in policy["roles"]:
        raise RuntimeError(f"Role {state['role']} not allowed to use tool {tool_name}")
    if state["rag_calls"]>=policy["max_calls"]:
        raise RuntimeError(f"Max calls exceeded for tool {tool_name}")