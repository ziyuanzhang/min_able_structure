from fastmcp import Client
from get_env import  MCP_ENDPOINT

client = Client(MCP_ENDPOINT)
async def search_tool(q:str):
    async with client:
        return await client.call_tool("search",{"query":q})



