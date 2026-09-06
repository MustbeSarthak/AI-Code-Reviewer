from __future__ import annotations

import asyncio
import sys
import tempfile
import uuid
from pathlib import Path
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

# Support both supported package execution (``python -m code_reviewer.main``)
# and direct execution during development (``python src/code_reviewer/main.py``).
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from code_reviewer.agents.planner import planner
from code_reviewer.agents.scanner import scanner
from code_reviewer.agents.validator import validator


# Memory
memory = InMemorySaver()

# State
class ReviewCode(TypedDict):
    project_path: str
    code: str
    language: str
    files: list
    review_plan: dict
    
    bug_findings: list
    security_findings: list
    quality_findings: list
    complexity_findings: list

    final_findings: dict
    needs_reanalysis: bool
    iteration: int
    final_report: str
    validation_result: dict

# Graph
builder = StateGraph(ReviewCode)

builder.add_node("planner", planner)
builder.add_node("scanner", scanner)
builder.add_node("validator", validator)

builder.add_edge(START, "planner")
builder.add_edge("planner", "scanner")
builder.add_edge("scanner", "validator")
builder.add_edge("validator", END)


# Compile
graph = builder.compile(checkpointer=memory)


# File extensions so a snippet lands in a realistic file inside a temp project.
LANGUAGE_EXTENSIONS = {
    "python": ".py",
    "javascript": ".js",
    "typescript": ".ts",
    "java": ".java",
    "c": ".c",
    "cpp": ".cpp",
    "csharp": ".cs",
    "go": ".go",
    "rust": ".rs",
    "ruby": ".rb",
    "php": ".php",
    "swift": ".swift",
    "kotlin": ".kt",
    "html": ".html",
    "css": ".css",
    "sql": ".sql",
    "bash": ".sh",
    "json": ".json",
    "yaml": ".yml",
    "plaintext": ".txt",
}


def _initial_state(project_path: str, code: str = "", language: str = "plaintext") -> dict:
    """Build the default state the review graph expects."""
    return {
        "project_path": project_path,
        "code": code,
        "language": language,
        "files": [],
        "review_plan": {},

        "bug_findings": [],
        "security_findings": [],
        "quality_findings": [],
        "complexity_findings": [],

        "final_findings": {},
        "needs_reanalysis": False,
        "iteration": 0,
        "final_report": "",
    }


async def run_snippet_review(code: str, language: str = "plaintext") -> dict:
    """Review a single code snippet through the full LangGraph workflow.

    The snippet is dropped into a temporary project directory so the existing
    planner -> scanner -> validator pipeline can process it unchanged.
    """
    extension = LANGUAGE_EXTENSIONS.get((language or "plaintext").lower(), ".txt")
    config = {"configurable": {"thread_id": f"snippet-{uuid.uuid4()}"}}

    with tempfile.TemporaryDirectory(prefix="code-review-") as project_dir:
        project_path = Path(project_dir)
        (project_path / f"snippet{extension}").write_text(code, encoding="utf-8")

        initial_state = _initial_state(
            project_path=str(project_path),
            code=code,
            language=language,
        )
        return await graph.ainvoke(initial_state, config)


# Test
async def run_review() -> None:
    initial_state = _initial_state(project_path="./sample_project")

    config = {
        "configurable": {
            "thread_id": "test-001"
        }
    }

    result = await graph.ainvoke(
        initial_state,
        config
    )

    print("\nFiles found:")
    print(result["files"])


def main() -> None:
    """Run the code review workflow from the command line."""
    asyncio.run(run_review())


if __name__ == "__main__":
    main()