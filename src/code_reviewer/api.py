from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Support both supported package execution (``python -m code_reviewer.api``)
# and direct execution during development (``python src/code_reviewer/api.py``).
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from code_reviewer.main import run_snippet_review


app = FastAPI(
    title="Code Reviewer API",
    description="Analyze code snippets for readability, security, and bugs.",
    version="0.1.0",
)

# The frontend may be served from a different origin during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to review.")
    language: str = Field("plaintext", description="Programming language of the snippet.")


class CategoryResult(BaseModel):
    score: int = Field(ge=0, le=100)
    suggestions: list[str] = Field(default_factory=list)


class ReviewResponse(BaseModel):
    readability: CategoryResult
    security: CategoryResult
    bugs: CategoryResult


def _clamp_score(value: Any) -> int:
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        return 0
    return max(0, min(100, score))


def _to_category(raw: Any) -> CategoryResult:
    raw = raw if isinstance(raw, dict) else {}
    suggestions = [
        suggestion
        for suggestion in (raw.get("suggestions") or [])
        if isinstance(suggestion, str) and suggestion.strip()
    ][:12]
    return CategoryResult(
        score=_clamp_score(raw.get("score", 0)),
        suggestions=suggestions,
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/review", response_model=ReviewResponse)
async def review(request: ReviewRequest) -> ReviewResponse:
    code = request.code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="code must not be empty.")

    try:
        result = await run_snippet_review(code, request.language)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Something went wrong while analyzing your code.",
        ) from exc

    findings = result.get("final_findings") or {}
    if not findings:
        raise HTTPException(
            status_code=502,
            detail="No analysis was produced for this code.",
        )

    return ReviewResponse(
        readability=_to_category(findings.get("readability")),
        security=_to_category(findings.get("security")),
        bugs=_to_category(findings.get("bugs")),
    )


if __name__ == "__main__":
    uvicorn.run("code_reviewer.api:app", host="127.0.0.1", port=8000)