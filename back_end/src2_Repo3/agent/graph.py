from langgraph.graph import  StateGraph,END
from agent.state import AgentState
from agent.nodes import policy,planner,tool,final

def build_graph():
    g = StateGraph(AgentState)

    g.add_node("policy",policy)
    g.add_node("planner",planner)
    g.add_node("tool",tool)
    g.add_node("final",final)

    g.set_entry_point("policy")
    g.add_edge("policy", "planner")
    g.add_edge("planner", "tool")
    g.add_edge("tool", "final")
    g.add_edge("final", END)

    return  g.compile()