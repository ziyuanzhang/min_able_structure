from langgraph.graph import StateGraph,END

def build_qa_graph():
    def qa_node(state):
        state["result"] =f"[QAAgent]问题:{state['input']}"
        return state

    g = StateGraph(dict)
    g.add_node("qa",qa_node)
    g.set_entry_point("qa")
    g.add_edge("qa",END)
    return  g.compile()

