"""Small OpenAI-compatible HTTP client with durable retry metadata."""

from __future__ import annotations

import json
import random
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from email.message import Message
from typing import Any


@dataclass(frozen=True)
class ChatResult:
    content: str
    attempts: int
    latency_seconds: float
    usage: dict[str, int | None]


class ChatRequestError(RuntimeError):
    def __init__(self, message: str, *, attempts: int, latency_seconds: float) -> None:
        super().__init__(message)
        self.attempts = attempts
        self.latency_seconds = latency_seconds


def _endpoint(api_base: str) -> str:
    value = api_base.rstrip("/")
    return value if value.endswith("/chat/completions") else value + "/chat/completions"


def _retry_after(headers: Message | None) -> float | None:
    if headers is None:
        return None
    value = headers.get("Retry-After")
    try:
        return max(0.0, float(value)) if value is not None else None
    except ValueError:
        return None


def chat_completion(
    *,
    api_key: str,
    api_base: str,
    model: str,
    prompt: str,
    temperature: float,
    max_tokens: int,
    timeout_seconds: float,
    max_retries: int,
    retry_backoff_seconds: float,
) -> ChatResult:
    started = time.monotonic()
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    if model.lower().startswith("qwen3"):
        payload["enable_thinking"] = False
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_error = "request failed"
    for attempt in range(1, max_retries + 2):
        request = urllib.request.Request(
            _endpoint(api_base),
            data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        retry_after = None
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"].get("content") or ""
            if not content.strip():
                raise ValueError("empty response")
            usage = result.get("usage") or {}
            return ChatResult(
                content=content,
                attempts=attempt,
                latency_seconds=time.monotonic() - started,
                usage={
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens"),
                },
            )
        except urllib.error.HTTPError as exc:
            retry_after = _retry_after(exc.headers)
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = f"HTTP {exc.code}: {detail[:2000]}"
            if exc.code not in {408, 409, 429, 500, 502, 503, 504}:
                break
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, IndexError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt <= max_retries:
            delay = retry_after
            if delay is None:
                delay = min(120.0, retry_backoff_seconds * (2 ** (attempt - 1)))
            time.sleep(delay + random.uniform(0.0, min(1.0, delay * 0.1)))
    raise ChatRequestError(
        last_error,
        attempts=attempt,
        latency_seconds=time.monotonic() - started,
    )
