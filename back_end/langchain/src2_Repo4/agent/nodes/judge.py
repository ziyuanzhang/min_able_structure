
from agent.runtime.tracer import trace_node

@trace_node("judge")
def judge(state):
    obs = state["observation"]

    if not obs["has_answer"]:
        state["success"] = False
        state["reason"] = "empty_result"
    elif obs["length"] <10:
        state["success"] = False
        state["reason"] = "too_short"
    else:
        state["success"] = True
        state["reason"] = "ok"
    return state