from agent.graphs.supervisor import build_supervisor

supervisor = build_supervisor()

async def run_supervisor(text:str):
    state = {
                "input":text,
                 "retry_count": 0,
                 "max_retry": 2
             }
    result = await supervisor.ainvoke(state)
    return result['result']