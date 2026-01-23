from fastmcp import FastMCP

mcp = FastMCP("search")
@mcp.tool()
def search(query: str) -> str:
    """Search for information using Google"""
    return f"[search result for '{query}']"

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=9000)