# Business Idea Generator (SaaS demo)

A small demo project that shows how to wire up:

- **Next.js** frontend (React)  
- **FastAPI** backend  
- **LLM provider switch** between:
  - Local **Ollama** (e.g. `llama3.1:8b`)
  - Hosted **OpenAI** (e.g. `gpt-4.1-mini`)

The frontend calls the backend `/api` endpoint and displays an AI-generated startup idea for PhD students.

---

## Project structure

```text
saas/
  api/
    index.py       # FastAPI app (Ollama / OpenAI switch)
    .env           # Backend env vars (LLM_PROVIDER, models, keys)
  pages/
    index.tsx      # Next.js page that fetches /api
    _app.tsx
    _document.tsx
  styles/
    globals.css
  package.json     # Next.js / React deps
  requirements.txt # Python deps (FastAPI, uvicorn, openai, ollama, dotenv)
```
### Environment variables (backend)
Create saas/api/.env:

Use local Llama via Ollama (default)
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b

Or switch to OpenAI later:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini
### Backend dependencies (Python)
From the saas directory:

pip install -r requirements.txt

### Frontend dependencies (Next.js)
From the saas directory:

npm install
npm run dev   # runs Next.js on http://localhost:3000
### How to run
uvicorn api.index:app --reload
