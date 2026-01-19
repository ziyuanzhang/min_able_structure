from tools.mcp_client import search_tool

def policy(state):
    return state

def planner(state):
    state["plan"] = f"search:{state['input']}"
    return state

async def tool(state):
    state["tool_result"] = await search_tool(state['input'])
    return state

def final(state):
    state["result"] = f'Answer: {state["tool_result"]}'
    return state