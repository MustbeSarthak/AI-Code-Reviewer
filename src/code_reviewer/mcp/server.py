from mcp.server.mcpserver import MCPServer
from .tools import list_files, write_file, read_file

mcp = MCPServer("code-reviewer")
mcp.tool()(list_files)
mcp.tool()(write_file)
mcp.tool()(read_file)


if __name__ == "__main__":
    mcp.run()

    
