from fastmcp import FastMCP 

from augury.mcp.tools import search_docs

mcp = FastMCP("augury")

mcp.tool(search_docs)

if __name__ == "__main__":
    mcp.run()