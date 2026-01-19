from agent.runtime.tracer import trace_node

@trace_node("retry")
def retry_policy(state):
    state["retry_count"] +=1
    return  state