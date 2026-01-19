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

    # HITL
    need_human: bool
    human_action: str  # approve / reject / edit
    human_input: str  # 人工修正内容
    status: str  # running / waiting / done

