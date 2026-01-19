from langgraph.graph import StateGraph,END,START
from agents.state import AgentState
from tools.ragflow_tool import rag_search
from models.llm import generate
from storage.audit_writer import record_event

# 辅助函数：清洗数据，防止循环引用
def safe_dict(d: dict) -> dict:
    """创建字典的浅拷贝并移除 _run 键"""
    new_d = d.copy()
    if "_run" in new_d:
        del new_d["_run"]
    return new_d

def audited(node_name,fn):
    async def wrapper(state):
        # 1. 获取 run 对象用于记录
        current_run = state.get("_run")
        # 2. 这里的 before 是要做日志记录的，必须剔除 _run 防止死循环
        safe_before = safe_dict(state)

        # before = dict(state)
        result = await fn(state)
        # 4. 这里的 result 也可能是 state，也需要剔除 _run
        # 注意：如果 result 是 state 字典，我们也需要清洗它
        safe_result = safe_dict(result) if isinstance(result, dict) else result
        if current_run:
            record_event(
                current_run,
                node=node_name,
                input_data=safe_before,
                output_data=safe_result
            )
        # result = dict(result)
        # record_event(state["_run"],node = node_name,input_data = before,output_data = result)
        return result
    return wrapper

async def decide(state:AgentState):
    state["need_rag"] = "什么" in state["query"]
    return state

async def call_rag(state:AgentState):
   docs = await rag_search(state["query"], state)
   state["context"] = docs
   return state

async def final_answer(state:AgentState):
    prompt = state["query"]
    if state.get("context"):
        prompt += f"\n\n参考资料：{state['context']}"
    state["answer"] = generate(prompt)
    return state

def route(state:AgentState):
    if state["need_rag"]:
        return "rag"
    else:
        return "final"

builder = StateGraph(AgentState)
builder.add_node("decide",audited("decide",decide))
builder.add_node("rag",audited("rag",call_rag))
builder.add_node("final",audited("final",final_answer))

builder.add_conditional_edges("decide",route,{
    "rag":"rag",
    "final":"final"
})

builder.add_edge(START,"decide")
builder.add_edge("rag","final")
builder.add_edge("final",END)

agent_graph = builder.compile()
