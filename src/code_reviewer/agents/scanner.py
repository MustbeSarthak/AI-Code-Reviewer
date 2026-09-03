from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcp.client import call_mcp_tool

if TYPE_CHECKING:
    from ..main import ReviewCode

async def scanner(state: ReviewCode):
    project_path = state["project_path"]
    result = await call_mcp_tool(
        "list_files",
        {
            "project_path": project_path
        }
    )
    files = result.content
    return {
        "files": files
    }