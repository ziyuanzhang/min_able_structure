from agent.graphs.supervisor import build_supervisor

supervisor = build_supervisor()

async def run_supervisor(text:str,tenant_id:str):
    state = {
                "input":text,
                "tenant_id":tenant_id,
                "retry_count": 0,
                "max_retry": 2
             }
    return await supervisor.ainvoke(state)