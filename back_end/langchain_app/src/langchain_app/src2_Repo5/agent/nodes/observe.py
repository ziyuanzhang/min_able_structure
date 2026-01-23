
from agent.runtime.tracer import trace_node

@trace_node("observe")
def observe(state):
    result =state.get("result","")
    state["observation"] ={
        "length":len(result),
        "has_answer":bool(result)
    }