
from agent.runtime.tracer import trace_node

@trace_node("judge")
def judge(state):
    obs = state["observation"]
    print('state:', type(state), dict(state))

    if state.get("human_action") == "approve":
        state["need_human"] =False
        state["success"] = True
        state["reason"] = "approved"
        state["status"] = "done"
    elif state.get("human_action") == "reject":
        state["need_human"] = False
        state["success"] = False
        state["reason"] = "rejected"
        state["status"] = "done"
    else:
        if not obs["has_answer"]:
            state["success"] = False
            state["reason"] = "empty_result"
        elif obs["length"] <100:
            state["success"] = False
            state["reason"] = "too_short"
        else:
            state["success"] = True
            state["reason"] = "ok"

        # 🔥 HITL 触发条件
        if not state["success"] and state["retry_count"] >= state["max_retry"]:
            state["need_human"] = True
            state["status"] = "waiting"
        else:
            state["need_human"] = False

    return state
