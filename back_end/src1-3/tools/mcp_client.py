from policies.tool_policy import check_tool_policy
from fastmcp import Client
from get_env import MCP_ENDPOINT

async def call_tool(tool_name:str, state:dict, payload:dict):
    """    Call a tool.    """
    check_tool_policy(tool_name,state)
    client = Client(MCP_ENDPOINT)
    async with client:
        result = await client.call_tool(tool_name,payload)
    return result