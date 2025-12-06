import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from openai import OpenAI

# ----------------- .env load -----------------
try:
    from dotenv import load_dotenv

    BASE_DIR = os.path.dirname(__file__)
    env_path = os.path.join(BASE_DIR, ".env")
    load_dotenv(env_path)
except Exception:
    # اگر python-dotenv نبود، از env سیستم استفاده می‌کنیم
    pass

app = FastAPI()


# =============== OpenAI backend ===============

def generate_with_openai(prompt: str) -> str:
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


# =============== Ollama / Llama backend ===============

def generate_with_ollama(prompt: str) -> str:
    # مطمئن شو `ollama` نصب و سرویسش در حال اجراست
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


# =============== FastAPI endpoint ===============

@app.get("/", response_class=PlainTextResponse)
def idea():
    """
    LLM_PROVIDER در env تعیین می‌کند از کدام بک‌اند استفاده کنیم:
      - ollama  → فقط Llama/Ollama (حالت فعلی تو)
      - openai  → فقط OpenAI (وقتی بعداً پول دادی)
    """

    prompt = "Come up with a new AI startup idea for PhD students."

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
