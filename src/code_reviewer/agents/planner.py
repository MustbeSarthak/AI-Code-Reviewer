from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv

if TYPE_CHECKING:
    from ..main import ReviewCode
load_dotenv()

# state
class ReviewPlan(TypedDict):
    bugs:bool
    security:bool
    quality:bool
    complexity:bool

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

planner_llm = llm.with_structured_output(ReviewPlan)

def planner(state:ReviewCode):
    project_path = state["project_path"]
    files = state["files"]
    prompt = f"""You are a code review planning agent.
    Project  : {project_path} Files:{files}

    Decide which types of code review should be performed"""

    try:
        plan = planner_llm.invoke(prompt)
    except Exception:
        # Some models intermittently answer without a tool call. Fall back to a
        # full review plan rather than failing the whole workflow.
        plan = ReviewPlan(bugs=True, security=True, quality=True, complexity=True)

    return {"review_plan": plan}