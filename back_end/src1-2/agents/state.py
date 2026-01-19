from typing import TypedDict

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
