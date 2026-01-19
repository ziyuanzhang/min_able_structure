from typing import TypedDict,List,Any

class AgentState(TypedDict):
    """
    The state of an agent.
    """
    input:str
    plan:str
    tool_result:str
    result:str