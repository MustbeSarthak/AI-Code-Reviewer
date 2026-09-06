# AI Code Reviewer

Analyze code snippets for **readability**, **security**, and **potential bugs**
and get three category scores with suggestions.

## Architecture

```
React Frontend                (frontend/ — Vite + Tailwind + lucide-react)
      │
      │  POST /review  { "code": "...", "language": "python" }
      ▼
FastAPI                       (src/code_reviewer/api.py)
      │
      ▼
LangGraph pipeline            planner → scanner → validator
      │                       (src/code_reviewer/agents/, MCP file tools)
      ▼
FastAPI converts result
      │
      ▼
{ readability: {score, suggestions}, security: {...}, bugs: {...} }
      │
      ▼
React ScoreCards
```

## Prerequisites

- Python 3.13 (managed with [uv](https://docs.astral.sh/uv/))
- Node.js 20+ (tested with Node 24)
- A `GROQ_API_KEY` in `.env` (used by the LLM agents)

## Run the backend (API server)

```powershell
cd "C:\Code Reviewer"
uv sync            # only the first time / after dependency changes
uv run uvicorn code_reviewer.api:app --reload --host 127.0.0.1 --port 8000
```

Or equivalently: `uv run python -m code_reviewer.api`

Verify it is up: `GET http://127.0.0.1:8000/health` → `{"status": "ok"}`.
Interactive docs: http://127.0.0.1:8000/docs

> Note: the first request to `/review` runs two LLM calls, so it takes a few seconds.

## Run the frontend

```powershell
cd "C:\Code Reviewer\frontend"
npm install        # only the first time
npm run dev
```

The Vite dev server runs at http://localhost:5173 and proxies `/review`
requests to the backend at `http://localhost:8000` (override with
`VITE_PROXY_TARGET` in `frontend/.env`).

## Command-line review (no web server)

```powershell
cd "C:\Code Reviewer"
uv run code-reviewer
```

## API contract

`POST /review`

Request:

```json
{
  "code": "string",
  "language": "string"
}
```

Response:

```json
{
  "readability": { "score": 82, "suggestions": ["..."] },
  "security":    { "score": 68, "suggestions": ["..."] },
  "bugs":        { "score": 74, "suggestions": ["..."] }
}
```

Scores are integers from 0–100. A `400` is returned for an empty snippet and a
`502` when the analysis back-end fails.

## Project layout

```
src/code_reviewer/
  api.py           FastAPI app (POST /review, GET /health)
  main.py          LangGraph workflow + snippet runner
  agents/
    planner.py     Decides which review types to run
    scanner.py     Discovers files via an MCP server
    validator.py   Validates the scan + LLM analysis (readability/security/bugs)
  mcp/             Model Context Protocol server & client (file tools)
frontend/          React + Tailwind UI (see frontend/README.md)
```
