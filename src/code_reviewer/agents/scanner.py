from __future__ import annotations
import json
from typing import TYPE_CHECKING
from ..mcp.client import call_mcp_tool

if TYPE_CHECKING:
    from ..main import ReviewCode


def _extract_paths(content) -> list[str]:
    """Normalize MCP tool output into a flat list of file path strings."""
    paths: list[str] = []
    for item in content or []:
        text = getattr(item, "text", None)
        if isinstance(text, str) and text.strip():
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    paths.extend(str(p) for p in parsed if str(p).strip())
                    continue
            except Exception:
                pass
            paths.append(text)
        else:
            paths.append(str(item))
    return paths


async def scanner(state: ReviewCode):
    project_path = state["project_path"]
    result = await call_mcp_tool(
        "list_files",
        {
            "project_path": project_path
        }
    )
    files = _extract_paths(result.content)
    return {
        "files": files,
        "scanned_files": files,
    }