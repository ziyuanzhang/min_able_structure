from langgraph.graph import StateGraph,END,START
from agents.state import AgentState
from tools.ragflow_tool import rag_search
from models.llm import generate

async def decide(state:AgentState):
    state["need_rag"] = "什么" in state["query"]
    return state

async def call_rag(state:AgentState):
   docs = await rag_search(state["query"], state)
   state["context"] = docs
   print("call_rag:",state)
   return state

async def final_answer(state:AgentState):
    print("final_answer:",state)
    prompt = state["query"]
    if state.get("context"):
        print("=========================================")
        prompt += f"\n\n参考资料：{state['context']}"
    state["answer"] = generate(prompt)
    return state

def route(state:AgentState):
    if state["need_rag"]:
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
