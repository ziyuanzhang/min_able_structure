from tools.mcp_client import search_tool
from agent.runtime.tracer import trace_node

@trace_node("policy")
def policy(state):
    return state

@trace_node("planner")
def planner(state):
    state["plan"] = f"search:{state['input']}"
    return state

@trace_node("tool")
async def tool(state):
    state["tool_result"] = await search_tool(state['input'])
    return state

@trace_node("final")
def final(state):
    state["result"] = f'Answer: {state["tool_result"]}'
    return state