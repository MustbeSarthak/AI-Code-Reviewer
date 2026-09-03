import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def call_mcp_tool(tool_name: str, arguments: dict):
    server_params = StdioServerParameters(
        # Launch with the same interpreter that started the app. A bare
        # ``python`` can point to a global interpreter where this package and
        # its dependencies have not been installed.
        command=sys.executable,
        args=["-m", "code_reviewer.mcp.server"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                tool_name,
                arguments
            )
            return result
