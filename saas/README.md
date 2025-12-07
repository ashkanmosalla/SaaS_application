# Business Idea Generator (FastAPI + Next.js + Ollama/OpenAI)

An AI-powered **business idea generator** with:

- **Backend:** FastAPI (`api/index.py`)
- **Frontend:** Next.js (pages router, `pages/index.tsx`)
- **LLM providers:**  
  - Local **Ollama** (e.g. `llama3.1:8b`)  
  - **OpenAI API** (optional – for later when billing is active)

---

## Project Structure (inside `saas/`)

```text
saas/
  api/
    index.py      # FastAPI backend + Ollama/OpenAI logic
    .env          # Backend env vars (LLM_PROVIDER, OLLAMA_MODEL, ...)
  pages/
    index.tsx     # Frontend UI
    _app.tsx
    _document.tsx
  public/
  styles/
    globals.css
    .env.local    # Frontend env (NEXT_PUBLIC_BACKEND_URL) – optional
  package.json
  requirements.txt
```

## LLM Provider Configuration

LLM_PROVIDER=ollama         # or: openai
OLLAMA_MODEL=llama3.1:8b    # default local model
```
# For later when you use OpenAI:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4.1-mini
# OPENAI_STREAM_MODEL=gpt-5-nano
```

## # Backend deps (FastAPI, OpenAI, Ollama client, ...)
pip install -r requirements.txt

# Frontend deps (Next.js, React, Tailwind)
npm install

## How to run (local development)

in two terminal:
Run FastAPI backend
``` uvicorn api.index:app --reload```
http://127.0.0.1:8000 will come up

Run Next.js frontend
in the second terminal saas/:
``` npm run dev```

then go to: http://localhost:3000


Scripts:
```
Backend dev server
uvicorn api.index:app --reload

Frontend dev server
npm run dev
```