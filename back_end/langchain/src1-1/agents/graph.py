from langgraph.graph import StateGraph,END,START
from agents.state import AgentState
from tools.rag_tool import rag_search
from policies.tool_policy import allow_rag

def decide(state:AgentState):
    state["need_rag"] = "什么" in state["query"]
    return state

def call_rag(state:AgentState):
    state["rag_calls"] +=1
    docs = rag_search(state["query"])
    state["answer"] = f"【来自RAG】{docs}"
    return state

def final_answer(state:AgentState):
    if not state.get("answer"):
        state["answer"] = f"【直接回答】{state['query']}"
    return state

def route(state:AgentState):
    if state["need_rag"] and allow_rag(state):
        return "rag"
    else:
        return "final"

builder = StateGraph(AgentState)
builder.add_edge(START,"decide")
builder.add_node("decide",decide)
builder.add_node("rag",call_rag)
builder.add_node("final",final_answer)

builder.add_conditional_edges("decide",route,{
    "rag":"rag",
    "final":"final"
})

builder.add_edge("rag","final")
builder.add_edge("final",END)

agent_graph = builder.compile()
# if __name__ == "__main__":
#     print(agent_graph.get_graph(xray=True).draw_mermaid_png())
