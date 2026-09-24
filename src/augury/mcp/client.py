from pathlib import Path
from fastmcp import Client
from pprint import pprint
import asyncio

server = Path("src/augury/mcp/server.py")

client = Client(server)

async def main():
    async with client:
        # await client.ping()
        pprint("pinned")

        tools = await client.list_tools()
        # pprint(tools)

        response = await client.call_tool("search_docs", { "query": "what is ardupilot"})
        pprint(response.structured_content)
if __name__ == "__main__":
    asyncio.run(main())
    
