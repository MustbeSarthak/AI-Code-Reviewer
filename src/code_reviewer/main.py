from __future__ import annotations

import asyncio
import sys
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
    files: list
    review_plan: dict
    
    bug_findings: list
    security_findings: list
    quality_findings: list
    complexity_findings: list

    final_findings: list
    needs_reanalysis: bool
    iteration: int
    final_report: str

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

# Test
async def run_review() -> None:
    initial_state = {
        "project_path": "./sample_project",
        "files": [],
        "review_plan": {},

        "bug_findings": [],
        "security_findings": [],
        "quality_findings": [],
        "complexity_findings": [],

        "final_findings": [],
        "needs_reanalysis": False,
        "iteration": 0,
        "final_report": ""
    }

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