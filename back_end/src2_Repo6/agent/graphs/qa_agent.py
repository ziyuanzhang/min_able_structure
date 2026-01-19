from langgraph.graph import StateGraph,END
from agent.runtime.tracer import trace_node

def build_qa_graph():
    @trace_node("qa_node")
    def qa_node(state):
        state["result"] =f"[QAAgent]问题:{state['input']}"
        return state

    g = StateGraph(dict)
    g.add_node("qa",qa_node)
    g.set_entry_point("qa")
    g.add_edge("qa",END)
    return  g.compile()

