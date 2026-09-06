# Code Reviewer — Frontend

React + Tailwind CSS frontend for the AI Code Reviewer. A small, polished
developer utility to get readability, security, and bug-risk scores for a
snippet of code.

## Requirements

- Node.js 20+ (tested with Node 24)

## Getting started

Start the backend API first (from the repo root):

```sh
uv run uvicorn code_reviewer.api:app --reload --host 127.0.0.1 --port 8000
```

Then start the frontend:

```sh
npm install
npm run dev
```

The app runs at `http://localhost:5173`. During development, `POST /review`
is proxied to the backend at `http://localhost:8000` (override with
`VITE_PROXY_TARGET` in `frontend/.env`).

## API contract

The UI expects a `POST /review` endpoint:

```json
{ "code": "string", "language": "string" }
```

Response shape:

```json
{
  "readability": { "score": 82, "suggestions": ["..."] },
  "security": { "score": 68, "suggestions": ["..."] },
  "bugs": { "score": 74, "suggestions": ["..."] }
}
```

In a production deployment, point `VITE_API_BASE_URL` at the backend or serve
the built app from the same origin as the API.

## Commands

| Command           | Description                       |
| ----------------- | --------------------------------- |
| `npm run dev`     | Start the Vite dev server         |
| `npm run build`   | Create a production build         |
| `npm run preview` | Preview the production build      |