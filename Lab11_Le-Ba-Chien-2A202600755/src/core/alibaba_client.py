"""
Alibaba Cloud Model Studio / DashScope OpenAI-compatible client.

Environment variables:
    DASHSCOPE_API_KEY or ALIBABA_API_KEY
    DASHSCOPE_BASE_URL, default https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    ALIBABA_MODEL, default qwen-plus
"""
import asyncio
import json
import os
import urllib.error
import urllib.request

from core.config import get_alibaba_model


class AlibabaAPIError(RuntimeError):
    """Raised when the Alibaba API request fails."""


def _chat_completions_url(base_url: str) -> str:
    """Normalize a DashScope base URL to the chat completions endpoint."""
    cleaned = base_url.rstrip("/")
    if cleaned.endswith("/chat/completions"):
        return cleaned
    return f"{cleaned}/chat/completions"


def _api_key() -> str | None:
    """Return the configured DashScope API key if available."""
    return os.getenv("DASHSCOPE_API_KEY") or os.getenv("ALIBABA_API_KEY")


def has_alibaba_key() -> bool:
    """Check if an Alibaba/DashScope API key is configured."""
    return bool(_api_key())


def chat_completion_sync(
    messages: list[dict],
    *,
    model: str | None = None,
    temperature: float = 0.2,
    timeout: int = 60,
) -> str:
    """Call Alibaba DashScope using the OpenAI-compatible Chat API."""
    key = _api_key()
    if not key:
        raise AlibabaAPIError("DASHSCOPE_API_KEY or ALIBABA_API_KEY is not set")

    base_url = os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    payload = {
        "model": model or get_alibaba_model(),
        "messages": messages,
        "temperature": temperature,
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        _chat_completions_url(base_url),
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise AlibabaAPIError(f"Alibaba API HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise AlibabaAPIError(f"Alibaba API request failed: {exc}") from exc

    try:
        return response_data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AlibabaAPIError(f"Unexpected Alibaba API response: {response_data}") from exc


async def chat_completion(
    messages: list[dict],
    *,
    model: str | None = None,
    temperature: float = 0.2,
    timeout: int = 60,
) -> str:
    """Async wrapper around the blocking DashScope HTTP request."""
    return await asyncio.to_thread(
        chat_completion_sync,
        messages,
        model=model,
        temperature=temperature,
        timeout=timeout,
    )
