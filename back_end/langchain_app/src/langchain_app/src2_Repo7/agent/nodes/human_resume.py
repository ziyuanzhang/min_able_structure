from agent.runtime.tracer import trace_node

@trace_node("human_resume")
def human_resume(state):
    action = state.get("human_action")

    if action == "approve":
        state["status"] = "done"
        state["success"] = True
    elif action == "edit":
        state["input"] = state.get("human_input")
        state["retry_count"] = 0
        state["need_human"] = False
        state["status"] = "running"
    elif action == "reject":
        state["status"] = "done"
        state["result"] = "人工终止"

    return  state