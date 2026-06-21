"""
LLM text generation. Groq primary (OpenAI-compatible), Together.ai fallback.
Both expose /chat/completions with the same request shape.
"""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"

# Together fallback model — verify against live catalog.
TOGETHER_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

TIMEOUT = 60


class LLMError(Exception):
    pass


def _call(url, api_key, model, system, user, *, json_mode):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    resp = requests.post(url, headers=headers, json=body, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def generate_text(system: str, user: str, *, json_mode: bool = True) -> tuple[str, str]:
    """
    Return (content, provider). Try Groq, fall back to Together.
    Raises LLMError if both fail / unconfigured.
    """
    if settings.GROQ_API_KEY:
        try:
            content = _call(
                GROQ_URL, settings.GROQ_API_KEY, settings.GROQ_MODEL,
                system, user, json_mode=json_mode,
            )
            return content, "groq"
        except requests.RequestException as e:
            logger.warning("Groq failed, trying Together: %s", e)

    if settings.TOGETHER_AI_API_KEY:
        try:
            content = _call(
                TOGETHER_URL, settings.TOGETHER_AI_API_KEY, TOGETHER_MODEL,
                system, user, json_mode=json_mode,
            )
            return content, "together"
        except requests.RequestException as e:
            logger.error("Together failed: %s", e)
            raise LLMError(f"All LLM providers failed: {e}") from e

    raise LLMError("No LLM provider configured (set GROQ_API_KEY)")
