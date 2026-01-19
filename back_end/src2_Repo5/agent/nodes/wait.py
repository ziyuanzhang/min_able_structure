from infra.save_state import save_state
from agent.runtime.tracer import trace_node

@trace_node("wait")
def wait(state):
    state["status"] = "waiting"
    save_state(state.get("request_id"),state)
    return state