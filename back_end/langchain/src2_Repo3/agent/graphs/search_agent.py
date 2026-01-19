from langgraph.graph import StateGraph,END

def build_search_graph():
    def search_node(state):
        state["result"] =f"[SearchAgent]搜索:{state['input']}"
        return state

    g = StateGraph(dict)
    g.add_node("search",search_node)
    g.set_entry_point("search")
    g.add_edge("search",END)
    return g.compile()