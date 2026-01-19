from typing import TypedDict,List,Any
from datetime import datetime

class AuditEvent(TypedDict):
    """    Audit event.    """
    ts: str
    node:str
    input:Any
    output:Any

class AgentRun(TypedDict):
    """    Agent run.    """
    run_id:str
    query:str
    role:str
    events: List[AuditEvent]