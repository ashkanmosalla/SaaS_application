import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from openai import OpenAI

# If you placed a .env file inside saas/api, this will load it automatically.
# (Optional) If python-dotenv isn't installed, we'll just rely on real OS env vars.
try:
    from dotenv import load_dotenv

    load_dotenv()  # By default, loads ".env" from the current working directory.
except Exception:
    # No problem—just make sure OPENAI_API_KEY is exported in your shell/environment.
    pass

app = FastAPI()


@app.get("/api", response_class=PlainTextResponse)
def idea():
    # Read the API key from environment variables (never hardcode secrets).
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not set. Put it in a .env file or export it in your shell.",
        )

    # Read the model from env so you can change it without touching code.
    # Example: OPENAI_MODEL=gpt-5.1
    model = os.getenv("OPENAI_MODEL", "gpt-5.1")

    client = OpenAI(api_key=api_key)

    try:
        # Responses API (recommended): returns a unified output object.
        resp = client.responses.create(
            model=model,
            input="Come up with a new business idea for AI Agents",
        )
        return resp.output_text
    except Exception as e:
        # Bubble up a readable error to the client (you can log it in production).
        raise HTTPException(status_code=500, detail=str(e))
