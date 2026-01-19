from agent.graphs.supervisor import build_supervisor

supervisor = build_supervisor()

async def run_supervisor(text:str):
    state = {"input":text}
    result = await supervisor.ainvoke(state)
    return result['result']