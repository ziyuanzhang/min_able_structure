from typing import TypedDict,Callable, Optional, Any

class AgentState(TypedDict):
    """
    The state of an agent.
    """
    query:str
    role:str
    rag_calls:int
    need_rag:bool
    answer:str
    context:str
    _run:Callable[..., Any]  # 接受任意参数，返回任意类型
