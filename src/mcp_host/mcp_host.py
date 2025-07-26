import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import litellm
from litellm.experimental_mcp_client import load_mcp_tools

mcp_server_url = "http://localhost:8000/mcp"

async def main():
    async with streamablehttp_client(f"{mcp_server_url}") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()
            
            tools = await load_mcp_tools(session=session, format="openai")
            print("MCP Tools:", tools)

            messages = [{'role': 'user', 'content': 'What is 2 + 3?'}]
            llm_response = await litellm.acompletion(
                model="gpt-4.1-mini",
                messages=messages,
                tools=tools
            )

            print("llm_response:", json.dumps(llm_response, indent=2, default=str))


            
            

if __name__ == "__main__":
    print("Connecting to MCP server...")
    asyncio.run(main())
    print("Connection closed.")