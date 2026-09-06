from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ..main import ReviewCode


class CategoryAnalysis(BaseModel):
    """Score and suggestions for a single review category."""

    score: int = Field(ge=0, le=100, description="Score from 0 to 100.")
    suggestions: list[str] = Field(
        description="Short, specific improvement suggestions for the category."
    )


class CodeAnalysis(BaseModel):
    """Review of a code snippet across the three frontend categories."""

    readability: CategoryAnalysis
    security: CategoryAnalysis
    bugs: CategoryAnalysis


llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
analyzer_llm = llm.with_structured_output(CodeAnalysis)

REVIEW_PROMPT = """You are an expert code reviewer. Review the following {language}
code snippet and assess it across exactly three categories.

For every category return a score between 0 and 100 (higher is better) and 2-4
short, specific suggestions.

- readability: how clear, consistent, and maintainable the code is.
- security: unsafe patterns, missing validation, exposed sensitive data.
- bugs: correctness issues, edge cases, missing error handling.

Code snippet:
```{language}
{code}
```"""


def _read_snippet(state: ReviewCode) -> str:
    """Return the code under review from the graph state."""
    code = state.get("code")
    if isinstance(code, str) and code.strip():
        return code

    # Fallback: read any scanned files directly from disk.
    parts: list[str] = []
    for file_ref in state.get("files", []):
        text = getattr(file_ref, "text", None)
        path = text if isinstance(text, str) else str(file_ref)
        try:
            parts.append(Path(path).read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
    return "\n".join(parts)


def _empty_analysis(message: str) -> CodeAnalysis:
    """Build an all-zero analysis used when the snippet cannot be scored."""
    return CodeAnalysis(
        readability=CategoryAnalysis(score=0, suggestions=[message]),
        security=CategoryAnalysis(score=0, suggestions=[message]),
        bugs=CategoryAnalysis(score=0, suggestions=[message]),
    )


def _analyze(code: str, language: str) -> CodeAnalysis:
    """Run the LLM review with one retry; never raise."""
    prompt = REVIEW_PROMPT.format(code=code, language=language or "plaintext")
    for _ in range(2):
        try:
            result = analyzer_llm.invoke(prompt)
            if isinstance(result, CodeAnalysis):
                return result
        except Exception:
            # A tool-call can fail transiently; retry once before falling back.
            continue
    return _empty_analysis("Unable to complete the analysis.")


def _to_findings(category: CategoryAnalysis) -> dict:
    """Convert a category model into the shape the API returns."""
    return {
        "score": max(0, min(100, int(category.score))),
        "suggestions": [
            suggestion.strip()
            for suggestion in category.suggestions
            if isinstance(suggestion, str) and suggestion.strip()
        ][:12],
    }


def validator(state: ReviewCode):
    """
    Validates the scanned snippet and produces the final code analysis.
    """
    scanned_files = state.get("files") or state.get("scanned_files") or []

    # Basic validation of the scan before analysis.
    if not scanned_files:
        return {
            **state,
            "validation_result": {
                "valid": False,
                "message": "No files were scanned from the project."
            }
        }

    code = _read_snippet(state)
    language = state.get("language") or "plaintext"

    analysis = _analyze(code, language) if code else _empty_analysis(
        "No code was provided for review."
    )

    findings = {
        "readability": _to_findings(analysis.readability),
        "security": _to_findings(analysis.security),
        "bugs": _to_findings(analysis.bugs),
    }

    validation_result = {
        "valid": True,
        "files_scanned": len(scanned_files),
    }

    return {
        **state,
        "bug_findings": findings["bugs"]["suggestions"],
        "security_findings": findings["security"]["suggestions"],
        "quality_findings": findings["readability"]["suggestions"],
        "final_findings": findings,
        "final_report": (
            f"Readability: {findings['readability']['score']}/100 | "
            f"Security: {findings['security']['score']}/100 | "
            f"Bugs: {findings['bugs']['score']}/100"
        ),
        "validation_result": validation_result,
    }