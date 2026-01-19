from typing import TypedDict,List,Any

class AgentState(TypedDict):
    """
    The state of an agent.
    """
    input:str
    plan:str
    tool_result:str
    result:str

    # 新增
    route: str
    success: bool
    reason: str
    retry_count: int
    max_retry: int

