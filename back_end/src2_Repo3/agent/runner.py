from agent.graph import build_graph

graph = build_graph()

async def run_agent(text:str):
    state = {"input":text}
    result = await graph.ainvoke(state)
    return result['result']