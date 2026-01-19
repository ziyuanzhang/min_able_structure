from tools.mcp_client import call_tool

async  def rag_search(query:str, state:dict) -> str:
    state["rag_calls"] += 1
    result = await call_tool(tool_name="ragflow.search",state=state,payload={"query":query,"top_k":5})
    # return result["content"]
    print("rag_search:",result)
    return result.content