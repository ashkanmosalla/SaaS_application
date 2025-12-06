import os

from fastapi import FastAPI, HTTPException  # type: ignore
from fastapi.responses import (
    PlainTextResponse,
    StreamingResponse,
)  # type: ignore
from openai import OpenAI  # type: ignore

# ----------------- .env load -----------------
try:
    from dotenv import load_dotenv  # type: ignore

    BASE_DIR = os.path.dirname(__file__)
    env_path = os.path.join(BASE_DIR, ".env")
    load_dotenv(env_path)
except Exception:
    # اگر python-dotenv نبود، از env سیستم استفاده می‌کنیم
    pass

app = FastAPI()


# =============== OpenAI backend (non-stream) ===============

def generate_with_openai(prompt: str) -> str:
    """
    Non-streaming OpenAI call.
    Reads:
      - OPENAI_API_KEY
      - OPENAI_MODEL (optional, default: gpt-4.1-mini)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # این ارور رو بالا می‌فرستیم تا HTTP 500 قشنگ‌تر برگردونیم
        raise RuntimeError("OPENAI_API_KEY is not set")

    # مدل سبک (معادل gpt5-nano – فعلاً مثلا gpt-4.1-mini)
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    client = OpenAI(api_key=api_key)
    resp = client.responses.create(
        model=model,
        input=prompt,
    )
    return resp.output_text


# =============== OpenAI backend (stream) ===============

def stream_with_openai(prompt: str):
    """
    Streaming OpenAI call (SSE style), شبیه ورژن قدیمی:
    client.chat.completions.create(..., stream=True)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    # اینجا مدل استریم رو هم می‌تونی از env کنترل کنی
    stream_model = os.getenv("OPENAI_STREAM_MODEL", "gpt-5-nano")

    client = OpenAI(api_key=api_key)
    messages = [{"role": "user", "content": prompt}]

    stream = client.chat.completions.create(
        model=stream_model,
        messages=messages,
        stream=True,
    )

    def event_stream():
        for chunk in stream:
            # مثل کد قدیمی‌ات:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return event_stream()


# =============== Ollama / Llama backend (non-stream) ===============

def generate_with_ollama(prompt: str) -> str:
    """
    Non-streaming Ollama call.
    Reads:
      - OLLAMA_MODEL (optional, default: llama3.1:8b)
    """
    import ollama  # type: ignore

    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    res = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    # پاسخ معمولاً res["message"]["content"] است
    try:
        return res["message"]["content"]
    except Exception:
        return str(res)


# =============== Ollama / Llama backend (stream) ===============

def stream_with_ollama(prompt: str):
    """
    Streaming Ollama call, خروجی را به صورت SSE می‌فرستیم.
    """
    import ollama  # type: ignore

    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    def event_stream():
        for chunk in stream:
            # ساختار معمول chunk: {"message": {"role": "assistant", "content": "..."}}
            content = chunk.get("message", {}).get("content", "")
            if content:
                lines = content.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return event_stream()


# =============== FastAPI endpoint (non-stream, روی "/") ===============

@app.get("/", response_class=PlainTextResponse)
def idea() -> str:
    """
    Endpoint ساده بدون استریم (برای تست سریع و fetch معمولی).

    LLM_PROVIDER در env تعیین می‌کند از کدام بک‌اند استفاده کنیم:
      - ollama  → فقط Llama/Ollama (حالت فعلی تو)
      - openai  → فقط OpenAI (وقتی بعداً پول دادی)
    """

    prompt = "Come up with a new AI startup idea for AI Agents."
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    try:
        if provider == "ollama":
            return generate_with_ollama(prompt)

        if provider == "openai":
            return generate_with_openai(prompt)

        # اگر یه چیز عجیب تو env نوشته باشی
        raise HTTPException(
            status_code=400,
            detail=f"Unknown LLM_PROVIDER: {provider}",
        )

    except RuntimeError as e:
        # مثلاً وقتی OPENAI_API_KEY ست نیست
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"{provider} error: {e}",
        )


# =============== FastAPI endpoint (stream, روی "/api") ===============

@app.get("/api")
def stream_idea():
    """
    Streaming endpoint (SSE) شبیه ورژن قبلی‌ات:

      - اگر LLM_PROVIDER=openai  → از stream_with_openai استفاده می‌کند.
      - اگر LLM_PROVIDER=ollama → از stream_with_ollama استفاده می‌کند.

    خروجی:
      StreamingResponse با media_type="text/event-stream"
    """

    prompt = "Come up with a new AI startup idea for AI Agents."
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    try:
        if provider == "openai":
            event_gen = stream_with_openai(prompt)
        elif provider == "ollama":
            event_gen = stream_with_ollama(prompt)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown LLM_PROVIDER: {provider}",
            )

        return StreamingResponse(
            event_gen,
            media_type="text/event-stream",
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"{provider} stream error: {e}",
        )
